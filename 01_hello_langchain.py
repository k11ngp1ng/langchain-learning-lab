"""
UNIDADE 3 — Laboratório LangChain + Ollama
01_hello_langchain.py — Primeiro modelo pela interface do LangChain.

Compare com a Unidade 2: lá montávamos o cliente e líamos
choices[0].message.content. Aqui o modelo é um objeto com uma
interface única, igual para todos os provedores.

Executar:  python 01_hello_langchain.py
"""

from config import criar_llm, rotulo

llm = criar_llm("groq", temperatura=0.5)
print(f"Modelo: {rotulo('groq')}\n")

# .invoke() devolve um objeto AIMessage — não um dicionário
resposta = llm.invoke("Explique, em 2 linhas, o que é LCEL no LangChain.")

print("CONTEÚDO:")
print(resposta.content)

print("\nMETADADOS:")
print(f"  tipo do objeto ..... {type(resposta).__name__}")
print(f"  tokens ............. {resposta.usage_metadata}")
print(f"  motivo da parada ... {resposta.response_metadata.get('finish_reason')}")

# Mensagens com papéis: mesma ideia de system/user da Unidade 2
from langchain_core.messages import HumanMessage, SystemMessage

conversa = [
    SystemMessage("Você é um professor de Sistemas de Informação. Seja direto."),
    HumanMessage("Cite 3 vantagens de usar um framework de orquestração de LLMs."),
]
print("\n" + "=" * 60)
print(llm.invoke(conversa).content)

# 💡 EXPERIMENTO: troque criar_llm("groq") por criar_llm("ollama").
#    O resto do arquivo continua funcionando sem nenhuma alteração.