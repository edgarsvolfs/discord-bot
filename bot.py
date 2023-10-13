import os
import discord
import random
import json
import datetime
import BalanceCommands
import BlackjackCommands
from datetime import timedelta
from keep_alive import keep_alive

import openai
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

intents = discord.Intents.all()
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)
cooldown = commands.CooldownMapping.from_cooldown(1, 15,
                                                  commands.BucketType.user)


def getChannel():
  return bot.get_channel(1047531070314250311)


@bot.event
async def on_member_join(member):
  role = discord.utils.get(member.guild.roles, name='Plebs')
  channel = bot.get_channel(401071542110388257)
  await member.add_roles(role)
  await channel.send(f'> Hey {member.mention}, welcome to **HeHeXD**')


@bot.event
async def on_member_remove(member):
  member_name = str(member).split('#')[0]
  channel = bot.get_channel(401071542110388257)
  await channel.send(f'> **{member_name}** finally pissed off')


async def printMessage(text):
  channel = getChannel()
  await channel.send(str(text))


@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
  BalanceCommands.checkUserInDictionary(ctx.author)
  await ctx.send('you redeemed 100 credits')
  BalanceCommands.updateUserBalance(ctx.author, 100)


@bot.command()
async def timeout(ctx, member: discord.Member, *, minutes):
  userCredits = BalanceCommands.getUserBalance(ctx.author)
  timeoutPrice = int(minutes) * 100
  if member.id == ctx.author.id:
    await ctx.send("You can't timeout yourself!")
    return

  if int(userCredits) >= int(timeoutPrice):
    duration = timedelta(minutes=int(minutes))
    await member.timeout(duration)
    BalanceCommands.updateUserBalance(ctx.author, -timeoutPrice)
    await ctx.send(
      f"<@{member.id}> has been timed out for {minutes} minutes by <@{ctx.author.id}>."
    )
  elif int(userCredits) < int(timeoutPrice):
    await ctx.send(
      f"you have {userCredits} credits but you need {timeoutPrice}")
  elif member.id == 898900187966218252:  # bot id
    await ctx.send(f'XD? <@{ctx.author.id}>')
    duration = timedelta(minutes=int(60))
    await ctx.author.timeout(duration)
  else:
    await ctx.send(f"type it like **!timeout @someone time_in_minutes**")


@bot.command()
async def info(ctx):
  await ctx.send(
    '> **!daily** to claim 100 daily credits\n > **!bal** to check your credits\n > **!blackjack '
    'credits** to play blackjack with a credit bet\n > **!timeout @user minutes** to timeout someone - '
    '100 credits for 1 minute')


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    hours = int(error.retry_after) / 3600
    minutes = (error.retry_after / 60) - (int(hours) * 60)

    await ctx.send(
      f'This command is on a {int(hours)} hour and {int(minutes)} minute cooldown'
    )
  raise error


@bot.command()
async def bal(ctx):
  await balance.invoke(ctx)


@bot.command(cooldown=cooldown)
async def top(ctx):
  with open('UserBalance.txt') as f:
    data = f.read()
  js = json.loads(data)  # nolasa informaciju to parversot dictionarya
  sortedDict = sorted(js.items(), key=lambda x: x[1], reverse=True)  # sorto
  await ctx.send(f'> **BALANCE TOP**')
  printedPeople = 0
  multilineString = ''
  for i, j in sortedDict:  ## i = name, j = balance
    if int(j) > 0 and printedPeople < 8:
      if '#' in i:
        i = i.split('#')[0]  # removes the id of the user ex asd#1513 = asd
      printedPeople += 1
      multilineString += f'''
{printedPeople}. {j}  {i}'''
  await ctx.send(formatMultilineString(multilineString, 10))


def formatMultilineString(
    string,
    field_width):  # allocates field width so all names are alligned vertically
  lines = string.split("\n")
  formatted_string = ""
  for line in lines:
    parts = line.split("  ")
    if len(parts) == 2:
      formatted_string += f"> {parts[0]:<{field_width}} {parts[1]:<{field_width}}\n"
  return formatted_string


