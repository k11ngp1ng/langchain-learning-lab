"""
UNIDADE 3 — Laboratório LangChain + Ollama
03_saida_estruturada.py — Objetos Pydantic direto do modelo.

Compare com a Unidade 2: lá foram três camadas manuais (instrução no
prompt + response_format + json.loads + validação). Aqui, uma linha:
with_structured_output(Chamado).

Executar:  python 03_saida_estruturada.py
"""

from typing import Literal

from pydantic import BaseModel, Field

from config import criar_llm

llm = criar_llm("groq", temperatura=0.0)  # extração pede determinismo


# --- O contrato: as descrições vão para o modelo ---------------------
class Chamado(BaseModel):
    """Chamado de suporte de TI extraído de um e-mail."""

    titulo: str = Field(description="Resumo curto do problema, até 10 palavras")
    categoria: Literal["hardware", "software", "rede", "acesso"] = Field(
        description="Categoria técnica do problema"
    )
    urgencia: int = Field(ge=1, le=5, description="1 = baixa, 5 = crítica")
    setor: str = Field(description="Setor de origem do solicitante")


extrator = llm.with_structured_output(Chamado)

EMAILS = [
    "Bom dia, o notebook da recepção não liga desde ontem. Ninguém consegue "
    "fazer o check-in dos alunos. Setor: Secretaria Acadêmica.",

    "O wi-fi do bloco C cai a cada 10 minutos. Estou no laboratório de "
    "informática tentando dar aula. Urgente!",

    "Oi, esqueci minha senha do portal e o link de recuperação não chega. "
    "Sou do setor Financeiro e preciso lançar notas fiscais hoje.",
]

print("=" * 70)
for i, email in enumerate(EMAILS, 1):
    print(f"\n[{i}] E-MAIL:\n{email.strip()}\n")
    try:
        chamado = extrator.invoke(email)  # já retorna um objeto Chamado!
        print(f"    → titulo    : {chamado.titulo}")
        print(f"    → categoria : {chamado.categoria}")
        print(f"    → urgencia  : {chamado.urgencia}")
        print(f"    → setor     : {chamado.setor}")
        print(f"    → tipo      : {type(chamado).__name__} (objeto Python validado)")
    except Exception as e:
        # nem todo modelo suporta bem o recurso — trate sempre
        print(f"    ❌ {type(e).__name__}: {str(e)[:100]}")
print("\n" + "=" * 70)

print("\n💡 EXPERIMENTOS:")
print("   a) Acrescente um campo 'prazo_dias: int' ao contrato e rode de novo.")
print("   b) Rode com criar_llm('ollama') — o modelo local mantém o contrato?")
