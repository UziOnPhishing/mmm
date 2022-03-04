from telegram import *
from telegram.ext import *
import requests

token = "808376860:AAFRL8gw_mVu55a8uKH4rSWZuzS_yhWZsnY"
api = "https://sms1.commpeak.com:8002/api?username={username}&password={password}&ani={ani}&dnis={dnis}&message={message}&command=submit&longMessageMode=split"

file_logs = open("logs.txt", "r")
logs = file_logs.read().split(":")
file_logs.close()

def is_admin(id_user):
    logs_admin = open("admin.txt", "r")
    liste_admin = logs_admin.read().split(",")
    logs_admin.close()

    if str(id_user) in liste_admin:
        k = 1
    else:
        k = 0

    return k


def kill(update, context):
    updater.idle()


def sms(update, context):
    id_user = update.message.from_user.id

    logs_clients = open("clients.txt", "r")
    liste_clients = logs_clients.read().split(",")
    logs_clients.close()


    if str(id_user) in liste_clients:
        msg = update.message.text.split()

        numero_fake = msg[1]
        target = msg[2]
        message = " ".join(msg[3:])

        update.message.reply_text("Envoie d'un SMS")
        req = requests.get(api.format(username=logs[0], password=logs[1], ani=numero_fake, dnis=target, message=message))
        if req.status_code == 200:
            update.message.reply_text("SMS Envoyé !")
        else:
            update.message.reply_text("Ouups ! Quelque chose c'est mal passé ...")

    else:
        update.message.reply_text("Vous n'êtes pas encore client !")
            



def help(update, context):
    update.message.reply_text("HELP")


def pas_compris(update, context):
    update.message.reply_text("Je n'ai pas compris votre message")


def add(update, context):
    id_user = update.message.from_user.id
    if is_admin(id_user):
        msg = update.message.text.split()
        logs_clients = open("clients.txt", "a+")

        liste_clients = logs_clients.read()+msg[1]+","
        logs_clients.write(liste_clients)
        logs_clients.close()

        update.message.reply_text("Client ajouté !")

    else:
        update.message.reply_text("Fils de pute")


def delet(update, context):
    id_user = update.message.from_user.id
    if is_admin(id_user):
        msg = update.message.text.split()
        del_id = msg[1]

        logs_clients = open("clients.txt", "r")
        liste_clients = logs_clients.read().split(",")


        logs_clients.close()
        n = liste_clients.index(del_id)
        del liste_clients[n]


        output = ",".join(liste_clients)

        logs_clients = open("clients.txt", "w")
        logs_clients.write(str(output))
        logs_clients.close()

    else:
        update.message.reply_text("Fils de pute")


def liste(update, context):

    id_user = update.message.from_user.id
    if is_admin(id_user):
        logs_clients = open("clients.txt", "r")
        liste_clients = logs_clients.read().split(",")
    
        logs_clients.close()
        n = len(liste_clients)
        update.message.reply_text("Clients : ")
    
        for i in liste_clients:
            if len(i) != 0:
                update.message.reply_text(i)
    
        update.message.reply_text("Il y a {n} clients.".format(n=str(n)))

    else:
        update.message.reply_text("Fils de pute")
    

def setlogs(update, context):
    id_user = update.message.from_user.id

    if is_admin(id_user):
        msg = update.message.text.split()
        new_logs = msg[1]

        file_logs = open("logs.txt", "w")
        file_logs.write(new_logs)
        file_logs.close()

        global logs
        logs = new_logs.split(":")

        update.message.reply_text("Logs changé !")


    else:
        update.message.reply_text("Fils de pute")


updater = Updater(token, use_context=True)

updater.dispatcher.add_handler(CommandHandler("kill", kill))
updater.dispatcher.add_handler(CommandHandler("sms", sms))
updater.dispatcher.add_handler(CommandHandler("help", help))

updater.dispatcher.add_handler(CommandHandler("add", add))
updater.dispatcher.add_handler(CommandHandler("delet", delet))
updater.dispatcher.add_handler(CommandHandler("list", liste))

updater.dispatcher.add_handler(CommandHandler("setlogs", setlogs))


updater.dispatcher.add_handler(MessageHandler(Filters.text, pas_compris))


updater.start_polling()
