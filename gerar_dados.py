import csv
import os
import random

random.seed(42)  # garante que os dados saiam sempre iguais

# Cada prato: (nome, descrição, preço base, vegetariano?)
CATALOGO = {
    "Japonesa": [
        ("Combinado de sushi 20 peças", "Sushis e sashimis de salmão, atum e peixe branco, com gengibre e wasabi", 62, False),
        ("Temaki de salmão", "Cone de alga recheado com salmão fresco, cream cheese e cebolinha", 28, False),
        ("Hot roll de salmão", "Oito peças empanadas e fritas, recheadas com salmão e cream cheese", 34, False),
        ("Yakisoba de legumes", "Macarrão oriental salteado com brócolis, cenoura, repolho e molho shoyu", 36, True),
        ("Gyoza de carne", "Pastéis japoneses grelhados recheados com carne suína e legumes", 30, False),
        ("Uramaki vegetariano", "Rolinhos com pepino, cenoura e manga, sem peixe", 32, True),
    ],
    "Pizza": [
        ("Pizza margherita", "Molho de tomate, muçarela de búfala, manjericão fresco e azeite", 52, True),
        ("Pizza calabresa", "Calabresa fatiada, cebola roxa, muçarela e azeitonas", 54, False),
        ("Pizza quatro queijos", "Muçarela, provolone, gorgonzola e parmesão sobre molho de tomate", 58, True),
        ("Pizza portuguesa", "Presunto, ovos, cebola, ervilha, azeitonas e muçarela", 56, False),
        ("Pizza de frango com catupiry", "Frango desfiado temperado com catupiry cremoso e milho", 55, False),
        ("Pizza doce de chocolate com morango", "Chocolate ao leite derretido com morangos frescos", 48, True),
    ],
    "Hambúrguer": [
        ("Cheeseburger clássico", "Hambúrguer bovino de 150g, queijo cheddar, alface, tomate e molho da casa", 32, False),
        ("Burger bacon duplo", "Dois hambúrgueres de 120g, muito bacon crocante e cheddar derretido", 42, False),
        ("Burger de frango crocante", "Filé de frango empanado, maionese temperada e picles", 30, False),
        ("Burger vegetariano de grão-de-bico", "Hambúrguer de grão-de-bico com abobrinha, queijo e rúcula", 34, True),
        ("Batata frita com cheddar e bacon", "Porção grande de batata frita coberta com cheddar e bacon", 28, False),
        ("Milkshake de chocolate", "Sorvete batido com calda de chocolate e chantilly, 400ml", 22, True),
    ],
    "Brasileira": [
        ("Feijoada completa", "Feijão preto com carnes suínas, arroz, couve, farofa e laranja", 45, False),
        ("Prato feito de frango grelhado", "Filé de frango grelhado, arroz, feijão, salada e batata frita", 28, False),
        ("Strogonoff de carne", "Carne em molho cremoso com champignon, arroz branco e batata palha", 34, False),
        ("Moqueca de peixe", "Peixe cozido em leite de coco, dendê e pimentões, com arroz e pirão", 52, False),
        ("Virado à paulista", "Bisteca suína, tutu de feijão, couve, ovo frito, banana e arroz", 38, False),
        ("Escondidinho de mandioca vegetariano", "Purê de mandioca gratinado com recheio de cogumelos e queijo", 32, True),
    ],
    "Saudável": [
        ("Salada caesar com frango", "Alface americana, frango grelhado, croutons e parmesão com molho caesar", 33, False),
        ("Bowl de quinoa com legumes", "Quinoa, grão-de-bico, abacate, tomate cereja e molho de limão", 36, True),
        ("Wrap integral de frango", "Tortilla integral com frango desfiado, folhas verdes e homus", 29, False),
        ("Salmão grelhado com legumes", "Filé de salmão com brócolis, cenoura e purê de batata-doce", 54, False),
        ("Açaí com granola", "Açaí batido com banana, granola e mel, 500ml", 26, True),
        ("Suco verde detox", "Couve, limão, gengibre, maçã e hortelã, 500ml", 14, True),
    ],
    "Italiana": [
        ("Espaguete à carbonara", "Espaguete com bacon crocante, gema de ovo, parmesão e pimenta-do-reino", 44, False),
        ("Lasanha à bolonhesa", "Camadas de massa, molho de carne, molho branco e queijo gratinado", 42, False),
        ("Fettuccine alfredo", "Fettuccine em molho cremoso de manteiga e parmesão", 40, True),
        ("Ravioli de queijo ao sugo", "Ravioli recheado de ricota e muçarela com molho de tomate fresco", 43, True),
        ("Risoto de cogumelos", "Arroz arbóreo cremoso com mix de cogumelos e parmesão", 48, True),
        ("Tiramisù", "Sobremesa italiana de café, mascarpone e cacau", 24, True),
    ],
    "Doces": [
        ("Brigadeiro gourmet (caixa com 6)", "Brigadeiros de chocolate belga, ninho e pistache", 24, True),
        ("Bolo de cenoura com chocolate", "Fatia generosa de bolo de cenoura com cobertura de chocolate", 14, True),
        ("Cheesecake de frutas vermelhas", "Torta cremosa de cream cheese com calda de frutas vermelhas", 22, True),
        ("Churros recheado com doce de leite", "Churros crocantes por fora e recheados com doce de leite", 18, True),
        ("Brownie com sorvete", "Brownie quente de chocolate com bola de sorvete de creme", 24, True),
        ("Torta de limão", "Massa crocante, creme de limão e merengue maçaricado", 16, True),
    ],
    "Mexicana": [
        ("Tacos de carne (3 unidades)", "Tortilhas de milho com carne moída temperada, cebola, coentro e limão", 36, False),
        ("Burrito de frango", "Tortilla de trigo com frango, arroz, feijão, queijo e molho picante", 33, False),
        ("Nachos com guacamole e queijo", "Tortilhas crocantes com queijo derretido, guacamole e pico de gallo", 30, True),
        ("Quesadilla de queijo e cogumelos", "Tortilla grelhada recheada com queijo e cogumelos salteados", 28, True),
        ("Chili con carne", "Ensopado de carne com feijão e pimenta, servido com arroz", 38, False),
        ("Guacamole com chips", "Abacate amassado com tomate, cebola e limão, com chips de milho", 22, True),
    ],
}

