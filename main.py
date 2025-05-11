import os
import asyncio
import requests
from googleapiclient.discovery import build
from telegram import Bot
from telegram.constants import ParseMode

# Variáveis de ambiente
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Configurar a API do YouTube
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Função para buscar lançamentos de produtos no YouTube
def buscar_lancamentos():
    request = youtube.search().list(
        part="snippet",
        q="testosterone fat burner male enhancement",
        type="video",
        order="date",
        maxResults=5
    )
    response = request.execute()

    lancamentos = []
    for item in response['items']:
        titulo = item['snippet']['title']
        url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        lancamentos.append(f"{titulo} - {url}")

    return lancamentos

# Função assíncrona para enviar mensagens no Telegram
async def enviar_alerta(lancamentos):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    mensagem = "\n\n".join(lancamentos)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensagem, parse_mode=ParseMode.HTML)

# Função principal
async def main():
    lancamentos = buscar_lancamentos()
    if lancamentos:
        await enviar_alerta(lancamentos)

if __name__ == "__main__":
    asyncio.run(main())
