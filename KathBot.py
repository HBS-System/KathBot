import discord, asyncio, typing, os, random, json, time
from datetime import date
from discord.ext import commands
from discord.ext.commands import ArgumentParsingError, BadArgument, TooManyArguments, MissingRequiredArgument, MissingRequiredArgument, BotMissingRole, BotMissingPermissions, CommandInvokeError, CheckFailure, MissingPermissions, MissingRole
from random import randint, choice

inviteLink = 'https://discord.gg/gd42PPv'
cwd = os.getcwd().replace("\\", "/")
client = commands.Bot(command_prefix = 'kt!')
client.remove_command('help')

def error_token(msgID):
    random.seed(msgID)
    errorID = randint(0, 10000000)
    return errorID

def AS():
    AS = client.get_user(id = 456282270974607361)
    return AS.name + "#" + AS.discriminator

with open("%s/tarot.json" % cwd) as cardList:
    cards = json.load(cardList)

def debug_error(ctx, error):
    now = time.localtime()
    errorTime = time.strftime("%H:%M:%S", now)
    errorDate = date.today()
    errorID = error_token(ctx.message.id)
    while(os.path.isfile("{0}/Data/ErrorLogs/{1}.txt".format(cwd, errorID))):
        print("An error log with the same ID has already been created. Generting new ID...")
        errorID = error_token(ctx.message.id + 1)

    ErrorLog = open("{0}/Data/ErrorLogs/{1}.txt".format(cwd, errorID), 'w+')
    ErrorLog.write("Error - {0}\nTime - {1}\nDate - {2}\nMessage - {3}: {4}\nMessage ID - {5}\nError ID - {6}".format(error, errorTime, errorDate, ctx.message.author.name, ctx.message.content, ctx.message.id, errorID))
    ErrorLog.close()
    return errorID

@client.event
async def on_ready():
    print("Logged on!")
    await client.change_presence(status = discord.Status.online, activity = discord.Game(name = "k!help | inside %s servers!" % len(client.guilds)))
    
@client.event
async def on_command_error(ctx, error):
    pass
    
@client.event
async def on_error(event, *args, **kwargs):
    pass

async def errorcheck(usage, ctx, error):

    errorID = debug_error(ctx, error)

    if isinstance(error, CheckFailure) or isinstance(error, MissingPermissions) or isinstance(error, MissingRole):
        await ctx.send("You do not have the permissions required to run this command.")
        
    elif isinstance(error, ArgumentParsingError) or isinstance(error, BadArgument) or isinstance(error, TooManyArguments) or isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(title = 'Improper usage.', description = " ", color = 0xFF88FF)
        embed.add_field(name = "Proper usage:", value = usage, inline = False)
        embed.add_field(name = "Need support with the bot, have concerns, or have a bug to report?\nJoin the support server!", value = inviteLink, inline = False)
        embed.set_footer(text = 'Bot created by %s' % AS())
        await ctx.send(embed = embed)
        
    elif isinstance(error, BotMissingRole) or isinstance(error, BotMissingPermissions):
        await ctx.send("Uh oh! I do not have the permissions to carry out the given command!")
        
    elif isinstance(error, CommandInvokeError):
        await ctx.send("Uh oh! Please contact my creators, or join the support server to get help with this command!\n{0}\nError ID: ``{1}``\n{2}".format(AS(), errorID, inviteLink))
    
    else:
        await ctx.send("An error has occurred.")

@client.event
async def on_message(message):
    if(message.author.bot != True):
        await client.process_commands(message)


#Commands v v v

@client.command(name = '8ball')
async def eightball(ctx, *args):
    message = await ctx.send("Shaking the 8-Ball...")
    await asyncio.sleep(1)
    Response = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    arg = " ".join(args)
    lowerArg = arg.lower()
    userid = ctx.author.id
    random.seed(str(userid) + lowerArg)
    await message.edit(content = "In response to {0}, it reads... \"{1}\"".format(arg, choice(Response)))

@client.command(name = 'cat')
async def cat(ctx):
    path = "%s\\Cats" % (cwd)
    randomCat = random.choice(os.listdir(path))
    await ctx.send("Here's your cat!", file = discord.File(path + '/' + randomCat))

