import discord, json, datetime, random, time, string, os
from discord.ext import commands

with open("config.json") as f:
    config = json.load(f)

PREFIX = config.get("prefix")
TOKEN = config.get("token")

client = commands.Bot(command_prefix = PREFIX, case_insensitive = True, intents = discord.Intents.all())
client.remove_command("help")

clearWindow = lambda: os.system("cls")


##### EVENTS #####
@client.event
async def on_ready():
    clearWindow()
    await client.change_presence(activity=discord.Game(name=f"TutorialBot | {PREFIX}help"))
    print("""
:::::::::  ::::::::::     :::     :::::::::  :::   ::: 
:+:    :+: :+:          :+: :+:   :+:    :+: :+:   :+: 
+:+    +:+ +:+         +:+   +:+  +:+    +:+  +:+ +:+  
+#++:++#:  +#++:++#   +#++:++#++: +#+    +:+   +#++:   
+#+    +#+ +#+        +#+     +#+ +#+    +#+    +#+    
#+#    #+# #+#        #+#     #+# #+#    #+#    #+#    
###    ### ########## ###     ### #########     ###      
    """)

@client.event
async def on_voice_state_update(member, before, after):
    with open("tempchannels.json") as f:
        tempchannels = json.load(f)

    if after.channel:
        for g in tempchannels:
            if tempchannels[g] == after.channel.id:
                if not after.channel.category:
                    category = None
                else:
                    category = after.channel.category

                guild = after.channel.guild
                tempchannel = await guild.create_voice_channel("temp-" + str(member.name), category = category, reason = "Temp Channel")
                await tempchannel.edit(user_limit = 2)
                await member.move_to(tempchannel, reason = "Temp Channel")

    elif before.channel.name.startswith("temp-") and not after.channel:
        if str(member.name) in before.channel.name:
            await before.channel.delete()

@client.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, "on_error"):
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send("Error: Command disabled.")
    elif isinstance(error, commands.NoPrivateMessage):
        pass
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Invalid input")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Error: Invalid argument")
    elif isinstance(error, commands.PrivateMessageOnly):
        pass
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("Error: Invalid input")
    elif isinstance(error, commands.UserInputError):
        await ctx.send("Error: Invalid input")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("Error: You are not allowed to use this command")
    elif isinstance(error, commands.MessageNotFound):
        await ctx.send("Error: Message not found")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Error: Member not found")
    elif isinstance(error, commands.UserNotFound):
        await ctx.send("Error: User not found")
    elif isinstance(error, commands.ChannelNotFound):
        await ctx.send("Error: Channel not found")
    elif isinstance(error, commands.ChannelNotReadable):
        await ctx.send("Error: I'm missing permissions")
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send("Error: Role not found")
    elif isinstance(error, commands.EmojiNotFound):
        await ctx.send("Error: Emoji not found")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Error: You are not allowed to use this command")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Error: I'm missing permissions")
    elif isinstance(error, commands.MissingAnyRole):
        await ctx.send("Error: You are not allowed to use this command")
    elif isinstance(error, commands.BotMissingAnyRole):
        await ctx.send("Error: I'm missing a required role")
    elif isinstance(error, commands.NSFWChannelRequired):
        await ctx.send("Error: This command can only be used in a NSFW channel")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Error: This command is on a cooldown, try again after: `{error.retry_ater:,.2f}s`")


##### HELP #####
@client.command()
async def help(ctx, module : str = "general"):
    module = module.lower()

    if module == "general":
        help_general = """
**STAFF** - `mute, unmute, kick, ban, unban, addrole, delrole, purge, nick, lock, unlock`
**FUN** - `penis, howgay, 8ball, hack, roast, guess, rps, coinflip`
**INFO** - `serverinfo, channelinfo, whois, roleinfo, membercount, botinfo`
**USEFUL** - `choose, calculate, rnumber, say, emsay, poll, passgen`
**IMAGES** - `pfp, servericon`
**TICKETS** - `ticket, close, adduser, deluser`
**CONFIG** - `settemp`
        """

        em = discord.Embed(description = help_general, color = 0x000000)
        em.set_author(name = "TutorialBot Help")
        em.set_footer(text = "TutorialBot")
        em.set_thumbnail(url = "https://i.imgur.com/h3CzTuJ.gif")
        em.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = em)

