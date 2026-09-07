"""
UNIDADE 3 — Laboratório LangChain + Ollama
07_chatbot_completo.py — ENTREGÁVEL: chatbot multi-provedor.

Reúne tudo da unidade: prompt template, LCEL, memória por sessão,
streaming e troca de provedor (nuvem ou local) por argumento.

Exemplos:
    python 07_chatbot_completo.py
    python 07_chatbot_completo.py --provedor ollama
    python 07_chatbot_completo.py --sessao maria --sem-stream
    python 07_chatbot_completo.py --persona "Você é um tutor de banco de dados."

Comandos durante a conversa:  /limpar   /historico   /sair
"""

import argparse

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import criar_llm, ollama_disponivel, rotulo

PERSONA_PADRAO = (
    "Você é o assistente virtual do curso de Sistemas de Informação da UDC. "
    "Seja claro e objetivo, responda em português do Brasil e admita quando "
    "não souber algo."
)

MAX_MENSAGENS = 12  # política de janela (6 turnos)
sessoes: dict[str, InMemoryChatMessageHistory] = {}


def historico_de(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in sessoes:
        sessoes[session_id] = InMemoryChatMessageHistory()
    hist = sessoes[session_id]
    if len(hist.messages) > MAX_MENSAGENS:
        hist.messages = hist.messages[-MAX_MENSAGENS:]
    return hist


def montar_bot(provedor: str, persona: str):
    llm = criar_llm(provedor, temperatura=0.5)   # ← a ÚNICA linha que muda
    prompt = ChatPromptTemplate.from_messages([
        ("system", persona),
        MessagesPlaceholder("historico"),
        ("human", "{pergunta}"),
    ])
    chain = prompt | llm | StrOutputParser()
    return RunnableWithMessageHistory(
        chain, historico_de,
        input_messages_key="pergunta",
        history_messages_key="historico",
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Chatbot LangChain multi-provedor.")
    ap.add_argument("--provedor", choices=["groq", "ollama"], default="groq")
    ap.add_argument("--sessao", default="aluno-01", help="Identificador da conversa")
    ap.add_argument("--persona", default=PERSONA_PADRAO)
    ap.add_argument("--sem-stream", action="store_true", help="Aguarda a resposta completa")
    args = ap.parse_args()

    if args.provedor == "ollama" and not ollama_disponivel():
        print("⚠️  Ollama não respondeu em localhost:11434.")
        print("   Rode 'ollama serve' e 'ollama pull llama3.2', ou use --provedor groq.")
        return

    bot = montar_bot(args.provedor, args.persona)
    cfg = {"configurable": {"session_id": args.sessao}}

    print("=" * 66)
    print(f"  🤖 Chatbot da Unidade 3  |  {rotulo(args.provedor)}")
    print(f"  sessão: {args.sessao}   |   comandos: /limpar /historico /sair")
    print("=" * 66)

    while True:
        try:
            entrada = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not entrada:
            continue
        if entrada in ("/sair", "sair"):
            break
        if entrada == "/limpar":
            sessoes.pop(args.sessao, None)
            print("🧹 Memória desta sessão apagada.")
            continue
        if entrada == "/historico":
            hist = historico_de(args.sessao).messages
            print(f"📜 {len(hist)} mensagens guardadas:")
            for m in hist:
                marca = "você" if type(m).__name__ == "HumanMessage" else "bot "
                print(f"   [{marca}] {m.content[:70]}")
            continue

        try:
            print("\nBot: ", end="", flush=True)
            if args.sem_stream:
                print(bot.invoke({"pergunta": entrada}, config=cfg).strip())
            else:
                for parte in bot.stream({"pergunta": entrada}, config=cfg):
                    print(parte, end="", flush=True)
                print()
        except Exception as e:
            print(f"\n❌ {type(e).__name__}: {str(e)[:120]}")

    print("\nAté a próxima aula! 👋")


if __name__ == "__main__":
    main()
