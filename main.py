import discord
import asyncio
import yaml
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    with open(".secrets.yaml", 'r') as data:
        try:
            print(yaml.safe_load(data))
        except yaml.YAMLError as exc:
            print(exc)

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')


with open(".secrets.yaml", 'r') as data:
    secrets = yaml.safe_load(data)
    client.run(secrets['token'])
