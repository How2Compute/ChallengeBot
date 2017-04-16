import sys
import datetime
import discord
import asyncio
import os
import json
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from commandHandler import CommandHandler
from submission_obj import Submission

# Create the discord client
client = discord.Client()
# Create the command handler
handler = CommandHandler(client)

# Setup the SQLAlchemy connection
Base = declarative_base()
engine = create_engine('sqlite:///challangeBot.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# (attempts to) read the json configuration file.
def getConfig():
    # Default the config to None
    config = None
    try:
        # Attempt to read the json
        with open('challangeConfig.conf') as configFile:
            config = json.load(configFile)
    except:
        # If it couldn't open the file or some other error occured
        return None
    # As it didn't catch any errors, return the json
    return config

# Create a dict to house all the information about a command event
def EventData(channel, author, args):
    return {
    "config": getConfig(),
    "db": session,
    "channel": channel,
    "author": author,
    "args": args
    }

# Log some debug data once it's started up
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Gets called whenever a message is sent.
@client.event
async def on_message(message):
    # Create the parameters to later pass into a command (if required)
    args = message.content.split()
    eventData = EventData(message.channel, message.author, args)
    # Setup the bot
    if message.content.startswith('!setup'):
        await handler.setup(eventData)

    elif message.content.startswith('!submit'):
        await handler.submit(eventData)

    elif message.content.startswith('!submissions'):
        await handler.submissions(eventData)

# Start the client and authenticate it with it's token
client.run('<YOUR TOKEN HERE>')