##### STAFF #####
@client.command()
async def mute(ctx, member : discord.Member, *, reason : str = None):
    for role in ctx.guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)
            await ctx.send("Succesfully muted " + member.name + "\nReason: `" + reason + "`")
            return

    role = await ctx.guild.create_role(name = "Muted", color = 0x000000)

    for channel in ctx.guild.text_channels:
        await channel.set_permissions(role, send_messages=False)

    for channel in ctx.guild.voice_channels:
        await channel.set_permissions(role, speak = False)

    await member.add_roles(role)
    await ctx.send("Succesfully muted " + member.name + "\nReason: `" + reason + "`")

@client.command()
async def unmute(ctx, member : discord.Member):
    for role in member.roles:
        if role.name == "Muted":
            await member.remove_roles(role)
            is_muted = True

    if not is_muted:
        await ctx.send("Error: This member is not muted!")
        return

    await ctx.send(member.name + " is not muted anymore!")

@client.command()
async def kick(ctx, member : discord.Member, *, reason : str = None):
    await member.kick(reason = reason)

    await ctx.send("Succesfully kicked " + member.name + "\nReason: `" + reason + "`")

@client.command()
async def ban(ctx, member : discord.Member, *, reason : str = None):
    await member.ban(reason = reason)
    await ctx.send("Succesfully banned `" + member.name + "`")

@client.command()
async def unban(ctx, *, member):
    if "#" in member:
        member_name, member_discriminator = str(member).split("#")
        for entry in await ctx.guild.bans():
            user = entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send("Succesfully unbanned `" + user.name + "`")
    else:
        try:
            member = int(member)
            for entry in await ctx.guild.bans():
                user = entry.user
                if user.id == member:
                    await ctx.guild.unban(user)
                    await ctx.send("Succesfully unbanned `" + user.name + "`")
        except:
            await ctx.send("Error: invalid input.")
            return

@client.command()
async def addrole(ctx, role : discord.Role, member : discord.Member):
    await member.add_roles(role)
    await ctx.send("Succesfully gave `" + member.name + "` the role `" + role.name + "`")

@client.command()
async def delrole(ctx, role : discord.Role, member : discord.Member):
    await member.remove_roles(role)
    await ctx.send("Succesfully removed `" + role.name + "` from `" + member.name + "`")

@client.command()
async def purge(ctx, amt : int = 10):
    await ctx.channel.purge(limit = amt + 1)
    await ctx.send("Succesfully purged `" + amt + "` messages.")

@client.command()
async def nick(ctx, member : discord.Member, *, nick : str = None):
    await member.edit(nick = nick)
    await ctx.send("Succesfully changed the name of " + member.mention)

@client.command()
async def lock(ctx, channel : discord.TextChannel = None, *, reason : str = None):
    if not channel:
        channel = ctx.channel

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    em = discord.Embed(description = "Locked channel\n\nReason: `" + reason + "`")
    em.set_author(name = "Channel Locked")
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = "https://i.imgur.com/h3CzTuJ.gif")
    em.timestamp = datetime.datetime.utcnow()

    await channel.send(embed = em)

@client.command()
async def unlock(ctx, *, channel : discord.TextChannel = None):
    if not channel:
        channel = ctx.channel

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await channel.send("This channel is now unlocked.")


##### FUN #####
@client.command(aliases = ["pp"])
async def penis(ctx, member : discord.Member = None):
    if not member:
        member = ctx.author

    pp = "8"

    for x in range(random.randint(0, 15)):
        pp += "="

    pp += "D"

    await ctx.send(f"{member.name}'s penis: {pp}")

@client.command(aliases = ["gayrate"])
async def howgay(ctx, member : discord.Member = None):
    if not member:
        member = ctx.author

    gayrate = random.randint(0,100)

    await ctx.send(f"{member.name} is {gayrate}% gay")

@client.command(aliases = ["8ball"])
async def _8ball(ctx, *, question : str):
    answers = ["It is certain",
               "Yes",
               "Yes, definitely",
               "Without a doubt",
               "Absolutely yes",
               "Most likely",
               "I'm not sure",
               "Ask again later",
               "Maybe",
               "Don't count on it",
               "Very doubtful",
               "No",
               "Definitely not",
               "My sources say no",
               "My reply is no",]

    answer = random.choice(answers)
    await ctx.send(answer)

