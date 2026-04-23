import os
import google.generativeai as genai
from dotenv import load_dotenv
from colector import fetch_rss_feed

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def curar_artigos(artigos):
    model = genai.GenerativeModel("gemini-1.5-flash")

    lista = ""
    for i, artigo in enumerate(artigos, 1):
        lista += f"{i}. Título: {artigo['title']}\n   Resumo: {artigo['summary'][:300]}\n\n"

    prompt = f"""Você é um curador de conteúdo especializado em Departamento Pessoal (DP) e Recursos Humanos (RH) no Brasil.

Analise os artigos abaixo e selecione os 3 mais relevantes para profissionais de DP/RH, considerando:
- Relevância para legislação trabalhista brasileira
- Impacto prático no dia a dia do DP
- Novidades ou mudanças importantes

Para cada artigo selecionado, informe:
- Número e título
- Nota de 1 a 10
- Por que é relevante (1 frase)

Artigos:
{lista}"""

    resposta = model.generate_content(prompt)
    return resposta.text


if __name__ == "__main__":
    feed_url = "https://www.conjur.com.br/rss.xml"

    print("Coletando artigos...")
    artigos = fetch_rss_feed(feed_url)
    print(f"{len(artigos)} artigos coletados. Enviando para o Gemini...\n")

    resultado = curar_artigos(artigos)
    print("=== CURADORIA DP/RH ===")
    print(resultado)
