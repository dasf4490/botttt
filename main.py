import os
from discord.ext import commands
from utils.ai_handler import analyze_message

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # AIハンドラーを呼び出して結果を取得
    is_inappropriate = analyze_message(message.content)
    if is_inappropriate:
        await message.delete()
        await message.channel.send(f"{message.author.mention} 不適切な発言が検出されたため、メッセージを削除しました。")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