@client.command()
async def hack(ctx, member : discord.Member):
    msg = await ctx.send(f"Hacking {member.name}")
    time.sleep(1.3)
    await msg.edit(content = f"Hacking {member.name}.")
    time.sleep(1.9)
    await msg.edit(content = f"Hacking {member.name}..")
    time.sleep(1.5)
    await msg.edit(content = f"Hacking {member.name}...")
    time.sleep(1.2)
    await msg.edit(content = "Injecting trojan - ▓▓▓▓▓▓▓▓▓▓ 0% done")
    time.sleep(2)
    await msg.edit(content = "Injecting trojan - ██▓▓▓▓▓▓▓▓ 23% done")
    time.sleep(2.4)
    await msg.edit(content = "Injecting trojan - █████▓▓▓▓▓ 51% done")
    time.sleep(2.3)
    await msg.edit(content = "Injecting trojan - ████████▓▓ 86% done")
    time.sleep(2.9)
    await msg.edit(content = "Injecting trojan - █████████▓ 99% done")
    time.sleep(5)
    await msg.edit(content = "Injecting trojan - ██████████ 100% done")
    time.sleep(1.1)
    await msg.edit(content = "Injecting trojan completed")
    time.sleep(1.8)
    await msg.edit(content = f"{member.name}'s email: {member.name}.ponylover@gmail.com")
    time.sleep(2.3)
    await msg.edit(content = f"{member.name}'s password: hello123")
    time.sleep(2.1)
    await msg.edit(content = f"Completed the hack on {member.name}")

@client.command()
async def roast(ctx):
    roasts = ["You're as useless as the 'ueue' in 'queue'.",
              "Mirrors can't talk. Lucky for you, they can't laugh either.",
              "Hey, you have something on your chin... no, the 3rd one down.",
              "You're the reason gene pool needs a lifeguard.",
              "If I had a face like yours, I'd sue my parents.",
              "Your only chance of getting laid is to crawl up a chicken's butt and wait.",
              "Some day you'll go far... and i hope you stay there.",
              "Aha! I see the fuck-up fairy has visited us again!",
              "You must have been born on a highway because that's where the most accidents happen.",
              "If laughter is the best medicine, your face must be curing the world.",
              "I'm glad to see you're not letting your education get in the way of your ignorance.",
              "Is your ass jealous of the amount of shit that just came out of your mouth?",
              "So, a thought crossed your mind? Must have been a long and lonely journey.",
              "If I wanted to kill myself I'd climb your ego and jump to your IQ.",
              "I'd agree with you but then we'd both be wrong.",
              "When I see your face there's not a thing I would change... except the direction I was walking in.",
              "If I had a dollar for every time you said something smart, I'd still be broke.",
              "When you were born the doctor threw you out the window and the window threw you back.",
              "I love what you've done with your hair. How do you get it to come out of the nostrils like that?",
              "If your brain was dynamite, there wouldn't be enough to blow your hat off.",
              "You are so annoying, you make a happy meal cry.",
              "I'll never forget the first time we met. But I'll keep trying.",
              "Your face makes onions cry.",
              "You bring everyone so much joy... when you leave the room.",
              "You are like a cloud. When you disappear, it's a beautiful day.",]

    roast = random.choice(roasts)

    await ctx.send(roast)

@client.command()
async def guess(ctx, num1 : int = 0, num2 : int = 10):
    answer = random.randint(num1, num2)
    count = 0
    guessed = False

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    while not guessed:
        q1 = await ctx.send(f"Guess the number between {num1} and {num2}.\nTries: {count}.")
        a1 = await client.wait_for("message", check=check, timeout=60)
        answer1 = a1.content
        answer1 = int(answer1)
        await q1.delete()
        await a1.delete()

        count += 1
        if answer1 == answer:
            guessed = True
        elif answer1 < answer:
            await ctx.send(f"The answer is higher than {answer1}.")
        elif answer1 > answer:
            await ctx.send(f"The answer is lower than {answer1}.")

    await ctx.send(f"You guessed the number between {num1} and {num2} ({answer}) in {count} tries.")

@client.command()
async def rps(ctx, choice : str):
    choice = choice.lower()

    answer = random.choice(["rock", "paper", "scissors"])

    if choice == answer:
        await ctx.send(f"Draw!\nYour choice: {choice}\nMy choice: {answer}")
    elif choice == "rock":
        if answer == "scissors":
            await ctx.send(f"You won!\nYour choice: {choice}\nMy choice: {answer}")
        else:
            await ctx.send(f"You lost!\nYour choice: {choice}\nMy choice: {answer}")
    elif choice == "paper":
        if answer == "rock":
            await ctx.send(f"You won!\nYour choice: {choice}\nMy choice: {answer}")
        else:
            await ctx.send(f"You lost!\nYour choice: {choice}\nMy choice: {answer}")
    elif choice == "scissors":
        if answer == "paper":
            await ctx.send(f"You won!\nYour choice: {choice}\nMy choice: {answer}")
        else:
            await ctx.send(f"You lost!\nYour choice: {choice}\nMy choice: {answer}")
    else:
        await ctx.send("Error: invalid input.")

