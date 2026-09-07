"""
UNIDADE 3 — Laboratório LangChain + Ollama
04_memoria_conversa.py — Memória de conversação por sessão.

Demonstra, em sequência:
  1. o bot LEMBRANDO (mesmo session_id);
  2. o ISOLAMENTO entre sessões diferentes;
  3. uma POLÍTICA DE JANELA para conter o crescimento do contexto.

Executar:  python 04_memoria_conversa.py
"""

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import criar_llm

llm = criar_llm("groq", temperatura=0.4)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é o assistente do curso de Sistemas de Informação. "
               "Seja breve e responda em português do Brasil."),
    MessagesPlaceholder("historico"),   # aqui entram as mensagens anteriores
    ("human", "{pergunta}"),
])

chain = prompt | llm | StrOutputParser()

# --- Armazenamento das sessões (em produção: Redis, banco, arquivo) --
sessoes: dict[str, InMemoryChatMessageHistory] = {}

MAX_MENSAGENS = 6  # política de janela: só os últimos turnos


def historico_de(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in sessoes:
        sessoes[session_id] = InMemoryChatMessageHistory()
    hist = sessoes[session_id]
    # janela deslizante: descarta as mensagens mais antigas
    if len(hist.messages) > MAX_MENSAGENS:
        hist.messages = hist.messages[-MAX_MENSAGENS:]
    return hist


bot = RunnableWithMessageHistory(
    chain,
    historico_de,
    input_messages_key="pergunta",
    history_messages_key="historico",
)


def perguntar(texto: str, sessao: str) -> None:
    cfg = {"configurable": {"session_id": sessao}}
    resposta = bot.invoke({"pergunta": texto}, config=cfg)
    print(f"\n[{sessao}] Você: {texto}")
    print(f"[{sessao}] Bot : {resposta.strip()}")


# --- 1. O bot lembra dentro da mesma sessão --------------------------
print("=" * 70)
print("1) MEMÓRIA — mesma sessão")
print("=" * 70)
perguntar("Meu nome é Ana e estou no 6º período.", "aluno-01")
perguntar("Estou estudando LangChain hoje.", "aluno-01")
perguntar("Qual é o meu nome e em que período eu estou?", "aluno-01")

# --- 2. Outra sessão não sabe de nada --------------------------------
print("\n" + "=" * 70)
print("2) ISOLAMENTO — sessão diferente")
print("=" * 70)
perguntar("Qual é o meu nome?", "aluno-02")

# --- 3. A janela em ação ---------------------------------------------
print("\n" + "=" * 70)
print(f"3) JANELA — mantendo no máximo {MAX_MENSAGENS} mensagens")
print("=" * 70)
for assunto in ["Fale de tokens.", "Fale de embeddings.", "Fale de vetores."]:
    perguntar(assunto, "aluno-01")
perguntar("Você ainda lembra o meu nome?", "aluno-01")

print(f"\nMensagens guardadas em 'aluno-01': {len(sessoes['aluno-01'].messages)}")
print("\n💡 Com a janela curta, o nome dito no início foi descartado.")
print("   Aumente MAX_MENSAGENS e rode de novo para comparar.")
