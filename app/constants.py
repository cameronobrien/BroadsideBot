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
                  "Miami finga' lickin", "Big up!","All I do is WIN, WIN, WIN no matter what","I remember when I ain’t have a jacuzzi","Watch your back, but more importantly when you get out the shower, dry your back. It’s a cold world out there.","Be a star. Be a Superstar","Almond milk + cinnamon crunch = major key to success.","The key is to enjoy life, because they don’t want you to enjoy life.","To succeed, you must believe. When you believe, you will succeed.","In life everyone has a choice. The key is: make a right choice.","We have to get money. We have no choice. It cost money to eat.","The key is: never fold."]

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


# Quotes #
# Open quotes.txt and read the contents into quote_list
def update_quotes():
    with open('quotes.txt', 'r') as f:
        for line in f:
            line.rstrip('\n')
            QUOTE_LIST.append(line)


def add_quote(msg):
    # Validate that the given quote has quotation marks and an author
    if '"' in msg:
        newMsg = msg.split('"')
        if '-' in newMsg[len(newMsg)-1]:
            # Write the quote to quotes.txt and strip the !add prefix
            with open('quotes.txt', 'a') as f:
                f.write('\n')
                for i in range(1, len(newMsg)):
                    f.write(newMsg[i] + " ")
            update_quotes()
            return True
        else:
            raise ValidationError('Please add an author at the end of your quote.')
    else:
        raise ValidationError('Please use quotation marks when adding a quote.')

