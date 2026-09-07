"""
UNIDADE 3 — Laboratório LangChain + Ollama
02_prompt_lcel.py — Prompt templates e o operador pipe (LCEL).

Demonstra: template com variáveis, a chain (prompt | llm | parser)
e as três formas de executar o MESMO Runnable: invoke, batch e stream.

Executar:  python 02_prompt_lcel.py
"""

import time

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config import criar_llm

llm = criar_llm("groq", temperatura=0.4)

# --- 1. O prompt é um COMPONENTE, com variáveis nomeadas ------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um tutor de {area}. Responda em até {limite} linhas, "
               "em português do Brasil, sem jargões desnecessários."),
    ("human", "{pergunta}"),
])

# --- 2. A chain: saída de um componente vira entrada do próximo -----
chain = prompt | llm | StrOutputParser()

# --- 3a. invoke: uma execução ---------------------------------------
print("=" * 62)
print("INVOKE — uma pergunta")
print("=" * 62)
print(chain.invoke({"area": "redes", "limite": 3, "pergunta": "O que é DNS?"}))

# --- 3b. batch: várias entradas em paralelo -------------------------
print("\n" + "=" * 62)
print("BATCH — três perguntas em paralelo")
print("=" * 62)
perguntas = [
    {"area": "redes", "limite": 2, "pergunta": "O que é DHCP?"},
    {"area": "banco de dados", "limite": 2, "pergunta": "O que é uma chave estrangeira?"},
    {"area": "segurança", "limite": 2, "pergunta": "O que é autenticação em dois fatores?"},
]

inicio = time.perf_counter()
respostas = chain.batch(perguntas)
tempo_batch = time.perf_counter() - inicio

for entrada, saida in zip(perguntas, respostas):
    print(f"\n▸ {entrada['pergunta']}\n  {saida.strip()}")
print(f"\n[batch com {len(perguntas)} perguntas: {tempo_batch:.2f}s]")

# --- 3c. stream: resposta em tempo real ------------------------------
print("\n" + "=" * 62)
print("STREAM — resposta chegando aos poucos")
print("=" * 62)
for parte in chain.stream({"area": "redes", "limite": 5,
                           "pergunta": "Explique o que acontece ao digitar uma URL no navegador."}):
    print(parte, end="", flush=True)
print()

print("\n💡 A MESMA chain atendeu aos três modos. É o contrato Runnable.")
print("   EXPERIMENTO: meça um for com invoke() e compare com o batch acima.")