@client.command(name = "grace")
async def grace(ctx):
    await ctx.send("GRACE.\nIS.\nTHE.\nGAYEST.\nGAY.\nEVER.")

@client.command(name = 'help')
async def help(ctx):
    
    embed = discord.Embed(title = "KathBot Commands", description="Here you can get a full list of this bot's commands!", color=0xFF88FF)
    embed.set_thumbnail(url = 'https://puu.sh/Fvnef.png')
    embed.set_footer(text = 'Bot created by %s' % AS())
    embed.add_field(name = "8ball [str]", value = "Shakes the Magic 8-Ball.", inline = False)
    embed.add_field(name = "cat", value = "Sends a cat picture from a selection of 20 cats.", inline = False)
    embed.add_field(name = "grace", value = "Gay", inline = False)
    embed.add_field(name = "invite", value = "Sends a bot invite link.", inline = False)
    embed.add_field(name = "ping", value = "Responds with the bot's current latency.", inline = False) 
    embed.add_field(name = "k!quote [delete|grab|list|store] [str]", value = "Quote storage! [WIP]", inline = False) 
    embed.add_field(name = "rate [str]", value = "Rates an argument from a 0 to 10. All people are a 10/10.", inline = False)
    embed.add_field(name = "say [str]", value = "Makes the bot say anything you want it to.", inline = False)
    embed.add_field(name = "tarot [int] [optional str]", value = "Generates a spread of tarot cards, anywhere from between 1 to 7.", inline = False)
    embed.add_field(name = "Need support with the bot, have concerns, or have a bug to report?\nJoin the support server!", value = inviteLink, inline = False)
    await ctx.send(embed = embed)

@client.command(name = "invite")
async def invite(ctx):
    async with ctx.channel.typing():
        await asyncio.sleep(.3)

    embed = discord.Embed(title="KathBot Invite", description="You want to invite me to your server?!", color=0xFF88FF)
    embed.set_thumbnail(url = 'https://puu.sh/Fvnef.png')
    embed.set_footer(text = 'Bot created by ' + AS())
    embed.add_field(name = "Here's my invite link!", value = "https://discordapp.com/api/oauth2/authorize?client_id=596683881575612429&permissions=67226688&scope=bot")
    await ctx.send(embed = embed)

@client.command(name = 'ping')
async def ping(ctx):
    async with ctx.channel.typing():
        await asyncio.sleep(.4)
        
    await ctx.send("Pong!" + " ``{}ms``".format(round(client.latency * 1000, 1)))