@client.command()
async def coinflip(ctx):
    answer = random.choice(["Heads", "Tails"])
    await ctx.send("I flipped a coin and the outcome was: " + answer)


##### INFO #####
@client.command(aliases = ["sinfo"])
async def serverinfo(ctx):
    category_count = 0
    channel_count = 0
    tchannel_count = 0
    vchannel_count = 0

    for discord.CategoryChannel in ctx.guild.categories:
        category_count +=1

    for discord.TextChannel in ctx.guild.text_channels:
        tchannel_count +=1

    for discord.VoiceChannel in ctx.guild.voice_channels:
        vchannel_count +=1

    channel_count = tchannel_count + vchannel_count

    em = discord.Embed(color = 0x000000)
    em.set_author(name = ctx.guild.name)
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = ctx.guild.icon_url)
    em.timestamp = datetime.datetime.utcnow()

    em.add_field(name = "Owner", value = client.get_user(ctx.guild.owner_id), inline = True)
    em.add_field(name = "Region", value = ctx.guild.region, inline = True)
    em.add_field(name = "Server ID", value = ctx.guild.id, inline = True)
    em.add_field(name = "Member Count", value = ctx.guild.member_count, inline = True)
    em.add_field(name = "Boosts", value = ctx.guild.premium_subscription_count, inline = True)
    em.add_field(name = "Categories", value = category_count, inline = True)
    em.add_field(name = "Total Channels", value = channel_count, inline = True)
    em.add_field(name = "Text Channels", value = tchannel_count, inline = True)
    em.add_field(name = "Voice Channels", value = vchannel_count, inline = True)

    await ctx.send(embed = em)

@client.command(aliases = ["cinfo"])
async def channelinfo(ctx, channel : discord.TextChannel = None):
    if not channel:
        channel = ctx.channel

    em = discord.Embed(color = 0x000000)
    em.set_author(name = channel.name)
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = "https://i.imgur.com/h3CzTuJ.gif")
    em.timestamp = datetime.datetime.utcnow()

    em.add_field(name = "Name", value = channel.name, inline = True)
    em.add_field(name = "Category", value = channel.category, inline = True)
    em.add_field(name = "ID", value = channel.id, inline = True)
    em.add_field(name = "NSFW?", value = channel.is_nsfw(), inline = True)
    em.add_field(name = "News?", value = channel.is_news(), inline = True)
    em.add_field(name = "Created at", value = channel.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline = True)

    await ctx.send(embed = em)

@client.command(aliases = ["memberinfo", "minfo"])
async def whois(ctx, member : discord.Member = None):
    if not member:
        member = ctx.author

    em = discord.Embed(color = 0x000000)
    em.set_author(name = member.name + "#" + member.discriminator)
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = member.avatar_url)
    em.timestamp = datetime.datetime.utcnow()

    em.add_field(name = "Nickname", value = member.nick, inline = True)
    em.add_field(name = "Bot?", value = member.bot, inline = True)
    em.add_field(name = "ID", value = member.id, inline = True)
    em.add_field(name = "Status", value = member.status, inline = True)
    em.add_field(name = "Discriminator", value = member.discriminator, inline = True)
    em.add_field(name = "Created at", value = member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline = True)
    em.add_field(name = "Top Role", value = member.top_role, inline = True)
    em.add_field(name = "Roles", value = len(member.roles), inline = True)
    em.add_field(name = "Joined at", value = member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline = True)

    await ctx.send(embed = em)

@client.command(aliases = ["rinfo"])
async def roleinfo(ctx, role : discord.Role):
    em = discord.Embed(color = 0x000000)
    em.set_author(name = role.name)
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = "https://i.imgur.com/h3CzTuJ.gif")
    em.timestamp = datetime.datetime.utcnow()

    em.add_field(name = "ID", value = role.id, inline = True)
    em.add_field(name = "Mentionable?", value = role.mentionable, inline = True)
    em.add_field(name = "Created at", value = role.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline = True)
    em.add_field(name = "Members", value = len(role.members), inline = True)
    em.add_field(name = "Default?", value = role.is_default(), inline = True)
    em.add_field(name = "Color", value = role.color, inline = True)

    await ctx.send(embed = em)

