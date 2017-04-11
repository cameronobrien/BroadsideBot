import discord
import logging
import sqlite3
import os
import urllib.request
import re
from discord.ext.commands import Bot
from random import randint, choice
from requests import get
from bs4 import BeautifulSoup as BS
from app.constants import CLIENT_ID, KHALED_CHOICES, ZOLTAR_CHOICES


my_bot = Bot(command_prefix="!")


@my_bot.event
async def on_read():
    print("Client logged in")


@my_bot.command()
async def hello():
    """
    Test command to ensure the bot is working
    Example: !hello
    """
    return await my_bot.say("Hi team!")


@my_bot.command()
async def question():
    """
    Ask a yes or no question and receive an answer to it.
    Example: !question Does she love me?
    """
    return await my_bot.say(choice(ZOLTAR_CHOICES))


@my_bot.command()
async def roll():
    """
    Roll a die which results somewhere between 1-100
    Example: !roll
    """
    return await my_bot.say(randint(1, 100))


@my_bot.command()
async def yt(args):
    """
    Get the first Youtube search result video
    Example: !yt how do I take a screenshot
    """

    if not args:
        return await my_bot.say("Empty search terms")

    enc_search = '+'.join(args.split())
    print(enc_search)
    url = f"https://www.youtube.com/results?search_query={enc_search}"
    resp = get(url)
    if resp.status_code != 200:
        return await my_bot.say("Failed to retrieve search")

    # Build a BS parser and find all Youtube links on the page
    bs = BS(resp.text, "html.parser")
    items = bs.find("div", id="results").find_all("div", class_="yt-lockup-content")
    if not items:
        return await my_bot.say("No videos found")

    # Construct an easy list of URLs
    links = []
    for i in items:
        try:
            links.append(i.find("a", class_="yt-uix-sessionlink")["href"])
        except TypeError:  # i.find() returned None
            return await my_bot.say("Was unable to find results for this query. Sorry!")

    hrefs = []
    for u in links:
        if u.startswith("/watch"):
            hrefs.append(u)

    # Check if we have any at all
    if not hrefs:
        return await my_bot.say("No URLs found (? wat)")

    # Finish by sending the URL out
    return await my_bot.say(f"https://www.youtube.com{hrefs[0]}")


@my_bot.command()
async def spam(args):
    """
    Spam a channel with dumb things
    Example: !spam :ok_hand:
    """

    if not args or len(args) > 25:
        return await my_bot.say("Invalid spam input")

    y = args * randint(5, 20)
    return await my_bot.say(f"{''.join(y)}")


@my_bot.command()
async def blessup():
    """
    Recite a DJ Khaled quote
    Example: !blessup
    """
    return await my_bot.say(choice(KHALED_CHOICES))


@my_bot.command()
async def getprice(msg):

    EVECENTRAL = "http://api.eve-central.com/api/marketstat?typeid=%s&regionlimit=10000002"
    EVESTATICDATADUMP = "data/sqlite-latest.sqlite"

    if os.path.isfile(os.path.expanduser(EVESTATICDATADUMP)):
        conn = sqlite3.connect(os.path.expanduser(EVESTATICDATADUMP))
    else:
        conn = None

    def get_type_id(name):
        c = conn.cursor()
        c.execute("select typeName, typeID from invTypes where typeName = '{0}%' collate nocase;".format(name))
        result = c.fetchone()
        if result:
            return result
        c.execute("select typeName, typeID from invTypes where typeName like '%{0}%' collate nocase;".format(name))
        results = c.fetchall()
        if len(results) == 0:
            return None
        results = sorted(results, key=lambda x: len(x[0]))
        print(results[0])
        return results[0]

    def item_to_price(item):
        try:
            result = get_type_id(item)
            assert result
            item = result[0]
            url = EVECENTRAL % result[1]
            print(url)
            soup = BS(urllib.request.urlopen(url), "html.parser")
            price = str(soup.find("sell").min)
            removetags = re.compile("<(.|\n)*?>")
            price = removetags.sub("", price)
            price = float(price)
            if price == 0:
                raise ZeroDivisionError
            import locale
            locale.setlocale(locale.LC_ALL, "")
            formatted_price = locale.format('%d', price, True)
            return item, formatted_price, price
        except Exception as e:
            return None, None, None

    if not conn:
        return await my_bot.say("EVE static data dump not loaded")
    term = msg.replace("!getprice ", "")
    try:
        item, formatted_price, price = item_to_price(term)
        print("%s :  %s ISK" % (item, formatted_price))
        return await my_bot.say("%s :  %s ISK" % (item, formatted_price))
    except Exception as e:
        return await my_bot.say("Unable to find search item")


my_bot.run(CLIENT_ID)
