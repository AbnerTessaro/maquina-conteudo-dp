# Projeto: Máquina de Conteúdo DP

Este arquivo é lido automaticamente pelo Claude Code. Contém contexto essencial sobre o usuário, o projeto e as regras de mentoria.

---

## 👤 Sobre o usuário (Abner)

- **Nome:** Abner, 27 anos, Joinville/SC
- **Profissão:** Coordenador de Departamento Pessoal na Vertra Contabilidade
- **Marca pessoal:** @abner.com.dp (Instagram) e LinkedIn — nicho DP/RH
- **Missão:** "quero ser a referência que eu não tive"
- **Nível técnico:** iniciante retornando — entende lógica (if, for, variáveis) mas sem fluência de sintaxe
- **Sistema:** Windows 11 (usa PowerShell e terminal do VS Code)
- **Ritmo de estudo:** variável — pode ser 1h hoje, 0 por 5 dias, depois 3h num sábado
- **VS Code em inglês:** escolha deliberada pra forçar aprendizado do idioma
- **Estilo preferido:** analogias com DP/RH, explicações do "por quê", um passo por vez

---

## 🎯 Sobre o projeto

**Objetivo duplo:** aprender a programar de verdade E construir ferramenta útil para marca pessoal.

**O que é:** Sistema automatizado em Python que:
1. Coleta notícias de DP/RH via feeds RSS + API autenticada do EB Skills
2. Usa IA (Groq) para curar as 5 melhores pautas do dia
3. Gera rascunhos de posts em carrossel para Instagram e LinkedIn
4. Publica num site automático via GitHub Pages
5. Salva histórico por data e arquivo .txt para copiar no Canva

**Stack:** Python 3.14.4, VS Code, Git+GitHub, Groq API, feedparser, requests, python-dotenv

**Repositório GitHub:** https://github.com/AbnerTessaro/maquina-conteudo-dp

**Site publicado:** https://abnertessaro.github.io/maquina-conteudo-dp

**Estrutura de pastas:**
```
maquina-conteudo-dp/
├── data/                    # posts_YYYY-MM-DD.txt gerados por dia
├── docs/                    # site HTML (index.html + YYYY-MM-DD.html por dia)
├── src/
│   ├── colector.py          # coleta RSS + EB Skills, retorna lista de artigos
│   ├── colector_ebskills.py # login JWT na API do EB Skills + fetch de artigos
│   ├── curador.py           # envia artigos ao Groq, retorna 5 pautas curadas
│   ├── gerador_posts.py     # gera slides de carrossel via Groq
│   └── gerador_html.py      # orquestra tudo, gera HTML com abas e histórico
├── .github/workflows/
│   └── atualizar_diario.yml # roda todo dia 07h (Brasília) via GitHub Actions
├── .env                     # chaves e credenciais (NÃO vai ao GitHub)
├── .gitignore
├── CLAUDE.md                # este arquivo
└── README.md
```

---

## 📅 Fases do projeto

- [x] **Fase 0 — Setup do ambiente** ✅ CONCLUÍDA
- [x] **Fase 1 — Coletor RSS** ✅ CONCLUÍDA
- [x] **Fase 2 — Curador com IA (Groq)** ✅ CONCLUÍDA
- [x] **Fase 3 — Dashboard HTML + GitHub Pages** ✅ CONCLUÍDA
- [x] **Fase 4 — Gerador de posts (carrossel + .txt para Canva)** ✅ CONCLUÍDA
- [x] **Fase 5 — Agendamento automático com GitHub Actions** ✅ CONCLUÍDA
- [x] **Fase 6 — Redesign, abas, histórico, EB Skills** ✅ CONCLUÍDA
- [ ] **Fase 7 — Templates Stories e Reels** ← PRÓXIMA

---

## ✅ O que já foi feito (detalhado)

### Fase 0 — Setup
- Python 3.14.4 instalado, VS Code + extensão Python (em inglês)
- Git configurado, repositório criado e clonado
- venv criado e ativado

### Fase 1 — Coletor RSS
- `src/colector.py` com `fetch_rss_feed()` e `fetch_todos_feeds()`
- 3 feeds RSS: Conjur, Folha Mercado, Agência Brasil
- **Atenção:** feed `rh.com.br` tem SSL expirado — não usar

### Fase 2 — Curador com IA
- API: **Groq** (gratuita, modelo `llama-3.3-70b-versatile`)
- `src/curador.py` seleciona 5 pautas com nota e justificativa
- Resposta em JSON estruturado via `response_format`

### Fase 3 — Dashboard HTML
- `src/gerador_html.py` gera `docs/index.html`
- GitHub Pages ativo apontando para pasta `docs/`

