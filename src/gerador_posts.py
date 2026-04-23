import os
import sys
import json
from groq import Groq
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TEMPLATES = {
    "carrossel": {
        "descricao": "Carrossel educativo estilo @Abner.com.dp",
        "prompt": """Você é um ghostwriter especializado em conteúdo para Instagram de profissionais de Departamento Pessoal (DP) e RH.

Você escreve no estilo de Abner Tessaro (@Abner.com.dp), coordenador de DP de 27 anos.

REGRAS DE ESTILO:
- Tom direto, técnico mas acessível
- Fala com o profissional de RH/DP ("sua empresa", "seu funcionário")
- Referencia legislação com precisão quando relevante (ex: "art. 473 da CLT", "Lei nº X/XXXX")
- SEM emojis no corpo do texto (✅ apenas em listas de checklist quando apropriado)
- Frases curtas e objetivas
- Títulos dos slides em CAIXA ALTA
- Palavras-chave importantes entre **asteriscos** para indicar negrito
- CTA fixo no último slide: "SALVA ESSE POST [motivo] ↓\\nFicou com dúvida? Me chama no direct."

ESTRUTURA DO CARROSSEL (7 slides):
1. CAPA: Pergunta ou afirmação de impacto (máx 10 palavras, sem ponto final)
2. Resposta direta ou contexto — frase curta + explicação em 2 linhas
3. O QUE MUDA NA PRÁTICA — bullet points com obrigações/mudanças (• Verbo em negrito + complemento)
4. COMO SE ADEQUAR / REQUISITOS — lista numerada (1. **Ação** + detalhe)
5. O RISCO DE NÃO SE ADEQUAR — consequências em bullet points
6. RESUMO PRÁTICO — síntese direta do que fazer
7. CTA FINAL — "SALVA ESSE POST [motivo] ↓ / Dúvida? Me chama no direct."

Baseado no artigo abaixo, gere o carrossel completo em JSON:
{
  "slides": [
    {"numero": 1, "titulo": "CAPA", "texto": "..."},
    {"numero": 2, "titulo": "CONTEXTO", "texto": "..."},
    {"numero": 3, "titulo": "O QUE MUDA NA PRÁTICA", "texto": "..."},
    {"numero": 4, "titulo": "COMO SE ADEQUAR", "texto": "..."},
    {"numero": 5, "titulo": "O RISCO DE NÃO SE ADEQUAR", "texto": "..."},
    {"numero": 6, "titulo": "RESUMO PRÁTICO", "texto": "..."},
    {"numero": 7, "titulo": "CTA", "texto": "..."}
  ]
}

ARTIGO:
Título: {titulo}
Resumo: {resumo}
Motivo da relevância: {motivo}"""
    }
}


def gerar_post(pauta, template="carrossel"):
    if template not in TEMPLATES:
        raise ValueError(f"Template '{template}' não encontrado. Disponíveis: {list(TEMPLATES.keys())}")

    prompt = TEMPLATES[template]["prompt"]
    prompt = prompt.replace("{titulo}", pauta["titulo"])
    prompt = prompt.replace("{resumo}", pauta.get("resumo", pauta.get("motivo", "")))
    prompt = prompt.replace("{motivo}", pauta["motivo"])

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    dados = json.loads(resposta.choices[0].message.content)
    return dados.get("slides", [])


def imprimir_post(slides, titulo_artigo):
    print(f"\n{'='*60}")
    print(f"POST: {titulo_artigo}")
    print(f"{'='*60}")
    for slide in slides:
        print(f"\n--- Slide {slide['numero']}: {slide['titulo']} ---")
        texto = slide["texto"]
        if isinstance(texto, list):
            print("\n".join(texto))
        else:
            print(texto)


if __name__ == "__main__":
    from colector import fetch_rss_feed
    from curador import curar_artigos

    print("Coletando e curando artigos...")
    artigos = fetch_rss_feed("https://www.conjur.com.br/rss.xml")
    pautas = curar_artigos(artigos)

    print(f"\n{len(pautas)} pautas curadas. Gerando posts...\n")

    for pauta in pautas[:1]:  # Gera post para a primeira pauta como teste
        slides = gerar_post(pauta, template="carrossel")
        imprimir_post(slides, pauta["titulo"])
