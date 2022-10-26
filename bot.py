import discord
import random


TOKEN = ''  # insert token

intents = discord.Intents.all()
intents.members = True

client = discord.Client(command_prefix="$", intents=intents)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Plebs')
    channel = client.get_channel(401071542110388257)  # channela id
    await member.add_roles(role)
    await channel.send(f'> Hey {member.mention}, welcome to **HeHeXD**')


@client.event
async def on_member_remove(member):
    member_name = str(member).split('#')[0]
    print('left')
    channel = client.get_channel(401071542110388257)  # channela id
    await channel.send(f'> **{member_name}** finally pissed off')


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    channel = str(message.channel.name)
    content = str(message.content)

    print(f'{username}: {content} ({channel})')

    if message.author == client.user:
        return

    s = random.randint(0, 500)
    if s > 499:
        await message.channel.send(f'yes but who asked?')
        return

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


client.run(TOKEN)