@client.command(name = 'quote')
async def quote(ctx, scmd, *, args = ""):
    if(scmd == 'store'):
        arg = "".join(args)
        if(os.path.isfile("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id))):
            quotesR = open("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id), 'r+')
            try:
                quotesList = json.loads(quotesR.read())

            except:
                await ctx.send("An error has occurred while storing a quote. Please either contact the developer, or delete your quotes file using ``k!quote delete``.")
                return 0
                
            quotesList['quotes'].append(arg)
            print(quotesList)
            quotesR.seek(0)
            quotesR.truncate(0)
            json.dump(quotesList, quotesR)

        else:
            quotesW = open("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id), 'w+')
            quotesList = {'quotes': [arg]}
            json.dump(quotesList, quotesW)

        await ctx.send("'{0}' has been stored!".format(arg))
        quotesR.close()

    elif(scmd == 'list'):
        if(os.path.isfile("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id))):
            quotesR = open("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id), 'r+')
            quotes = json.loads(quotesR.read())['quotes']
            embed = discord.Embed(title = "Here are your stored quotes:", description = " ", color=0xFF88FF)
            embed.set_footer(text = '\nBot created by ' + AS())
            for index in quotes:
                embed.add_field(name = "** **",  value = index, inline = False)

            await ctx.send(embed = embed)
            quotesR.close()

        else:
            await ctx.send("You have not stored any quotes. Store some with ``k!quote store [quote]``!")

    elif(scmd == 'delete'):
        if(os.path.isfile("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id))):
            quotesR = open("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id), 'r+')
            quotes = json.loads(quotesR.read())['quotes']
            for i in len(quotes):
                print('a')


            quotesR.close()

@quote.error
async def quote_error(ctx, error):
    await errorcheck("k!quote [delete|grab|list|store] [str]", ctx, error)

@client.command(name = 'rate')
async def rate(ctx, *args):
    arg = " ".join(args)
    lowerArg = arg.lower()
    async with ctx.channel.typing():
        await asyncio.sleep(1)
        
    if(lowerArg == 'drukon'):
        await ctx.send("Hm... I rate %s a 11/10, for being an amazing friend! <3" % arg)
             
    elif(lowerArg == 'fir'):
        await ctx.send("Hm... I rate %s a 11/10, for being such a precious little bean! <3" % arg)
        
    elif(lowerArg == 'grace'):
        await ctx.send("Grace is the bestest she gets a 11/10 for being such an awesome little sister! <3")
        
    elif(lowerArg == 'pixie' or lowerArg == "sillipha"):
        await ctx.send("Hm.. I rate %s a 11/10! <3" % arg)
        
    else:
        random.seed(lowerArg)
        await ctx.send("Hm... I rate {0} a... {1}/10!".format(arg, randint(0,10)))

@client.command(name = 'say')
async def say(ctx, *args):
    arg = " ".join(args)
    await ctx.send(arg)
    await asyncio.sleep(.75)
    try:
        await ctx.message.delete()
        
    except:
        pass

@client.command(name = "tarot")
async def tarot(ctx, arg = 1, *args):
    try:
        count = int(arg)

    except:
        return BadArgument

    if(count in range(1,8)):
        async with ctx.channel.typing():
            await asyncio.sleep(.6)
    
        embed = discord.Embed(title = "Your spread:", description = " ", color=0xFF88FF)
        embed.set_footer(text = '\nBot created by ' + AS())
        for card in range(0, count):
            card += 1
            flip = random.randint(0, 1)
            if(flip == 0):
                embed.add_field(name = "Card #%s" % card, value = random.choice(cards['cards']), inline = False)
            
            else:
                embed.add_field(name = "Card #%s" % card, value = "Flipped %s\n"% random.choice(cards['cards']), inline = False)

        embed.set_footer(text = "Command is a WIP, type k!help and join the support server if you need help!\nBot created by %s" % AS())
        await ctx.send(embed = embed)

    else:
        await ctx.send("Argument is out of bounds.")


#Staff commands v v v

#None so far, sorry :<


#Owner commands v v v

@client.command(name = "status")
async def OWNER_status(ctx, *, arg):
    if(ctx.author.id == 456282270974607361):
        await client.change_presence(status = discord.Status.online, activity = discord.Game(name = "k!help | {0} | inside {1} servers!".format(arg, len(client.guilds))))
        
    else:
        await ctx.send("You can not command me, mortal!")
        
@client.command(name = "announce")
async def announcement(ctx, *, arg):
    if(ctx.author.id == 456282270974607361):
        for guild in client.guilds:
            embed = discord.Embed(title = "Announcement", description = "Announcement from KathBot's Developer(s)", color = 0xFF88FF)
            embed.add_field(name = "Message:", value = arg, inline = False)
            embed.set_footer(text = "Have concerns? type k!help and join the support server to tell us!\nBot created by %s" % AS())
            for channel in guild.text_channels:
                try:
                    await channel.send(embed = embed)
                    break

                except:
                    continue
        
    else:
        await ctx.send("You cannot command me, mortal!")


#Error checking v v v

@eightball.error
async def eightball_error(ctx, error):
    await errorcheck("k!8ball Argument(s)", ctx, error)

@rate.error
async def rate_error(ctx, error):
    await errorcheck("k!rate Argument(s)", ctx, error)

@say.error
async def say_error(ctx, error):
    await errorcheck("k!say Argument(s)", ctx, error)

@tarot.error
async def tarot_error(ctx, error):
    await errorcheck("k!tarot [int] [optional str]", ctx, error)



with open("%s/token.txt" % cwd) as token:
    client.run(token.read())
