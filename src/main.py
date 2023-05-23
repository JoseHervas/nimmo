from modules.chat_engine import ChatEngine
from modules.telegram_client import TelegramClient
# from modules.journal_scrapper import get_latest_papers
# from modules.weather import get_weather_forecasts
# from modules.news import NewsAPI
# from memory.messages import MessageStore
import asyncio
import os
from dotenv import load_dotenv


def main():
    # Load environment variables
    load_dotenv()

    # Feature flags
    send_papers_summary = os.getenv('SEND_SUMMARY_ON_BOOTUP')
    send_weather_forecasts = os.getenv('SEND_WEATHER_FORECAST_ON_BOOTUP')
    send_news = os.getenv('SEND_NEWS_ON_BOOTUP')

    # Initialize the modules
    # MessageStore()
    chat = ChatEngine()
    telegram = TelegramClient()
    # news = NewsAPI()

    # Get weather forecasts
    if (send_weather_forecasts.lower() == "true"):
        weather_rawdata = get_weather_forecasts()
        chatbot_summary = chat.answer_question(
            f"Dame los buenos días y actúa como un hombre del tiempo que informa del parte metereológico. Haz un breve resumen de no más de 4 líneas. Expresa las temperaturas en grados celsius. Aquí tienes los datos de las previsiones metereológicas: {weather_rawdata}")
        asyncio.run(telegram.send_message(chatbot_summary))
        asyncio.run(telegram.send_file("weather.png"))

    # Get news headlines
    if (send_news.lower() == "true"):
        for category in news.get_categories():
            news_headlines = news.get_top_headlines(category)
            chatbot_summary = chat.answer_question(
                f"Actúa como un presentador y resume las siguientes noticias de {category} en 1 sólo párrafo: {news_headlines}")
            asyncio.run(telegram.send_message(chatbot_summary))

    # Get latest papers
    if (send_papers_summary.lower() == "true"):
        latest_papers = get_latest_papers("Nature")
        summary = chat.create_summary(latest_papers)
        asyncio.run(telegram.send_message(summary))

    # store = MessageStore()
    # print(store.get_relevant("noticias de salud"))

    telegram.start_listening(chat.answer_question)


main()
