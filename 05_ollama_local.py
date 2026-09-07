"""
UNIDADE 3 — Laboratório LangChain + Ollama
05_ollama_local.py — A MESMA chain na nuvem e na sua máquina.

Executa prompt | llm | parser no Groq e no Ollama, medindo latência e
mostrando as respostas lado a lado. Se o Ollama não estiver rodando, o
script avisa e segue apenas com o Groq.

Pré-requisito:  ollama pull llama3.2

Executar:  python 05_ollama_local.py
"""

import time

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config import criar_llm, ollama_disponivel, rotulo

PERGUNTAS = [
    "O que é uma API REST? Responda em 2 linhas.",
    "Cite 3 boas práticas de segurança de senhas.",
    "Um servidor processa 3 requisições por segundo. Quantas são em 8 horas? "
    "Mostre o cálculo passo a passo.",
]

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um professor de TI. Seja objetivo e responda em português."),
    ("human", "{pergunta}"),
])

# --- Quais provedores estão disponíveis? -----------------------------
provedores = ["groq"]
if ollama_disponivel():
    provedores.append("ollama")
    print("✅ Servidor do Ollama detectado.\n")
else:
    print("⏭  Ollama não detectado (rode 'ollama serve' e 'ollama pull llama3.2').")
    print("   Seguindo apenas com o Groq.\n")

resultados = {}

for provedor in provedores:
    print("=" * 72)
    print(f"PROVEDOR: {rotulo(provedor)}")
    print("=" * 72)

    try:
        llm = criar_llm(provedor, temperatura=0.3)
        chain = prompt | llm | StrOutputParser()   # a MESMA chain!
    except Exception as e:
        print(f"❌ Falha ao criar o modelo: {e}\n")
        continue

    tempos = []
    for pergunta in PERGUNTAS:
        try:
            inicio = time.perf_counter()
            resposta = chain.invoke({"pergunta": pergunta})
            latencia = time.perf_counter() - inicio
            tempos.append(latencia)
            print(f"\n▸ {pergunta}")
            print(f"  ({latencia:.2f}s) {resposta.strip()[:320]}")
        except Exception as e:
            print(f"\n▸ {pergunta}\n  ❌ {type(e).__name__}: {str(e)[:90]}")

    if tempos:
        resultados[rotulo(provedor)] = sum(tempos) / len(tempos)
    print()

# --- Comparativo ------------------------------------------------------
if resultados:
    print("=" * 72)
    print(f"{'PROVEDOR / MODELO':<44}{'LATÊNCIA MÉDIA':>16}")
    print("=" * 72)
    for nome, media in sorted(resultados.items(), key=lambda t: t[1]):
        print(f"{nome:<44}{media:>15.2f}s")
    print("=" * 72)

print("\n📝 Entrega: monte a tabela comparando latência E qualidade.")
print("   Lembre-se: a 1ª chamada ao Ollama carrega o modelo na RAM e é mais lenta.")
print("   Onde o local compensa? E onde a nuvem é indispensável?")
