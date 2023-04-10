import discord

TOKEN = "MTA5NDcwMDMzMDA5NDE3ODQ4NA.G2KfYT.kVh8uWMaVwyXJxAaoOG752kyLEvNLGr5baXoVw"

# créer un objet Intent pour votre bot
intents = discord.Intents.default()
intents.members = True  # activer l'intention pour accéder aux membres du serveur

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await test()

async def test():
    channel = client.get_channel(1076592826978152470)
    # Envoyer le message
    await channel.send("Bonjour, je suis en ligne !")
    # envoyer l'image
    with open('database/img/map.png', 'rb') as f:
        image = discord.File(f)
        message = await channel.send(file=image)
        url = message.attachments[0].url
        print(url)

    # terminer la session
    await client.close()

client.run(TOKEN)

