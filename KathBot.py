import discord, asyncio, typing, os, random, json
from discord.ext import commands
from discord.ext.commands import *
from random import randint, choice

with open("tarot.json") as cardList:
    cards = json.load(cardList)

client = commands.Bot(command_prefix = 'k!') #Release Only
#client = commands.Bot(command_prefix = 'kd!') #Development Only

client.remove_command('help')

@client.event
async def on_ready():
    print("Logged on!")
    await client.change_presence(status = discord.Status.online, activity = discord.Game(name = "k!help | inside " + str(len(client.guilds)) + " servers!"))
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Invalid command. Use ``k!help`` for help using my commands!")
        
    else:
        pass
    
@client.event
async def on_error(event, *args, **kwargs):
    #print("Error: " + event + " at line: " + args.toString())
    pass
    
async def errorcheck(usage, ctx, error):
        
    if isinstance(error, CheckFailure) or isinstance(error, MissingPermissions) or isinstance(error, MissingRole):
        await ctx.send("You do not have the permissions required to run this command.")
        
    elif isinstance(error, ArgumentParsingError) or isinstance(error, BadArgument) or isinstance(error, TooManyArguments) or isinstance(error, MissingRequiredArgument):
        await ctx.send("Improper usage.")
        embed = discord.Embed(title = 'Proper Usage: ', description = usage, color = 0xFF88FF)
        await ctx.send(embed = embed)
        
    elif isinstance(error, BotMissingRole) or isinstance(error, BotMissingPermissions):
        await ctx.send("Uh oh! I do not have the permissions to carry out the given command!")
        
    elif isinstance(error, CommandInvokeError):
        HBS = client.get_user(id = 456282270974607361)
        await ctx.send("Uh oh! Please contact my creators to get help with this command! " + "``" + HBS.name + "#" + HBS.discriminator + "``")
    
    else:
        await ctx.send("An error has occurred.")

@client.event
async def on_message(message):
    #print('{0.content}'.format(message)) #DEVELOPMENT ONLY
    if(message.author.bot != True):
        await client.process_commands(message)
        if(message.content == "owo"):
            await message.channel.send("uwu")

        if(message.content == "uwu"):
            await message.channel.send("owo")
            
        if(message.content == "who's babie?"):
            await message.channel.send("IM BABIE!!!")

@client.command(name = 'help')
async def help(ctx):
    HBS = client.get_user(id = 456282270974607361)
    #if(ctx.message.author.server_permissions):
    embed = discord.Embed(title = "KathBot Commands", description="Here you can get a full list of this bot's commands!", color=0xFF88FF)
    embed.set_thumbnail(url = 'https://puu.sh/Fvnef.png')
    embed.set_footer(text = 'W.I.P. Bot, created by ' + HBS.name + "#" + HBS.discriminator)
    embed.add_field(name = "ping", value = "Pong!", inline = False) 
    embed.add_field(name = "say", value = "Make me say something!", inline = False)
    embed.add_field(name = "rate", value = "Give me something to rate!", inline = False)
    embed.add_field(name = "8ball", value = "Shake the Magic 8ball!", inline = False)
    embed.add_field(name = "cat", value = "Use this command to get a random cat picture!", inline = False)
    embed.add_field(name = "invite", value = "Want to invite me to your server? Run this command!", inline = False)
    embed.add_field(name = "grace", value = "Bow down to your gay overlord!", inline = False)
    embed.add_field(name = "tarot", value = "Read a tarot spread!", inline = False)
    await ctx.send(embed = embed)

@client.command(name = 'ping')
async def ping(ctx):
    async with ctx.channel.typing():
        await asyncio.sleep(.4)
        
    await ctx.send("Pong!" + " ``{}ms``".format(round(client.latency * 1000, 1)))

@client.command(name = 'say')
async def say(ctx, *, arg):
    await ctx.send(arg)

@say.error
async def say_error(ctx, error):
    errorcheck("``k!say Argument(s)``", ctx, error)

@client.command(name = 'rate')
async def rate(ctx, *args):
    arg = " ".join(args)
    lowerArg = arg.lower()
    async with ctx.channel.typing():
        await asyncio.sleep(1)
        
    if(lowerArg == 'drukon'):
        await ctx.send("Hm... I rate " + arg + " a 11/10, for being an amazing friend! <3")
             
    elif(lowerArg == 'fir'):
        await ctx.send("Hm... I rate " + arg + " a 11/10, for being such a precious little bean! <3")
        
    elif(lowerArg == 'grace'):
        await ctx.send("Grace is the bestest she gets a 11/10 for being such an awesome little sister! <3")
        
    elif(lowerArg == 'full cock annihilation'):
        await ctx.send("Hm... I rate " + arg + " a cock/10!")
        
    elif(lowerArg == 'pixie' or lowerArg == "sillipha"):
        await ctx.send("Hm.. I rate " + arg + " a 11/10! <3")
        
    else:
        random.seed(lowerArg)
        await ctx.send("Hm... I rate " + arg + " a... " + str(randint(0,10)) + "/10!")

