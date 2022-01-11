import asyncio
import youtube_dl
import pafy
import discord
from discord.ext import commands

class Player(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    self.song_queue = {}

    self.setup()
  
  def setup(self):
    for guild in self.bot.guilds:
      self.song_queue[guild.id] = []

  async def check_queue(self, ctx):
    if len(self.song_queue[ctx.guild.id]) > 0:
        await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
        self.song_queue[ctx.guild.id].pop(0)
  
  async def search_song(self, amount, song, get_url=False):
    info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
    if len(info["entries"]) == 0: return None

    return [entry["webpage_url"] for entry in info["entries"]] if get_url else info
  
  async def play_song(self, ctx, song):
    url = pafy.new(song).getbestaudio().url
    ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
    ctx.voice_client.source.volume = 0.5


  
  @commands.command()
  async def join(self, ctx):
    if ctx.author.voice is None:
      return await ctx.send("No estas conectado a ningun canal de voz pa")
    
    if ctx.voice_client is not None:
      await ctx.voice_client.disconnect()
    
    await ctx.author.voice.channel.connect()

  @commands.command()
  async def leave(self, ctx):
    if ctx.voice_client is not None:
      return await ctx.voice_client.disconnect()

    await ctx.send("No estoy conectado a ningun canal de voz")

  @commands.command()
  async def play(self, ctx, *, song=None):
      if song is None:
          return await ctx.send("Tenes que decirme que cancion queres poner pa.")

      if ctx.voice_client is None:
          return await ctx.send("Tengo que estar en un canal de voz para poder ponerte la rola.")

      # handle song where song isn't url
      if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
          await ctx.send("Buscando...")

          result = await self.search_song(1, song, get_url=True)

          if result is None:
              return await ctx.send("Esa cancion no existe pa, decime una que si exista.")

          song = result[0]

      if ctx.voice_client.source is not None:
          queue_len = len(self.song_queue[ctx.guild.id])

          if queue_len < 10:
              self.song_queue[ctx.guild.id].append(song)
              return await ctx.send(f"Cancion agregada a la cola en posicion: {queue_len+1}.")

          else:
              return await ctx.send("Lo siento pa, solo puedo poner 10 canciones en cola, sino se me olvidan.")

      await self.play_song(ctx, song)
      await ctx.send(f"Ahora pleyeando: {song}")
  
  @commands.command()
  async def search(self, ctx, *, song=None):
      if song is None: return await ctx.send("Pa, se te olvido la cancion")

      await ctx.send("Buscando...")

      info = await self.search_song(5, song)

      embed = discord.Embed(title=f"Resultados para '{song}':", description="Podes usar estos links para buscar la cancion que queres\n", colour=discord.Colour.red())
      
      amount = 0
      for entry in info["entries"]:
          embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
          amount += 1

      embed.set_footer(text=f"Estos son los primeros {amount} resultados.")
      await ctx.send(embed=embed)

  @commands.command()
  async def queue(self, ctx): # display the current guilds queue
      if len(self.song_queue[ctx.guild.id]) == 0:
          return await ctx.send("There are currently no songs in the queue.")

      embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
      i = 1
      for url in self.song_queue[ctx.guild.id]:
          embed.description += f"{i}) {url}\n"

          i += 1

      embed.set_footer(text="Thanks for using me!")
      await ctx.send(embed=embed)

  @commands.command()
  async def skip(self, ctx):
    if ctx.voice_client is None:
      return await ctx.send("No estoy pleyeando ninguna cancion pibe")
    if ctx.author.voice is None:
      return await ctx.send("No estas conectado al canal de voz pa")
    
    skip = True

    if skip:
      ctx.voice_client.stop()
      await self.check_queue(ctx)

  @commands.command()
  async def pause(self, ctx):
      if ctx.voice_client.is_paused():
          return await ctx.send("Pero si ya la pause gilipollas.")

      ctx.voice_client.pause()
      await ctx.send("Ahorita se la pauso rey.")

  @commands.command()
  async def resume(self, ctx):
      if ctx.voice_client is None:
          return await ctx.send("No estoy en el canal pa.")

      if not ctx.voice_client.is_paused():
          return await ctx.send("Ya estoy pleyeando una cancion.")
      
      ctx.voice_client.resume()
      await ctx.send("Ya resumi la cancion.")
  




  
