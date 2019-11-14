# Instructions

## Prerequisites

Add your Discord Bot token in `token.txt`
Get Imgur API Credentials and add them inside `imgur_creds.txt` (First line contains `client_id` and the second line contains `client_secret`)

## Setting up all requirements

### Linux Users:

* Run: `./setup.py` (Note: You may need `sudo` priviliges to install certain packages if you haven't already)

* Finally, after running the inital setup, install all requirements using :
```
    pip3 install -r requirements.txt
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

## Running the Bot

### Options

* There can be cases where, due to slow internet connection, the Bot may need time to retreive the Webpage information. Due to this, especially in cases where you run the bot locally, you can run the program using an extra argument `slow`, i.e,

Run the program using `./stockbot.py slow`

In other cases, run:

```
./stockbot.py
```
