from twitch import TwitchClient

CLIENT_ID = 'c055pgzaw9pyj8l4s346riofs4i95q'
ZLIVE_ID = 28466675

client = TwitchClient(client_id=CLIENT_ID)
zlive = client.channels.get_by_id(ZLIVE_ID)

def get_summary():
    stream = client.streams.get_stream_by_user(ZLIVE_ID)
    if stream:
        return {
            'preview': stream['preview']['large'],
            'game': stream['game'],
            'stream_type': stream['stream_type'],
            'viewers': stream['viewers'],
        }
    return None

