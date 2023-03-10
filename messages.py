WelcomeMessage = '''Hello, <b>{name}</b>!
I am MatchMate ð¤ - a bot that helps people to find each other!

Privately submit a Telegram handle of a person, and when they decide to submit yours - you both will be notified about the match â¤ï¸âð¥

Now, type and send the handle of a person with @ symbol
â° Be accurate, because you will be able to change it only in 24 hours!

âï¸Your matches are stored in a hashed and undecryptable form
'''
AliasError = '''â¼ï¸ Wrong alias!
You have either tried to add yourself, or forgot the @ symbol!

Now try again.
'''

Throttle = '''â° You have submitted another alias too soon!

You should wait for at least 24 hours before submitting another alias!
'''
FirstlyRemove = '''âï¸ You cannot have two matches submitted on the same time!

No, I cannot simply remove previous alias by myself - because it's encrypted!

Please, use the /unmatch @alias
'''

Match = '''OMG, it's a match!!! â¤ï¸âð¥â¤ï¸âð¥â¤ï¸âð¥
@{alias} has picked you as their match as well!
'''
MatchMessageToAnotherPerson = '''OMG, it's a match!!! â¤ï¸âð¥â¤ï¸âð¥â¤ï¸âð¥
@{alias} has picked you as their match as well!
'''
MatchPending = '''Your match has been saved successfully

Now we should wait. If they decide to submit your handle - both of you will be messaged'''

NoMatchesDuringRemove = '''You don't seem to be having any matches right now...
Try to submit a new one!
'''
MatchRemoved = ''' ð¾ Match successfully removed.

Now you can submit another person's handle'''

MatchNotFound = '''Match not found. You should submit previous alias.'''

NoAlias = '''âï¸ You do not seem to have an alias!

I won't be able to match you with anyone!

Add an alias to your Telegram account and come back, I will wait!
'''

UnmatchUsage = '''ð Type "/unmatch @(Alias of your current match)" to delete your current match!
'''