import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://ebplay-aegjcdfgcnf8cjaz.eastus-01.azurewebsites.net"


def login():
    url = f"{BASE_URL}/api/Usuarios/login"
    payload = {
        "email": os.getenv("EBSKILLS_EMAIL"),
        "password": os.getenv("EBSKILLS_PASSWORD"),
        "invalidatePreviousSessions": False,
        "rememberMe": False
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()

    token = (data.get("token") or
             data.get("accessToken") or
             data.get("jwtToken") or
             data.get("jwt"))

    if not token:
        raise ValueError(f"Token não encontrado. Campos na resposta: {list(data.keys())}")

    return token


def fetch_ebskills():
    token = login()

    url = f"{BASE_URL}/api/Noticias/home?termo=&pageSize=20&page=1"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    items = data if isinstance(data, list) else (
        data.get("items") or data.get("noticias") or
        data.get("data") or data.get("content") or []
    )

    articles = []
    for item in items:
        title = item.get("titulo") or item.get("title") or ""
        summary = item.get("descricaoReduzida") or item.get("descricao") or ""
        article_id = item.get("id", "")
        link = f"https://ebskills.com.br/noticia/{article_id}" if article_id else "https://ebskills.com.br"

        if title:
            summary_limpo = re.sub(r'<[^>]+>', '', summary)
            summary_limpo = summary_limpo.replace('&nbsp;', ' ').replace('&amp;', '&').strip()
            articles.append({
                "title": title,
                "link": link,
                "summary": summary_limpo[:300] if summary_limpo else ""
            })

    return articles


if __name__ == "__main__":
    print("Testando EB Skills...")
    try:
        artigos = fetch_ebskills()
        print(f"{len(artigos)} artigos encontrados\n")
        for i, a in enumerate(artigos[:5], 1):
            print(f"{i}. {a['title']}")
            print(f"   Link: {a['link']}")
            print(f"   Resumo: {a['summary'][:100]}\n")
    except Exception as e:
        print(f"Erro: {e}")
