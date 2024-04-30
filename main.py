import discord
import datetime
import time
import sourceserver.sourceserver as source
import os
from discord.ext import commands, tasks

intents = discord.Intents.all()
client = commands.Bot(command_prefix="=", intents=intents, help_command=None)

s0 = source.SourceServer("65.21.189.168:27015")
message = None


def getinfo():
    hostname = s0.info['name']
    map = s0.info['map']
    playercount = s0.info['players']

    return hostname, map, playercount


@client.command()
async def check_server(ctx: commands.Context):
    if s0.isClosed is True:
        await ctx.send("Server is closed.")
    else:
        await ctx.send("Server is open.")


@client.command()
@commands.is_owner()
async def start_loop(ctx: commands.Context):
    try:
        s0.retry()
        if s0.isClosed is True:
            await ctx.send("Connection failed, server is closed.")
        else:
            try:
                s0.info
            except source.SourceError:
                ctx.send("Couldn't connect, trying again.")
                s0.retry()
            else:
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
    if server_status.is_running() is False:
        await ctx.send("Loop not running.")
    else:
        current = server_status.current_loop
        await ctx.send(f"Current iteration: {current}")


@tasks.loop(seconds=120, reconnect=True)
async def server_status(ctx: commands.Context):
    server_status.add_exception_type(UnboundLocalError)
    global message

    dnow = datetime.datetime.now()
    dnow_format = dnow.strftime("%d.%m.%Y %H:%M:%S")
    ctime = int(time.time())

    try:
        info = getinfo()
    except source.SourceError or UnboundLocalError:
        print(f"Something went wrong, probably lost connection. Retrying. ({dnow_format})")
        embed = discord.Embed(title="Server Status",
                    description=f"Getting server status failed.\nIf this doesn't go away, contact <@237605319159709696>\nLast retry: <t:{ctime}:T>",
                    colour=0xb450b1)
        await message.edit(embed=embed)
        time.sleep(5)
        server_status.restart(ctx)

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

    if message is None:
        message = await ctx.send(embed=embed)
    else:
        await message.edit(embed=embed)

    print(f"Last update: {dnow_format}")

TOKEN = os.environ['TOKEN']
client.run(TOKEN)
