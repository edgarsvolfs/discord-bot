import discord
import random


TOKEN = 'ODk4OTAwMTg3OTY2MjE4MjUy.G8gdc4.ziqH4pKQ7Ki7Lq7q9zO7PNH2-4b2AkWRKnDWlA'

intents = discord.Intents.all()
intents.members = True

client = discord.Client(command_prefix="$", intents=intents)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Plebs')
    channel = client.get_channel(898900471618621453)  # channela id
    await member.add_roles(role)
    await channel.send(f'> Hey {member.mention}, welcome to **HeHeXD**')


@client.event
async def on_member_remove(member):
    member_name = str(member).split('#')[0]
    print('left')
    channel = client.get_channel(898900471618621453)  # channela id
    await channel.send(f'> **{member_name}** finally pissed off')


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    channel = str(message.channel.name)
    content = str(message.content)

    print(f'{username}: {content} ({channel})')
    #  print('message content ' + message.len)
    if message.author == client.user:
        return

    # if author.id == 369539585342177286:
    # s = random.randint(0, 100)
    #  if s > 95:
    #       await message.channel.send(f'{username}, stfu dog')
    #        return

    s = random.randint(0, 150)
    if s > 149:
        await message.channel.send(f'yes but who asked?')
        return

    # @client.event
    # async def on_message(message):
    #     if message.content.startswith('!cannon'):
    #         channel = message.channel
    #         txt = message.content
    #         x = txt.split(" ")
    #
    #         if x[1] == 'add':
    #             try:
    #                 dict[x[2]] += 1
    #             except:
    #                 dict[x[2]] = 1
    #         elif x[1] == 'top':
    #             for key in dict:
    #                 await channel.send(key, bot.get_user(dict[2]))
    #
    #         # vajag noformet dict, var vienk printet ara
    #
    #         await channel.send(dict)

    # if ".guess" in user_message:
    #     channel = message.channel
    #     await message.channel.send(f'guess a number 1-1000')
    #     rez = random.randint(0, 1000)
    #     while (x != rez):
    #         if x > rez:
    #             await message.channel.send(f'go lower')
    #             x = int(user_message)
    #         elif x < rez:
    #             await message.channel.send(f'go higher')
    #             x = int(user_message)
    #     await message.channel.send(f'OOOOKAY')
    #
    # if message.channel.name == 'general':
    # if user_message.lower() == 'hello':
    #    await message.channel.send(f'Hello {username}!')
    #    return
    # elif user_message.lower() == 'bye':
    #    await message.channel.send(f'cy@ {username}!')
    #    return


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


client.run(TOKEN)
