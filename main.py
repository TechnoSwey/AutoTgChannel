import asyncio
from config import BOT_TOKEN, CHANNEL_ID, POSTED_NEWS_FILE
from parser import FootballNewsParser
from bot import NewsBot

async def main():
    print("🚀 Запуск футбольного бота...")
    print("🎯 Лиги: АПЛ, Ла Лига, Серия А, ЛЧ, ЛЕ")
    
    parser = FootballNewsParser()
    bot = NewsBot(BOT_TOKEN, CHANNEL_ID, POSTED_NEWS_FILE)
    
    news = parser.get_all_news()
    await bot.post_all(news)
    
    print("\n✅ Готово!")

if __name__ == "__main__":
    asyncio.run(main())
