import json
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.getcwd())
from assistente import recomendar

df = pd.read_csv("data/pratos.csv")
NOMES_PRATOS = df["prato"].unique().tolist()
VEGETARIANOS = set(df[df["vegetariano"]]["prato"])
PALAVRAS_RECUSA = ["infelizmente", "nenhum", "não temos", "não há", "não tem", "não encontrei", "não consegui"]


def precos_na_resposta(texto):
    return [float(p.replace(",", ".")) for p in re.findall(r"R\$\s*(\d+(?:,\d{1,2})?)", texto)]


def tempos_na_resposta(texto):
    return [int(t) for t in re.findall(r"(\d+)\s*min", texto)]


def avaliar(caso, resposta):
    texto = resposta.lower()
    checks = {}
    if caso.get("deve_recusar"):
        checks["recusou_corretamente"] = any(p in texto for p in PALAVRAS_RECUSA)
    elif caso.get("esperados"):
        checks["citou_prato_esperado"] = any(e.lower() in texto for e in caso["esperados"])
    if caso.get("preco_max") is not None:
        checks["respeitou_preco"] = all(p <= caso["preco_max"] for p in precos_na_resposta(resposta))
    if caso.get("tempo_max") is not None:
        checks["respeitou_tempo"] = all(t <= caso["tempo_max"] for t in tempos_na_resposta(resposta))
    if caso.get("vegetariano"):
        citados = [n for n in NOMES_PRATOS if n.lower() in texto]
        checks["so_vegetariano"] = all(n in VEGETARIANOS for n in citados)
    return checks


nome_saida = sys.argv[1] if len(sys.argv) > 1 else "resultados"
casos = json.load(open("eval/perguntas.json", encoding="utf-8"))

resultados = []
aprovados = 0
for caso in casos:
    resposta = recomendar(
        caso["pergunta"],
        preco_max=caso.get("preco_max"),
        tempo_max=caso.get("tempo_max"),
        vegetariano=caso.get("vegetariano"),
    )
    checks = avaliar(caso, resposta)
    ok = all(checks.values())
    aprovados += ok
    falhas = [nome for nome, passou in checks.items() if not passou]
    print(f"[{'OK' if ok else 'FALHOU'}] {caso['pergunta']}" + (f"  -> falhou: {', '.join(falhas)}" if falhas else ""))
    resultados.append({"pergunta": caso["pergunta"], "ok": ok, "checks": checks, "resposta": resposta})

print(f"\nResultado: {aprovados}/{len(casos)} perguntas aprovadas ({aprovados / len(casos):.0%})")
with open(f"eval/{nome_saida}.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)
print(f"Respostas salvas em eval/{nome_saida}.json")