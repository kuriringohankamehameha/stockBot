# Instructions

## Prerequisites

* You must have a Developer token associated with you, for the Bot. Go to your Discord Developer Account(go to https://discordapp.com/developers/ and select your application or create one if you haven't already)

* You must also have the client_id and client_secret from the Imgur API (Go to https://api.imgur.com/oauth2/addclient and register your application to get the credentials)

Add your Discord Bot token in `token.txt`

Get Imgur API Credentials and add them inside `imgur_creds.txt` (First line contains `client_id` and the second line contains `client_secret`)

## Setting up all requirements

### Linux Users:

* Run: `./setup.py` (Note: You may need `sudo` priviliges to install certain packages if you haven't already)

* Finally, after running the inital setup, install all requirements using :
```
    pip3 install -r requirements.txt
```

* Make the script executable using :
```
chmod +x stockbot.py
```

### Mac Users:

Install the required packages using MacPorts/Homebrew:

* Firefox
* Python3
* Pypy for Python3

* Finally, after running the inital setup, install all requirements using :
```
    pip3 install -r requirements.txt
```

* Make the script executable using :
```
chmod +x stockbot.py
```

## Running the Bot

### Options

* There can be cases where, due to slow internet connection, the Bot may need time to retreive the Webpage information. Due to this, especially in cases where you run the bot locally, you can run the program using an extra argument `slow`, i.e,

Run the program using `./stockbot.py slow`

In other cases, run:

```
./stockbot.py
```

* The Bot has now started, and you can now run commands on it

### Passing Commands to the Bot:

* To pass commands, you have the command as : "!YourBOTName COUNTRY COMPANY TIME"

* COUNTRY can be : 1. US -> USA (OR) 2. SG -> Singapore

* COMPANY can be : "AAPL" or "Apple Inc" (Read the full list in nyse_stocks.txt and sgx_stocks.txt)

TIME can be : 
* 1D = Within 1 Days </br>
* 5D = 5 Days (For US ONLY) </br>
* 1W = Within 1 Week (For SG ONLY) </br>
* 1M = Within the last 1 Month </br>
* 6M = Within the last 6 months(For US ONLY) </br>
* 1Y = Within the last 1 year </br>
* 5y = Within the last 5 years </br>

An Example Command : "!YourBOTName US AAPL 1D"
The same can be achieved by : "!YourBOTName US Apple Inc 1D"
This gives the price and the graph of the Company within the past day
