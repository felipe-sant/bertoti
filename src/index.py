# from transformers import pipeline
import telebot
import requests
import json
from dados import dados

bot = telebot.TeleBot(dados["token"])
# classifier = pipeline("zero-shot-classification")

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
    # intents = ["pedido", "cardapio", "fato"]
    # classication_result = classifier(mensagem, intents)
    # detect_intent = classication_result['labels'][0]
    detect_intent = mensagem
    if detect_intent == "pedido":
        pedido(m)
        return
    if detect_intent == "cardapio":
        cardapio(m)
        bot.send_message(m.chat.id, "Escreva algo para voltar.")
        bot.register_next_step_handler(m, start)
        return
    if detect_intent == "fato":
        fato(m)
        return
    
def pedido(m):
    bot.send_message(m.chat.id, "Pedido")

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
    
def fato(m):
    bot.send_message(m.chat.id, "Fato")

bot.polling()