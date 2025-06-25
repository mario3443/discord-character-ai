import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv  
import os
import asyncio
from edge_tts import Communicate
import uuid

load_dotenv()

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

# 將文字轉換成語音檔（MP3），回傳檔案名稱
async def text_to_speech(text, voice="zh-TW-YunJheNeural"):
    filename = f"voice_{uuid.uuid4().hex[:8]}.mp3"
    communicate = Communicate(text=text, voice=voice)

    await communicate.save(filename)
    return filename

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
            
            # 將文字轉語音 + 上傳檔案
            audio_file = await text_to_speech(ai_reply)
            #await message.channel.send(file=discord.File(audio_file))
            # 如果使用者在語音頻道中，bot 就加入並播放語音
            if message.author.voice and message.author.voice.channel:
                voice_channel = message.author.voice.channel

                 # 加入語音頻道（若已在就重用）
                vc = discord.utils.get(bot.voice_clients, guild=message.guild)
                if not vc or not vc.is_connected():
                     vc = await voice_channel.connect()

                 # 播放 mp3
                if vc.is_playing():
                    vc.stop()
                vc.play(discord.FFmpegPCMAudio(audio_file))

                # 等待播放完畢再離開或刪除
                while vc.is_playing():
                    await asyncio.sleep(1)

                await vc.disconnect()
                os.remove(audio_file)

            else:
                # 沒在語音頻道就改回用檔案上傳
                await message.channel.send(file=discord.File(audio_file))
                os.remove(audio_file)

            # 用完後刪除檔案避免堆積
            os.remove(audio_file)
        else:
            await message.channel.send("flask伺服器回復錯誤")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        await message.channel.send("出問題了，等我一下！")

# 啟動機器人
bot.run(TOKEN)
