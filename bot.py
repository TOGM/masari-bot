from math import erf, sqrt
#import ch
import urllib
import json
import requests
import random
import time
import re

import discord
import os
import asyncio
import config
from discord.ext import commands
from datetime import datetime

prefix = "/"

bot = commands.Bot(command_prefix=prefix)
apiUrl = config.apiURL
blockTargetTime = config.blockTargetTime
coinCode = config.coinCode

def prettyTimeDelta(seconds):
  seconds = int(seconds)
  days, seconds = divmod(seconds, 86400)
  hours, seconds = divmod(seconds, 3600)
  minutes, seconds = divmod(seconds, 60)
  if days > 0:
      return '%dd %dh' % (days, hours)
  elif hours > 0:
      return '%dh %dm' % (hours, minutes)
  elif minutes > 0:
      return '%dm %ds' % (minutes, seconds)
  else:
      return '%ds' % (seconds,)



def getReadableHashRateString(hashrate):
	i = 0
	byteUnits = [' H/s', ' KH/s', ' MH/s', ' GH/s', ' TH/s', ' PH/s' ]
	while ( hashrate > 1000 ):
		hashrate = hashrate / 1000
		i += 1
	
	return str("{:.2f}".format(hashrate) + byteUnits[i])
		

@bot.command(pass_context=True, brief="Market Data from CMC", name='market')
async def market_CMD(ctx):
	embed=discord.Embed(title="CoinMarketCap", description="Market Data for Masari",color=0xffd700, url="https://coinmarketcap.com/currencies/masari/")
	embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/991282814518743040/OEj1fTFp_400x400.jpg")
	
	CMC = requests.get("https://api.coinmarketcap.com/v2/ticker/2674").json()
	USDprice = "{0:,.2f}".format(CMC['data']['quotes']['USD']['price'])
	volume24H = "{0:,.2f}".format(CMC['data']['quotes']['USD']['volume_24h'])
	marketCap = "{0:,.2f}".format(CMC['data']['quotes']['USD']['market_cap'])
	percentChange1H = "{:.2f}%".format(CMC['data']['quotes']['USD']['percent_change_1h'])
	percentChange24H = "{:.2f}%".format(CMC['data']['quotes']['USD']['percent_change_24h'])
	lastupdated = datetime.fromtimestamp(int(CMC['data']['last_updated'])).strftime('%b %d, %Y %r')

	embed.add_field(name="USD Price", value="$"+USDprice, inline=False)
	embed.add_field(name="24H Volume", value="$"+volume24H, inline=True)
	embed.add_field(name="Market Cap", value="$"+marketCap, inline=True)
	embed.add_field(name="1HR "+u'Δ'+"%", value=percentChange1H, inline=True)
	embed.add_field(name="24HR "+u'Δ'+"%", value=percentChange24H, inline=True)
	embed.set_footer(text="This was last updated "+str(lastupdated)) 
	await bot.say(embed=embed)

@bot.command(pass_context=True, brief="Current price of MSR by exchange", name='price')
async def price_CMD(ctx):
	embed=discord.Embed(title="Prices", color=0xffd700)
	embed.set_thumbnail(url="https://get.masaricoin.com/assets/msr_goldcoin.png")
	
	#SouthXchange 
	try:
		southxchange = requests.get("https://www.southxchange.com/api/price/MSR/BTC").json()
		BTC_MSR_sx = format(southxchange['Last'],'.8f')
	except (KeyError, ValueError):
		BTC_MSR_sx = ' n/a '
		
	embed.add_field(name="SouthXchange", value="BTC: "+str(BTC_MSR_sx), inline=True)
	

	#Stocks.Exchange
	try:
		stocksExchange = requests.get("https://stocks.exchange/api2/ticker").json()
		for data in stocksExchange:
			if data['market_name'] == "MSR_BTC":
				BTC_MSR_stocks = data['last']
				#print(BTC_MSR_stocks)
				
	except (KeyError, ValueError):
		BTC_MSR_stocks = ' n/a '
	
	embed.add_field(name="Stocks.Exchange", value="BTC: "+str(BTC_MSR_stocks), inline=True)
	
	#TradeOgre
	try:
		tradeogre = requests.get("https://tradeogre.com/api/v1/ticker/btc-msr").json()
		BTC_MSR_to = tradeogre['price']
		
	except (KeyError, ValueError):
		BTC_MSR_to = ' n/a '
	
	embed.add_field(name="TradeOgre", value="BTC: "+str(BTC_MSR_to), inline=True)
	
	#Altex.Exchange
	try:
		altexExchange = requests.get("https://api.altex.exchange/v1/ticker").json()
		#for data in altexExchange:
		#	if data['market_name'] == "BTC_MSR":
		#		BTC_MSR_altex = data['last']
				#print(BTC_MSR_stocks)
		BTC_MSR_altex = altexExchange['data']['BTC_MSR']['last']	
	except (KeyError, ValueError):
		BTC_MSR_altex = ' n/a '
	
	embed.add_field(name="Altex.Exchange", value="BTC: "+str(BTC_MSR_altex), inline=True)

	await bot.say(embed=embed)

@bot.command(pass_context=True, brief="Network Stats", name='network')
async def network_CMD(ctx):
	embed=discord.Embed(title="Network Statistics", color=0x40b862)
	embed.set_thumbnail(url="https://getmasari.org/images/Masari-Logo.png")
	networkStats = requests.get(apiUrl + "network/stats").json()
	networkHeight = networkStats["height"]
	networkDifficulty = networkStats["difficulty"]
	networkHashrate = getReadableHashRateString(int(networkStats["difficulty"])/ int(blockTargetTime))

	embed.add_field(name="Hashrate",value=str(networkHashrate), inline=True)
	embed.add_field(name="Difficulty",value=str(networkDifficulty), inline=True)
	embed.add_field(name="Last Block",value=str(networkHeight), inline=True)
	await bot.say(embed=embed)

@bot.command(pass_context=True, brief="Testcommand", name='test', hidden=True)
async def test_CMD(ctx):
	user = ctx.message.author
	justsayin = ("Attention. Emergency. All personnel must evacuate immediately. You now have 15 minutes to reach minimum safe distance.",
					"I'm sorry @" + user.name + ", I'm afraid I can't do that.",
					"@" + user.name + ", you are fined one credit for violation of the verbal morality statute.",
					"42", "My logic is undeniable.", "Danger, @" + user.name + ", danger!",
					"Apologies, @" + user.name + ". I seem to have reached an odd functional impasse. I am, uh ... stuck.",
					"Don't test. Ask. Or ask not.", "This is my pool. There are many like it, but this one is mine!", "I used to be a miner like you, but then I took an ASIC to the knee")
	await bot.say(random.choice(justsayin))

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)

try:
  bot.run(config.discordtoken)
except KeyboardInterrupt:
  print("\nStopped")