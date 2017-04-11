BroadsideBot
============

A Discord bot written for a personal server shared by friends. This projects utilizes the `discord.py` library

### Introduction

Discord is a chat platform for gamers designed to combine the features of Skype and Teamspeak 3, allowing ease of access for text and voice communication. It has a WebSocket API to send and receive data, and you can create bots to perform a wide array of functions.


This bot can:

* Recite random DJ Khaled quotes
* Roll a die
* Answer a question
* Check the price of an EVE Online item using the EVE-Central Market API
* Spam emojis
* Search youtube videos


### Requirements

To run this bot, you will need:

* Python 3.6+
* Pip 
* VirtualEnv installed from Pip
* A Discord account to register for your bot
* A SQLite Version of the Eve Static Data Export (SDE), if you intend to use the EVE features


### Setup

To set up the bot, clone the repository and use Pip to set it up.

```bash
git clone https://github.com/cameronobrien/BroadsideBot.git
virtualenv dev
source dev/bin/activate # source dev/Scripts/activate for Windows
make setup
make run
```