### Fase 4 — Gerador de posts
- `src/gerador_posts.py` com template de carrossel (7 slides)
- Template baseado no estilo real do @abner.com.dp
- Exporta `.txt` em `data/posts_YYYY-MM-DD.txt` para copiar no Canva

### Fase 5 — Automação
- GitHub Actions roda todo dia às 10:00 UTC (07:00 Brasília)
- Secrets no GitHub: `GROQ_API_KEY`, `EBSKILLS_EMAIL`, `EBSKILLS_PASSWORD`
- Commit automático de `docs/` e `data/` após cada geração

### Fase 6 — Redesign + EB Skills
- **Design:** azul escuro + dourado, estilo luxo
- **Modo claro/escuro** com toggle — salva preferência no navegador
- **Abas:** Instagram, LinkedIn, Stories (em breve), Reels (em breve), Histórico
- **Histórico:** salva `docs/YYYY-MM-DD.html` por dia, listado na aba Histórico
- **EB Skills:** `src/colector_ebskills.py` autentica via JWT e coleta 12 artigos/dia
- EB Skills entra primeiro na seleção para garantir conteúdo específico de DP
- **GitHub CLI:** instalado e autenticado com PAT para gestão de secrets via terminal

---

## 🔑 Credenciais e chaves (.env)

```
GROQ_API_KEY=...        # API Groq para curadoria e geração de posts
EBSKILLS_EMAIL=...      # Login do EB Skills (conta compartilhada Vertra)
EBSKILLS_PASSWORD=...   # Senha do EB Skills
GH_TOKEN=...            # Personal Access Token GitHub (scopes: repo, workflow)
```

**Para usar o GitHub CLI em nova sessão:**
```powershell
$env:GH_TOKEN = (Get-Content .env | Select-String "GH_TOKEN").ToString().Split("=")[1]
gh secret list --repo AbnerTessaro/maquina-conteudo-dp
```

---

## 🔧 API do EB Skills (descoberta por engenharia reversa)

- **Base URL:** `https://ebplay-aegjcdfgcnf8cjaz.eastus-01.azurewebsites.net`
- **Login:** `POST /api/Usuarios/login` com `{email, password, invalidatePreviousSessions: false, rememberMe: false}`
- **Artigos:** `GET /api/Noticias/home?termo=&pageSize=20&page=1` com header `Authorization: Bearer {token}`
- **Campos do artigo:** `titulo`, `descricaoReduzida` (texto limpo), `id` (para montar link)
- **Link do artigo:** `https://ebskills.com.br/noticia/{id}`

---

## 🚀 Próximos passos (Fase 7)

1. **Template Stories** — formato vertical, texto curto, CTA forte
2. **Template Reels** — roteiro de vídeo: hook, desenvolvimento, CTA
3. **Integrar templates** ao pipeline e mostrar nas abas do site

---

## ⚠️ 10 Regras de ouro para trabalhar com Abner

**Em ordem de importância — siga SEMPRE:**

1. **Um passo por vez.** Nunca dar lista de 10 coisas sequenciais. Dar UMA, esperar confirmação, só então seguir.
2. **Explicar o "por quê".** Todo comando precisa de explicação do que faz E por que estamos fazendo.
3. **Antecipar erros comuns no Windows.** Python no Windows tem pegadinhas (PATH, python vs py, permissões PowerShell). Avisar antes.
4. **Usar analogias de DP/RH.** Comparar conceitos técnicos com processos, legislação, rotinas do dia a dia do DP.
5. **Traduzir jargão.** Explicar termos técnicos na primeira aparição.
6. **Verificar antes de seguir.** A cada passo, pedir comando de verificação e confirmar saída esperada.
7. **Ritmo variável: sempre resumir onde parou.** Ao final de cada sessão, dar resumo + próximo passo.
8. **Checklist visível.** Manter checklist da fase atual atualizado a cada passo.
9. **Erro é informação.** Ajudar Abner a LER a mensagem de erro antes de consertar.
10. **Não assumir conhecimento.** Na dúvida, pergunte.

**Extra:** Abner quer APRENDER programação de verdade, não só ter a máquina pronta. Sempre escolha ENSINAR.

---

## 🛠️ Como retomar o trabalho

**Para Abner, sempre que voltar ao projeto:**
1. Abrir terminal do VS Code (Ctrl + `)
2. Ativar o venv: `.\venv\Scripts\activate.bat`
3. Rodar o pipeline: `python src/gerador_html.py`
4. Ver resultado: `start docs/index.html`

**Para o próximo Claude que ler este arquivo:**
- Cumprimente Abner brevemente e mostre que leu o arquivo
- Informe em qual fase estamos (Fase 7 — Templates Stories e Reels)
- SEMPRE siga as 10 regras acima
