import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict

class FootballNewsParser:
    def __init__(self):
        self.sources = [
            {
                'name': 'Чемпионат',
                'url': 'https://www.championat.com/football/news.html',
                'article_selector': '.news-item',
                'title_selector': '.news-item__title',
                'date_selector': '.news-item__time',
            },
            {
                'name': 'Sports.ru',
                'url': 'https://www.sports.ru/football/',
                'article_selector': '.short-news',
                'title_selector': '.short-news__title',
                'date_selector': '.short-news__date',
            }
        ]
        
        self.leagues_keywords = {
            'apl': ['apl', 'премьер-лига', 'premier league', 'англия', 'манчестер', 'ливерпуль', 'арсенал', 'челси', 'тоттенхэм', 'сити'],
            'laliga': ['ла лига', 'la liga', 'испания', 'реал', 'барселона', 'ати', 'атлетико', 'мадрид'],
            'seriea': ['серия а', 'serie a', 'италия', 'милан', 'интер', 'ювентус', 'юве', 'наполи'],
            'champions': ['лига чемпионов', 'champions league', 'лч', 'ucl'],
            'europa': ['лига европы', 'europa league', 'ле', 'uel']
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_news_id(self, title: str, date: str) -> str:
        clean = ''.join(c for c in title if c.isalnum() or c == ' ')
        return f"{clean}_{date}".replace(' ', '_').lower()
    
    def check_league(self, title: str) -> tuple:
        title_lower = title.lower()
        
        for league, keywords in self.leagues_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    league_names = {
                        'apl': '🇬🇧 АПЛ',
                        'laliga': '🇪🇸 Ла Лига',
                        'seriea': '🇮🇹 Серия А',
                        'champions': '🇪🇺 Лига Чемпионов',
                        'europa': '🇪🇺 Лига Европы'
                    }
                    return True, league_names.get(league, league)
        
        return False, None
    
    def parse_source(self, source: Dict) -> List[Dict]:
        news_list = []
        
        try:
            print(f"📡 Парсинг {source['name']}...")
            resp = requests.get(source['url'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            articles = soup.select(source['article_selector'])[:20]
            
            for art in articles:
                title_elem = art.select_one(source['title_selector'])
                date_elem = art.select_one(source['date_selector'])
                
                if title_elem and date_elem:
                    title_text = title_elem.get_text(strip=True)
                    date_text = date_elem.get_text(strip=True)
                    
                    is_needed, league_name = self.check_league(title_text)
                    
                    if is_needed:
                        news_list.append({
                            'id': self.get_news_id(title_text, date_text),
                            'title': title_text,
                            'date': date_text,
                            'source': source['name'],
                            'league': league_name
                        })
                        print(f"  ✅ {league_name}: {title_text[:50]}...")
                    
        except Exception as e:
            print(f"❌ Ошибка парсинга {source['name']}: {e}")
        
        return news_list
    
    def get_all_news(self) -> List[Dict]:
        print("\n🔍 Поиск новостей по лигам:")
        print("   АПЛ | Ла Лига | Серия А | ЛЧ | ЛЕ\n")
        
        all_news = []
        for source in self.sources:
            news = self.parse_source(source)
            all_news.extend(news)
        
        print(f"\n📊 Всего найдено: {len(all_news)}")
        return all_news