@bot.command()
async def balance(ctx):
  BalanceCommands.checkUserInDictionary(ctx.author)
  await ctx.send('you have ' +
                 str(BalanceCommands.getUserBalance(ctx.author)) + ' credits')


@bot.command()
async def tip(ctx, member: discord.Member, *, tipAmount: int):
  if tipAmount < 1:
    await ctx.send(f"nice try nerd")
    tipAmount = -tipAmount
  userBalance = BalanceCommands.getUserBalance(ctx.author)
  if tipAmount > userBalance:
    await printMessage('you too broke for that fella, you only have ' +
                       str(userBalance) + ' credits')
    return
  else:
    BalanceCommands.updateUserBalance(member, tipAmount)
    BalanceCommands.updateUserBalance(ctx.author, -tipAmount)
    await ctx.send(
      f"<@{member.id}> has been tipped for {tipAmount} credits by <@{ctx.author.id}>."
    )


cooldowns = {}


async def get_cooldown(user_id):
  if user_id in cooldowns:
    cooldown_end = cooldowns[user_id]
    if datetime.datetime.now() < cooldown_end:
      return cooldown_end
  return None


@bot.command()
async def rob(ctx, member: discord.Member):
  randomNumber = random.randint(1, 50)
  user_cooldown = await get_cooldown(ctx.author.id)
  if user_cooldown and user_cooldown > datetime.datetime.now():
    remaining_time = user_cooldown - datetime.datetime.now()
    hours = int(remaining_time.total_seconds()) / 3600
    minutes = (remaining_time.total_seconds() / 60) - (int(hours) * 60)
    await ctx.send(
      f'you are still in the gulag for {int(hours)} hours and {int(minutes)} minutes'
    )
    return
  if BalanceCommands.getUserBalance(member) < 100:
    await ctx.send(
      f"<@{member.id}> has almost nothing to steal, shame on you <@{ctx.author.id}>!"
    )
    return
  if randomNumber > 18:
    BalanceCommands.updateUserBalance(member, -randomNumber)
    BalanceCommands.updateUserBalance(ctx.author, randomNumber)
    await ctx.send(
      f"<@{member.id}> has been robbed for {randomNumber} credits by <@{ctx.author.id}>."
    )
  else:
    await ctx.send(
      f"<@{ctx.author.id}> is being taken to the gulag for stealing ")
    cooldowns[ctx.author.id] = datetime.datetime.now() + datetime.timedelta(
      seconds=43200)

# chrome version incompatibility?
# os.environ[
#   "OPENAI_API_KEY"] = ""
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Create ChromeOptions object
# chrome_options = Options()

# # Set headless mode
# chrome_options.add_argument("--headless")

# # Create a new instance of the browser with headless option
# driver = webdriver.Chrome(options=chrome_options)

# # Navigate to Google
# driver.get("https://www.google.com/")


