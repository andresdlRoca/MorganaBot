import discord
from discord.ext import commands

class Frases(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.command()
  async def cool(self, ctx, *, member:discord.Member=None):
    member = ctx.author
    await ctx.send('Looking cool {0.name}'.format(member))
  
  @commands.command()
  async def rajon(self, ctx, *, user:discord.Member=None):
    if user:
      await ctx.send(f'{user.mention} rajoX1000000000000')
    else:
      await ctx.send("Me tenes que decir quien rajo para mandarlo a mamar pa")
  
  @commands.command()
  async def mamar(self, ctx, *, user:discord.Member=None):
    if user:
      await ctx.send(f'A MAMARLA {user.mention}')
    else:
      await ctx.send("Me tenes que decir a quien mando a mamar pa")

  @commands.command()
  async def eva(self, ctx):
    await ctx.send("Evangelion besto anime ever")
  
  @commands.command()
  async def miko(self, ctx):
    await ctx.send("Mommy Miko")
    