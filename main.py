import asyncio
import logging
import os
import random

import discord

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
        await client.send_message(message.channel, 'Hello')
    elif message.content.startswith('!namegame'):
        author = message.author

        def check(msg):
            return author.name in msg.content

        await client.send_message(message.channel, "What's your name?")
        await client.wait_for_message(author=author, check=check)
        await client.send_message(message.channel, 'Correct.')
    elif message.content.startswith('!random'):
        user = get_random_present_member(message.server)
        responses = [
            'Come forward, {}',
            'I choose you, {}',
            'Make me proud, {}',
            'You deserve another go, {}',
            'Despite my better judgement, it has to be {}',
            "What's that coming over the hill, is it a monster?? Oh no it's {}",
            "Safe clart, you knows it's gorra be {}. Tidy.",
            "{}!! YEAAAAAAAHHHHHH!!111two",
            "{}ybaby",
        ]
        ret = random.choice(responses).format(user.name)
        await client.send_message(message.channel, ret)


def get_random_present_member(server):
    valid_statuses = [discord.Status.online]
    online_members = [m for m in server.members if m.status in valid_statuses and not m.bot]
    return random.choice(online_members)


client.run(token)
