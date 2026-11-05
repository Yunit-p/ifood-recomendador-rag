from dotenv import load_dotenv
import anthropic

load_dotenv()  # carrega a chave do arquivo .env
cliente = anthropic.Anthropic()  # usa a chave automaticamente

resposta = cliente.messages.create(
    model="claude-haiku-5-5",
    max_tokens=200,
    messages=[{"role": "user", "content": "Diga olá em uma frase curta."}],
)
print(resposta.content[0].text)
print("Tokens usados (entrada, saída):", resposta.usage.input_tokens, resposta.usage.output_tokens)