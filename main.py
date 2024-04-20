import discord
from discord.ext import commands, tasks
from sourceserver.sourceserver import SourceServer
from time import sleep

intents = discord.Intents.all()
client = commands.Bot(command_prefix="=", intents=intents, help_command=None)

s0 = SourceServer("65.21.189.168:27015")
message = None


def getinfo():
    hostname = s0.info['name']
    map = s0.info['map']
    playercount = s0.info['players']

    return hostname, map, playercount


@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context):
    synced = await client.tree.sync()
    await ctx.send(f"{len(synced)} commands synced")


@client.command(description="Force update server status")
@commands.is_owner()
async def fupdate(ctx: commands.Context):
    try:
        server_status.start(ctx)
    except RuntimeError:
        server_status.restart(ctx)


@tasks.loop(seconds=120)
async def server_status(ctx: commands.Context):
    info = getinfo()
    embed = discord.Embed(title="Server Status",
                    description=f"{info[0]}",
                    colour=0xb450b1)
    embed.set_author(name="65.21.189.168:27015")
    embed.add_field(name="map:",
                    value=f"{info[1]}",
                    inline=True)
    embed.add_field(name="players:",
                    value=f"{info[2]}/24",
                    inline=True)
    embed.set_footer(text="Bot created by LunaXCBN | discord.py")

    global message
    if message is None:
        message = await ctx.send(embed=embed)
    else:
        await message.edit(embed=embed)


client.run("MTIyNTg3NzU4MDAyMDk3NzgyNg.Gsc7N_.OyuzoLetilab7j3ir2NZ60fQAPhNcXI-42mQt4")