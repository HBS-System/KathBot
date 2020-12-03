import discord, asyncio, os, random, json, time
from datetime import date
from discord import HTTPException
from discord.errors import Forbidden, NotFound
from discord.ext import commands
from discord.ext.commands import *
from random import randint, choice

from discord.gateway import DiscordClientWebSocketResponse

inviteLink = 'https://discord.gg/gd42PPv'
cwd = os.getcwd( ).replace('\\', '/')
client = commands.Bot(command_prefix = 'kt!')
client.remove_command('help')

#If you have tips on formatting or code, please notify me.

def AS( ):
    AS = client.get_user(id = 456282270974607361)
    return AS.name + '#' + AS.discriminator

with open('%s/tarot.json' % cwd) as cardList:
    cards = json.load(cardList)

def debug_error(ctx, error):
    now = time.localtime( )
    errorTime = time.strftime('%H:%M:%S', now)
    errorDate = date.today( )
    random.seed(ctx.message.id)
    errorID = randint(0, 10000000)
    while(os.path.isfile("{0}/Data/ErrorLogs/{1}.txt".format(cwd, errorID) ) ):
        print("An error log with the same ID has already been created. Generting new ID...")
        errorID += 1

    ErrorLog = open("{0}/Data/ErrorLogs/{1}.txt".format(cwd, errorID), 'w+')
    ErrorLog.write("Error - {0}\nTime - {1}\nDate - {2}\nMessage - {3}: {4}\nMessage ID - {5}\nError ID - {6}".format(error, errorTime, errorDate, ctx.message.author.name, ctx.message.content, ctx.message.id, errorID) )
    ErrorLog.close( )
    return errorID

@client.event
async def on_ready( ):
    print("Successfully logged on.")
    await client.change_presence(status = discord.Status.online, activity = discord.Game(name = "k!help | inside %s servers!" % len(client.guilds) ) )
    
@client.event #on_command_error is required to generate an error that can be output in debug logs.
async def on_command_error(ctx, error):
    pass

async def errorcheck(usage, ctx, error):
    errorID = debug_error(ctx, error)

    if isinstance(error, CheckFailure) or isinstance(error, MissingPermissions) or isinstance(error, MissingRole):
        embed = discord.Embed(title = 'An error has occurred.', description = ' ', color = 0xFF88FF)
        embed.add_field(name = "** ** \nPermission error.", value = "You do not have permission to use this command.", inline = False)
        embed.add_field(name = "** ** \nPlease read above message, or contact my developers if you believe this may be a bug.", value = "Error ID: ``{0}`` \n[KathBot Support Server]({1})".format(errorID, inviteLink), inline = False)
        embed.set_footer(text = 'Bot created by %s' % AS( ) )
        await ctx.send(embed = embed)
        
    elif isinstance(error, ArgumentParsingError) or isinstance(error, UserInputError) or isinstance(error, BadArgument) or isinstance(error, TooManyArguments) or isinstance(error, MissingRequiredArgument) or isinstance(error, HTTPException):
        embed = discord.Embed(title = 'An error has occurred.', description = ' ', color = 0xFF88FF)
        embed.add_field(name = "** ** \nImproper usage.", value = "Proper usage: %s" % usage, inline = False)
        embed.add_field(name = "** ** \nPlease read above message, or contact my developers if you believe this may be a bug.", value = "Error ID: ``{0}`` \n[KathBot Support Server]({1})".format(errorID, inviteLink), inline = False)
        embed.set_footer(text = 'Bot created by %s' % AS( ) )
        await ctx.send(embed = embed)
        
    elif isinstance(error, BotMissingRole) or isinstance(error, BotMissingPermissions) or isinstance(error, Forbidden):
        embed = discord.Embed(title = 'An error has occurred.', description = ' ', color = 0xFF88FF)
        embed.add_field(name = "** ** \nPermission error.", value = "I do not have the permission to cary out this command.", inline = False)
        embed.add_field(name = "** ** \nPlease read above message, or contact my developers if you believe this may be a bug.", value = "Error ID: ``{0}`` \n[KathBot Support Server]({1})".format(errorID, inviteLink), inline = False)
        embed.set_footer(text = 'Bot created by %s' % AS( ) )
        await ctx.send(embed = embed)
        
    elif isinstance(error, CommandInvokeError) or isinstance(error, NotFound):
        embed = discord.Embed(title = 'An internal error has occurred.', description = ' ', color = 0xFF88FF)
        embed.add_field(name = "** ** \nContact developers for assistance.", value = "Error ID: ``{0}`` \n[KathBot Support Server]({1})".format(errorID, inviteLink), inline = False)
        embed.set_footer(text = 'Bot created by %s' % AS( ) )
        await ctx.send(embed = embed)

    else:
        embed = discord.Embed(title = 'An i͝m̡p̧͜o̧̕s҉̕͠s̵͝͝i͏̶̨͜b̷̛̕͠l̀͘͞͝ȩ̶́͘͞ error has occurred.', description = "How the hell are you even seeing this?\n This shouldn't be happening.", color = 0xFF88FF)
        embed.add_field(name = "** ** \nContact my developers for assistance. \nPlease. Something is wrong.", value = "Error ID: ``{0}`` \n[KathBot Support Server]({1})".format(errorID, inviteLink), inline = False)
        embed.set_footer(text = 'Bot created by {0} \nBroken by {1}'.format(AS( ), ctx.author.name + '#' + ctx.author.discriminator) )
        await ctx.send(embed = embed)

