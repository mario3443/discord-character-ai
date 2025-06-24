import discord
from discord.ext import commands

TOKEN = ""  # 改成你自己的

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"機器人已開啟")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  

    print(f"收到訊息：{message.content}")
    await message.channel.send("你好！這是一個 AI 回應測試機器人。")

bot.run(TOKEN)