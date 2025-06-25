import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

TOKEN = os.getenv("DISCORD_TOKEN")
AI_SERVER_URL = "http://localhost:5005/chat"

# 設定要接收訊息的權限
intents = discord.Intents.default()
intents.message_content = True

# Bot 指令前綴（不一定會用到，但習慣寫）
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"機器人已上線：{bot.user}")

@bot.event
async def on_message(message):
    # 忽略自己講的話（避免自言自語）
    if message.author == bot.user:
        return

    user_input = message.content.strip()
    print(f"收到訊息：{user_input}")

    # 把資料傳給FLASK ai_server.py
    # 這裡假設 ai_server.py 已經在本地端運行 記得去打開
    try:
        res = requests.post(
            AI_SERVER_URL,
            json={"message": user_input},
            timeout=5  # 避免伺服器沒回應卡住
        )

        if res.status_code == 200: #如果出問題給一些回復
            ai_reply = res.json().get("reply", "reply not found")
            await message.channel.send(ai_reply)
        else:
            await message.channel.send("flask伺服器回復錯誤")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        await message.channel.send("出問題了，等我一下！")

# 啟動機器人
bot.run(TOKEN)
