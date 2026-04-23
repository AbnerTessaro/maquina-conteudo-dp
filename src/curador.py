import os
import json
from groq import Groq
from dotenv import load_dotenv
from colector import fetch_rss_feed

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def curar_artigos(artigos):
    lista = ""
    for i, artigo in enumerate(artigos, 1):
        lista += f"{i}. Título: {artigo['title']}\n   Resumo: {artigo['summary'][:300]}\n   Link: {artigo['link']}\n\n"

    prompt = f"""Você é um curador de conteúdo especializado em Departamento Pessoal (DP) e Recursos Humanos (RH) no Brasil.

Analise os artigos abaixo e selecione os 5 mais relevantes para profissionais de DP/RH, considerando:
- Relevância para legislação trabalhista brasileira
- Impacto prático no dia a dia do DP
- Novidades ou mudanças importantes

Responda APENAS com JSON neste formato exato:
{{
  "artigos": [
    {{
      "titulo": "título do artigo",
      "link": "url do artigo",
      "nota": 8,
      "motivo": "explicação em 1 frase de por que é relevante para DP/RH"
    }}
  ]
}}

Artigos:
{lista}"""

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    texto = resposta.choices[0].message.content
    dados = json.loads(texto)
    return dados.get("artigos", [])


if __name__ == "__main__":
    feed_url = "https://www.conjur.com.br/rss.xml"

    print("Coletando artigos...")
    artigos = fetch_rss_feed(feed_url)
    print(f"{len(artigos)} artigos coletados. Enviando para curadoria...\n")

    pautas = curar_artigos(artigos)

    print("=== CURADORIA DP/RH ===")
    for i, pauta in enumerate(pautas, 1):
        print(f"\n{i}. {pauta['titulo']}")
        print(f"   Nota: {pauta['nota']}/10")
        print(f"   Por que: {pauta['motivo']}")
        print(f"   Link: {pauta['link']}")
