# 🍽️ Assistente de recomendação de comida (RAG + LLM)

Assistente que recomenda pratos de delivery a partir de pedidos em linguagem natural, como *"algo leve e saudável"* ou *"uma comida quente e reconfortante"*. Ele só recomenda o que existe no cardápio e avisa quando não encontra nada que combine.

**👉 Demo ao vivo: https://assistente-delivery-ifood.streamlit.app**

> Se o app estiver "dormindo" (hospedagem gratuita hiberna após cerca de 12 horas sem acesso), clique no botão para acordá-lo. Leva cerca de 1 minuto. A primeira pergunta também demora um pouco mais, porque o app carrega o modelo de busca.

## Como funciona

```
Pedido do usuário
   │
   ▼
1. Correção de digitação (Claude Haiku 5.5)
   │
   ▼
2. Filtros exatos: preço máximo, tempo de entrega, vegetariano
   │
   ▼
3. Busca semântica (embeddings + ChromaDB): 15 pratos mais parecidos com o pedido
   │
   ▼
4. LLM escolhe até 3 pratos da lista e explica por quê
   │
   ▼
Resposta
```

- **Filtros exatos + busca por significado:** regras como preço e tempo não podem depender de "semelhança", então são aplicadas como filtros. A busca vetorial só ordena o que sobrou.
- **Recuperar 15 candidatos e deixar o LLM escolher:** a busca vetorial sozinha erra em pedidos subjetivos, como "leve". Com mais candidatos, o LLM consegue selecionar os que realmente combinam.
- **Prompt com regras anti-invenção:** o LLM só pode usar pratos, preços e tempos da lista fornecida, não pode inventar nada e deve admitir quando nenhum prato combina.

## Stack

| Parte | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Embeddings | `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`) |
| Banco vetorial | ChromaDB |
| LLM | Claude Haiku 5.5 (API da Anthropic) |
| Interface | Streamlit |
| Hospedagem | Streamlit Community Cloud |

## Dados

144 pratos **sintéticos** de 24 restaurantes fictícios em 8 categorias (japonesa, pizza, hambúrguer, brasileira, saudável, italiana, doces e mexicana), gerados por `gerar_dados.py` com preços, tempos de entrega e notas variando por restaurante. Os dados não vêm de nenhum cardápio real.

## Avaliação

O script `eval/run_eval.py` faz perguntas ao assistente e confere o resultado automaticamente: se a resposta cita um prato esperado, se respeita preço, tempo e a restrição vegetariana, e se recusa pedidos impossíveis (camarão, picanha e lagosta, que não existem no cardápio).

| Etapa | Mudança | Resultado |
|---|---|---|
| Versão inicial | Busca + LLM | 16/17 (94%): falhou com erro de digitação ("saldavel") |
| + Correção de digitação | LLM corrige o pedido antes da busca | 17/17 |
| + Perfil dos pratos | Etiqueta ("leve", "farta", "sobremesa") no texto indexado | 18/18 |

O 18º caso (*vegetariano + "algo leve"*) surgiu em teste manual no app publicado: a busca trazia só doces, e o LLM respondia que o cardápio "só tinha doces". Passou a ser um teste automático, e o ajuste de perfil dos pratos o resolveu. Os resultados completos de cada rodada estão na pasta `eval/`.

## Limitações conhecidas

- **Avaliação pequena e criada por mim:** os casos de teste foram escritos por quem construiu o sistema, e alguns foram adicionados *depois* de ver uma falha. O 100% mostra que o sistema acerta o que conheço, não que ele seja robusto para qualquer pedido.
- **Perfil dos pratos feito à mão:** as listas de pratos "leves", "pesados" e "sobremesas" foram escritas manualmente. Em um cardápio grande, isso teria que ser gerado automaticamente (por exemplo, por um LLM).
- **Modelo de embeddings pequeno:** ele é sensível a erros de digitação (por isso a etapa de correção) e não ligou "camarão" a "frutos do mar" em um teste.
- **Recusas medidas por palavras-chave:** a checagem de recusa procura termos como "infelizmente" ou "não há". É uma verificação aproximada.
- **O LLM varia:** respostas podem mudar entre execuções e, raramente, trazer erros de redação.
- **Sem controle de uso no app:** o app é público. O gasto da API é limitado no painel do provedor, mas o app não tem limite de perguntas por usuário.

## Custo

Cada pergunta faz duas chamadas curtas ao Claude Haiku 5.5. Pelas contagens de tokens que medi, o custo estimado é uma fração de centavo por pergunta.

## Como rodar localmente

```bash
git clone https://github.com/Yunit-p/ifood-recomendador-rag.git
cd ifood-recomendador-rag
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz com a sua chave da API da Anthropic:

```
ANTHROPIC_API_KEY=sua-chave-aqui
```

Depois:

```bash
python indexar.py               # cria o banco vetorial (chroma_db/)
python -m streamlit run app.py  # abre o app em localhost:8501
python eval/run_eval.py teste   # roda a avaliação
```

## Estrutura

```
app.py            interface em Streamlit
assistente.py     correção do pedido, busca e chamada ao LLM
rag.py            busca vetorial com filtros
indexar.py        gera embeddings e cria o banco
gerar_dados.py    gera os dados sintéticos
data/pratos.csv   cardápio sintético
eval/             perguntas de teste, script de avaliação e resultados
```

## Próximos passos

- Aumentar e diversificar os casos de teste, com perguntas escritas sem olhar os resultados.
- Gerar o perfil dos pratos automaticamente com um LLM.
- Testar um modelo de embeddings maior e comparar na avaliação.
- Expor a lógica como API (FastAPI) e adicionar limite de uso por usuário.

## Autor

**Pedro Henrique** · [LinkedIn](https://www.linkedin.com/in/pedro-henrique-aa89a1421/)