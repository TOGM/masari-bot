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
welcomeChannel = config.welcomeChannel
hourly = 3600

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

def getMarketInfo():
	embed=discord.Embed(title="CoinMarketCap", description="Market Data for Masari",color=0x0000ff, url="https://coinmarketcap.com/currencies/masari/")
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
	return embed

def getExchangeInfo():
	embed=discord.Embed(title="Prices", color=0xffd700)
	embed.set_thumbnail(url="https://get.masaricoin.com/assets/msr_goldcoin.png")
	
	#SouthXchange 
	try:
		southxchange = requests.get("https://www.southxchange.com/api/price/MSR/BTC").json()
		BTC_MSR_sx = format(southxchange['Last'],'.8f')
	except (KeyError, ValueError):
		BTC_MSR_sx = ' n/a '
		
	embed.add_field(name="SouthXchange", value="[BTC: "+str(BTC_MSR_sx)+"](https://www.southxchange.com/Market/Book/MSR/BTC)", inline=True)
	
	#Stocks.Exchange
	try:
		stocksExchange = requests.get("https://app.stocks.exchange/api2/ticker").json()
		for data in stocksExchange:
			if data['market_name'] == "MSR_BTC":
				BTC_MSR_stocks = data['last']
				#print(BTC_MSR_stocks)
				
	except (KeyError, ValueError):
		BTC_MSR_stocks = ' n/a '
	
	embed.add_field(name="Stocks.Exchange", value="[BTC: "+str(BTC_MSR_stocks)+"](https://app.stocks.exchange/en/basic-trade/pair/BTC/MSR/)", inline=True)
	
	#TradeOgre
	try:
		tradeogre = requests.get("https://tradeogre.com/api/v1/ticker/btc-msr").json()
		BTC_MSR_to = tradeogre['price']
		
	except (KeyError, ValueError):
		BTC_MSR_to = ' n/a '
	
	embed.add_field(name="TradeOgre", value="[BTC: "+str(BTC_MSR_to)+"](https://tradeogre.com/exchange/BTC-MSR)", inline=True)
	
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
	
	embed.add_field(name="Altex.Exchange", value="[BTC: "+str(BTC_MSR_altex)+"](https://altex.exchange/markets&pair=BTC_MSR)", inline=True)
	
	#Maple Change
	try:
		mapleChange = requests.get("https://maplechange.com/api/v2/tickers/msrbtc").json()
		BTC_MSR_maple = format(float(mapleChange['ticker']['last']),'.8f')
	except (KeyError, ValueError):
		BTC_MSR_maple = ' n/a '
	embed.add_field(name="Maple Change", value="[BTC: "+str(BTC_MSR_maple)+"](https://maplechange.com/markets/msrbtc)", inline=True)
	
	#Crex24
	try:
		crex24 = requests.get("https://api.crex24.com/v2/public/tickers").json()
		for data in crex24:
			if data["instrument"] == "MSR-BTC":
				BTC_MSR_crex = format(float(data['last']),'.8f')
	
	except (KeyError, ValueError):
		BTC_MSR_crex = ' n/a '
	embed.add_field(name="Crex24", value="[BTC: "+str(BTC_MSR_crex)+"](https://crex24.com/exchange/MSR-BTC)", inline=True)
	
	return embed

def getNetworkInfo():
	embed=discord.Embed(title="Network Statistics", color=0x40b862)
	embed.set_thumbnail(url="https://getmasari.org/images/Masari-Logo.png")
	networkStats = requests.get(apiUrl + "network/stats").json()
	networkHeight = networkStats["height"]
	networkDifficulty = networkStats["difficulty"]
	networkHashrate = getReadableHashRateString(int(networkStats["difficulty"])/ int(blockTargetTime))
	embed.add_field(name="Hashrate",value=str(networkHashrate), inline=True)
	embed.add_field(name="Difficulty",value=str(networkDifficulty), inline=True)
	embed.add_field(name="Last Block",value=str(networkHeight), inline=True)
	return embed

async def hourlyUpdate():
	await bot.wait_until_ready()
	while not bot.is_closed:
		if config.exchangeChannel is not "":
			exchangeChannel = discord.utils.find(lambda m: str(m.id) == str(config.exchangeChannel), bot.get_all_channels())
			exchangeEmbed = getExchangeInfo()
			await bot.send_message(exchangeChannel,embed=exchangeEmbed)
		if config.marketChannel is not "":
			marketChannel = discord.utils.find(lambda m: str(m.id) == str(config.marketChannel), bot.get_all_channels())
			marketEmbed = getMarketInfo()
			await bot.send_message(marketChannel,embed=marketEmbed)
		if config.networkChannel is not "":
			networkChannel = discord.utils.find(lambda m: str(m.id) == str(config.networkChannel), bot.get_all_channels())
			networkEmbed = getNetworkInfo()
			await bot.send_message(networkChannel,embed=networkEmbed)
		await asyncio.sleep(hourly)
	
@bot.command(pass_context=True, brief="Market Data from CMC", name='market')
async def market_CMD(ctx):
	embed = getMarketInfo()
	await bot.say(embed=embed)
	

@bot.command(pass_context=True, brief="Current price of MSR by exchange", name='price')
async def price_CMD(ctx):
	embed = getExchangeInfo()
	await bot.say(embed=embed)

@bot.command(pass_context=True, brief="Network Stats", name='network')
async def network_CMD(ctx):
	embed = getNetworkInfo()
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
	bot.loop.create_task(hourlyUpdate())

newUserMessage = """Hey there! Welcome to the Masari Discord Server!
A few things to get you started:
Frequently Asked Questions are found at #faq
Masari resources (client, pools, etc) can be found at #resources
If you need any help, check out #support or #mining
See ya around!
"""

@bot.event
async def on_member_join(member):
	await bot.send_message(member, newUserMessage)
	if config.welcomeChannel is not "":
		foundChannel = discord.utils.find(lambda m: str(m.id) == str(config.welcomeChannel), bot.get_all_channels())
		welcomeMessage = "Welcome @" + member.name + "! What brings you to Masari?"
		await bot.send_message(foundChannel, welcomeMessage)
	print("Sent message to " + member.name)

try:
  bot.run(config.discordtoken)
except KeyboardInterrupt:
  print("\nStopped")