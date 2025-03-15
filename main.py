import os
import logging
import openai
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# OpenAI APIキーとDiscordトークン
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# OpenAIのAPIキーを設定
openai.api_key = OPENAI_API_KEY

# 必要なintentsを設定
intents = discord.Intents.default()
intents.messages = True  # メッセージ関連のイベントを有効化
intents.guilds = True    # サーバー情報へのアクセスを許可

# Botのインスタンスを作成
bot = commands.Bot(command_prefix="!", intents=intents)

# 禁止ワードリスト（例として簡単なものを定義）
forbidden_words = ["badword", "exampleword"]

# OpenAIを用いてメッセージを解析する関数
def analyze_message_with_ai(message: str) -> bool:
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"このメッセージが不適切かどうか判定してください: \"{message}\"",
            max_tokens=50
        )
        result = response['choices'][0]['text'].strip().lower()
        logging.debug(f"OpenAI API Response: {result}")
        return "不適切" in result
    except Exception as e:
        logging.error(f"Error during OpenAI API analysis: {e}")
        return False

# Botの準備完了時イベント
@bot.event
async def on_ready():
    logging.info(f"Bot is ready as {bot.user}")  # 起動メッセージ
    for guild in bot.guilds:
        logging.info(f"Connected to guild: {guild.name} (ID: {guild.id})")

# メッセージを監視するイベント
@bot.event
async def on_message(message):
    logging.debug(f"Received message from {message.author}: {message.content}")  # メッセージ受信ログ

    # ボット自身のメッセージを無視
    if message.author.bot:
        logging.debug("Ignored a message from a bot.")
        return

    # 禁止ワードリストでのチェック
    if any(word in message.content for word in forbidden_words):
        logging.info(f"Forbidden word detected in message: {message.content}")
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} 禁止された言葉を含むメッセージが削除されました。")
        except discord.Forbidden:
            logging.error("Bot lacks permissions to delete messages or send messages.")
        except Exception as e:
            logging.error(f"An unexpected error occurred while deleting message: {e}")
        return

    # AIでメッセージを解析
    is_inappropriate = analyze_message_with_ai(message.content)
    if is_inappropriate:
        logging.info(f"AI flagged the message as inappropriate: {message.content}")
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} 不適切なメッセージが検出されました！")
        except discord.Forbidden:
            logging.error("Bot lacks permissions to delete messages or send messages.")
        except Exception as e:
            logging.error(f"An unexpected error occurred while handling inappropriate message: {e}")

    # コマンド処理を有効にする
    await bot.process_commands(message)

# Botを起動
try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure:
    logging.critical("Invalid Discord token provided. Please check your .env file.")
except Exception as e:
    logging.critical(f"An unexpected error occurred: {e}")
