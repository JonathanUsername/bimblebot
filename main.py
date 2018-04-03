import asyncio
import logging
import os
import random

import discord

from consts import VIEWER_DESCRIPTORS, SUMMONING_RESPONSES
from twitch_utils import get_summary

token = os.environ['CLIENT_TOKEN']

logging.basicConfig(level=logging.INFO)

client = discord.Client()


@client.event
async def on_ready():
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!namegame'):
        author = message.author

        def check(msg):
            return author.name in msg.content

        await client.send_message(message.channel, "What's your name?")
        await client.wait_for_message(author=author, check=check)
        await client.send_message(message.channel, 'Correct.')
    elif message.content.startswith('!random'):
        user = get_random_present_member(message.server)
        ret = random.choice(SUMMONING_RESPONSES).format(user.name)
        await client.send_message(message.channel, ret)
    elif message.content.startswith('!badzoot'):
        await play_sound_for_message(message, 'badzoot')
    elif message.content.startswith('!crackfox'):
        await play_sound_for_message(message, 'crackfox')
    elif message.content.startswith('!laurence'):
        await play_sound_for_message(message, 'laurence')
    elif message.content.startswith('!slink'):
        await play_sound_for_message(message, 'slink')
    elif message.content.startswith('!zlive'):
        summary = get_summary()
        if summary:
            e = discord.Embed()
            e.set_image(url=summary['preview'])
            content = "Zoot is playing {} ({}) and {} {} are watching him do it."
            formatted = content.format(
                summary['game'],
                summary['stream_type'],
                summary['viewers'],
                random.choice(VIEWER_DESCRIPTORS)
            )
            await client.send_message(message.channel, formatted, embed=e)
        else:
            await client.send_message(message.channel, "Zoot is not streaming right now.")

async def play_sound_for_message(message, sound):
    author = message.author
    voice_channel = author.voice_channel
    bot_voice = client.user.voice
    if bot_voice:
        if bot_voice.voice_channel != voice_channel:
            vc = await client.join_voice_channel(voice_channel)
        else:
            vc = bot_voice.voice_channel
    audio_path = "audio/{}.mp3".format(sound)
    player = vc.create_ffmpeg_player(audio_path)
    player.start()

def get_random_present_member(server):
    valid_statuses = [discord.Status.online]
    online_members = [m for m in server.members if m.status in valid_statuses and not m.bot]
    return random.choice(online_members)


client.run(token)
