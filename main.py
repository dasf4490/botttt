import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Botトークンとコマンドプレフィックス
BOT_PREFIX = "!"
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 必要なintentsを設定
intents = discord.Intents.default()
intents.messages = True  # メッセージ関連のイベントを有効化
intents.guilds = True    # サーバー関連のイベントを有効化

# Botのインスタンスを作成
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Bot準備完了時のイベント
@bot.event
async def on_ready():
    logging.info(f"Bot is ready as {bot.user}")

# メッセージを監視するイベント
@bot.event
async def on_message(message):
    logging.info(f"Received message from {message.author}: {message.content}")

    if message.author.bot:
        logging.info("Message ignored: Sent by bot.")
        return  # ボットのメッセージは無視

    # 簡易的な禁止ワードチェック（例として「badword」を使用）
    forbidden_words = ["badword", "exampleword"]
    if any(word in message.content for word in forbidden_words):
        logging.info(f"Forbidden word detected in message: {message.content}")
        await message.delete()  # メッセージを削除
        await message.channel.send(f"{message.author.mention} 禁止された言葉を含むメッセージが削除されました。")

# Botを起動
bot.run(DISCORD_TOKEN)
