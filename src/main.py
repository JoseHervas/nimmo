from dotenv import load_dotenv
from modules.language import LanguageEngine
from modules.ui import TelegramClient
# from modules.scientific_journals import get_latest_papers

def main():

    # Load environment variables
    load_dotenv()

    # Initialize the main modules
    chat = LanguageEngine()
    telegram = TelegramClient()

    # Get weather forecasts
    # if (send_weather_forecasts.lower() == "true"):
    #     weather_rawdata = get_weather_forecasts()
    #     chatbot_summary = chat.answer_question(
    #         f"Dame los buenos días y actúa como un hombre del tiempo que informa del parte metereológico. Haz un breve resumen de no más de 4 líneas. Expresa las temperaturas en grados celsius. Aquí tienes los datos de las previsiones metereológicas: {weather_rawdata}")
    #     asyncio.run(telegram.send_message(chatbot_summary))
    #     asyncio.run(telegram.send_file("weather.png"))

    # Get news headlines
    # if (send_news.lower() == "true"):
    #     for category in news.get_categories():
    #         news_headlines = news.get_top_headlines(category)
    #         chatbot_summary = chat.answer_question(
    #             f"Actúa como un presentador y resume las siguientes noticias de {category} en 1 sólo párrafo: {news_headlines}")
    #         asyncio.run(telegram.send_message(chatbot_summary))

    # Get latest papers
    # if (send_papers_summary.lower() == "true"):
    #     latest_papers = get_latest_papers("Nature")
    #     summary = chat.create_summary(latest_papers)
    #     asyncio.run(telegram.send_message(summary))

    telegram.start_listening(chat.answer_question)


main()