@bot.command()
async def chat(ctx):
  sendMessage = "Small disclaimer some of these questions might be in Latvian. " \
                "I want you to act as a stand-up comedian. " \
                "I will provide you with some topics related and you will use your wit," \
                " creativity, and observational skills to create a routine " \
                "based on those topics. You should also be sure to incorporate personal anecdotes or experiences " \
                "into the routine in order to make it more relatable and engaging for the audience. " \
                f"My first question is '{ctx.message.content}'"
  response = openai.Completion.create(
    engine="text-curie-001",  ##engine="text-davinci-003",
    prompt=sendMessage,
    max_tokens=50,
    temperature=0.7,
    n=1,
    stop=None,
    timeout=15,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
  ##await ctx.send(response.choices)
  await ctx.send(response.choices[0].text)


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  print(f'{message.content} by {message.author}')
  if "!blackjack" in message.content.lower():
    global userBet, player
    player = message.author
    BalanceCommands.checkUserInDictionary(message.author)
    splitMsg = message.content.split(' ')

    try:
      userBet = int(splitMsg[1])
    except:
      await printMessage('specify an amount ex. !blackjack 50')
      return

    if int(userBet) < 0:
      await printMessage('nice try nerd')
      return
    if userBet > BalanceCommands.getUserBalance(message.author):
      await printMessage('you too broke for that fella, you only have ' +
                         str(BalanceCommands.getUserBalance(message.author)) +
                         ' credits')
      return
    else:
      BalanceCommands.updateUserBalance(message.author, -userBet)

    global deck, dealer_cards, players, player_cards, gamestate, msg, usrBet, gState
    msg = message
    usrBet = userBet
    gState = True
    deck = BlackjackCommands.Deck()
    dealer_cards = BlackjackCommands.Hand()
    dealer_cards.addCard(deck.draw(2))
    players = [dealer_cards]
    player_cards = BlackjackCommands.Hand()
    player_cards.addCard(deck.draw(2))
    players.append(player_cards)
    gamestate = True

    if player_cards.sumCards() == 21 and len(player_cards.getCards()) == 2:
      player_sum = players[1].sumCards()
      dealer_sum = players[0].sumCards()
      if player_sum != dealer_sum or len(players[1].getCards()) != len(
          players[1].getCards()):
        gamestate = False
        userBet = userBet * 2.5
        BalanceCommands.updateUserBalance(message.author, userBet)
        await BlackjackCommands.printResult("**BLACKJACK!**", players[1],
                                            players[0], getChannel())
      else:
        gamestate = False
        BalanceCommands.updateUserBalance(message.author, userBet)
        await BlackjackCommands.printResult("**You tied!**", players[1],
                                            players[0], getChannel())

    else:
      await BlackjackCommands.printResult('', players[1], players[0],
                                          getChannel())

  await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
  global gState

  if user.bot:
    return
  # if reaction.emoji:
  #   print(f'The ID of emoji is {reaction.emoji.id}')
  if reaction.emoji == '⛔' and gState == True and player == msg.author:
    ####################DEALER CODE###################
    while players[0].not_done:
      sum = players[0].sumCards()
      if sum >= 17:
        players[0].done()
        if sum > 21:
          players[0].dealerCheckHandAceValue(players[0])

      else:
        players[0].addCard(deck.draw(1))
    #################################################
    gState = False
    player_sum = players[1].sumCards()
    dealer_sum = players[0].sumCards()
    if dealer_sum > 21 or player_sum > dealer_sum:
      userBet = usrBet * 2
      BalanceCommands.updateUserBalance(msg.author, userBet)
      await BlackjackCommands.printResult(f"> **You Won!**", players[1],
                                          players[0], getChannel())
    elif player_sum == dealer_sum:
      BalanceCommands.updateUserBalance(msg.author, usrBet)
      await BlackjackCommands.printResult("> **Tie!**", players[1], players[0],
                                          getChannel())
    elif dealer_sum > player_sum:
      await BlackjackCommands.printResult("> **You Lose!**", players[1],
                                          players[0], getChannel())
    else:
      await BlackjackCommands.printResult("> **this shouldn't happen**",
                                          players[1], players[0],
                                          getChannel())  ##1116670205763010671

  elif int(
      reaction.emoji.id
  ) == 1116670205763010671 and gState == True and player == msg.author:
    print('aaaaaa')
    players[1].addCard(deck.draw(1))
    sum = players[1].sumCards()
    if sum > 21:
      players[1].checkHandAceValue(
      )  # checks the hand for an ace and changes the ace's value from 11 -> 1
      sum = players[1].sumCards()
    if sum > 21:
      players[1].done()
      gState = False
      await BlackjackCommands.printResult("> **🚫 Bust!**", players[1],
                                          players[0], getChannel())
    elif sum == 21:  # and len(players[1].get_cards()) == 2
      gState = False
      userBet = usrBet * 2
      BalanceCommands.updateUserBalance(msg.author, userBet)
      await BlackjackCommands.printResult("> **You Win!**", players[1],
                                          players[0], getChannel())
      players[1].done()
    elif sum < 21:
      await BlackjackCommands.printResult('', players[1], players[0],
                                          getChannel())




@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))


my_secret = os.environ['TOKEN']
keep_alive()
bot.run(my_secret)
