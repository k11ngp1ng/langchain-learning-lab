"""
Configuração compartilhada pelos scripts da Unidade 3.

Uma única fábrica de modelos para nuvem (Groq) e local (Ollama). Como
ambos implementam a mesma interface do LangChain, o restante do código
não muda ao trocar de provedor.
"""

import os

from dotenv import load_dotenv

load_dotenv()

MODELO_GROQ = "openai/gpt-oss-20b"
MODELO_OLLAMA = "llama3.2:1b"          # use "llama3.2:1b" em máquinas com pouca RAM
URL_OLLAMA = "http://localhost:11434"


def criar_llm(provedor: str = "groq", temperatura: float = 0.5):
    """Devolve um ChatModel do LangChain para o provedor escolhido."""
    if provedor == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=MODELO_OLLAMA, temperature=temperatura,
                          base_url=URL_OLLAMA)

    if not os.getenv("GROQ_API_KEY"):
        raise SystemExit("GROQ_API_KEY não encontrada. Configure o arquivo .env.")

    from langchain_groq import ChatGroq
    return ChatGroq(model=MODELO_GROQ, temperature=temperatura)


def ollama_disponivel() -> bool:
    """Verifica se o servidor do Ollama está no ar (sem quebrar o script)."""
    try:
        import urllib.request
        with urllib.request.urlopen(URL_OLLAMA, timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def rotulo(provedor: str) -> str:
    return f"Groq / {MODELO_GROQ}" if provedor == "groq" else f"Ollama / {MODELO_OLLAMA}"
