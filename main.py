import os
import discord
from discord.ext import commands

# 必要なintentsを初期化
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# 環境変数からトークンを取得
discord_token = os.getenv("DISCORD_BOT_TOKEN")

# Botを初期化
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # ボットのメッセージを無視

    # 簡単な動作確認用
    if "hello" in message.content.lower():
        await message.channel.send("Hello! How can I assist you?")

# Botを起動
bot.run(discord_token)
