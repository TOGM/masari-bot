# Discord (Chum) Bot for Masari
This is a python bot I've created for Masari. Current implentation requires to connect to a Nodejs-pool API. 

Features Include:
* Welcomes new users to the server.
* Network Statistics
* Exchange prices (pairings)
* Market Info (provided by CoinMarketCap)

You can always use !help to get more information or find more commands. 

Setup Instructions
===================
You will need:
* Discord token 
* Client ID of your App
* Server ID
* Channel ID

Create a Bot
-------------
1. Go to https://discordapp.com/developers
2. Select **My APPS**, then **New App**
3. Set **APP NAME** and then **Create App**
4. Go to the **Bot** Section and select **CREATE A BOT USER**

Add Bot to Discord Server
-------------
Inside of your new app under **APP DETAILS** Section, you will find the CLIENT ID.

Plug your client ID into the following link to add the bot to the Discord Server:
``` 
https://discordapp.com/api/oauth2/authorize?client_id=[CLIENT_ID]&scope=bot&permissions=0
```
*Note: You will need to be signed in to Discord and have Manage Roles permission to the Server*


Support me by mining at https://get.masaricoin.com
