# Máquina de Conteúdo DP

Sistema automatizado em Python que coleta notícias de DP/RH, usa IA para curar as melhores pautas, salva num kanban no Notion e gera rascunhos de posts para redes sociais.

Projeto de aprendizado de programação com aplicação prática para a marca pessoal [@abner.com.dp](https://instagram.com/abner.com.dp).

---

## Fases do projeto

- [x] **Fase 0 — Setup do ambiente** (Python, VS Code, Git, venv)
- [x] **Fase 1 — Coletor RSS** (`src/colector.py`)
- [x] **Fase 2 — Curador com IA** (`src/curador.py`)
- [ ] Fase 3 — Integração Notion
- [ ] Fase 4 — Gerador de posts
- [ ] Fase 5 — Agendamento automático

---

## Como usar

### Pré-requisitos

- Python 3.11+
- Conta no [Google AI Studio](https://aistudio.google.com) para obter uma API key do Gemini

### Instalação

```bash
# Clone o repositório
git clone https://github.com/AbnerTessaro/maquina-conteudo-dp.git
cd maquina-conteudo-dp

# Crie e ative o ambiente virtual
python -m venv venv
.\venv\Scripts\activate.bat   # Windows

# Instale as dependências
pip install feedparser google-generativeai python-dotenv
```

### Configuração

Crie um arquivo `.env` na raiz do projeto:

```
GEMINI_API_KEY=sua_chave_aqui
```

> O arquivo `.env` está no `.gitignore` e nunca será enviado ao GitHub.

### Executar

```bash
# Apenas coletar artigos
python src/colector.py

# Coletar e curar os mais relevantes para DP/RH
python src/curador.py
```

---

## Stack

- Python 3.14
- [feedparser](https://pythonhosted.org/feedparser/) — coleta feeds RSS
- [google-generativeai](https://pypi.org/project/google-generativeai/) — curadoria com Gemini
- [python-dotenv](https://pypi.org/project/python-dotenv/) — gerenciamento de variáveis de ambiente
- Notion API *(em breve)*
