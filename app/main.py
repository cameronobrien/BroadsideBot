import discord
import logging
from discord.ext.commands import Bot
from random import randint, choice
from requests import get
from bs4 import BeautifulSoup as BS
import urllib.parse
my_bot = Bot(command_prefix="!")


@my_bot.event
async def on_read():
    print("Client logged in")


@my_bot.command()
async def hello(*args):
    return await my_bot.say("Hi team!")


@my_bot.command()
async def istimgay(*args):
    return await my_bot.say(choice(["Yes.", "No."]))


@my_bot.command()
async def roll(*args):
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

    if not args or len(args) > 10:
        return await my_bot.say("Invalid spam input")

    y = args * randint(5, 20)
    return await my_bot.say(f"{''.join(y)}")


my_bot.run("MzAwNzQxNjQ4OTAyNzgyOTc3.C8w3Og.bcqIDv5WeKzOXAyzbnl0WKLuP4Y")



