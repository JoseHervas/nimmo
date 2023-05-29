import requests, os

class NewsAPI:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = 'https://newsapi.org/v2'

    def get_top_headlines(self, category):
        if (self.api_key is None):
            return 'ERROR: Missing NEWS_API_KEY in environment variables'
        print(f'[+] Getting top headlines for {category}...')
        url = f'{self.base_url}/top-headlines?category={category}&apiKey={self.api_key}'
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            articles = response.json()['articles']
            filtered_articles = []
            for article in articles:
                title = article['title']
                url = article['url']
                content = article['content']
                filtered_articles.append({'title': title, 'content': content})
            print(f'[+] found {len(filtered_articles)} articles')
            return filtered_articles
        return f'[!] Error retrieving top headlines: {response.status_code}'
