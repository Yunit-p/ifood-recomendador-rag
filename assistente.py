from dotenv import load_dotenv
import anthropic
from rag import buscar

load_dotenv()
cliente = anthropic.Anthropic()

INSTRUCOES = """Você é um assistente de recomendação de comida de um app de delivery.
Responda em português do Brasil, de forma simpática e curta.

REGRAS:
- Recomende SOMENTE pratos da lista fornecida. Nunca invente pratos, restaurantes, preços ou tempos.
- Use apenas as informações da lista (preço, tempo de entrega, descrição).
- Se nenhum prato da lista combinar bem com o pedido, diga isso com honestidade, em vez de forçar uma recomendação.
- Recomende no máximo 3 pratos e explique em uma frase por que cada um combina com o pedido.
- Não sugira pratos, categorias ou lugares que não estejam na lista (por exemplo, não diga 'procure saladas no app')."""

def corrigir_pergunta(pergunta):
    resposta = cliente.messages.create(
        model="claude-haiku-5-5",
        max_tokens=500,
        system=(
            "Você corrige erros de digitação em pedidos de comida em português. "
            "Devolva APENAS o pedido corrigido, sem explicações e sem acrescentar nada. "
            "Se já estiver correto, devolva igual."
        ),
        messages=[{"role": "user", "content": pergunta}],
    )
    textos = [bloco.text for bloco in resposta.content if bloco.type == "text"]
    corrigida = "".join(textos).strip().strip('"')
    return corrigida or pergunta

def recomendar(pergunta, preco_max=None, tempo_max=None, vegetariano=None):
    pergunta = corrigir_pergunta(pergunta)
    pratos = buscar(pergunta, preco_max=preco_max, tempo_max=tempo_max, vegetariano=vegetariano, n=15)
    if not pratos:
        return "Não encontrei pratos com esses filtros. Tente aumentar o preço ou o tempo de entrega."

    lista = "\n".join(
        f"- {p['prato']} | {p['restaurante']} | R$ {p['preco']:.2f} | {p['tempo_entrega_min']} min | {p['descricao']}"
        for p in pratos
    )

    resposta = cliente.messages.create(
        model="claude-haiku-5-5",
            max_tokens=1500,
        system=INSTRUCOES,
        messages=[{
            "role": "user",
            "content": f"Pedido do cliente: {pergunta}\n\nPratos disponíveis:\n{lista}",
        }],
    )
    textos = [bloco.text for bloco in resposta.content if bloco.type == "text"]
    return "".join(textos).strip() or "Não consegui gerar uma resposta agora. Tente de novo."


if __name__ == "__main__":
    print(recomendar("algo leve e saudável", preco_max=40, tempo_max=30, vegetariano=True))
    print("\n-----\n")
    print(recomendar("quero um prato com camarão"))