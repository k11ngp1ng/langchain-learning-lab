"""
UNIDADE 3 — Laboratório LangChain + Ollama
06_tools_agente.py — Ferramentas com @tool e agente ReAct.

Compare com a Unidade 2: o JSON Schema escrito à mão dá lugar aos type
hints + docstring. E o laço de function calling vira um agente pronto.

Executar:  python 06_tools_agente.py
"""

from datetime import datetime

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from config import criar_llm

# --- Ferramentas: type hints + docstring viram o schema --------------
ESTOQUE = {"B123": 42, "A900": 0, "C777": 8}


@tool
def consultar_estoque(sku: str) -> str:
    """Consulta a quantidade em estoque de um produto pelo código SKU."""
    qtd = ESTOQUE.get(sku.upper())
    if qtd is None:
        return f"SKU {sku} não encontrado no catálogo."
    return f"SKU {sku.upper()}: {qtd} unidades em estoque."


@tool
def calcular(expressao: str) -> str:
    """Calcula uma expressão aritmética simples, por exemplo '42 * 89.90'."""
    permitidos = set("0123456789+-*/(). ")
    if not set(expressao) <= permitidos:
        return "Erro: a expressão contém caracteres não permitidos."
    try:
        return str(eval(expressao))  # entrada filtrada acima
    except Exception as e:
        return f"Erro ao calcular: {e}"


@tool
def data_atual() -> str:
    """Retorna a data de hoje no formato dd/mm/aaaa."""
    return datetime.now().strftime("%d/%m/%Y")


FERRAMENTAS = [consultar_estoque, calcular, data_atual]

# --- Parte 1: o modelo apenas PEDE a ferramenta ----------------------
llm = criar_llm("groq", temperatura=0.0)
llm_com_tools = llm.bind_tools(FERRAMENTAS)

print("=" * 72)
print("1) bind_tools — o modelo devolve a INTENÇÃO, não o resultado")
print("=" * 72)
msg = llm_com_tools.invoke("Quantas unidades do SKU B123 temos?")
print(f"conteúdo em texto : {msg.content!r}")
print(f"tool_calls        : {msg.tool_calls}")
print("\n→ Repare: a execução ainda é responsabilidade do SEU código.")

# --- Parte 2: o agente fecha o laço sozinho --------------------------
print("\n" + "=" * 72)
print("2) create_react_agent — raciocinar, agir, observar")
print("=" * 72)

agente = create_react_agent(llm, FERRAMENTAS)

PERGUNTA = ("Quantas unidades do SKU B123 temos em estoque? Se cada uma custa "
            "R$ 89,90, qual o valor total imobilizado? Informe também a data de hoje.")
print(f"\nPergunta: {PERGUNTA}\n")

resultado = agente.invoke(
    {"messages": [("user", PERGUNTA)]},
    config={"recursion_limit": 12},  # teto de passos: evita laço infinito
)

# Rastreia cada passo do raciocínio
for m in resultado["messages"]:
    tipo = type(m).__name__
    if tipo == "AIMessage" and m.tool_calls:
        for tc in m.tool_calls:
            print(f"🔧 pediu  : {tc['name']}({tc['args']})")
    elif tipo == "ToolMessage":
        print(f"   obteve : {m.content}")

print("\nRESPOSTA FINAL:")
print(resultado["messages"][-1].content)

print("\n💡 EXPERIMENTOS:")
print("   a) Piore a docstring de calcular() e veja o agente deixar de usá-la.")
print("   b) Rode com criar_llm('ollama') — o modelo local usa as ferramentas?")
