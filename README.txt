INSTRUCTIONS FOR RUNNING THE BOT:

To Run the Bot, there are certain requirements:
* You must have python 3.5+ installed. If not, go to https://www.python.org to download it.

* You must have Mozilla Firefox installed in your system.

* You must have a Discord Developer Account, and must have a Bot ready for this.

* Go to terminal, and type:
    "sudo pip3 install requirements.txt"

    ALTERNATIVELY, manually install these packages:
    
    sudo pip3 install selenium
    sudo pip3 install discord
    sudo pip3 install re
    sudo pip3 install pillow

* After all packages have been installed, go to your channel to test your bot.

* You must have a Developer token associated with you, for the Bot. Go to your Discord Developer Account(go to https://discordapp.com/developers/ and select your application or create one if you haven't already), and paste the Token into "token.txt"

* You must also have the client_id and client_secret from the Imgur API (Go to https://api.imgur.com/oauth2/addclient and register your application to get the credentials)

* Go to the directory containing the source code, and go to stockbot.py, and change "stock" to your Bot. Now run :
    "./stockbot.py"

    Incase this does not work, type the following commands in order:
    
    1. sudo chmod +x stockbot.py
    2. ./stockbot.py
    
    You should now be able to run this successfully

* The Bot has now started, and you can now run commands on it

PASSING COMMANDS TO THE BOT:

To pass commands, you have the command as : "!YourBOTName COUNTRY COMPANY TIME"

COUNTRY can be : 1. US -> USA (OR) 2. SG -> Singapore
COMPANY can be : "AAPL" or "Apple Inc"
(Read the full list in nyse_stocks.txt and sgx_stocks.txt)
TIME can be : 1D = Within 1 Day
              5D = 5 Days (For US ONLY)
              1W = Within 1 Week (For SG ONLY)
              1M = Within the last 1 Month
              6M = Within the last 6 months(For US ONLY)
              1Y = Within the last 1 year
              5y = Within the last 5 years

An Example Command : "!YourBOTName US AAPL 1D"
The same can be achieved by : "!YourBOTName US Apple Inc 1D"
This gives the price and the graph of the Company within the past day
