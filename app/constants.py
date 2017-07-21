from pymongo import MongoClient
import random

client = MongoClient()
db = client.quotes
collection = db.fb_quotes

with open('data/bot_key.txt') as f:
    CLIENT_ID = f.read().strip()

KHALED_CHOICES = ["They don't want you to eat!", "Bless Up", "All Praise to the most high",
                  "Some people can't handle success...heh...I can!", "Follow me on the pathway to more success",
                  "Asahd let's hit the studio", "Asahd send me this video!", "Honey, did the Drake vocals come in yet?!?",
                  "Everything is top secret.", "Always have faith, always have hope.", "The key is to make it",
                  "Smh, they mad when you have joy...", "Key to more success is a clean heart and a clean face.",
                  "Baby, you smart! You loyal! You a genius!", "They'll try to close the door on you... Just open it.",
                  "Another one. No, another two!", "Another one.", "Cocoa Butter is the Key.",
                  "Congratulations, you played yourself.", "Don't ever play yourself.", "They don't want you to jetski, so we on the jetski",
                  "Miami finga' lickin", "Big up!"]

ZOLTAR_CHOICES = ["As I see it, yes", "It is certain", "It is decidedly so", "Most likely",
                  "Outlook good", "Signs point to yes", "Without a doubt", "Yes", "Definitely",
                  "You may rely on it", "Reply hazy, try again", "Ask again later",
                  "Better not tell you now", "Cannot predict now'", "My reply is no",
                  "Don't count on it", "Very doubtful"]
IMPLANT_TYPES = ["alpha", "beta", "gamma", "delta", "epsilon", "omega"]

QUOTE_LIST = []


# Used for validating in add_quote
class ValidationError(Exception):
    pass


class Quote(object):

    def __init__(self, ctx):
        temp = ctx.split('"')
        self.msg = temp[1]
        self.author = temp[-1]
        self.call_count = 0

    def to_dict(self):
        return self.__dict__

    def to_mongo(self):
        collection.insert(self.to_dict())


# Used by main.py to get a random quote for the !quote command #
# Gets the max size of the collection -1 and picks a quote
# at that index for use
def get_random():
    collection_max = int(db.fb_quotes.find().count())-1
    rand_index = random.randint(0, collection_max)
    return db.fb_quotes.find()[rand_index]


def print_quote():
    # Used by main.py to display a quote and increments call_count by 1
    rand_quote = get_random()
    db.fb_quotes.update_one({'_id': rand_quote['_id']}, {'$inc': {'call_count': 1}}, upsert=False)
    return rand_quote


# Validate that the given quote has quotation marks and an author
def validate_quote(msg):
    if '"' in msg:
        new = msg.split('"')
        if '-' in new[-1]:
            print('Successful Validation!')
            # Adds the quote to collection after validation success
            add_quote(msg)
            return True
        else:
            raise ValidationError('Please add an author at the end of your quote.')
    else:
        raise ValidationError('Please use quotation marks when adding a quote.')


def add_quote(msg):
    # Accepts message after validation to add to collection
    Quote(msg).to_mongo()


def get_call_count_total():
    call_total = 0
    for i in range(0, db.fb_quotes.find().count()-1):
        temp = db.milk_quotes.find()[i]
        call_total = call_total+int(temp['call_count'])
    return call_total


def convert_txt():
    with open('quotes.txt', 'r+') as f:
        for line in f:
            n = line.rstrip()
            add_quote(n)

if __name__ == "__main__":
    convert_txt()