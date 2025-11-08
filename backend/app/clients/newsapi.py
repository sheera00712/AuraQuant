import os
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

class NewsAPIClient:
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY')
        self.base_url = "https://newsapi.org/v2"
        
    def _make_request(self, endpoint: str, params: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """Helper method to make requests to NewsAPI"""
        if params is None:
            params = {}
            
        params['apiKey'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"NewsAPI Error: {e}")
            return None
    
    async def get_forex_news(self, query: str = "forex OR currency OR EUR USD OR Federal Reserve"):
        """Get recent news articles related to Forex markets"""
        # Get news from last 24 hours
        from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        params = {
            'q': query,
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en'
        }
        
        return self._make_request("everything", params)
    
    async def get_sentiment_score(self, query: str = "forex") -> Optional[float]:
        """Basic sentiment analysis based on news titles"""
        news_data = await self.get_forex_news(query)
        
        if not news_data or 'articles' not in news_data:
            return None
            
        # Simple sentiment: count positive vs negative words in titles
        positive_words = {'up', 'rise', 'gain', 'bullish', 'strong', 'buy', 'positive'}
        negative_words = {'down', 'fall', 'drop', 'bearish', 'weak', 'sell', 'negative'}
        
        sentiment_score = 0
        article_count = 0
        
        for article in news_data['articles'][:10]:  # Analyze first 10 articles
            title = article.get('title', '').lower()
            
            positive_count = sum(1 for word in positive_words if word in title)
            negative_count = sum(1 for word in negative_words if word in title)
            
            if positive_count + negative_count > 0:
                sentiment_score += (positive_count - negative_count) / (positive_count + negative_count)
                article_count += 1
        
        if article_count > 0:
            return sentiment_score / article_count  # Average sentiment (-1 to +1)
        
        return 0.0  # Neutral if no articles found

# Create a global client instance
news_client = NewsAPIClient()