@client.event
async def on_message(message):
    if(message.author.bot != True): #This is to exclude bot messages from running commands, to prevent errors with PluralKit and spam with other bots.
        await client.process_commands(message)



#Commands v v v

@client.command(name = '8ball')
async def eightball(ctx, *args):
    message = await ctx.send("Shaking the 8-Ball...")
    await asyncio.sleep(2)
    response = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    arg = ' '.join(args)
    lowerArg = arg.lower( )
    userID = ctx.author.id
    random.seed(str(userID) + lowerArg)
    await message.edit(content = "In response to {0}, it reads... \"{1}\"".format(arg, choice(response) ) )

@client.command(name = 'cat') #I need to make a pylint scraper to get cat images off of a site with strictly cat images for more of a variety.
async def cat(ctx):
    path = '%s/Cats' % (cwd)
    randomCat = random.choice(os.listdir(path) )
    await ctx.send("Here's your cat!", file = discord.File(path + '/' + randomCat) )

@client.command(name = 'grace')
async def grace(ctx):
    await ctx.send("GRACE. \nIS. \nTHE. \nGAYEST. \nGAY. \nEVER.") #i love you grace :)

@client.command(name = 'help')
async def help(ctx):
    embed = discord.Embed(title = "KathBot Commands", description="Here you can get a full list of this bot's commands!", color=0xFF88FF)
    embed.set_thumbnail(url = 'https://puu.sh/Fvnef.png')
    embed.add_field(name = "8ball [str]", value = "Shakes the Magic 8-Ball.", inline = False)
    embed.add_field(name = 'cat', value = "Sends a cat picture from a selection of 20 cats.", inline = False)
    embed.add_field(name = 'invite', value = "Sends a bot invite link.", inline = False)
    embed.add_field(name = 'ping', value = "Responds with the bot's current latency.", inline = False) 
    embed.add_field(name = "quote [delete|list|store] [str]", value = "Stores up to 15 quotes!", inline = False) 
    embed.add_field(name = "rate [str]", value = "Rates an argument from a 0 to 10. All people who rate themselves are an 11/10!", inline = False)
    embed.add_field(name = "say [str]", value = "Makes the bot say anything you want it to.", inline = False)
    embed.add_field(name = "info", value = "Run this command to get a little more info on me!", inline = False)
    embed.add_field(name = "tarot [int] [optional str]", value = "Generates a spread of tarot cards, anywhere from between 1 to 7. [WIP]", inline = False)
    embed.add_field(name = "Need support with the bot, have concerns, or have a bug to report?", value = "**Join the [KathBot Support Server!](%s)**" % inviteLink, inline = False)
    embed.set_footer(text = "Bot created by %s" % AS( ) )
    await ctx.send(embed = embed)

