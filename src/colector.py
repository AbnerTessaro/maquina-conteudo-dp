import feedparser


def fetch_rss_feed(feed_url):
    """
    Fetches articles from an RSS feed.
    
    Args:
        feed_url (str): The URL of the RSS feed
        
    Returns:
        list: A list of articles with title, link, and summary
    """
    feed = feedparser.parse(feed_url)
    
    articles = []
    for entry in feed.entries:
        article = {
            'title': entry.get('title', 'No title'),
            'link': entry.get('link', 'No link'),
            'summary': entry.get('summary', 'No summary')
        }
        articles.append(article)
    
    return articles


if __name__ == '__main__':
    # Test with a real DP/HR RSS feed
    feed_url = 'https://www.conjur.com.br/rss.xml'
    
    print("Collecting articles from:", feed_url)
    articles = fetch_rss_feed(feed_url)
    
    print(f"\nFound {len(articles)} articles:\n")
    
    for i, article in enumerate(articles[:5], 1):  # Show first 5
        print(f"{i}. {article['title']}")
        print(f"   Link: {article['link']}\n")