@client.command(aliases = ["mcount"])
async def membercount(ctx):
    total_members = len(ctx.guild.members)
    human_members = 0
    bot_members = 0

    for member in ctx.guild.members:
        if member.bot:
            bot_members += 1
        else:
            human_members += 1

    description = f"""
    **Total Members** 
    {total_members}

    **Humans** 
    {human_members}

    **Bots** 
    {bot_members}
    """

    em = discord.Embed(description = description, color = 0x000000)
    em.set_author(name = "Member Count")
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = "https://i.imgur.com/h3CzTuJ.gif")
    em.timestamp = datetime.datetime.utcnow()

    await ctx.send(embed = em)

@client.command()
async def botinfo(ctx):
    description = f"""
    **Ping** 
    {round(client.latency * 1000)}ms

    **Creator**
    jappie._#1379

    **Information**
    This bot is a bot made for a tutorial. It is not perfect, but it does the things it's supposed to!
    """

    em = discord.Embed(description = description, color = 0x000000)
    em.set_author(name = "TutorialBot Info")
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = "https://i.imgur.com/h3CzTuJ.gif")
    em.timestamp = datetime.datetime.utcnow()

    await ctx.send(embed = em)


##### USEFUL #####
@client.command()
async def choose(ctx, *, choices : str):
    choicelist = choices.split(",")
    choice = random.choice(choicelist)

    await ctx.send(choice)

@client.command(aliases = ["calc"])
async def calculate(ctx, *, calculation : str):
    try:
        answer = eval(calculation)
    except:
        await ctx.send("Error: invalid input.")
        return

    await ctx.send(calculation + " = " + str(answer))

@client.command(aliases = ["rnum"])
async def rnumber(ctx, minimum : int, maximum : int):
    rnum = random.randint(minimum, maximum)
    await ctx.send(rnum)

@client.command()
async def say(ctx, *, txt : str):
    await ctx.send(txt)

@client.command()
async def emsay(ctx, *, txt : str):
    em = discord.Embed(description = txt, color = 0x000000)
    em.set_author(name = "TutorialBot")
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = "https://i.imgur.com/h3CzTuJ.gif")
    em.timestamp = datetime.datetime.utcnow()

    await ctx.send(embed = em)

@client.command()
async def poll(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    q1 = await ctx.send("What is the question for the poll?")
    a1 = await client.wait_for("message", check=check, timeout=60)
    question = a1.content
    await q1.delete()
    await a1.delete()

    q1 = await ctx.send("What is the first possible answer for the poll?")
    a1 = await client.wait_for("message", check=check, timeout=60)
    answer1 = a1.content
    await q1.delete()
    await a1.delete()

    q1 = await ctx.send("What is the second possible answer for the poll?")
    a1 = await client.wait_for("message", check=check, timeout=60)
    answer2 = a1.content
    await q1.delete()
    await a1.delete()

    q1 = await ctx.send("What is the third possible answer for the poll? (send `done` if you don't have any more answers)")
    a1 = await client.wait_for("message", check=check, timeout=60)
    answer3 = a1.content
    await q1.delete()
    await a1.delete()

    if not answer3.lower() == "done":
        q1 = await ctx.send("What is the fourth possible answer for the poll? (send `done` if you don't have any more answers)")
        a1 = await client.wait_for("message", check=check, timeout=60)
        answer4 = a1.content
        await q1.delete()
        await a1.delete()

        if not answer4.lower() == "done":
            q1 = await ctx.send("What is the fifth possible answer for the poll? (send `done` if you don't have any more answers)")
            a1 = await client.wait_for("message", check=check, timeout=60)
            answer5 = a1.content
            await q1.delete()
            await a1.delete()

            if not answer5.lower() == "done":
                count = 5
                description = f"""
                🇦 - {answer1}
                🇧 - {answer2}
                🇨 - {answer3}
                🇩 - {answer4}
                🇪 - {answer5}
                """
            else:
                count = 4
                description = f"""
                🇦 - {answer1}
                🇧 - {answer2}
                🇨 - {answer3}
                🇩 - {answer4}
                """
        else:
            count = 3
            description = f"""
            🇦 - {answer1}
            🇧 - {answer2}
            🇨 - {answer3}
            """
    else:
        count = 2
        description = f"""
        🇦 - {answer1}
        🇧 - {answer2}
        """

    description = "**" + question + "**" + "\n" + description

    em = discord.Embed(description = description, color = 0x000000)
    em.set_author(name = "Poll")
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = "https://i.imgur.com/h3CzTuJ.gif")
    em.timestamp = datetime.datetime.utcnow()

    msg = await ctx.send(embed = em)

    await msg.add_reaction("🇦")
    await msg.add_reaction("🇧")
    if count == 3 or count == 4 or count == 5:
        await msg.add_reaction("🇨")
        if count == 4 or count == 5:
            await msg.add_reaction("🇩")
            if count == 5:
                await msg.add_reaction("🇪")

