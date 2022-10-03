# Project 1
這到底是哪個天兵寫的報告......把論文格式當成甚麼......<br>
<br>
主題為根據活動之各種資料判斷該活動是否適合各種年齡參與。<br>
首先要求各組對自身負責的一部分訓練資料做標記並計算Cohen's kappa，而後公開各組Cohen's kappa並統整全班標記資料集舉行kaggle競賽，各組自行選擇有興趣之模型嘗試。<br>
<br>
kaggle競賽網址:https://www.kaggle.com/competitions/ncu2020aihw1<br>
kaggle競賽初期限制每日上傳五次，後期調整至十次。由於班上有些同學沒有太多相關的競賽經驗，助教發現之後趕緊公告：一般應該先自行再分割訓練資料集進行簡單的validation，確定模型效果比較滿意之後才嘗試上傳結果。然而已經太遲了，排行榜上充斥著各組為了進行測試而創的分身帳號......<br>
<br>
"kappa_calculator.cpp"為我負責計算Cohen's kappa時面對重複枯燥計算過程開發的輔助工具。<br>
標記活動中我分配至第7組，但其後組員在需課堂分組討論時不巧曠課，我於群組中糾正後其逕行退群......最終小組解散，我獨立分配至第11組繼續進行專題。<br>
本次專題我使用Colab開發：https://colab.research.google.com/drive/1QaLxYzlXAJybnFCfOwGTWfNvDz-qy_SF?usp=sharing
# Project 2
感謝助教的指教，這天兵寫的報告總算沒那麼糟糕了。<br>
<br>
專題要求各組結合爬蟲及啟發式搜尋技術對指定列表中的各網址進行搜尋，目標為找出各網址所屬網站之「將舉辦活動總覽頁面(Event Source Page)」。課程提供Java API執行validation，學員開發之程式需與API互動，對每個提交的網址API僅回傳"正確"或"錯誤"。<br>
<br>
時過境遷，有些當時課程指定的網站已經關閉。且project需要額外安裝許多程式方能執行；爬蟲應用部分也需要搭配browser driver並根據版本調整部分程式碼。故PyCharm project壓縮檔僅供參考：https://drive.google.com/file/d/1Uh1Vv_FK_DmHlR3nTrYXDaT5Yv6fTOHV/view?usp=sharing<br>
<br>
Interpreter: Python 3.8<br>
"Output_records_from_program.txt": the outputs from my program through execution<br>
"Report_file_from_API.txt": the output file from the evaluation API.
