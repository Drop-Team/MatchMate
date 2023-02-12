WelcomeMessage = '''Hello, <b>{name}</b>!
I am MatchMate 🤖 - a bot that helps people to find each other!

Privately submit a Telegram handle of a person, and when they decide to submit yours - you both will be notified about the match ❤️‍🔥

Now, type and send the handle of a person with @ symbol
⏰ Be accurate, because you will be able to change it only in 24 hours!

❗️Your matches are stored in a hashed and undecryptable form
'''
AliasError = '''‼️ Wrong alias!
You have either tried to add yourself, or forgot the @ symbol!

Now try again.
'''

Throttle = '''⏰ You have submitted another alias too soon!

You should wait for at least 24 hours before submitting another alias!
'''
FirstlyRemove = '''✏️ You cannot have two matches submitted on the same time!

No, I cannot simply remove your previous alias by myself - because it's encrypted!

Please, use the /unmatch command and follow its instructions to remove your current match!
'''

Match = '''OMG, it's a match!!! ❤️‍🔥❤️‍🔥❤️‍🔥
@{alias} has picked you as their match as well!
'''
MatchMessageToAnotherPerson = '''OMG, it's a match!!! ❤️‍🔥❤️‍🔥❤️‍🔥
@{alias} has picked you as their match as well!
'''
MatchPending = '''Your match has been saved successfully

Now we should wait. If they decide to submit your handle - both of you will be messaged'''

NoMatchesDuringRemove = '''You don't seem to be having any matches right now...
Try to submit a new one!
'''
MatchRemoved = ''' 💾 Match successfully removed.

Now you can submit another person's handle'''

NoAlias = '''⁉️ You do not seem to have an alias!

I won't be able to match you with anyone!

Add an alias to your Telegram account and come back, I will wait!
'''

UnmatchUsage = '''📖 Type "/unmatch @(Alias of your current match)" to delete your current match!
'''