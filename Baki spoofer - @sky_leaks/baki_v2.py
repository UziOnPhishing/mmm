\ t.me/sky_leaks

from telegram import *
from telegram.ext import *
import requests
import mysql.connector

bdd = mysql.connector.connect(host="localhost",user="zystew",password="2w6Txj9PH", database="baki")

token = "1885083925:AAEO7exKWsv4qA2EDfKZ0q7Lr_niOWUct48"
api = "https://sms1.commpeak.com:8002/api?username={username}&password={password}&ani={ani}&dnis={dnis}&message={message}&command=submit&longMessageMode=split"
webhook = "https://api.telegram.org/bot1885083925:AAEO7exKWsv4qA2EDfKZ0q7Lr_niOWUct48/sendMessage?chat_id=-598348335&text={text}"


MSG_ADMIN = "Vous n'êtes pas Admin !"

file_logs = open("logs.txt", "r")
logs = file_logs.read().split(":")
file_logs.close()


def send_webhook(commande, id):
    try:
        sender = "{id} à taper : {commande}".format(id=str(id), commande=commande)
        req = requests.get(webhook.format(text=sender))
    except:
        pass


def is_admin(id_user):
    logs_admin = open("admin.txt", "r")
    liste_admin = logs_admin.read().split(",")
    logs_admin.close()

    if str(id_user) in liste_admin:
        k = 1
    else:
        k = 0

    return k



def sms(update, context):
    send_webhook(update.message.text, update.message.from_user.id)
    try:
        id_user = update.message.from_user.id
    
        cursor = bdd.cursor()
        cursor.execute("SELECT * FROM clients WHERE id_client="+ str(id_user))
        data = cursor.fetchone()
    
        if data != None and data[1] == str(id_user):
            max_sms = data[2] - 1
            if max_sms >= 0:
                msg = update.message.text.split()
        
                numero_fake = msg[1]
                target = msg[2]
                message = " ".join(msg[3:])
        
                update.message.reply_text("Envoie d'un SMS")
                req = requests.get(api.format(username=logs[0], password=logs[1], ani=numero_fake, dnis=target, message=message))
        
                if req.status_code == 200:
                    cursor = bdd.cursor()
                    cursor.execute("UPDATE clients set max=%s WHERE id_client=%s", (max_sms, str(id_user)))
                    bdd.commit()
                    update.message.reply_text("SMS Envoyé !")
                else:
                    update.message.reply_text("Ouups ! Quelque chose c'est mal passé ...")
    
            else:
                update.message.reply_text("Vous avez utilisé tous vos sms pour la journée !")
    
        else:
            update.message.reply_text("Vous n'êtes pas encore client !")
    
    except:
        pass
    
def help(update, context):
    send_webhook(update.message.text, update.message.from_user.id)
    update.message.reply_text("[Leak on t.me/sky_leaks] - Bienvenue sur le BakiBot, ce bot a été conçu pour envoyer des SMS Spoof depuis celui-ci. Pour en savoir plus voici notre Canal : @BakiSpoofer")
    update.message.reply_text(" Voici les commandes Clients :")
    update.message.reply_text("/sms <SenderName> <+33> <Message>")
    update.message.reply_text("/info <Nombre de crédit restant>")


def pas_compris(update, context):
    send_webhook(update.message.text, update.message.from_user.id)
    update.message.reply_text("Je n'ai pas compris votre message")


def add(update, context):
    send_webhook(update.message.text, update.message.from_user.id)
    try:
        id_user = update.message.from_user.id
        if is_admin(id_user):

            msg = update.message.text.split()

            cursor = bdd.cursor()
            cursor.execute("SELECT * FROM clients WHERE id_client="+ str(msg[1]))
            data = cursor.fetchone()
    
            if data == None:
                cursor = bdd.cursor()
                cursor.execute("INSERT INTO clients (id_client, max) VALUES (%s, %s)", (str(msg[1]), 500))
                bdd.commit()
    
                update.message.reply_text("Client ajouté !")
            else:
                update.message.reply_text("Le client est déjà enregistré !")
    
        else:
            update.message.reply_text(MSG_ADMIN)

    except:
        pass


def delet(update, context):
    send_webhook(update.message.text, update.message.from_user.id)
    try:
        id_user = update.message.from_user.id
        if is_admin(id_user):
            cursor = bdd.cursor()
            cursor.execute("DELETE FROM clients WHERE id_client="+str(id_user))
            bdd.commit()
            update.message.reply_text("Client supprimé !")
            
        else:
            update.message.reply_text(MSG_ADMIN)
    except:
        pass

def info(update, context):
    send_webhook(update.message.text, update.message.from_user.id)
    try:
        id_user = update.message.from_user.id
    
        cursor = bdd.cursor()
        cursor.execute("SELECT max FROM clients WHERE id_client="+ str(id_user))
        data = cursor.fetchone()
    
        update.message.reply_text("Il te reste " + str(data[0])+ " SMS aujourd'hui")
    except:
        pass

def liste(update, context):
    send_webhook(update.message.text, update.message.from_user.id)
    try:
        id_user = update.message.from_user.id
        if is_admin(id_user):
            cursor = bdd.cursor()
            cursor.execute("SELECT id_client FROM clients")
            data = cursor.fetchall()
    
            update.message.reply_text("Clients : ")
            n = len(data)
        
            for i in data:
                    update.message.reply_text(i)
        
            update.message.reply_text("Il y a {n} clients.".format(n=str(n)))
    
        else:
            update.message.reply_text(MSG_ADMIN)

    except:
        pass
        

def setlogs(update, context):
    send_webhook(update.message.text, update.message.from_user.id)
    try:
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
            update.message.reply_text(MSG_ADMIN)

    except:
        pass


updater = Updater(token, use_context=True)

updater.dispatcher.add_handler(CommandHandler("sms", sms))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("info", info))


updater.dispatcher.add_handler(CommandHandler("add", add))
updater.dispatcher.add_handler(CommandHandler("delet", delet))
updater.dispatcher.add_handler(CommandHandler("list", liste))


updater.dispatcher.add_handler(CommandHandler("setlogs", setlogs))


updater.dispatcher.add_handler(MessageHandler(Filters.text, pas_compris))


updater.start_polling()
