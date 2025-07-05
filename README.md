# discord-character-ai - Discord 個性化 AI 機器人

## 學習背景

這個專案是我在看到YouTube上的一位實況主的影片時產生的靈感。影片中他展示了一個可以讀取聊天室並依照指定「個性」回應的機器人，覺得非常有趣，因此我也試著自己實作，當作一個小型專題來學習後端整合與 AI 應用。

## 功能介紹

- 可以在 `ai_server.py` 中修改 prompt，自訂機器人的個性（目前裡面是用 DeepSeek 生成的範例）
  
- 將在discord所指定的文字頻道所收到的訊息收到傳送到flask後端來連結chatgpt API來回答

- 若今天使用者不在discord語音頻道，則會將語音檔直接上傳到頻道，供用戶聆聽
  
![image](https://github.com/user-attachments/assets/ceedaf02-468a-493a-8c0e-196076bd8384)

![image](https://github.com/user-attachments/assets/9e9ebd6a-af99-4c5c-ad9b-8ac85fbf3c8d)

![image](https://github.com/user-attachments/assets/3b4b7622-ea6f-4d32-b299-d98d39e28a87)

## 如何使用

先clone此專案到你的資料夾當中

然後設置一個檔案為.env後放入以下資訊

```
DISCORD_TOKEN=你的 Discord Bot Token
OPENAI_API_KEY=你的 OpenAI API Key
```

隨後即可啟動python

分別為

```python bot.py```

和

```python ai_server.py```

## 學習或利用到的知識

### discord.py（discord機器人知識）

### Flask（作為後端連接chatgpt的API）

### edge-tts （將文字轉為語音）

### dotenv （做.env檔案來保存自己的apikey之類的不能上傳的檔案）

## 注意事項

若沒有安裝ffmpeg請記得安裝，然後將環境變數的PATH進行指定，不然會有沒辦法撥放tts的mp3檔案的問題出現