@client.command(name = 'invite')
async def invite(ctx):
    async with ctx.channel.typing( ):
        await asyncio.sleep(.3)

    embed = discord.Embed(title="KathBot Invite", description="You want to invite me to your server?!", color=0xFF88FF)
    embed.set_thumbnail(url = 'https://puu.sh/Fvnef.png')
    embed.add_field(name = "Which version would you like to invite?", value = "[Public](https://discordapp.com/oauth2/authorize?client_id=596683881575612429&scope=bot&permissions=335890512) \n[Public Dev](https://discord.com/oauth2/authorize?client_id=610044394854416404&scope=bot&permissions=335890512)")
    embed.add_field(name = "Need support with the bot, have concerns, or have a bug to report?", value = "**Join the [KathBot Support Server!](%s)**" % inviteLink, inline = False)
    embed.set_footer(text = "Bot created by %s" % AS( ) )
    await ctx.send(embed = embed)

@client.command(name = 'ping')
async def ping(ctx):
    async with ctx.channel.typing( ):
        await asyncio.sleep(.4)
        
    await ctx.send('Pong!' + ' ``{}ms``'.format(round(client.latency * 1000, 1) ) )

@client.command(name = 'poggers')
async def poggers(ctx):
    await ctx.send('pogChampers')

@client.command(name = 'quote') #this is a fucking mess oH GOD MY EYES
async def quote(ctx, scmd, *, args = ''):
    if(scmd == 'store' or scmd == 's'):
        arg = ''.join(args)
        if(arg == '' or arg == '** **' or arg == ' '):
            errorID = debug_error(ctx, "User input an invalid or empty quote for storage.")
            embed = discord.Embed(title = 'An error has occurred.', description = ' ', color = 0xFF88FF)
            embed.add_field(name = "** **\n", value = "You can't store an empty quote.", inline = False)
            embed.add_field(name = "** ** \nPlease read above message, or contact my developers if you believe this may be a bug.", value = "Error ID: ``{0}`` \n[KathBot Support Server]({1})".format(errorID, inviteLink), inline = False)
            embed.set_footer(text = 'Bot created by %s' % AS( ) )
            await ctx.send(embed = embed)
            return 0

        if(len(arg) < 100):
            if(os.path.isfile("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id) ) ):
                quotesR = open("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id), 'r+')
                try:
                    quotesList = json.loads(quotesR.read( ) )
                    quotesList['quotes'].append(arg)

                except:
                    quotesList = {'quotes': ["persist", arg] }
                if(len(quotesList['quotes'] ) > 16):
                    await ctx.send("Can not store quote. (Quote storage limit exceeded)")
                    return 0

                elif(len(quotesList['quotes'] ) < 1):
                    pass

                quotesR.seek(0)
                quotesR.truncate(0)
                json.dump(quotesList, quotesR)

            else:
                quotesW = open("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id), 'w+')
                quotesList = {'quotes': ["persist", arg] }
                json.dump(quotesList, quotesW)

            await ctx.send("\"{0}\" has been stored!".format(arg) )

        else:
            await ctx.send("Can not store quote. (Quote exceeds 100 character limit)")

    elif(scmd == 'list' or scmd == 'l'):
        if(os.path.isfile("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id) ) ):
            try:
                quotesR = open("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id), 'r+')
                quotes = json.loads(quotesR.read( ) )['quotes']
                if(len(quotes) <= 1):
                    await ctx.send("You have not stored any quotes. Store some with ``k!quote store [quote]``!")
                    return 0
                    
                embed = discord.Embed(title = "Here are your stored quotes:", description = ' ', color=0xFF88FF)
                for index in quotes:
                    if(index == quotes[0]):
                        continue

                    embed.add_field(name = '** **',  value = index, inline = False)

                embed.add_field(name = "Need support with the bot, have concerns, or have a bug to report?", value = "**Join the [KathBot Support Server!](%s)**" % inviteLink, inline = False)
                embed.set_footer(text = "Bot created by %s" % AS( ) )
                await ctx.send(embed = embed)

            except:
                errorID = debug_error(ctx, "User input an invalid or empty quote for storage.")
                embed = discord.Embed(title = 'An internal error has occurred.', description = ' ', color = 0xFF88FF)
                embed.add_field(name = "** ** \nContact developers for assistance.", value = "Error ID: ``{0}`` \n[KathBot Support Server]({1})".format(errorID, inviteLink), inline = False)
                embed.set_footer(text = 'Bot created by %s' % AS( ) )
                await ctx.send(embed = embed)

        else:
            await ctx.send("You have not stored any quotes. Store some with ``k!quote store [quote]``!")

    elif(scmd == 'delete' or scmd == 'd' or scmd == 'del'): #May need to be refined a little bit in the future
        if(os.path.isfile("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id) ) ):
            quotesR = open("{0}/Data/QuotesStorage/{1}.json".format(cwd, ctx.author.id), 'r+')
            quotesList = json.loads(quotesR.read( ) )['quotes']
            if(len(quotesList) <= 1):
                await ctx.send("You have not stored any quotes. Store some with ``k!quote store [quote]``!")
                return 0

            embed = discord.Embed(title = "Which quote would you like to delete?", description = "Respond with \"cancel\" to stop. \nCommand will time out in 30 seconds", color=0xFF88FF)
            count = 0
            for i in quotesList:
                if(i == quotesList[0]):
                    continue

                count += 1
                embed.add_field(name = str(count), value = i, inline = False)
            
            embed.add_field(name = "Need support with the bot, have concerns, or have a bug to report?", value = "**Join the [KathBot Support Server!](%s)**" % inviteLink, inline = False)
            embed.set_footer(text = "Bot created by %s" % AS( ) )
            await ctx.send(embed = embed)

            def check(m):
                return m.channel == ctx.channel, m.author == ctx.author, m.content == ctx.message.content

            try:
                while True:
                    msg = await client.wait_for('message', check=check, timeout = 30.0)
                    if(msg.author != ctx.author):
                        continue

                    else:
                        try:
                            intMsg = int(msg.content)
                            if(intMsg == "cancel" or intMsg == "exit"):
                                await ctx.send("Quote deletion cancelled.")
                                return 0
                            try:
                                deletedQuote = quotesList[intMsg]
                                quotesList.remove(quotesList[intMsg] )
                                quotes = {'quotes': quotesList}
                                quotesR.seek(0)
                                quotesR.truncate(0)
                                json.dump(quotes, quotesR)
                                await ctx.send("\"{0}\" has been deleted.".format(deletedQuote) )
                                break
                    
                            except:
                                await ctx.send("\"{0}\" is not a valid number. Please specify the number above the quote you want deleted.".format(msg.content) )

                        except:
                            await ctx.send("\"{0}\" is not a valid number. Please specify the number above the quote you want deleted.".format(msg.content) )

            except:
                await ctx.send("Command has timed out.")

@client.command(name = 'rate')
async def rate(ctx, *args):
    arg = ' '.join(args)
    lowerArg = arg.lower( )
    async with ctx.channel.typing( ):
        await asyncio.sleep(1)
             
    if(lowerArg == 'pixie' or lowerArg == 'sillipha' or lowerArg == 'grace' or lowerArg == 'nfs' or lowerArg == 'draco' or lowerArg == 'lucas'):
        await ctx.send("Hm.. I rate %s a 11/10! <3" % arg)
        
    else:
        random.seed(lowerArg)
        await ctx.send("Hm... I rate {0} a... {1}/10!".format(arg, randint(0,10) ) )

@client.command(name = 'say')
async def say(ctx, *, args = ''):
    arg = ' '.join(args)
    if(args == ' ' or args == '' or args == "** **"):
        await ctx.send("There's nothing there!")
        return 0

    await ctx.send(arg)
    await asyncio.sleep(.75)
    try:
        await ctx.message.delete( )
        
    except:
        return 0

@client.command(name = 'info')
async def info(ctx):
    embed = discord.Embed(title = 'Information', description = '** **', color = 0xFF88FF)
    embed.add_field(name = "Source Code", value = "You can find a link to my source code [here](https://github.com/HBS-System/KathBot)! \n** **", inline = False)
    embed.add_field(name = "Trello", value = "You can visit my trello [here](https://trello.com/b/1VH1OE4n/kathbot-python)! \n** **", inline = False)
    embed.add_field(name = "Twitter", value = "You can visit the dev twitter (here)[https://twitter.com/kathbot_dev]!", inline = False)
    embed.add_field(name = "About KathBot!", value = "Just a bot AS decided to work on in their spare time. There isn't any specific goal for the bot, but it's going.", inline = False)
    embed.add_field(name = "Need support with the bot, have concerns, or have a bug to report?", value = "**Join the [KathBot Support Server!](%s)**" % inviteLink, inline = False)
    embed.set_footer(text = "Bot created by %s" % AS( ) )
    await ctx.send(embed = embed)

@client.command(name = 'tarot')
async def tarot(ctx, arg = 1, *args):
    try:
        count = int(arg)

    except:
        return BadArgument

    if(count in range(1,8)):
        async with ctx.channel.typing( ):
            await asyncio.sleep(.6)
    
        embed = discord.Embed(title = "Your spread:", description = ' ', color=0xFF88FF)
        embed.set_footer(text = 'Bot created by ' + AS( ) )
        for card in range(0, count):
            card += 1
            flip = random.randint(0, 1)
            if(flip == 0):
                embed.add_field(name = "Card #%s" % card, value = random.choice(cards['cards'] ), inline = False)
            
            else:
                embed.add_field(name = "Card #%s" % card, value = "Flipped %s\n"% random.choice(cards['cards'] ), inline = False)

        embed.add_field(name = "Need support with the bot, have concerns, or have a bug to report?", value = "**Join the [KathBot Support Server!](%s)**" % inviteLink, inline = False)
        embed.set_footer(text = "Bot created by %s" % AS( ) )
        await ctx.send(embed = embed)

    else:
        await ctx.send("Argument is out of bounds.")



#Moderation commands are currently in development.



#Owner commands v v v

@client.command(name = 'status')
async def owner_status(ctx, *, arg):
    if(ctx.author.id == 456282270974607361):
        await client.change_presence(status = discord.Status.online, activity = discord.Game(name = "k!help | {0} | inside {1} servers!".format(arg, len(client.guilds) ) ) )
        await ctx.send("Status has been changed to ``k!help | {0} | inside {1} servers!``".format(arg, len(client.guilds) ) )
        
    else:
        await ctx.send("You can not command me, mortal!")
        
@client.command(name = 'announce')
async def owner_announce(ctx, *, arg):
    if(ctx.author.id == 456282270974607361):
        for guild in client.guilds:
            embed = discord.Embed(title = 'Announcement', description = "Announcement from KathBot's Developer(s)", color = 0xFF88FF)
            embed.add_field(name = 'Message:', value = arg, inline = False)
            embed.add_field(name = "Need support with the bot, have concerns, or have a bug to report?", value = "**Join the [KathBot Support Server!](%s)**" % inviteLink, inline = False)
            embed.set_footer(text = "Bot created by %s" % AS( ) )
            for channel in guild.text_channels:
                if(bot_has_permissions(discord.Permissions.view_channel, discord.Permissions.send_messages)):
                    pass

                else:
                    continue

                try:
                    await channel.send(embed = embed)
                    break

                except:
                    continue
        
    else:
        await ctx.send("You cannot command me, mortal!")



#Owner command error checking v v v

@owner_announce.error
async def announcement_error(ctx, error):
    await errorcheck("k!announce [args] \nBOT OWNER ONLY", ctx, error)

@owner_status.error
async def status_error(ctx, error):
    await errorcheck("k!status [args] \nBOT OWNER ONLY", ctx, error)



#Moderator command error checking is currently in development.



#User command error checking v v v

@eightball.error
async def eightball_error(ctx, error):
    await errorcheck("k!8ball Argument(s)", ctx, error)

@cat.error
async def eightball_error(ctx, error):
    await errorcheck("k!cat", ctx, error)

@help.error
async def help_error(ctx, error):
    await errorcheck("k!help", ctx, error)

@invite.error
async def invite_error(ctx, error):
    await errorcheck("k!invite", ctx, error)

@ping.error
async def ping_error(ctx, error):
    await errorcheck("k!ping", ctx, error)

@quote.error
async def quote_error(ctx, error):
    await errorcheck("k!quote [store|list|delete] [str]", ctx, error)

@rate.error
async def rate_error(ctx, error):
    await errorcheck("k!rate Argument(s)", ctx, error)

@say.error
async def say_error(ctx, error):
    await errorcheck("k!say [args]", ctx, error)

@info.error
async def info_error(ctx, error):
    await errorcheck("k!info", ctx, error)

@tarot.error
async def tarot_error(ctx, error):
    await errorcheck("k!tarot [int] [optional str]", ctx, error)



#Running the bot v v v

with open('%s/token.txt' % cwd) as token:
    try:
        client.run(token.read( ) )
    
    except:
        if(isinstance(Forbidden)):
            print("Error 403, Forbidden.")
        
        elif(isinstance(NotFound)):
            print("Error 404, Not Found.")

        else:
            print("Unknown error. Check code and/or token.")

        input(">Press any key to exit...")
        quit()