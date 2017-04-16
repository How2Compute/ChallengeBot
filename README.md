# ChallengeBot
A shitty, half finished discord bot made for submittable challenges. Designed to work on docker &amp; Uses SQLAlchemy + discord.py
# Commands
### !setup
Usage: !setup #channel ShouldClear(true/false)
### !submit
Usage: !submit <github url> (optional) <additional notes>
### !submissions
Usage: !submissions (optional) <users id>

## This bot has not (yet) been fully implmeneted, and what was implemented was implemented was implemented by a newbie. Use at your own risk!

# TODO
- Make setup restricted to only roles & make it work with #channel (instead of only channel, which it currently does)
- Port submit over to accept more than 3 arguements as currently it won't accept over a word
- Make submissions convert username -> id
- Implement create challenge function
- Implement stop challenge function
