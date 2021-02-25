from webbot import Browser 
from bs4 import BeautifulSoup
import time
import discord
import sys

TOKEN = ''
client = discord.Client()
@client.event
async def on_ready():
	await client.change_presence(activity = discord.Game('th!help'))



@client.event
async def on_message(message):
	if message.content == "th!help":
		await message.channel.send("Use th!workout to get todays workout! Please note that it may take a while for the workout to be sent after the command")
	if message.content == "th!workout":
		global pretext
		global insactive
		global flexactive
		global h5active
		global iactive
		global cellactive
		global headactive
		global hactive
		url = 'https://athlete.trainheroic.com/#/login?redirectUrl=https%253A%252F%252Fathlete.trainheroic.com%252F%2523%252Ftraining'
		web = Browser()
		web.go_to(url)
		web.type('@gmail.com' , into='Email')
		web.type('' , into='Password' , id='passwordFieldId')
		web.click('Log in' , tag='span')
		time.sleep(3)
		pretext = ''
		text = ''
		insactive = False
		flexactive = False
		h5active = False
		iactive = False
		cellactive = False
		headactive = False
		hactive = False
		textlist = []
		def textgrab(start, end, funactive):
			global pretext
			global insactive
			global flexactive
			global h5active
			global iactive
			global cellactive
			global headactive
			global hactive
			if webtext[i+len(start)-1:i+len(start)+len(end)-1] == end and funactive:
				if start == '<p flex="" class="instruction flex">':
					textlist.append([pretext, 'flex'])
					pretext = ''
					flexactive = False
				if start == '<p class="instruction">':
					textlist.append([pretext, 'ins'])
					pretext = ''
					insactive = False
				if start == '<h5>':
					textlist.append([pretext, 'h5'])
					pretext = ''
					h5active = False
				if start == '<i class="icon icon-barbell combo-title-icon"></i>':
					pretext = pretext[:-1] + '\n' + pretext[-1:]				
					textlist.append([pretext, 'i'])
					pretext = ''
					iactive = False
				if start == 'cell" aria-hidden="false">':
					textlist.append([pretext, 'cell'])
					pretext = ''
					cellactive = False
				if start == 'class="header ng-hide" aria-hidden="true">':
					textlist.append([pretext, 'head'])
					pretext = ''
					headactive = False
				if start == 'class="header" aria-hidden="false">':
					textlist.append([pretext, 'head'])
					pretext = ''
					hactive = False
				return False


			if funactive or webtext[i:i+len(start)] == start:
				if start == '<h5>':
					h5active = True
				if start == '<p flex="" class="instruction flex">':
					flexactive = True
				if start == '<p class="instruction">':
					insactive = True
				if start == '<i class="icon icon-barbell combo-title-icon"></i>':
					iactive = True
				if start == 'cell" aria-hidden="false">':
					cellactive = True
				if start == 'class="header ng-hide" aria-hidden="true">':
					headactive = True
				if start == 'class="header" aria-hidden="false">':
					hactive = True
				pretext += webtext[i+len(start)]

				return True
			else:
				return False

		webtext = web.get_page_source()


		for i in range(len(webtext) - 24):
			textgrab('<p class="instruction">', '</p>', insactive)
			textgrab('<p flex="" class="instruction flex">', '</p>', flexactive)
			textgrab('<h5>', '</h5>', h5active)
			textgrab('<i class="icon icon-barbell combo-title-icon"></i>', '</div>', iactive)
			textgrab('cell" aria-hidden="false">', '</div>', cellactive)
			textgrab('class="header ng-hide" aria-hidden="true">', '</div>', headactive)
			textgrab('class="header" aria-hidden="false">', '</div>', hactive)

		def divide_chunks(l, n): 
			for i in range(0, len(l), n):  
				yield l[i:i + n]

		
		newtextlist = []
		newnewtextlist = []
		embed = discord.Embed(
			color=0x5CDBF0,
			timestap='now'
			)

		for i in range(len(textlist)):
			if len(textlist[i][0]) >= 1 and 'COMPLETE<!---->' not in textlist[i][0]:
				newtextlist.append([textlist[i][0][:-1], textlist[i][1]])
		
		print(newtextlist)
		for i in range(len(newtextlist)):
			if newtextlist[i][1] == 'head':
				newtextlist[i+1][0] += ' '+ int(newtextlist[i][0][0]) * '- '
				newtextlist[i+1][0] = '\n' + newtextlist[i+1][0] + '\n'
				newtextlist[i+2][0] += ' ' + int(newtextlist[i][0][0]) * '- ' + '\n\n'
			if newtextlist[i][1] == 'h5':
				newnewtextlist.append([newtextlist[i][0], ''])
			elif len(newnewtextlist) > 0 and newtextlist[i][1] != 'head':
				newnewtextlist[-1][1] += newtextlist[i][0]
		for i in newnewtextlist:
			if i[0] != '':
				embed.add_field(name = i[0], value = i[1])
		await message.channel.send(embed=embed)
		
	if str(message.author) == 'amberhalo#7086':
		if message.content == "th!end":
			sys.exit()
client.run(TOKEN)
