import asyncio
from telegram import Bot
from telegram.error import TelegramError
from collections import defaultdict

class NewsBot:
    def __init__(self, token: str, channel_id: str, storage_file: str):
        self.bot = Bot(token=token)
        self.channel_id = channel_id
        self.storage_file = storage_file
        self.posted = self.load_posted()
    
    def load_posted(self) -> set:
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f)
        except FileNotFoundError:
            return set()
    
    def save_posted(self, news_id: str):
        with open(self.storage_file, 'a', encoding='utf-8') as f:
            f.write(f"{news_id}\n")
    
    def format_message(self, news: dict) -> str:
        source_emoji = '⚽' if news['source'] == 'Чемпионат' else '🏆'
        
        hashtag = news['league'].replace('🇬🇧', 'APL').replace('🇪🇸', 'LaLiga').replace('🇮🇹', 'SerieA').replace('🇪🇺', 'UCL').replace(' ', '_')
        
        return (f"{news['league']} {source_emoji}\n\n"
                f"*{news['title']}*\n\n"
                f"🕒 {news['date']} | {news['source']}\n"
                f"#{hashtag} #футбол")
    
    async def post_news(self, news: dict):
        if news['id'] in self.posted:
            return False
        
        try:
            msg = self.format_message(news)
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=msg,
                parse_mode='Markdown'
            )
            self.posted.add(news['id'])
            self.save_posted(news['id'])
            print(f"✅ [{news['league']}] {news['title'][:50]}...")
            return True
        except TelegramError as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    async def post_all(self, news_list: list):
        if not news_list:
            print("📭 Новых новостей нет")
            return
        
        by_league = defaultdict(list)
        for news in news_list:
            by_league[news['league']].append(news)
        
        print("\n📢 Отправка в канал:")
        for league, items in by_league.items():
            print(f"{league}: {len(items)}")
            for news in items:
                await self.post_news(news)
                await asyncio.sleep(1)
