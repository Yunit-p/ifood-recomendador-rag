import streamlit as st

st.set_page_config(page_title="Assistente de Delivery", page_icon="🍽️")
st.title("🍽️ Assistente de recomendação de comida")
st.write("Conte o que você quer comer e eu sugiro pratos do nosso cardápio.")


@st.cache_resource(show_spinner="Carregando o modelo de busca (só na primeira vez, pode levar 1 minuto)...")
def carregar_assistente():
    from assistente import recomendar
    return recomendar


recomendar = carregar_assistente()

pergunta = st.text_input(
    "O que você está com vontade de comer?",
    placeholder="Ex.: algo leve e saudável",
)

col1, col2 = st.columns(2)
with col1:
    preco_max = st.slider("Preço máximo (R$)", 10, 100, 60)
with col2:
    tempo_max = st.slider("Tempo máximo de entrega (min)", 15, 60, 45)
vegetariano = st.checkbox("Apenas vegetariano")

if st.button("Recomendar") and pergunta.strip():
    with st.spinner("Buscando as melhores opções..."):
        resposta = recomendar(
            pergunta,
            preco_max=preco_max,
            tempo_max=tempo_max,
            vegetariano=vegetariano,
        )
    st.markdown(resposta)