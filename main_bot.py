#on remplace le "client" par un "bot", c'est plus simple pour les commandes

import os
import sys
sys.path.append("D:\DocBot\Lib\site-packages")
sys.path.append("Lib\site-packages\discord")
import discord
from discord.ext import commands
import dotenv
#fonction qui va nous permettre de créer un fichier externe pour cacher le token en bref
from dotenv import load_dotenv
import random
from Biblio_de_mots import bad_words,reponses_neg

#on déclare où se trouve la variable d'environnement TOKEN (notre token qu'on doit garder secret)
load_dotenv(dotenv_path=".env")

#intents=intents=discord.Intents.all()

default_intents = discord.Intents.default()
default_intents.members = True


#on cré une classe qui hérite de commands.bot comme ca on aura accès à tout ce qu'il y a à l'intérieur
#créer cette classe permet de créer des events facilement !!!
class DocBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=default_intents)
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        
        msg_content = message.content.lower()
        
        
        
        #bad_word=['pute', 'putain']

        if any(word in msg_content for word in bad_words):
            await message.reply(random.choice(reponses_neg))

        if message.content.lower().startswith('ping'):
            await message.reply('pong', mention_author=True)
        
        if message.content.startswith("!del"):
            number = int(message.content.split()[1])
            msg = await message.channel.history(limit=number + 1).flatten()        
            #CREER UN TRYEXCPET POUR LES ERREURS 
            try:   
                for each_message in msg:
                    await each_message.delete()
            except IndexError:
                print('Mets un chiffre valide connard')
                
    async def on_member_join(self, member):
        await member.send(content=f'Bienvenue dans ce serveur enculé de {member.display_name} !')
                
#on cré une instance pour le bot
doc_bot = DocBot()

doc_bot.run(os.getenv("TOKEN"))
