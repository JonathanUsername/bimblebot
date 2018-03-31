import discord
import asyncio
import logging
import os
import random

token = os.environ['CLIENT_TOKEN']

logging.basicConfig(level=logging.INFO)

client = discord.Client()
server = discord.Server()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel,
                                        'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!namegame'):
        author = message.author

        def check(msg):
            return author.name in msg.content

        await client.send_message(message.channel, "What's your name?")
        await client.wait_for_message(author=author, check=check)
        await client.send_message(message.channel, 'Correct.')
    elif message.content.startswith('!random'):
        valid_statuses = [discord.Status.online, discord.Status.idle]
        online_members = [
            m for m in server.get_all_members() if m.status in valid_statuses
        ]
        return random.choice(online_members)


client.run(token)
