import chromadb
from sentence_transformers import SentenceTransformer

MODELO = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
colecao = chromadb.PersistentClient(path="chroma_db").get_collection("pratos")


def buscar(pergunta, preco_max=None, tempo_max=None, vegetariano=None, n=5):
    # Monta a lista de filtros exatos, só com o que o usuário pediu
    condicoes = []
    if preco_max is not None:
        condicoes.append({"preco": {"$lte": preco_max}})
    if tempo_max is not None:
        condicoes.append({"tempo_entrega_min": {"$lte": tempo_max}})
    if vegetariano:
        condicoes.append({"vegetariano": True})

    filtro = None
    if len(condicoes) == 1:
        filtro = condicoes[0]
    elif len(condicoes) > 1:
        filtro = {"$and": condicoes}

    # Primeiro filtra pelas regras, depois ordena por semelhança de significado
    vetor = MODELO.encode([pergunta]).tolist()
    resultado = colecao.query(query_embeddings=vetor, n_results=n, where=filtro)
    return resultado["metadatas"][0]


if __name__ == "__main__":
    pratos = buscar("algo leve e saudável", preco_max=40, tempo_max=30, vegetariano=True)
    for p in pratos:
        print(f"- {p['prato']} ({p['restaurante']}) - R$ {p['preco']:.2f} - {p['tempo_entrega_min']} min")