# Cada restaurante: (nome, tempo de entrega base em min, fator de preço, nota)
RESTAURANTES = {
    "Japonesa": [("Sakura Express", 35, 1.15, 4.7), ("Tokyo Box", 30, 1.0, 4.4), ("Mar & Sushi", 45, 1.25, 4.8)],
    "Pizza": [("Forno Napoli", 40, 1.1, 4.7), ("Pizzaria Dona Maria", 35, 0.95, 4.3), ("Massa Fina", 45, 1.2, 4.6)],
    "Hambúrguer": [("Burger do Zé", 25, 0.95, 4.4), ("Smash House", 30, 1.1, 4.8), ("Grill Brasa", 35, 1.0, 4.2)],
    "Brasileira": [("Cozinha da Vovó", 30, 0.9, 4.6), ("Marmitaria Sabor Caseiro", 20, 0.85, 4.3), ("Tempero Mineiro", 35, 1.0, 4.7)],
    "Saudável": [("Verde Vivo", 25, 1.1, 4.6), ("Fit Bowl", 20, 1.0, 4.5), ("Natural & Cia", 30, 1.05, 4.4)],
    "Italiana": [("Nonna Rosa", 40, 1.15, 4.8), ("Trattoria Bella", 45, 1.2, 4.6), ("Massa Express", 30, 0.95, 4.2)],
    "Doces": [("Doce Encanto", 25, 1.0, 4.7), ("Confeitaria Aurora", 30, 1.1, 4.5), ("Sweet Box", 20, 0.95, 4.3)],
    "Mexicana": [("El Taco Loco", 30, 1.0, 4.5), ("Casa Mexicana", 35, 1.1, 4.6), ("Burrito Rápido", 20, 0.9, 4.2)],
}

linhas = []
id_prato = 1

for categoria, restaurantes in RESTAURANTES.items():
    for nome, tempo_base, fator_preco, nota in restaurantes:
        # tempo e nota são do restaurante, então ficam iguais para todos os pratos dele
        tempo = tempo_base + random.randint(-3, 3)
        for prato, descricao, preco_base, vegetariano in CATALOGO[categoria]:
            preco = round(preco_base * fator_preco * random.uniform(0.95, 1.05), 2)
            linhas.append({
                "id": id_prato,
                "restaurante": nome,
                "categoria": categoria,
                "prato": prato,
                "descricao": descricao,
                "preco": preco,
                "tempo_entrega_min": tempo,
                "vegetariano": vegetariano,
                "nota_restaurante": nota,
            })
            id_prato += 1

os.makedirs("data", exist_ok=True)
with open("data/pratos.csv", "w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=linhas[0].keys())
    escritor.writeheader()
    escritor.writerows(linhas)

print(f"Pronto! {len(linhas)} pratos salvos em data/pratos.csv")