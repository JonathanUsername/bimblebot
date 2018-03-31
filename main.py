import discord
import asyncio
import logging
import os

token = os.environ['CLIENT_TOKEN']

logging.basicConfig(level=logging.INFO)

client = discord.Client()


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
        tmp = await client.send_message(message.channel, 'Calculating messages...')
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


client.run(token)