@client.command()
async def passgen(ctx, length : int = 10):
    letters = string.ascii_letters
    numbers = string.digits
    symbols = string.punctuation

    pass_choices = letters + numbers + symbols

    password = "".join(random.sample(pass_choices, length))

    await ctx.author.send("Your password is: `" + password + "`")
    await ctx.send("Your password is sent in your dms.")


##### IMAGES #####
@client.command(aliases = ["avatar"])
async def pfp(ctx, member : discord.Member = None):
    if not member:
        member = ctx.author

    em = discord.Embed(color = 0x000000)
    em.set_author(name = f"{member.name}'s avatar")
    em.set_image(url = member.avatar_url)

    await ctx.send(embed = em)

@client.command()
async def servericon(ctx):
    em = discord.Embed(color = 0x000000)
    em.set_author(name = f"{ctx.guild.name}'s icon")
    em.set_image(url = ctx.guild.icon_url)

    await ctx.send(embed = em)


##### TICKETS #####
@client.command(aliases = ["new"])
async def ticket(ctx):
    ticket_name = "ticket-" + str(ctx.author.name)

    for channel in ctx.guild.channels:
        if channel.name == ticket_name:
            await ctx.send("You already have an open ticket! Close this one before opening a new ticket.")
            return

    ticket_channel = await ctx.guild.create_text_channel(ticket_name)
    await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await ticket_channel.set_permissions(ctx.author, read_messages=True)

    em = discord.Embed(description = "Support will be with you shortly!", color = 0x000000)
    em.set_author(name = "TutorialBot")
    em.set_footer(text = "TutorialBot")
    em.set_thumbnail(url = "https://i.imgur.com/h3CzTuJ.gif")
    em.timestamp = datetime.datetime.utcnow()

    await ticket_channel.send(embed = em)
    ticket_ping = await ticket_channel.send(ctx.author.mention)
    await ticket_ping.delete()
    await ctx.send("Your ticket has been created: " + ticket_channel.mention)

@client.command()
async def close(ctx, channel : discord.TextChannel = None):
    if not channel:
        channel = ctx.channel

    if not channel.name.startswith("ticket-"):
        await ctx.send("This channel is not a ticket!")
        return

    msg = await ctx.send("Are you sure you want to close this ticket?")
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

    def check(reaction, user):
        return reaction.emoji in ["✅","❌"] and reaction.message == msg and user == ctx.author

    reaction, user = await client.wait_for("reaction_add", check=check, timeout=60)

    if reaction.emoji == "❌":
        await ctx.send("Ticket deletion cancelled.")
        return
    else:
        await channel.delete()

@client.command()
async def adduser(ctx, member : discord.Member, ticket_channel : discord.TextChannel = None):
    if not ticket_channel:
        ticket_channel = ctx.channel

    if not ticket_channel.name.startswith("ticket-"):
        await ctx.send("This is not a ticket channel!")
        return

    await ticket_channel.set_permissions(member, read_messages=True)
    await ticket_channel.send(member.mention + " has succesfully been added to this ticket.")

@client.command()
async def deluser(ctx, member : discord.Member, ticket_channel : discord.TextChannel = None):
    if not ticket_channel:
        ticket_channel = ctx.channel

    if not ticket_channel.name.startswith("ticket-"):
        await ctx.send("This is not a ticket channel!")
        return

    await ticket_channel.set_permissions(member, read_messages=False)
    await ticket_channel.send(member.mention + " has succesfully been removed from this ticket.")


##### CONFIG #####
@client.command()
async def settemp(ctx, tempchannelID : int):
    with open("tempchannels.json") as f:
        tempchannels = json.load(f)

    tempchannels[str(ctx.guild.id)] = tempchannelID

    with open("tempchannels.json", "w") as f:
        json.dump(tempchannels, f, indent = 2)

    tempchannel = ctx.guild.get_channel(tempchannelID)

    await ctx.send("Succesfully set `" + tempchannel.name + "` to the temp channel")


client.run(TOKEN)
