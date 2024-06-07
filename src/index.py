from transformers import pipeline
import telebot
import requests
import random

classifier = pipeline("zero-shot-classification")
bot = telebot.TeleBot("6907327488:AAETfaFgEMVLIG300-e4zIXXxbtn95mAqzA")

def buscarProdutos(url):
    response = requests.get(url)
    data = response.json()
    return data

@bot.message_handler(commands=['start', 'help'])
def start(m):
    bot.send_message(m.chat.id, '''Bem vindo a pizzaria PedroAugusto's!\nVocê pode fazer seu pedido, ver o cardápio ou ver um fato interessante sobre pizza!''')
    keyBoard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    bot.send_message(m.chat.id, "O que você deseja fazer?", reply_markup=keyBoard)
    bot.register_next_step_handler(m, escolhaDoUsuario)
    
def escolhaDoUsuario(m):
    mensagem = m.text
    intents = ["voltar", "pedido", "cardapio", "fato"]
    classication_result = classifier(mensagem, intents)
    detect_intent = classication_result['labels'][0]
    if detect_intent == "voltar":
        start(m)
        return
    if detect_intent == "pedido":
        pedido(m)
        return
    if detect_intent == "cardapio":
        cardapio(m)
        return
    if detect_intent == "fato":
        fato(m)
        return
    
def pedido(m):
    pizzas = buscarProdutos("http://localhost:3000/Pizzas")
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for pizza in pizzas:
        button = telebot.types.KeyboardButton(pizza['nome'])
        keyboard.add(button)
    bot.send_message(m.chat.id, "Qual pizza você deseja?", reply_markup=keyboard)
    bot.register_next_step_handler(m, pedidoPizza)
    
def pedidoPizza(m):
    pizza = m.text
    pizzas = buscarProdutos("http://localhost:3000/Pizzas")
    if pizza not in [p['nome'] for p in pizzas]:
        bot.send_message(m.chat.id, "Pizza não encontrada, tente novamente")
        pedido(m)
        return

    bebidas = buscarProdutos("http://localhost:3000/Bebidas")
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for bebida in bebidas:
        button = telebot.types.KeyboardButton(bebida['nome'])
        keyboard.add(button)
    bot.send_message(m.chat.id, "Qual bebida você deseja?", reply_markup=keyboard)
    bot.register_next_step_handler(m, pedidoBebida)

def pedidoBebida(m):
    bebida = m.text
    bebidas = buscarProdutos("http://localhost:3000/Bebidas")
    if bebida not in [b['nome'] for b in bebidas]:
        bot.send_message(m.chat.id, "Bebida não encontrada, tente novamente")
        pedido(m)
        return
    bot.send_message(m.chat.id, "Pedido realizado com sucesso!")
    start(m)

def cardapio(m):
    pizzas = buscarProdutos("http://localhost:3000/Pizzas")
    bebidas = buscarProdutos("http://localhost:3000/Bebidas")
    cardapio = "-=- Cardápio -=-\n"
    cardapio += "\nPizzas:\n"
    for pizza in pizzas:
        cardapio += f"{pizza['nome']} - R${pizza['preco']}\n"
    cardapio += "\nBebidas:\n"
    for bebida in bebidas:
        cardapio += f"{bebida['nome']} - R${bebida['preco']}\n"
    bot.send_message(m.chat.id, cardapio)
    bot.send_message(m.chat.id, "O que deseja fazer: pedido, cardapio ou fato")
    bot.register_next_step_handler(m, escolhaDoUsuario)
    
def fato(m):
    fatos = buscarProdutos("http://localhost:3000/Fatos")
    random_fato = random.choice(fatos)
    bot.send_message(m.chat.id, random_fato['fato'])
    bot.send_message(m.chat.id, "O que deseja fazer: pedido, cardapio ou fato")
    bot.register_next_step_handler(m, escolhaDoUsuario)

print("Bot rodando...")
bot.polling()