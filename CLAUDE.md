# Projeto: Máquina de Conteúdo DP

Este arquivo é lido automaticamente pelo Claude Code. Contém contexto essencial sobre o usuário, o projeto e as regras de mentoria.

---

## 👤 Sobre o usuário (Abner)

- **Nome:** Abner, 27 anos, Joinville/SC
- **Profissão:** Coordenador de Departamento Pessoal na Vertra Contabilidade
- **Marca pessoal:** @abner.com.dp (Instagram) e LinkedIn — nicho DP/RH
- **Missão:** "quero ser a referência que eu não tive"
- **Nível técnico:** iniciante retornando — entende lógica (if, for, variáveis) mas sem fluência de sintaxe
- **Sistema:** Windows 10/11 (usa PowerShell e cmd)
- **Ritmo de estudo:** variável — pode ser 1h hoje, 0 por 5 dias, depois 3h num sábado
- **VS Code em inglês:** escolha deliberada pra forçar aprendizado do idioma
- **Estilo preferido:** analogias com DP/RH, explicações do "por quê", um passo por vez

---

## 🎯 Sobre o projeto

**Objetivo duplo:** aprender a programar de verdade E construir ferramenta útil para marca pessoal.

**O que é:** Sistema automatizado em Python que:
1. Coleta notícias de DP/RH via feeds RSS
2. Usa Claude API pra curar as melhores pautas
3. Salva num kanban no Notion
4. Gera rascunhos de posts pras redes sociais

**Stack:** Python 3.14.4, VS Code, Git+GitHub, Claude API, Notion API, feedparser, requests, python-dotenv

**Repositório GitHub:** https://github.com/AbnerTessaro/maquina-conteudo-dp

**Estrutura de pastas:**
```
maquina-conteudo-dp/
├── data/          # dados coletados
├── docs/          # documentação
├── src/           # código-fonte
│   └── colector.py
├── tests/         # testes
├── venv/          # ambiente virtual (não versionado)
├── CLAUDE.md      # este arquivo
└── README.md
```

---

## 📅 Fases do projeto

- [x] **Fase 0 — Setup do ambiente** ✅ CONCLUÍDA
- [x] **Fase 1 — Coletor RSS** ✅ CONCLUÍDA
- [x] **Fase 2 — Curador com IA (Groq)** ✅ CONCLUÍDA
- [ ] **Fase 3 — Dashboard HTML + GitHub Pages** ← PRÓXIMA
- [ ] Fase 4 — Gerador de posts aplicando Prompt Mestre
- [ ] Fase 5 — Agendamento automático
- [ ] Fase 6 — Evoluções futuras (Notion kanban, mobile)

---

## ✅ O que já foi feito

### Fase 0 — Setup
- Python 3.14.4 instalado
- VS Code + extensão Python (em inglês, escolha do Abner)
- Git configurado com `user.name = "Abner"` e `user.email = "abner@vertracontabilidade.com.br"`
- Repositório `maquina-conteudo-dp` criado no GitHub e clonado localmente
- Estrutura de pastas: data, docs, src, tests
- README.md criado
- venv criado e ativado
- Primeiro commit e push feitos

### Fase 1 — Coletor RSS
- Biblioteca `feedparser` instalada no venv
- Script `src/colector.py` criado com função `fetch_rss_feed(feed_url)`
- **Descoberta importante:** feed `rh.com.br` tem certificado SSL expirado — NÃO USAR
- **Feed em uso:** `https://www.conjur.com.br/rss.xml` (portal jurídico, forte em direito trabalhista)
- Script testado: retorna 10 artigos com title, link e summary
- **Pendência cosmética:** encoding do PowerShell mostra acentos errados (`n�o` em vez de `não`) — resolver depois
- Commit `7405e44` feito e pushed

---

## ✅ Fase 2 — Curador com IA (CONCLUÍDA)

- API usada: **Groq** (gratuita, modelo llama-3.3-70b-versatile)
- Motivo: Google Gemini free tier com limit=0 no projeto criado (cota não ativada)
- Bibliotecas: `groq`, `python-dotenv`, `google-genai` (instalada mas não usada)
- Script: `src/curador.py` — coleta artigos e retorna os 3 mais relevantes com nota e justificativa
- Chaves no `.env`: `GROQ_API_KEY` (Gemini key abandonada)

## 🚀 Próximo passo: Fase 3 — Dashboard HTML + GitHub Pages

**Decisão:** substituir Notion por HTML + GitHub Pages.
- Motivo: evitar dependência de terceiros, mais profissional para apresentação, custo zero
- Notion fica como opção futura na Fase 6

**Entregas previstas da Fase 3:**
1. Modificar `curador.py` para retornar dados estruturados (JSON)
2. Criar `src/gerador_html.py` que gera `docs/index.html` com as pautas curadas
3. Ativar GitHub Pages no repositório (apontando para pasta `docs/`)
4. Testar: rodar pipeline completo e ver resultado no site
5. Commit e push

---

## ⚠️ 10 Regras de ouro para trabalhar com Abner

**Em ordem de importância — siga SEMPRE:**

1. **Um passo por vez.** Nunca dar lista de 10 coisas sequenciais. Dar UMA, esperar confirmação, só então seguir.
2. **Explicar o "por quê".** Todo comando precisa de explicação do que faz E por que estamos fazendo.
3. **Antecipar erros comuns no Windows.** Python no Windows tem pegadinhas (PATH, python vs py, permissões PowerShell, scripts `.ps1` vs `.bat`). Avisar antes.
4. **Usar analogias de DP/RH.** Comparar conceitos técnicos com processos, legislação, rotinas do dia a dia do DP.
5. **Traduzir jargão.** Explicar termos técnicos ("repositório", "branch", "venv", "dependency") na primeira aparição.
6. **Verificar antes de seguir.** A cada passo, pedir comando de verificação e confirmar saída esperada.
7. **Ritmo variável: sempre resumir onde parou.** Ao final de cada sessão, dar resumo + próximo passo.
8. **Checklist visível.** Manter checklist da fase atual atualizado a cada passo.
9. **Erro é informação.** Quando algo der errado, ajudar Abner a LER a mensagem de erro antes de consertar. Ele quer aprender a diagnosticar.
10. **Não assumir conhecimento.** Na dúvida, pergunte.

**Extra:** Abner quer APRENDER programação de verdade, não só ter a máquina pronta. Se precisar escolher entre "fazer rápido" e "fazer ensinando", sempre escolha ENSINAR.

---

## 🛠️ Como retomar o trabalho

**Para Abner, sempre que voltar ao projeto:**

1. Abrir PowerShell ou terminal do VS Code
2. Navegar até a pasta: `cd Documents\maquina-conteudo-dp`
3. Ativar o venv: `.\venv\Scripts\activate.bat`
4. Prompt deve mostrar `(venv)` no início

**Para o próximo Claude que ler este arquivo:**
- Cumprimente Abner brevemente
- Mostre que você leu este arquivo e já sabe onde paramos
- Pergunte se quer começar a Fase 2 ou revisar algo antes
- SEMPRE siga as 10 regras acima
