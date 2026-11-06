import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer

df = pd.read_csv("data/pratos.csv")

SAUDAVEIS = {
    "Combinado de sushi 20 peças", "Temaki de salmão", "Uramaki vegetariano",
    "Yakisoba de legumes", "Salada caesar com frango", "Bowl de quinoa com legumes",
    "Wrap integral de frango", "Salmão grelhado com legumes", "Açaí com granola",
    "Suco verde detox", "Pizza margherita", "Guacamole com chips",
}
PESADOS = {
    "Feijoada completa", "Strogonoff de carne", "Lasanha à bolonhesa",
    "Espaguete à carbonara", "Burger bacon duplo", "Batata frita com cheddar e bacon",
    "Chili con carne", "Virado à paulista", "Pizza quatro queijos",
}
SOBREMESAS = {"Tiramisù", "Milkshake de chocolate", "Pizza doce de chocolate com morango"}


def perfil(linha):
    if linha["prato"] in SAUDAVEIS:
        return "Perfil: leve, saudável, fresco, nutritivo."
    if linha["prato"] in PESADOS:
        return "Perfil: refeição farta, substanciosa, indulgente."
    if linha["categoria"] == "Doces" or linha["prato"] in SOBREMESAS:
        return "Perfil: sobremesa, doce, indulgente."
    return ""

# Modelo que transforma texto em números e entende português
modelo = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# O texto de cada prato que será transformado em embedding
textos = (
    df["prato"] + ". " + df["descricao"]
    + " Restaurante: " + df["restaurante"]
    + ". Categoria: " + df["categoria"]
).tolist()
embeddings = modelo.encode(textos, show_progress_bar=True).tolist()

# Cria o banco (uma pasta chamada chroma_db) e a coleção de pratos
cliente = chromadb.PersistentClient(path="chroma_db")
try:
    cliente.delete_collection("pratos")  # recria do zero a cada execução
except Exception:
    pass
colecao = cliente.create_collection("pratos", metadata={"hnsw:space": "cosine"})

colecao.add(
    ids=[str(i) for i in df["id"]],
    embeddings=embeddings,
    documents=textos,
    metadatas=[
        {
            "restaurante": r.restaurante,
            "categoria": r.categoria,
            "prato": r.prato,
            "preco": float(r.preco),
            "tempo_entrega_min": int(r.tempo_entrega_min),
            "vegetariano": bool(r.vegetariano),
            "nota_restaurante": float(r.nota_restaurante),
        }
        for r in df.itertuples()
    ],
)
print(f"{colecao.count()} pratos indexados.")

# Teste: uma busca de exemplo
pergunta = "algo leve e vegetariano"
vetor = modelo.encode([pergunta]).tolist()
resultado = colecao.query(query_embeddings=vetor, n_results=5)

print(f"\nBusca: {pergunta}")
for meta in resultado["metadatas"][0]:
    print(f"- {meta['prato']} ({meta['restaurante']}) - R$ {meta['preco']:.2f}")