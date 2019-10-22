#coding=utf-8

import random
import telegram
import datetime
import logging
from telegram.ext import Updater

#MachineGodBot - Telegram Bot designed for helping Warhammer 40.0000 players
updater = Updater(token='apitoken')
logger = logging.basicConfig(filename="DeusMechanicus.log", filemode="w", level= logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

dispatcher = updater.dispatcher

#Functions
def unknown(bot,update):
    logging.info('Received UNKNOWN command')
    unknown_Message = "La tua preghiera non è stata ascoltata!\n" \
                      "Digita /help per una lista di comandi"
    bot.sendMessage(chat_id=update.message.chat_id, text= unknown_Message, parse_mode=telegram.ParseMode.MARKDOWN)

def feedback(bot,update):
    logging.info('Received FEEDBACK command')
    feedback_Message = "Aiuta l'Omnissiah a crescere di popolarità.\n" \
                       "Clicka [qui](https://telegram.me/storebot?=MachineGodBot) e vota!"
    bot.sendMessage(chat_id=update.message.chat_id, text= feedback_Message, parse_mode=telegram.ParseMode.MARKDOWN)

def help(bot,update):
    logging.info('Received HELP command')
    help_message = "Utilizza i seguenti comandi: \n" \
                    "/help - per mostrare questa finestra di aiuto \n" \
                    "/roll *x* _y_ - tira *x*D6 e restituisce i valori superiori a _y_ \n" \
                    "/feedback - vota e aiutaci a crescere" \
                    # "/start - per avviare il bot \n" \
                    # "/stop - per arrestare il bot \n" \
                    # "/rule _regola_ - restituisce l'estratto della _regola_ dal manuale di 7a edizione"

    bot.sendMessage(chat_id=update.message.chat_id, text=help_message, parse_mode=telegram.ParseMode.MARKDOWN)

def roll(bot,update, args):
    if len(args) == 0:
        roll_message= "La sintassi del comando prevede /roll *x* _y_ \n" \
                      "dove *x* è il numero di d6 da lanciare e _y_ il valore da superare per il test\n" \
                      "_y_ può essere omesso se si desidera solo lanciare dei dadi"
        bot.sendMessage(chat_id=update.message.chat_id, text= roll_message, parse_mode=telegram.ParseMode.MARKDOWN)

    elif len(args)==1:
        results = "Effettuati i seguenti tiri: \n"
        die = int(args[0]) #Numero di dadi

        for x in range(die):
            dice = random.randint(1,6)
            results = results + telegram.Emoji.GAME_DIE + " " + str(dice) + "\n"

        bot.sendMessage(chat_id=update.message.chat_id, text= results, parse_mode=telegram.ParseMode.MARKDOWN)

    else:
        results = "Effettuati i seguenti tiri: \n"
        die = int(args[0]) #Numero di dadi
        value = int(args[1]) #Valore inserito dall'utente
        counter = 0 #Numero di dadi superiori all'input dell'utente

        for x in range(die):
            dice = random.randint(1,6)
            if dice >= value:
                counter=counter+1
            results = results + telegram.Emoji.GAME_DIE + " " + str(dice) + "\n"

        results = results + "\n"
        results = results + telegram.Emoji.DIRECT_HIT + " Prove superate: " + str(counter)

        bot.sendMessage(chat_id=update.message.chat_id, text= results, parse_mode=telegram.ParseMode.MARKDOWN)

def meme(bot, update):
    logging.info('Received MEME command')
    imgNumber = random.randint(1,11)
    img = "/home/pi/MachineGodBot/meme/" + str(imgNumber) + ".jpg"
    bot.sendPhoto(chat_id=update.message.chat_id, photo=open(img,'rb'))

def rule(bot,update,args):
    if len(args)==0:
        rule_message = "La sintassi del comando prevede /rule _regola_\n" \
                       "dove _regola_ è il nome della regola da cercare"
        bot.sendMessage(chat_id=update.message.chat_id, text=rule_message, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        rule_to_find= args[:]
        index = ''.join(rule_to_find)
        if index.lower() == "aduemani":
            rule_title= telegram.Emoji.BOOKS + " *A DUE MANI* " + telegram.Emoji.BOOKS +"\n"
            rule_message= "Un modello che combatte con quest'arma non riceve mai" \
                          " *+1* attacchi in mischia per il fatto che combatte con due armi da mischia"
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "abilepilota":
            rule_title= telegram.Emoji.BOOKS + " *ABILE PILOTA* " + telegram.Emoji.BOOKS +"\n"
            rule_message= "Un'unità che contiene almeno un modello con questa regola speciale supera automaticamente" \
                          "i test per i terreni pericolosi e riceve un modificatore di *+1* ai tiri copertura conferiti" \
                          "da Zigzagare (altri tiri copertura non vengono influenzati)"
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "accecare":
            rule_title= telegram.Emoji.BOOKS + " *ACCECARE* " + telegram.Emoji.BOOKS +"\n"
            rule_message= "Ogni unità colpita da uno o più armi o modelli con questa regola speciale deve effettura un test" \
                          "d'Iniziativa alla fine della fase in corso. Se lo supera non succede nulla: i guerrieri hanno distolto" \
                          "lo sguardo grazie ad un avvertimento. Se fallisce, i valori di *AC* e *AB* di tutti i modelli nell'unità" \
                          "sono ridotti ad *1* fino alla fine del loro prossimo turno." \
                          "Se l'unità attaccante colpisce se stessa, si suppone che sia preparata e supera il test automaticamente." \
                          "Qualsiasi modello privo della caratteristica di Iniziativa (ad esempio veicoli non Camminatori, edifici ecc.)" \
                          "non è influenzate da questa regola speciale."
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "aggirare":
            rule_title= telegram.Emoji.BOOKS + " *AGGIRARE* " + telegram.Emoji.BOOKS +"\n"
            rule_message= "Durante lo schieramento i giocatori possono dichiarare che qualsiasi unità che contiene almeno un modello" \
                          "con questa regola speciale sta tentando di Aggirare il nemico. Ciò significa che compie una lunga manovra" \
                          "di accerchiamento per superare le linee di battaglia avversarie o assalirle da una direzione inaspettata." \
                          "Quando un'unità che Aggira arriva dalla Riserva, ma non dalle Riserve Provvisorie, il giocatore che la controlla" \
                          "tira un D6: con 1-2 l'unità arriva dal bordo del tavolo alla sinistra del tavolo del giocatore che la controlla;" \
                          "con 3-4 arriva da quello a destra; con 5-6 il giocatore sceglie se da quello a destra o a sinistra. I modelli" \
                          "arrivano sul tavolo come descritto per le altre Riserve. Se tale unità si schiera dentro un Trasporto Apposito," \
                          "può Aggirare assieme al proprio Trasporto"
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "altamanovrabilità":
            rule_title= telegram.Emoji.BOOKS + " *ALTA MANOVRABILITA'* " + telegram.Emoji.BOOKS +"\n"
            rule_message= "Un modello con questa regola speciale può compiere una rotazione sul posto addizionale di massimo 90° al termine" \
                          "del proprio movimento. Se usa questa rotazione addizionale, esso non può muoversi A tavoletta nella successiva fase" \
                          "di Tiro."
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "ammantato":
            rule_title= telegram.Emoji.BOOKS + " *AMMANTATO* " + telegram.Emoji.BOOKS +"\n"
            rule_message= "Un'unità che contiene almeno un modello con questa regola speciale considera i propri tiri copertura di 2 punti migliore" \
                          "del normale. Ciò significa che un modello con la regola speciale Ammantato ha sempre un tiro copertura di almeno *5+*," \
                          "anche in terreno aperto. I modificatori ai tiri copertura per le regole Ammantato e Furtività sono cumulabili (fino ad" \
                          "un tiro copertura massimo di *2+*)."
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "armadistruttrice":
            rule_title= telegram.Emoji.BOOKS + " *ARMA DISTRUTTRICE* " + telegram.Emoji.BOOKS +"\n"
            rule_message= "Se nel suo profilo un'arma ha D invece di un valore di Forza, essa è un'arma Distruttrice. Per risolvere l'attacco di tale arma" \
                          "tira per Colpire come faresti con un attacco normale. Se colpisce, tira sulla tabella seguente invece di tirare per Ferire o per" \
                          "la penetrazione della corazza. La maggior parte delle armi Distruttrici ha VP1 o VP2, quindi solutamente non si possono effettuare" \
                          "tiri armatura. I tiri copertura e invulnerabilità possono essere effettuati normalmente, a meno che non si ottenga un risultato" \
                          "Colpo devastante o Colpo fatale. Al fine di determinare se il colpo di un'arma Distruttrice ha la regola speciale Morte Immediata," \
                          "considera che abbia Fo10. Le Ferite o i danni ai Punti Scafo in eccesso inflitti da un colpo di un'arma Distruttrice non vengono assegnati" \
                          "agli altri modelli nell'unità, ma sono perduti."
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)
            bot.sendPhoto(chat_id=update.message.chat_id, photo=open('omnissiah/armadistruttrice.jpg','rb'))

        elif index.lower() == "armaspecialistica":
            rule_title= telegram.Emoji.BOOKS + " *ARMA SPECIALISTICA* " + telegram.Emoji.BOOKS +"\n"
            rule_message= "Un modello che combatte con quest'arma non ottiene *+1* Attacchi se combatte con due armi, a meno che sia armato" \
                          "con due o più armi da Mischia con la regola speciale Arma Specialistica."
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "attaccoradente":
            rule_title= telegram.Emoji.BOOKS + " *ATTACCO RADENTE* " + telegram.Emoji.BOOKS +"\n"
            rule_message= "Quando spara con armi d'Assalto, Pesanti, a Cadenza Rapida o a Raffica contro Artiglieria, Bestie, Moto," \
                          "Cavalleria, Fanteria, Creature Mostruore e veicoli che non sono Velivoli né Aeromobili, questo veicolo ha *+1* AB."
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "atterrare":
            rule_title= telegram.Emoji.BOOKS + " *ATTERRARE* " + telegram.Emoji.BOOKS +"\n"
            rule_message="Ogni modello non veicolo che subisce una o più Ferite non salvate o supera uno o più tiri salvezza contro" \
                         "un attacco speciale Atterrare si muove come su un terreno accidentanto fino alla fine del suo turno successivo." \
                         "E' meglio indicare i modelli influenzati con monete o segnalini"
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "avvelenato":
            rule_title= telegram.Emoji.BOOKS + " *ATTERRARE* " + telegram.Emoji.BOOKS +"\n"
            rule_message="Se un modello possiede la regola speciale Avvelenato o se attacca con un'arma da Mischia che ha la regola speciale" \
                         "Avvelenato, in combattimento ferisce sempre con un risultato fisso (generalmente indicato fra parentesi)," \
                         "a meno che non ne sia necessario uno inferiore. Inoltre, se la Forza del portatore (o dell'arma Avvelenata)" \
                         "è superiore alla Resistenza della vittima, esso deve ripetere i tiri per Ferire falliti in combattimento." \
                         "Allo stesso modo, se un modello effettua un attacco da tiro con un'arma che la regola speciale Avvelenato," \
                         "ferisce sempre con un risultato fisso (generalmente indicato fra parentesi), a meno che non ne sia necessario" \
                         "uno inferiore. Se fra parentesi non viene indicato nessun numero, la regola è Avvelenato (*4+*)." \
                         "Se non viene diversamente specificato, le armi Avvelenate vengono sempre considerate avere *Fo1*. La regola" \
                         "speciale Avvelenato non ha effetto contro i veicoli."
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "area":
            rule_title= telegram.Emoji.BOOKS + " *AREA* " + telegram.Emoji.BOOKS +"\n"
            rule_message=""
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)

        elif index.lower() == "binata":
            rule_title= telegram.Emoji.BOOKS + " *BINATA* " + telegram.Emoji.BOOKS +"\n"
            rule_message="Per aumentare la precisione, queste armi sono collegate allo stesso sistema di puntamento." \
                         "Le armi Binate non sparano più di quelle normali, ma hanno maggiori probabilità di colpire. Se un'arma da tiro" \
                         "ha la regola speciale Binata, o viene descritta come Binata nella voce dell'equipaggiamento di un modello," \
                         "ripete tutti i tiri per Colpire falliti. \n" \
                         "\n" \
                         "*ARMI AD AREA BINATE\n" \
                         "Se il dado deviazione non ottiene un Colpito! con un'arma ad Area o ad Area Grande Binata, puoi scegliere" \
                         "di ripetere il tiro. In tal caso devi tirare di nuovo sia i 2d6 che il dado deviazione.\n" \
                         "\n" \
                         "*ARMI A SAGOMA BINATE\n" \
                         "Le armi a Sagoma Binate sparano come un'arma singola, ma devono ripetere i tiri per Ferire falliti e quelli" \
                         "per la penetrazione della corazza falliti."
            bot.sendMessage(chat_id=update.message.chat_id, text= rule_title + rule_message, parse_mode=telegram.ParseMode.MARKDOWN)


#Handlers
dispatcher.addUnknownTelegramCommandHandler(unknown)
#dispatcher.addTelegramCommandHandler('start',start)
#dispatcher.addTelegramCommandHandler('stop',stop)
dispatcher.addTelegramCommandHandler('help',help)
dispatcher.addTelegramCommandHandler('roll', roll)
dispatcher.addTelegramCommandHandler('meme', meme)
dispatcher.addTelegramCommandHandler('feedback',feedback)
#dispatcher.addTelegramCommandHandler('rule',rule)

#Bot polling
updater.start_polling()
