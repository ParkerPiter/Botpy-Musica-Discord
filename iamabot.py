import discord #Libreria de discord
from discord.ext import commands #Libreria de comnados de discord
import datetime #Libreria de tiempo
import youtube_dl #Libreria de Youtube

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='<')


#PARA UNIR AL BOT AL VOICE
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

#PARA QUE EL BOT SE SALGA
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

#Evento del Bot
@bot.event
async def on_ready():
    game = discord.Game('Jugando a aprender')
    await bot.change_presence(status=discord.Status.online, activity=game)
    print('Toy listo mi pana')

@bot.command(name='hola')
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name='suma') #Funcion que realizara la suma entre dos numeros enteros
async def sumar(ctx, num1,num2):
    response = int(num1)+int(num2)
    await ctx.send(response)

@bot.command(name='m') #Funcion que realizara la suma entre dos numeros enteros
async def multiplicar(ctx, num1,num2):
    response = int(num1)* int(num2)
    await ctx.send(response)

@bot.command(name="Epa")
async def saludo (ctx):
    await ctx.send('Epa camarada')


#EMBEDS

@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Lorem Ipsum asdasd", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)

#Codigo que deja poner musiquita
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
#Aqui termina

#Pone Play a la cancion
@bot.command(name='play', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")

#Pausa la cancion
@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

#Pausa
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


#client = discord.Client()

#@client.event
#async def on_ready():
#    print('We have logged in as {0.user}'.format(client))

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

#    if message.content.startswith('$hello'):
#        await message.channel.send('Hello!')



bot.run('ODMzNTQ2NzU4NTAzNTMwNTA2.YHz66Q.Pz5X_Y28CmzLNofpxNWXlAWvreA')
#client.run('ODMzNTQ2NzU4NTAzNTMwNTA2.YHz66Q.Pz5X_Y28CmzLNofpxNWXlAWvreA')

import os
import urllib.request
import json



