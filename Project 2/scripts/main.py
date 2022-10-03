from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, UnexpectedAlertPresentException
import pandas as pd
import numpy as np
import re
import subprocess
import time
from collections import defaultdict
interests = ['活動', '展覽', '演', '影展', '節目', '講', '課', '近期', '最新', '焦點']
noise = '視窗|頁|下載|統計|故事|花絮|寫真|紀|照|影|片|過|往|歷|果|回|發'
moreTextRex = 'more|更多|探索|前往|瀏覽|所有'
moreUrlRex = '(e|E)vent|(n|N)ews|(a|A)ctivity|(e|E)xhibition'
start = 0

tasks = pd.read_excel('./tasks.xlsx', sheet_name=0, header=0, converters={'UrlId': int, 'Seed URL': str})
Options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
options = Options()
options.add_argument('start-maximized')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
driver = webdriver.Chrome(options=options)
testVer = str(time.time())
apiFile = 'report_'+testVer.replace(".", "_")+'.txt'
outputFile = open('record_'+testVer.replace(".", "_")+'.txt', mode='a', encoding='utf-8')

def output(str):
    print(str)
    outputFile.write(str+'\n')
def explore(url):
    # priority0: perfect short text > 'more' links > long text > img links > short text containing noises
    # priority1: kind of interest
    # priority2: position of interest
    # priority3: length of text
    # priority4: length of url
    linkTableType = [('priority0', 'i8'), ('priority1', 'i8'), ('priority2', 'i8'), ('priority3', 'i8'), ('priority4', 'i8'), ('text', 'U1000'), ('url', 'U1000')]
    linkTable = np.array([], dtype=linkTableType)
    try:
        driver.get(url)
    except WebDriverException:
        output('Connection Failed: ' + url)
        return linkTable
    try:
        links = driver.find_elements_by_tag_name('a')
    except UnexpectedAlertPresentException:
        output('Blocked by IO: ' + url)
        return linkTable
    for link in links:
        try:
            anchorText = link.get_attribute('title')
            if not anchorText:
                anchorText = link.text
            if len(anchorText) <= 0:
                anchorText = link.get_attribute('textContent')
                anchorText = re.sub('\W', '', anchorText)
            if len(anchorText) <= 0:
                anchorText = link.get_attribute('innerHTML')
            text = re.sub('</?(div|span|p|li)', '', anchorText)
            text = re.sub('<img.*alt\s?=', 'img', text)
            text = re.sub('\W', '', text)
            subURL = link.get_attribute('href')
            if subURL and ('http' in subURL) and ('#' not in subURL):
                data = None
                if re.search(moreTextRex, text) and re.search(moreUrlRex, subURL[subURL.find(re.search('\w/', subURL).group()) + 2:]):
                    data = (1, 0, 0, len(text), len(subURL), anchorText, subURL)
                for j in range(len(interests)):
                    if interests[j] in text:
                        if re.search(noise, text):
                            if not data and(len(text) <= 7):
                                data = (4, j, text.find(interests[j]), len(text), len(subURL), anchorText, subURL)
                        elif len(text) <= 7:
                            data = (0, j, text.find(interests[j]), len(text), len(subURL), anchorText, subURL)
                        elif not data:
                            data = (2, j, text.find(interests[j]), len(text), len(subURL), anchorText, subURL)
                        break
                if not data and ('img' in text) and re.search(moreUrlRex, subURL[subURL.find(re.search('\w/', subURL).group()) + 2:]):
                    data = (3, 0, 0, len(text), len(subURL), anchorText, subURL)
                if data:
                    linkTable = np.append(linkTable, np.array([data], dtype=linkTableType))
        except StaleElementReferenceException:
            continue
    return linkTable

output('test version: ' + str(testVer))
if start == 0:
    start = 1
for i in range(start - 1, tasks.shape[0]):
    id = tasks['UrlId'][i]
    seedURL = tasks['Seed URL'][i]
    output('Task ID: ' + str(id))
    output('Task URL: ' + seedURL)
    rootURL = seedURL[:seedURL.find(re.search('\w/', seedURL).group()) + 2]
    output('Root URL: ' + rootURL)
    urlTable = []
    repeatNoisesList = []
    repeatNoisesRecord = defaultdict(lambda: 0)
    accept = False
    testURL = None

    output('Explore root URL and task URL...')
    linkTable = np.append(explore(rootURL), explore(seedURL))
    linkTable = np.sort(linkTable, order=['priority0', 'priority1', 'priority2', 'priority3', 'priority4'])
    if linkTable.shape[0] > 0:
        for j in range(linkTable.shape[0]):
            testURL = linkTable[j]['url']
            repeatDetect = linkTable[j]['text'][:20]
            if (testURL not in urlTable) and (repeatDetect not in repeatNoisesList):
                urlTable.append(testURL)
                output(str(linkTable[j]))
                command='java -cp event.source.page.discovery-0.0.2.jar nculab.widm.event.source.page.discovery.QueryEventSourcePage '\
                        '--test-version '+testVer+' '\
                        '--url-id '+str(id)+' '\
                        '--query-url "'+testURL+'" '\
                        '--anchor-text "'+linkTable[j]['text']+'"'
                if 'true' in str(subprocess.check_output(command, shell=True)):
                    accept = True
                    break
                else:
                    repeat = 0
                    repeatTable = [testURL]
                    for k in range(j+1, linkTable.shape[0]):
                        if linkTable[k]['text'][:20] == repeatDetect:
                            if linkTable[k]['url'] not in repeatTable:
                                repeatTable.append(linkTable[k]['url'])
                                repeat += 1
                        else:
                            break
                    if repeat >= 3:
                        repeatNoisesList.append(repeatDetect)
                    else:
                        repeatNoisesRecord[repeatDetect] += 1
                        if repeatNoisesRecord[repeatDetect] >= 3:
                            repeatNoisesList.append(repeatDetect)

    if not accept:
        output('Failed, test the root url...')
        testURL = rootURL
        command='java -cp event.source.page.discovery-0.0.2.jar nculab.widm.event.source.page.discovery.QueryEventSourcePage '\
                '--test-version ' + testVer + ' '\
                '--url-id ' + str(id) + ' '\
                '--query-url "' + testURL + '" '\
                '--anchor-text "rootURL"'
        if 'true' in str(subprocess.check_output(command, shell=True)):
            accept = True
    if not accept:
        output('Failed, test exactly the task url...')
        testURL = seedURL
        command='java -cp event.source.page.discovery-0.0.2.jar nculab.widm.event.source.page.discovery.QueryEventSourcePage ' \
                '--test-version ' + testVer + ' ' \
                '--url-id ' + str(id) + ' ' \
                '--query-url "' + testURL + '" ' \
                '--anchor-text "seedURL"'
        if 'true' in str(subprocess.check_output(command, shell=True)):
            accept = True
    if accept:
        output('Accepted: ' + testURL)
    else:
        output('Failed, cannot find the event source page.')
driver.close()
outputFile.close()
command='java -cp event.source.page.discovery-0.0.2.jar nculab.widm.event.source.page.discovery.Evaluation '\
        '--test-version '+testVer+' '\
        '--output-file report_'+testVer.replace(".", "_")+'.txt'
print(subprocess.check_output(command, shell=True))