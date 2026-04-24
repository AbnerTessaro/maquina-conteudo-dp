import feedparser
from colector_ebskills import fetch_ebskills

FEEDS = [
    "https://www.conjur.com.br/rss.xml",          # Consultor Jurídico — direito trabalhista
    "https://feeds.folha.uol.com.br/mercado/rss091.xml",  # Folha — mercado/emprego
    "https://agenciabrasil.ebc.com.br/rss/economia/feed.rss",  # Agência Brasil — economia
]


def fetch_rss_feed(feed_url):
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


def fetch_todos_feeds():
    todos = []
    try:
        artigos_eb = fetch_ebskills()
        todos.extend(artigos_eb[:12])  # EB Skills primeiro — conteúdo específico de DP
    except Exception:
        pass
    for url in FEEDS:
        try:
            artigos = fetch_rss_feed(url)
            todos.extend(artigos[:5])  # 5 por feed RSS — contexto geral
        except Exception:
            pass
    return todos


if __name__ == '__main__':
    print("Coletando de todos os feeds...")
    artigos = fetch_todos_feeds()
    print(f"\nTotal: {len(artigos)} artigos coletados de {len(FEEDS)} fontes\n")
    for i, article in enumerate(artigos[:5], 1):
        print(f"{i}. {article['title']}")
        print(f"   Link: {article['link']}\n")