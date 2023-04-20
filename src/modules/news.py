import requests, os

class NewsAPI:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = 'https://newsapi.org/v2'
        self.categories = os.getenv('NEWS_DESIRED_CATEGORIES').split(',')

    def get_categories(self):
        return self.categories
        
    def get_top_headlines(self, category):
        print(f"[+] Retrieving top headlines for {category}...")
        url = f'{self.base_url}/top-headlines?category={category}&apiKey={self.api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json()['articles']
            filtered_articles = []
            for article in articles:
                title = article['title']
                url = article['url']
                content = article['content']
                filtered_articles.append({'title': title, 'content': content})
            return filtered_articles
        else:
            print(f'Error retrieving top headlines: {response.status_code}')
            return None