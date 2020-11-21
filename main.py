import asyncio
import json
import os
from datetime import datetime
from discord.ext.commands import Bot
from discord.ext import commands
import discord
import pytz
from discord import Message, Guild, TextChannel, Permissions
from discord.ext import commands

bot = commands.Bot(command_prefix=';')

if os.path.isfile("servers.json"):
    with open('servers.json', encoding='utf-8') as f:
        servers = json.load(f)
else:
    servers = {"servers": []}
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

@bot.event
async def on_ready():
    print('Logged in!')
    bot.loop.create_task(status_task())


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game('https://fakect.tk'), status=discord.Status.online)
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Game('https://bit.ly/fakect'), status=discord.Status.online)
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Streaming(name="Codet by: byCRXHIT", url='https://twitch.tv/officialcryhitx'))
        await asyncio.sleep(5)

@bot.command()
async def addGlobal(ctx):
    if ctx.author.guild_permissions.administrator:
        if not guild_exists(ctx.guild.id):
            server = {
                "guildid": ctx.guild.id,
                "channelid": ctx.channel.id,
                "invite": f'{(await ctx.channel.create_invite()).url}'
            }
            servers["servers"].append(server)
            with open('../../Desktop/pybot/pybot6/servers.json', 'w') as f:
                json.dump(servers, f, indent=4)
            embed = discord.Embed(title="**Welcome in the GlobalChat from the Paradise™**",
                                  description="Your server is now ready!"
                                              " Now all message will be send in this channel and will be "
                                              " redirect to all server that has this Bot in their server.",
                                  color=0x2ecc71)
            embed.set_footer(text='Please keep in mind that this server need an 5 sec slowmode if someone is spamming!')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="You server already has an GlobalChat channel.\r\n"
                                              "Every server can only have 1 GlobalChat channel's.",
                                  color=0x2ecc71)
            await ctx.send(embed=embed)


@bot.command()
async def removeGlobal(ctx):
    if ctx.member.guild_permissions.administrator:
        if guild_exists(ctx.guild.id):
            globalid = get_globalChat_id(ctx.guild.id)
            if globalid != -1:
                servers["servers"].pop(globalid)
                with open('../../Desktop/pybot/pybot6/servers.json', 'w') as f:
                    json.dump(servers, f, indent=4)
            embed = discord.Embed(title="**We'll hope wel'll see you again!**",
                                  description="The GlobalChat got removed."
                                              " with `;addGlobal` you can add the chat back.",
                                  color=0x2ecc71)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="You don't have an GlobalChat channel in your server.\r\n"
                                              "Add one with `;addGlobal`.",
                                  color=0x2ecc71)
            await ctx.send(embed=embed)


#########################################

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.content.startswith(';'):
        if get_globalChat(message.guild.id, message.channel.id):
            await sendAll(message)
    await bot.process_commands(message)


#########################################

async def sendAll(message: Message):
    conent = message.content
    author = message.author
    attachments = message.attachments
    de = pytz.timezone('Europe/Berlin')
    embed = discord.Embed(description=conent, timestamp=datetime.now().astimezone(tz=de), color=author.color)

    icon = author.avatar_url
    embed.set_author(name=author.name, icon_url=icon)

    icon_url = "https://cdn.discordapp.com/attachments/775423744256114690/775825111688282142/1.png"
    icon = message.guild.icon_url
    if icon:
        icon_url = icon
    embed.set_thumbnail(url=icon_url)
    embed.set_footer(text='Server: {}'.format(message.guild.name), icon_url=icon_url)

    links = '[Check out FakeCT!](https://fakect.tk) ║ '
    globalchat = get_globalChat(message.guild.id, message.channel.id)
    if len(globalchat["invite"]) > 0:
        invite = globalchat["invite"]
        if 'discord.gg' not in invite:
            invite = 'https://discord.gg/{}'.format(invite)
        links += f'[Join this server!]({invite})'

    embed.add_field(name='⠀', value='⠀', inline=False)
    embed.add_field(name='Links & Help', value=links, inline=False)

    if len(attachments) > 0:
        img = attachments[0]
        embed.set_image(url=img.url)

    for server in servers["servers"]:
        guild: Guild = bot.get_guild(int(server["guildid"]))
        if guild:
            channel: TextChannel = guild.get_channel(int(server["channelid"]))
            if channel:
                perms: Permissions = channel.permissions_for(guild.get_member(bot.user.id))
                if perms.send_messages:
                    if perms.embed_links and perms.attach_files and perms.external_emojis:
                        await channel.send(embed=embed)
                    else:
                        await channel.send('{0}: {1}'.format(author.name, conent))
                        await channel.send('I am missing following permissions: '
                                           '`Send messages` `Embed Links` `Attach Files`'
                                           '`Use external Emojis`')
    await message.delete()


###############################

def guild_exists(guildid):
    for server in servers['servers']:
        if int(server['guildid'] == int(guildid)):
            return True
    return False


def get_globalChat(guild_id, channelid=None):
    globalChat = None
    for server in servers["servers"]:
        if int(server["guildid"]) == int(guild_id):
            if channelid:
                if int(server["channelid"]) == int(channelid):
                    globalChat = server
            else:
                globalChat = server
    return globalChat


def get_globalChat_id(guild_id):
    globalChat = -1
    i = 0
    for server in servers["servers"]:
        if int(server["guildid"]) == int(guild_id):
            globalChat = i
        i += 1
    return globalChat


###########################################################

bot.run(YOUR_BOT_TOKEN)
