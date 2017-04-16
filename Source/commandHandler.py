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
from sqlalchemy.orm import sessionmaker

from submission_obj import Submission
# *private* class to house helpers such as formatters etc
class _Helpers():
    def formatConfig(self, channel_id, challenge_active, challenge_id, challenge_description):
        return { "setup": True,
            "channel_id": channel_id,
            "challenge_active": challenge_active,
            "challenge_id": challenge_id,
            "challenge_description": challenge_description
        }

    def formatSubmission(self, submission):
        if submission.notes == None:
            return "**Challange ID**: {}\n**User ID**: {}\n**URL**: {}".format(submision.challange_id, submission.user_id, submission.url)
        else:
            return "**Challange ID**: {}\n**User ID**: {}\n**URL**: {}\n**Additional Notes**:()".format(submission.challange_id, submission.user_id, submission.url, submission.notes)


# A class to handle the bots' commands
class CommandHandler():
    def __init__(self, client):
        self.client = client
        self.helpers = _Helpers()

    # An asyncronous function to create the bot it's configuration file
    async def setup(self, eventData):
        # TODO roles and look at channel_mentions (of the message)
        if len(eventData["args"]) == 3:
            if eventData["args"][2][0] == 't' or eventData["args"][2][0] == 'T' or eventData["args"][2][0] == 'f' or eventData["args"][2][0] == 'F':
                tmp = await self.client.send_message(eventData["channel"], 'Setting up...')
                # If it should reset the database
                if eventData["args"][2][0] == 't' or eventData["args"][2][0] == 'T':
                    eventData["db"].query(Submission).delete()

                channelId = None
                # Go over all the channels and match it by name
                for channel in self.client.get_all_channels():
                    # Is this channels name (with or without a #) the same?
                    if channel.name == eventData["args"][1] or "#{}".format(channel.name) == eventData["args"][1]:
                        # Save this channels id and exit
                        channelId = channel.id
                        break
                if channelId == None:
                    await self.client.edit_message(tmp, "Could not find channel({})! (bug, try the channel name without the #)".format(eventData["args"][1]))
                else:
                    # Format and save the config
                    with open('challangeConfig.conf', 'w') as outfile:
                        format_dict = self.helpers.formatConfig(channelId, False, -1, "No challenge active!")
                        json.dump(format_dict, outfile)

                    # Show it as successfully set up!
                    await self.client.edit_message(tmp, "Successfully setup ChallangeBot in {}".format(eventData["args"][1]))
            else:
                await self.client.send_message(eventData["channel"], "Usage: !setup #channel ShouldClear(true/false)")
        else:
            await self.client.send_message(eventData["channel"], "Usage: !setup #channel ShouldClear(true/false)")
    # An asyncronous function to let the user submit their entry
    async def submit(self, eventData):
        # Has the bot already been set up?
        if eventData["config"] == None or eventData["config"]["setup"] == False:
            await self.client.send_message(eventData["channel"], 'A moderator needs to set this bot up first! Use !setup for more information.')
            return None
        # Was a valid amount of arguements provided? TODO work with longer messages too
        if(len(eventData["args"]) != 2 and len(eventData["args"]) != 3):
            await self.client.send_message(eventData["channel"], "Usage: !submit <github url> (optional) <additional notes>")
            return None
        # Is there an active challenge the user can submit to?
        if eventData["config"]["challenge_active"] == False:
            await self.client.send_message(eventData["channel"], "There isn't currently a challenge active!")
            return None

        # Show the user it's bussy submitting...
        tmp = await self.client.send_message(eventData["channel"], 'Submitting...')

        if "github.com" not in eventData["args"][1]:
            # "Invalid" url! User should have uploaded to a github repository
            await self.client.edit_message(tmp, "Please upload your submission a http://github.com repository!")
            return None
        if len(eventData["args"]) == 2:
            submission = Submission(123, eventData["author"].id, eventData["args"][1])
            eventData["db"].add(submission)
            eventData["db"].commit()
        elif len(eventData["args"]) == 3:
            submission = Submission(123, eventData["author"].id, eventData["args"][1], eventData["args"][2])
            eventData["db"].add(submission)
            eventData["db"].commit()
        else:
            # Wait how did it get here?
            await self.client.edit_message(tmp, "Unknown error, please contact an admin!")
        # Show the user it was successfully submitted
        await self.client.edit_message(tmp, "Successfully submitted")
    # An asyncronous function to handle the listing of submissions
    async def submissions(self, eventData):
        # Has the bot already been set up?
        if eventData["config"] == None or eventData["config"]["setup"] == False:
            await self.client.send_message(eventData["channel"], 'A moderator needs to set this bot up first! Use !setup for more information.')
            return None
        else:
            # Should it print the submissions for a specific user?
            if len(eventData["args"]) == 2:
                # Get all the users's submissions. TODO make name -> id
                row = eventData["db"].query(Submission).filter_by(user_id=eventData["args"][1]).first()
                # Could not find the user/any submissions of the user
                if row is None:
                    await self.client.send_message(eventData["channel"], 'Could not find user {} or the user did not submit anything yet!'.format(eventData["args"][1]))
                else:
                    # Format and show the users' latest submission
                    _submission = self.helpers.formatSubmission(rows[0])
                    await self.client.send_message(eventData["channel"], '**Last Submission by {}:**\n{}'.format(eventData["args"][1], _submission))
            else:
                # Get all the entries for this challange
                rows = eventData["db"].query(Submission).filter_by(challange_id=eventData['config']['challenge_id'])
                # Print all the submissions one by one
                for row in rows:
                    _submission = self.helpers.formatSubmission(row)
                    await self.client.send_message(eventData["channel"], '{}'.format(_submission))
