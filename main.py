import discord, os, requests, json, random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

client = discord.Client()
os.environ['TOKEN']


triggerPhrases = ["death","murder","die"]

triggerResponses = ["don't die","don't kill"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)

def addTrigger(trigger_message): #adds a trigger response
  if "trigger" in db.keys():
    trigger = db["trigger"]
    trigger.append(trigger_message)
    db["trigger"] = trigger
  else: 
    db["trigger"] = [trigger_message]

def deleteTrigger(index): #deletes a trigger response
  trigger = db["trigger"]
  if len(trigger) > index:
    del trigger[index]
    db["trigger"] = trigger
  
@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client)) 

@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return
  if msg.startswith("$quote"):
    quote = get_quote()
    await message.channel.send(quote)
  
  if db["responding"]:    
    options = triggerResponses
    if "trigger" in db.keys():
      options = options + db["trigger"].value
  
    if any(word in msg for word in triggerPhrases):
      await message.channel.send(random.choice(options)) 
      
  if msg.startswith("$new"):
    trigger_message = msg.split("$new ",1)[1]
    addTrigger(trigger_message)
    await message.channel.send("Trigger Response Added")

  if msg.startswith("$del"): #won't delete hardcoded responses, only those added with $new. These are NOT permanent across launches
    trigger = []
    if "trigger" in db.keys():
      index = int(msg.split("$del",1)[1])
      deleteTrigger(index)
      trigger = db["trigger"]
    await message.channel.send(trigger)

  if msg.startswith("$list"):
    trigger = []
    if "trigger" in db.keys():
      trigger = db["trigger"]
    await message.channel.send(trigger)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off")

keep_alive()      
client.run(os.environ["TOKEN"])

#OBSERVED LIST PRINTED?!