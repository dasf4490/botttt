import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# ログ設定（デバッグしやすいようにレベルをDEBUGに設定）
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Discordトークン
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 必要なintentsを設定
intents = discord.Intents.default()
intents.messages = True  # メッセージ関連のイベントを有効化
intents.guilds = True    # サーバー情報へのアクセスを許可

# Botのインスタンスを作成
bot = commands.Bot(command_prefix="!", intents=intents)

# Botの準備完了時イベント
@bot.event
async def on_ready():
    logging.info(f"Bot is ready as {bot.user}")  # Botの準備完了メッセージ
    for guild in bot.guilds:  # 参加しているギルド（サーバー）一覧を表示
        logging.info(f"Connected to guild: {guild.name} (ID: {guild.id})")

# メッセージを監視
@bot.event
async def on_message(message):
    logging.debug(f"Received message from {message.author}: {message.content}")  # メッセージ受信ログ

    # ボット自身のメッセージを無視
    if message.author.bot:
        logging.debug("Ignored a message from a bot.")
        return

    # 禁止ワードリスト
    forbidden_words = ["badword", "exampleword"]

    # 禁止ワードチェック
    if any(word in message.content for word in forbidden_words):
        logging.info(f"Forbidden word detected in message: {message.content}")
        try:
            await message.delete()  # メッセージを削除
            await message.channel.send(f"{message.author.mention} 禁止された言葉を含むメッセージが削除されました。")
        except discord.Forbidden:
            logging.error("Bot lacks permissions to delete messages or send messages.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        return

    # 通常の返信処理（例：挨拶メッセージ）
    if message.content.lower() == "hello":
        try:
            await message.channel.send(f"Hello, {message.author.mention}! How can I help you?")
        except discord.Forbidden:
            logging.error("Bot lacks permissions to send messages in this channel.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

# Botを起動
try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure:
    logging.critical("Invalid Discord token provided. Please check your .env file.")