@rate.error
async def rate_error(ctx, error):
    await errorcheck("``k!rate Argument(s)``", ctx, error)

@client.command(name = '8ball')
async def eightball(ctx, *args):
    await ctx.send("Shaking ball...")
    await asyncio.sleep(1)
    async with ctx.channel.typing():
        await asyncio.sleep(.5)

    Response = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    arg = " ".join(args)
    lowerArg = arg.lower()
    random.seed(lowerArg)
    await ctx.send("In response to "+ arg +", it reads... " + '"' + choice(Response) + '"')

@eightball.error
async def eightball_error(ctx, error):
    await errorcheck("``k!8ball Argument(s)``", ctx, error)

@client.command(name = 'cat')
async def cat(ctx):
    path = "Cats"
    randomCat = random.choice(os.listdir(path))
    await ctx.send("Here's your cat!", file = discord.File(path + '/' + randomCat))

@client.command(name = "invite")
async def invite(ctx):
    async with ctx.channel.typing():
        await asyncio.sleep(.3)

    HBS = client.get_user(id = 456282270974607361)
    embed = discord.Embed(title="KathBot Invite", description="You want to invite me to your server?!", color=0xFF88FF)
    embed.set_thumbnail(url = 'https://puu.sh/Fvnef.png')
    embed.set_footer(text = 'W.I.P. Bot, created by ' + HBS.name + "#" + HBS.discriminator)
    embed.add_field(name = "Here's my invite link!", value = "https://discordapp.com/api/oauth2/authorize?client_id=596683881575612429&permissions=67226688&scope=bot")
    await ctx.send(embed = embed)

@client.command(name = "grace")
async def grace(ctx):
    await ctx.send("GRACE")
    await asyncio.sleep(1.0)
    await ctx.send("IS")
    await asyncio.sleep(1.0)
    await ctx.send("THE")
    await asyncio.sleep(1.0)
    await ctx.send("GAYEST")
    await asyncio.sleep(1.0)
    await ctx.send("GAY")
    await asyncio.sleep(1.0)
    await ctx.send("EVER")

@client.command(name = "tarot")
async def tarot(ctx, arg, *args):
    try:
        count = int(arg)

    except:
        await ctx.send("Improper usage.")
        embed = discord.Embed(title = 'Proper Usage: ', description = "``k!tarot Number Question(Optional)``", color = 0xFF88FF)
        await ctx.send(embed = embed)
    
    HBS = client.get_user(id = 456282270974607361)
    embed = discord.Embed(title = "Your spread:", description = " ", color=0xFF88FF)
    embed.set_footer(text = "W.I.P. Bot, created by " + HBS.name + "#" + HBS.discriminator)
    card = 0
    for x in range(0, count):
        card += 1
        flip = random.randint(0, 1)
        if(flip == 0):
            embed.add_field(name = "Card #" + str(card), value = random.choice(cards['cards']) + "\n", inline = False)
            
        else:
            embed.add_field(name = "Card #" + str(card), value = "Flipped " + random.choice(cards['cards']) + "\n", inline = False)

    await ctx.send(embed = embed)
    await ctx.send("This command is in a very rough stage, please give us some time to refine it.")

@tarot.error
async def tarot_error(ctx, error):
    await errorcheck("``k!tarot Number Question(Optional)``")

@client.command(name = "status")
async def OWNER_status(ctx, *, arg):
    if(ctx.author.id == 456282270974607361):
        await client.change_presence(status = discord.Status.online, activity = discord.Game(name = "k!help | " + arg + " | inside " + str(len(client.guilds)) + " servers!"))
        
    else:
        await ctx.send("You can not command me, mortal!")
        
@client.command(name = "announce")
async def announcement(ctx, *, arg):
    if(ctx.author.id == 456282270974607361):
        for guild in client.guilds:
            embed = discord.Embed(title = "Announcement", description = "Announcement from KathBot's Developer(s)", color = 0xFF88FF)    #Creates an embed to send in the message
            embed.add_field(name = "Message:", value = "" + arg, inline = False)    #Adds to the embed
            for channel in guild.text_channels:
                try:
                    await channel.send(embed = embed)
                    break

                except:
                    pass
        
    else:
        await ctx.send("You cannot command me, mortal!")
        
with open("token.txt").read() as tokenTxt:
    token = tokenTxt.read()
    
    client.run(token)
