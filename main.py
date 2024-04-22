import discord
import datetime
import time
from discord.ext import commands, tasks
from sourceserver.sourceserver import SourceServer


intents = discord.Intents.all()
client = commands.Bot(command_prefix="=", intents=intents, help_command=None)

s0 = SourceServer("65.21.189.168:27015")
message = None


def getinfo():
    hostname = s0.info['name']
    map = s0.info['map']
    playercount = s0.info['players']

    return hostname, map, playercount


@client.command(description="Force update server status")
@commands.is_owner()
async def start_loop(ctx: commands.Context):
    try:
        server_status.start(ctx)
    except RuntimeError:
        await ctx.send("Loop already running.")

@client.command()
@commands.is_owner()
async def stop_loop(ctx: None):
    server_status.cancel()
    await ctx.send("Stopped loop.")

@client.command()
@commands.is_owner()
async def check_loop(ctx: commands.Context):
    if server_status.is_running() == False:
        await ctx.send("Loop not running.")
    else:
        current = server_status.current_loop
        await ctx.send(f"Current iteration: {current}")

@tasks.loop(minutes=2, reconnect=True)
async def server_status(ctx: commands.Context):
    info = getinfo()
    dnow = datetime.datetime.now()
    dnow_format = dnow.strftime("%d.%m.%Y %H:%M:%S")
    ctime = int(time.time())

    embed = discord.Embed(title="Server Status",
                    description=f"{info[0]}\nLast update: <t:{ctime}:R>",
                    colour=0xb450b1)
    embed.set_author(name="65.21.189.168:27015")
    embed.add_field(name="map:",
                    value=f"{info[1]}",
                    inline=True)
    embed.add_field(name="players:",
                    value=f"{info[2]}/24",
                    inline=True)
    embed.set_footer(text="Is this wrong? Contact Luna.")

    global message
    if message is None:
        message = await ctx.send(embed=embed)
    else:
        await message.edit(embed=embed)

    print(f"Last update: {dnow_format}")


client.run("MTIyNTg3NzU4MDAyMDk3NzgyNg.Gsc7N_.OyuzoLetilab7j3ir2NZ60fQAPhNcXI-42mQt4")