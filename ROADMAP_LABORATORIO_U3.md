# 🗺️ Roadmap do Laboratório — Unidade 3
## LangChain e modelos locais com Ollama

> **Objetivo:** reconstruir com LangChain tudo o que você fez na mão na Unidade 2 — e ir além: memória por sessão, agente com ferramentas e o mesmo código rodando na nuvem **ou** localmente.
>
> **Pré-requisito:** laboratórios das Unidades 1 e 2 concluídos (venv + `GROQ_API_KEY` no `.env`).
> **Tempo estimado:** 100–140 minutos (o download do modelo do Ollama roda em paralelo).

---

## ✅ Passo 1 — Instalar o LangChain

Reutilize o venv da disciplina (ou crie a pasta `lab-langchain-ollama` e copie o `.env`). Com o `(.venv)` ativo:

```bash
pip install -r requirements.txt
```

| Pacote | Para quê |
|---|---|
| `langchain` / `langchain-core` | Prompts, chains, parsers e a interface Runnable |
| `langchain-groq` | Provedor de nuvem gratuito (o mesmo da Unidade 1) |
| `langchain-ollama` | Modelos rodando na sua máquina |
| `langgraph` | Agente ReAct pronto (`create_react_agent`) |

> ⚠️ **O LangChain evolui rápido.** O `requirements.txt` fixa a faixa de versões testada nesta aula. Se algum import falhar, confira a documentação oficial da versão instalada antes de sair alterando o código.

**Dica de tempo:** já inicie o Passo 5 (download do modelo do Ollama) agora, em outro terminal — ele leva alguns minutos e roda em segundo plano.

---

## ✅ Passo 2 — Primeira chain (`01` e `02`)

```bash
python 01_hello_langchain.py
python 02_prompt_lcel.py
```

- **01** — `ChatGroq`, `.invoke()`, e o objeto `AIMessage` (`.content`, `.usage_metadata`).
- **02** — `ChatPromptTemplate` + o operador pipe: `prompt | llm | StrOutputParser()`. Demonstra também `batch()` e `stream()` na **mesma** chain.

**Observe:** a chain é montada uma vez e reaproveitada com entradas diferentes. Compare com as f-strings da Unidade 2.

---

## ✅ Passo 3 — Saída estruturada (`03`)

```bash
python 03_saida_estruturada.py
```

`with_structured_output(Chamado)` substitui, em uma linha, as três camadas que você escreveu manualmente na Unidade 2 (instrução no prompt + `response_format` + `json.loads` + validação).

**Experimente:** quebre o contrato (peça um campo que o texto não contém) e observe o tratamento de erro.

---

## ✅ Passo 4 — Memória por sessão (`04`)

```bash
python 04_memoria_conversa.py
```

Demonstra três coisas em sequência:
1. o bot **lembrando** do que foi dito (mesmo `session_id`);
2. o **isolamento** entre sessões (outro `session_id` não sabe nada);
3. uma **política de janela** que mantém só as últimas mensagens.

---

## ✅ Passo 5 — Instalar o Ollama e rodar local (`05`)

1. Baixe e instale em **https://ollama.com** (Windows, macOS ou Linux).
2. No terminal:

```bash
ollama pull llama3.2      # ~2 GB, roda com 8 GB de RAM
ollama list               # confirma o download
ollama run llama3.2       # teste rápido no terminal (digite /bye para sair)
```

3. Rode a comparação nuvem × local:

```bash
python 05_ollama_local.py
```

O script executa **a mesma chain** no Groq e no Ollama, medindo latência e mostrando as duas respostas lado a lado.

> 💡 Sem RAM suficiente? Use `ollama pull llama3.2:1b`. Sem conseguir instalar? O script detecta a ausência do servidor e segue apenas com o Groq — você ainda entrega o exercício.

---

## ✅ Passo 6 — Ferramentas, agente e chatbot completo (`06` e `07`)

```bash
python 06_tools_agente.py
python 07_chatbot_completo.py                      # nuvem (Groq)
python 07_chatbot_completo.py --provedor ollama    # local
python 07_chatbot_completo.py --sessao maria       # outra sessão
```

- **06** — `@tool`, `bind_tools` e o agente ReAct com `create_react_agent`, imprimindo cada passo do raciocínio.
- **07** — o entregável: chatbot de terminal com memória, streaming e troca de provedor por argumento.

---

## 🧪 Experimentos propostos

1. **Mesma chain, dois cérebros** — no `05`, troque a pergunta por algo que exija raciocínio em etapas. O modelo local acompanha?
2. **A docstring importa** — no `06`, piore de propósito a descrição de uma ferramenta e veja o agente deixar de usá-la.
3. **Memória em ação** — no `07`, diga seu nome, mude de assunto e depois pergunte "qual é o meu nome?". Repita com `--sessao outro`.
4. **Batch** — no `02`, compare o tempo de `batch()` com um `for` chamando `invoke()` cinco vezes.

---

## 🆘 Erros comuns (troubleshooting)

| Sintoma | Causa provável | Solução |
|---|---|---|
| `ImportError` em `langchain_groq` | Pacote não instalado no venv ativo | Ative o `(.venv)` e rode `pip install -r requirements.txt` |
| `ConnectionError` / `Connection refused` (Ollama) | Servidor não está rodando | Execute `ollama serve` ou abra o aplicativo do Ollama |
| `model "llama3.2" not found` | Modelo não baixado | `ollama pull llama3.2` e confirme com `ollama list` |
| Ollama muito lento | Modelo grande para a RAM disponível | Use `llama3.2:1b` ou feche outros programas |
| `RateLimitError` no Groq | Limite do plano gratuito | Aguarde ~30 s; evite laços com muitas chamadas |
| Agente não usa a ferramenta | Docstring vaga ou modelo sem suporte a tools | Melhore a descrição; para agentes prefira Groq ou um modelo local com suporte a ferramentas |
| Agente entra em laço | Sem limite de iterações | O script já usa `recursion_limit`; não o aumente sem necessidade |
| `ValidationError` no `03` | O texto não contém os dados do contrato | Ajuste o texto de entrada ou torne o campo opcional |

---

## 📦 Estrutura final

```
lab-langchain-ollama/
├── .env                      ← GROQ_API_KEY
├── .gitignore
├── requirements.txt
├── config.py                 ← fábrica de modelos (nuvem/local)
├── 01_hello_langchain.py
├── 02_prompt_lcel.py
├── 03_saida_estruturada.py
├── 04_memoria_conversa.py
├── 05_ollama_local.py
├── 06_tools_agente.py
└── 07_chatbot_completo.py
```

**Entrega:** prints da execução dos scripts 02 a 07 (incluindo a comparação nuvem × local do `05`) e as respostas dos experimentos.

Bom laboratório! 🚀
