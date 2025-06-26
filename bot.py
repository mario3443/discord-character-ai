import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv  
import os
import asyncio
from edge_tts import Communicate
import uuid
from pathlib import Path

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

# 將文字轉換為語音並儲存為 mp3 檔案
# 使用 edge_tts 進行語音合成
# 把檔案儲存在 ./voices 資料夾下
# 檔名格式為 voice_<uuid>.mp3
async def text_to_speech(text, voice="zh-TW-HsiaoChenNeural"):
    base_dir = Path("./voices")
    base_dir.mkdir(exist_ok=True)

    filename = f"voice_{uuid.uuid4().hex[:8]}.mp3"
    filepath = base_dir / filename

    communicate = Communicate(text=text, voice=voice)
    try:
        await communicate.save(str(filepath))
        print(f"✅ 已儲存語音檔：{filepath}")
        return str(filepath)
    except Exception as e:
        print(f"❌ 語音轉換失敗：{e}")
        return None

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_input = message.content.strip()
    print(f"🗨️ 收到訊息：{user_input}")

    try:
        res = requests.post(
            AI_SERVER_URL,
            json={"message": user_input},
            timeout=10
        )

        if res.status_code == 200:
            ai_reply = res.json().get("reply", "reply not found")
            await message.channel.send(ai_reply)

            # 將回應文字轉成語音檔案
            audio_file = await text_to_speech(ai_reply)

            # 防呆：如果檔案根本沒成功生成就中止
            if not audio_file or not os.path.exists(audio_file):
                await message.channel.send("語音檔案生成失敗，請稍後再試 😢")
                return

            # 如果使用者在語音頻道中，bot 就進來播放
            if message.author.voice and message.author.voice.channel:
                voice_channel = message.author.voice.channel
                vc = discord.utils.get(bot.voice_clients, guild=message.guild)

                if not vc or not vc.is_connected():
                    vc = await voice_channel.connect()

                if vc.is_playing():
                    vc.stop()
                # 如果之前有播放過，就先停止
                print(f"🎵 開始播放語音：{audio_file}")
                vc.play(discord.FFmpegPCMAudio(audio_file))

                while vc.is_playing():
                    await asyncio.sleep(1)

                await vc.disconnect()
                await asyncio.sleep(1)
                # 播放完畢後刪除語音檔案
                try:
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                        print(f"已刪除語音檔：{audio_file}")
                except Exception as e:
                    print(f"無法刪除語音檔：{e}")

            else:
                # 如果使用者不在語音頻道，則傳 mp3 檔案
                await message.channel.send(file=discord.File(audio_file))

                try:
                    os.remove(audio_file)
                    print(f"已刪除語音檔：{audio_file}")
                except Exception as e:
                    print(f"無法刪除語音檔：{e}")

        else:
            await message.channel.send(" Flask 伺服器回應錯誤，請稍後再試！")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        await message.channel.send("出問題了，等我一下！")

# 啟動機器人
bot.run(TOKEN)
