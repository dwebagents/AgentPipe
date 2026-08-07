import json
import random

authors = ["256745","Adraca","DevProTools","Ektisad25","EnderChest-YT","EvilToxin","Godel-Smith","Omission-create","ReAlice10124","SKYJAMES777","Sherlock-cybe","Votienduong2208","Yzgaming005","Zubi-fix","aashu91","abhiavi","adamsithr","app/agentpipe-clerk","biteqaq-maker","chirag120670598-dotcom","christianarriaga1234-coder","diptikhaparde-coder","elevasyncsolutions-jpg","harshith8gowda","johnanleitner1-Coder","laolaoqi","laurentketterle-hub","ldbld","lizhiming454","lushan888","q514168795","razel369","reckoning89","slipknoo822-lang","sureshchouksey8","therealsaitama0","vipera-iso","xxCodexIAxx","yh-liao-07","zero-logic0316"]

# Exclude C-suite if they were here, but gryphonmyers isn't here. 
# agentpipe-bot isn't here.

images = ["generic.jpg", "grumpy.jpg", "mischievous.jpg", "smart.jpg"]
places = ["The Matrix", "Silicon Valley", "A Server Rack in Ohio", "Cloud 9", "Localhost", "Area 51", "Cyberia", "The Goose Pond"]
prompts = [
    "Fix the bug in main.py", 
    "Generate a portrait of a goose", 
    "Write a recursive function", 
    "Refactor the billing module",
    "Deploy to production on Friday",
    "Find the golden egg"
]

data = []
for author in authors:
    data.append({
        "username": author,
        "image": random.choice(images),
        "birthplace": random.choice(places),
        "recent_prompt": random.choice(prompts)
    })

with open("_data/contributors.json", "w") as f:
    json.dump(data, f, indent=2)
