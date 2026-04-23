import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
from colector import fetch_rss_feed
from curador import curar_artigos
from gerador_posts import gerar_post

FEED_URL = "https://www.conjur.com.br/rss.xml"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "docs", "index.html")


def renderizar_slides(slides):
    html = ""
    for slide in slides:
        texto = slide["texto"]
        if isinstance(texto, list):
            texto = "\n".join(texto)
        texto_html = texto.replace("\n", "<br>")
        html += f"""
        <div class="slide">
            <div class="slide-header">
                <span class="slide-num">Slide {slide['numero']}</span>
                <span class="slide-titulo">{slide['titulo']}</span>
                <button class="btn-copiar" onclick="copiar(this)">Copiar</button>
            </div>
            <p class="slide-texto" data-texto="{texto.replace('"', '&quot;')}">{texto_html}</p>
        </div>"""
    return html


def gerar_html(pautas_com_posts):
    data_hoje = datetime.now().strftime("%d/%m/%Y às %H:%M")

    cards = ""
    for i, (pauta, slides) in enumerate(pautas_com_posts):
        nota = pauta.get("nota", 0)
        cor = "#22c55e" if nota >= 8 else "#f59e0b" if nota >= 6 else "#ef4444"
        slides_html = renderizar_slides(slides)

        cards += f"""
        <div class="card">
            <span class="nota" style="background:{cor};">{nota}/10</span>
            <h2><a href="{pauta['link']}" target="_blank">{pauta['titulo']}</a></h2>
            <p class="motivo">{pauta['motivo']}</p>
            <div class="card-acoes">
                <a href="{pauta['link']}" target="_blank" class="btn">Ler artigo →</a>
                <button class="btn btn-post" onclick="togglePost('post-{i}')">Ver rascunho do post ▼</button>
            </div>
            <div class="post-slides" id="post-{i}">
                <h3 class="post-titulo">Rascunho — Carrossel Instagram</h3>
                {slides_html}
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pautas DP/RH — @abner.com.dp</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #f1f5f9; color: #1e293b; }}
        header {{ background: #1e293b; color: white; padding: 2rem; text-align: center; }}
        header h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; }}
        header p {{ color: #94a3b8; font-size: 0.95rem; }}
        .atualizacao {{ text-align: center; margin: 1.5rem 0; color: #64748b; font-size: 0.9rem; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 0 1rem 3rem; }}
        .card {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .nota {{ display: inline-block; color: white; font-weight: bold; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; margin-bottom: 0.8rem; }}
        .card h2 {{ font-size: 1.1rem; margin-bottom: 0.7rem; line-height: 1.4; }}
        .card h2 a {{ color: #1e293b; text-decoration: none; }}
        .card h2 a:hover {{ color: #3b82f6; }}
        .motivo {{ color: #475569; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem; }}
        .card-acoes {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0; }}
        .btn {{ display: inline-block; background: #3b82f6; color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; font-size: 0.85rem; border: none; cursor: pointer; }}
        .btn:hover {{ background: #2563eb; }}
        .btn-post {{ background: #6366f1; }}
        .btn-post:hover {{ background: #4f46e5; }}
        .post-slides {{ display: none; margin-top: 1.2rem; border-top: 1px solid #e2e8f0; padding-top: 1rem; }}
        .post-slides.aberto {{ display: block; }}
        .post-titulo {{ font-size: 0.85rem; color: #64748b; margin-bottom: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        .slide {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin-bottom: 0.7rem; }}
        .slide-header {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }}
        .slide-num {{ background: #1e293b; color: white; font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 4px; }}
        .slide-titulo {{ font-size: 0.8rem; font-weight: bold; color: #475569; flex: 1; }}
        .btn-copiar {{ background: #10b981; color: white; border: none; padding: 0.25rem 0.6rem; border-radius: 4px; font-size: 0.75rem; cursor: pointer; }}
        .btn-copiar:hover {{ background: #059669; }}
        .btn-copiar.copiado {{ background: #6b7280; }}
        .slide-texto {{ font-size: 0.9rem; line-height: 1.6; color: #334155; white-space: pre-wrap; }}
        footer {{ text-align: center; color: #94a3b8; font-size: 0.8rem; padding: 1.5rem; }}
    </style>
</head>
<body>
    <header>
        <h1>Pautas DP/RH do Dia</h1>
        <p>Curadas por IA para @abner.com.dp</p>
    </header>
    <p class="atualizacao">Atualizado em {data_hoje}</p>
    <div class="container">
        {cards}
    </div>
    <footer>Gerado automaticamente · Máquina de Conteúdo DP</footer>
    <script>
        function togglePost(id) {{
            const el = document.getElementById(id);
            el.classList.toggle('aberto');
        }}
        function copiar(btn) {{
            const texto = btn.closest('.slide').querySelector('.slide-texto').dataset.texto;
            navigator.clipboard.writeText(texto).then(() => {{
                btn.textContent = 'Copiado!';
                btn.classList.add('copiado');
                setTimeout(() => {{ btn.textContent = 'Copiar'; btn.classList.remove('copiado'); }}, 2000);
            }});
        }}
    </script>
</body>
</html>"""


def main():
    print("Coletando artigos...")
    artigos = fetch_rss_feed(FEED_URL)
    print(f"{len(artigos)} artigos coletados. Curando com IA...")

    pautas = curar_artigos(artigos)
    print(f"{len(pautas)} pautas selecionadas. Gerando posts...")

    pautas_com_posts = []
    for i, pauta in enumerate(pautas):
        print(f"  Gerando post {i+1}/{len(pautas)}: {pauta['titulo'][:50]}...")
        slides = gerar_post(pauta, template="carrossel")
        pautas_com_posts.append((pauta, slides))

    print("Gerando HTML...")
    html = gerar_html(pautas_com_posts)

    os.makedirs(os.path.dirname(os.path.abspath(OUTPUT_FILE)), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("Site gerado em: docs/index.html")


if __name__ == "__main__":
    main()
