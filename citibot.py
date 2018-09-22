import telebot
from telebot import types
import time
import markups as m
import citibackend as citi
import requests
from bs4 import BeautifulSoup
import re
import logging
import redis
import datetoday as d

r = redis.StrictRedis(host='localhost', port=6379, db=0)


#### Variables
bot_token = ""  #Insert your token!

mstatus = None
joint = None
age = None
citizenship1 = None
citizenship2 = None
scheme = None

funds = None # Savings
joint2 = None
income1 = None # Income - Single
com1 = None # Financial Commitment for 1st person
funds2 = None # Savings for 2nd person
income2 = None # Income - Joint (for the second person)
com2 = None # Financial Commitment for 2nd person

affordability = None

budget = None # Budget
districtCode = None # Area Code
minimum = None
maximum = None
propertyTypeSelection = None # Property Type Selection
districtIdentifier = None
propertyTypeIdentifier = None
messageStorage = []
counter = 0
cid = 0
mid = 0
sort = "None"
favouriteList = []


#### Assessment messages
ssc = "You are eligible to purchase <b>2-Room Flexi Flats</b> if your average gross monthly household income does not exceed 6 000. \
Do make sure that You do not own other properties overseas or locally, and have not disposed of any within the last 30 months You have not \
purchased a new HDB/ DBSS flat or EC, or received a CPF Housing Grant before; or, have only purchased 1 of those properties/ received \
1 CPF Housing Grant thus far. \n\nYou are also eligible to purchase a <b>resale flat</b>, however You must dispose of any HDB flat or private property \
you own within 6 months of the resale flat purchase."

jss = "You are eligible to purchase <b>2-Room Flexi Flats</b> if your average gross monthly household income does not exceed 6 000. \
You are also eligible to purchase a new <b>Executive Condominium (EC)</b> from a developer if your average gross monthly household \
income does not exceed 14 000. For the above two types of flat, do make sure that You do not own other properties overseas or locally, \
and have not disposed of any within the last 30 months You have not purchased a new HDB/ DBSS flat or EC, or received a CPF Housing Grant \
before; or, have only purchased 1 of those properties/ received 1 CPF Housing Grant thus far. \n\nYou are also eligible to purchase a <b>resale \
flat</b>, however You must dispose of any HDB flat or private property you own within 6 months of the resale flat purchase."

ncs = "You are eligible to purchase <b>2-Room Flexi Flats</b> in non-mature estates if your average gross monthly household income does not exceed 6 000. \
Do make sure that You do not own other properties overseas or locally, and have not disposed of any within the last 30 months You have not \
purchased a new HDB/ DBSS flat or EC, or received a CPF Housing Grant before; or, have only purchased 1 of those properties/ received \
1 CPF Housing Grant thus far. Your non-citizen spouse must be holding a valid Visit Pass or Work Pass at the time of your application. \
The pass need not have a validity period of 6 months.\n\nYou are also eligible to purchase a <b>resale flat</b>, however You must dispose of any HDB \
flat or private property you own within 6 months of the resale flat purchase."

allok = "You are eligible to purchase a <b>new HDB</b> flat! To purchase a <i>4-room flat</i> or bigger, your average gross monthly household income should not \
exceed 12 000. To purchase a <i>3-room flat</i>, your average gross monthly household income should not exceed 12 000. (However, for some projects in non-mature estates, \
the income ceiling is lower at 6 000). You are also eligible to purchase <b>2-Room Flexi Flats</b> in non-mature estates if your average gross monthly household income does \
not exceed 6 000. Additionally, You are eligible to purchase a new <b>Executive Condominium (EC)</b> from a developer if your average gross monthly household \
income does not exceed 14 000. \n\nFor the above three types of flats, Do make sure that You do not own other properties overseas or locally, and have not \
disposed of any within the last 30 months You have not purchased a new HDB/ DBSS flat or EC, or received a CPF Housing Grant before; or, have only \
purchased 1 of those properties/ received 1 CPF Housing Grant thus far. \n\nLastly, You are also eligible to purchase a <b>resale flat</b>, however You must dispose of any HDB \
flat or private property you own within 6 months of the resale flat purchase. "




bot = telebot.TeleBot(bot_token)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


#### Handlers
@bot.message_handler(commands=['start'])
def send_introduction(message):
	r.hmset(message.chat.id, {"lastupdated":d.today()})
	print(message.chat.id) #Your user id = 276269485
	print('\n\n\n\n\n')
	print(r.hgetall(message.chat.id))
	print('\n\n\n\n\n')

	bot.send_message(message.chat.id, """Hi! I am your friendly Housing Bot, able to help you analyse your financial situation and eligibility for\
		properties. Also, I can help you search for properties based on your budget and requirements! \n\n Sounds exciting? Enter any of the\
		following commands to try out!\n'/ask': To analyse your financial situation and eligibility for properties\n\n\
		'/mypref': To set up your preferences BEFORE the property search\n\n\
		'/searchnow': To search for properties based on your budget and requirements\n\n\
		'/info': To assess your saved profile and preferences""")

@bot.message_handler(commands=['ask'])
def send_welcome(message):
	msg = bot.send_message(message.chat.id, "Hi! I am your friendly Housing Bot, what would you like to analyse today? :)",reply_markup=m.source_markup)
	bot.register_next_step_handler(msg, whichtwo)


@bot.message_handler(commands=['help'])
def send_help(message):
	print(r.hgetall("message.chat.id"))
	print('\n\n\n\n\n')

	text= "To use this bot, use the following commands:\n\n'/ask': To analyse your financial situation and eligibility for properties\n\n\
	'/mypref': To set up your preferences BEFORE the property search\
	'/searchnow': To search for properties based on your budget and requirements\n\n\
	'/info': To assess your saved profile and preferences"
	bot.reply_to(message, text)


@bot.message_handler(commands=['info'])
def send_info(message):
	text = "Hello, you are able to access your <b>saved profile</b> (Eligibility status and current calculated affordability) and your \
	favourited apartments. \
	You are also able to <b>clear your saved information</b> here. What would you like to do?"
	msg = bot.send_message(message.chat.id, text, reply_markup=m.info1_markup,parse_mode="HTML")
	bot.register_next_step_handler(msg, whichinfo)

@bot.message_handler(commands=['mypref'])
def getRequirements(message):
	getPropertyType(message)

@bot.message_handler(commands=['sort'])
def sortOrder(message):
	getSort(message)

@bot.message_handler(commands=['searchnow'])
def searchProperty(message):
	print(citi.addPropertyTypeFilter(propertyTypeSelection))
	new_url = citi.urlGenerator(citi.addPropertyTypeFilter(propertyTypeIdentifier), budget)
	print(new_url)
	bot.send_message(message.chat.id, 'Searching in progress\nPlease wait patiently')

	longdict = citi.getAllListingDetails(citi.getListingLinks(new_url))

	global messageStorage
	messageStorage = []
	for index, listing in enumerate(longdict):
		messageStorage.append(str(longdict[listing]).strip("{}").replace(":'","").replace("'", ''))

	r.hmset(message.chat.id, {"lastupdated":d.today(),"propertylistingsData":messageStorage})

	keyboard = types.InlineKeyboardMarkup()
	nextButton = types.InlineKeyboardButton(text='Next', callback_data='next')
	favButton = types.InlineKeyboardButton(text='Favorite', callback_data='fav')
	keyboard.row(nextButton)
	keyboard.row(favButton)
	bot.send_message(message.chat.id, messageStorage[0], reply_markup=keyboard)
	bot.send_message(message.chat.id, "If you would like me to do other things for you, just enter '/start'! :)")

	#call back data to get the next in line


##====================================================
## Information
##====================================================
def whichinfo(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	mark = types.ReplyKeyboardRemove(selective=False)
	if message.text == "Assess my saved user profile":
		text = "Here are your saved profile:\n\nAffordability: {}\n\nEligibility Status: {}".format(aff_status(affordability),eligibility_status(scheme))
		bot.send_message(chat_id, text,reply_markup=mark,parse_mode="HTML")
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	elif message.text == "Assess my favourited listings":
		if len(favouriteList) == 0:
			bot.send_message(chat_id, "You have not favourited any listing!", reply_markup=mark)
		elif len(favouriteList) == 1:
			text = "Here is your favourited listings:\n\n" + "1." + str(favouriteList[0])
			bot.send_message(chat_id, text, reply_markup=mark)

		elif len(favouriteList) == 2:
			text = "Here are your favourited listings:\n\n" + "1." + str(favouriteList[0]) + "\n\n2." + str(favouriteList[1])
			bot.send_message(chat_id, text, reply_markup=mark)
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	elif message.text == "Clear my saved information":
		msg = bot.send_message(chat_id, "What do you want to clear?", reply_markup=m.clearopt_markup)
		bot.register_next_step_handler(msg, clear1)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whichinfo)


def aff_status(affordability):
	if affordability == None:
		return "Not saved yet :("
	elif type(affordability) == int:
		return str(affordability)
	else:
		return "Error"

def eligibility_status(scheme):
	if scheme == "ff":
		return ("You are eligible to purchase a <b>resale flat</b> if all SPR owners and essential occupiers have SPR status for at least 3 years.\
			Additionally, You must dispose of any HDB flat or private property you own within 6 months of the resale flat purchase.")
	elif scheme == "ssc":
		return ssc
	elif scheme == "jss":
		return jss
	elif scheme == "ncs":
		return ncs
	elif scheme == "public":
		return allok
	elif scheme == "no":
		return "Not eligible"
	else:
		return "Not saved yet :("

def clear1(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	mark = types.ReplyKeyboardRemove(selective=False)
	global favouriteList
	if message.text == "User Profile":
		bot.send_message(chat_id, "Your User Profile has been cleared!",reply_markup=mark)
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")
	elif message.text == "Clear my favourited listings":
		favouriteList = []
		bot.send_message(chat_id, "The listings has been cleared!",reply_markup=mark)
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, clear)

def clear(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	mark = types.ReplyKeyboardRemove(selective=False)
	if message.text == "Yes":
		global affordability; global scheme; global joint
		affordability=None; scheme=None; joint=None
		bot.send_message(chat_id, "All of your information have been cleared!",reply_markup=mark)
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")
	elif message.text == "No":
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)", reply_markup=mark)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, clear)


##====================================================
## Eligibility
##====================================================

# Source
def whichtwo(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	if message.text == "Eligibility":
		msg = bot.send_message(chat_id, "You have selected to assess your eligibility to buy a new or resale HDB flat!\
			As the Main applicant, do answer the following questions! \n\n Firstly, What is your marital status?",reply_markup=m.marital_markup)
		bot.register_next_step_handler(msg, whatage)
	elif message.text == "Affordability":
		msg = bot.send_message(chat_id, "Would you like us to use your information given in the Eligibility assessment?", reply_markup=m.info_markup)
		bot.register_next_step_handler(msg, whatjoint)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whichtwo)


def whatage(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	response_ls = ["Single","Married","Divorced","Widowed"]
	if message.text in response_ls:
		global mstatus
		mstatus = message.text
		msg = bot.send_message(chat_id, "What is your age range?", reply_markup=m.age_markup)
		bot.register_next_step_handler(msg, whatciti)

	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whatage)

def whatciti(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	response_ls = ["Under 21","Above 21 but below 35","Above 35 but below 55","Above 55"]
	if message.text in response_ls:
		global age
		global scheme
		age = message.text
		if age == "Under 21":
			mark = types.ReplyKeyboardRemove(selective=False)
			scheme = "no"
			bot.send_message(chat_id, "You are under 21 and hence not eligible to purchase a HDB flat! :(", reply_markup=mark)
			bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")
		elif mstatus == "Divorced" and age in ["Under 21","Above 21 but below 35"]:
			mark = types.ReplyKeyboardRemove(selective=False)
			scheme = "no"
			bot.send_message(chat_id, "You are under 35 and hence not eligible to purchase a HDB flat! :(", reply_markup=mark)
			bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")
		elif mstatus == "Single" and age in ["Under 21","Above 21 but below 35"]:
			mark = types.ReplyKeyboardRemove(selective=False)
			scheme = "no"
			bot.send_message(chat_id, "You are under 35 and hence not eligible to purchase a HDB flat! :(", reply_markup=mark)
			bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")
		else:
			msg = bot.send_message(chat_id, "What type of citizenship do you hold?", reply_markup=m.citi_markup)
			bot.register_next_step_handler(msg, whattype)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whatciti)


def whattype(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	response_ls = ["Singaporean","Permanent Resident","Foreigner"]
	if message.text in response_ls:
		global citizenship1
		citizenship1 = message.text
		if citizenship1 == "Foreigner":
			mark = types.ReplyKeyboardRemove(selective=False)
			global scheme
			scheme = "no"
			bot.send_message(chat_id, "The main applicant cannot be a foreigner. Hence, you are not eligible to purchase a HDB flat! :(", reply_markup=mark)
			bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")
		else:
			msg = bot.send_message(chat_id, "Which type of purchase is this?",reply_markup=m.app_markup)
			bot.register_next_step_handler(msg, assess)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whattype)

def assess(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	response_ls = ["Single","Joint (Married)","Joint (Not Married)","Joint (Fiance/Fiancee)"]
	if message.text in response_ls:
		global joint
		joint = message.text
		if joint != "Single":
			msg = bot.send_message(chat_id, "What citizenship does your co-applicant hold?",reply_markup=m.citi2_markup)
			bot.register_next_step_handler(msg, assess_joint)
		else:
			assessing(chat_id)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, assess)

def assess_joint(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	response_ls = ["Singaporean","Permanent Resident","Foreigner"]
	if message.text in response_ls:
		global citizenship2
		citizenship2 = message.text
		assessing(chat_id)

	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, assess_joint)



# Helper function to check eligibility scheme
def assessing(chat_id):
	mark = types.ReplyKeyboardRemove(selective=False)
	global scheme
	if citizenship1=="Singaporean" and (mstatus=="Single" or mstatus=="Widowed" or mstatus=="Divorced"):
		scheme = "ssc"
		bot.send_message(chat_id, ssc, reply_markup=mark,parse_mode="HTML")
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	elif citizenship1==citizenship2=="Singaporean" and joint=="Joint (Not Married)":
		scheme = "jss"
		bot.send_message(chat_id, jss, reply_markup=mark,parse_mode="HTML")
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	elif citizenship1=="Singaporean" and citizenship2=="Foreigner" and joint=="Joint (Married)":
		scheme = "ncs"
		bot.send_message(chat_id, ncs, reply_markup=mark, parse_mode="HTML")
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	elif citizenship1==citizenship2=="Permanent Resident" and joint=="Joint (Fiance/Fiancee)":
		scheme = "ff"
		bot.send_message(chat_id,"You are eligible to purchase a <b>resale flat</b> if all SPR owners and essential occupiers have SPR status for at least 3 years.\
			Additionally, You must dispose of any HDB flat or private property you own within 6 months of the resale flat purchase.", reply_markup=mark,parse_mode="HTML")
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	elif (citizenship1=="Permanent Resident" and citizenship2=="Foreigner") or (citizenship1==citizenship2=="Permanent Resident" and joint=="Joint (Married)"):
		scheme = "no"
		bot.send_message(chat_id,"You are not eligible to purchase a new or resale HDB nor a new Executive Condominium. :(", reply_markup=mark)
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	elif citizenship1=="Permanent Resident" and joint=="Single":
		scheme = "no"
		bot.send_message(chat_id,"You are not eligible to purchase a new or resale HDB nor a new Executive Condominium. :(", reply_markup=mark)
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	elif (citizenship1==citizenship2=="Singaporean" and joint=="Joint (Married)") \
	or (citizenship1=="Singaporean" and citizenship2=="Permanent Resident" and joint=="Joint (Married)"):
		scheme = "public"
		bot.send_message(chat_id, allok , reply_markup=mark,parse_mode="HTML")
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	elif (citizenship1=="Singaporean" and citizenship2=="Permanent Resident" and joint=="Joint (Fiance/Fiancee)") \
	or (citizenship1=="Permanent Resident" and citizenship2=="Singaporean" and joint=="Joint (Married)"):
		scheme = "public"
		bot.send_message(chat_id, allok , reply_markup=mark,parse_mode="HTML")
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")

	else:
		bot.send_message(chat_id,"I seem to have ran into a bug, try again later! :(", reply_markup=mark)
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")



##====================================================
## Affordability
##====================================================
def whatjoint(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	response_ls = ["Yes","No"]
	mark = types.ReplyKeyboardRemove(selective=False)
	global joint2
	if message.text == "Yes":
		if joint == None:
			msg = bot.send_message(chat_id, "You have not done an Eligibility test!\n\n Are you buying a home on your own or with a partner?", reply_markup=m.type_markup)
			bot.register_next_step_handler(msg, grant)
		elif scheme == "ssc":
			joint2 = "On my own"
			msg = bot.send_message(chat_id, "How much funds do you have available? (Include your CPF OA savings, Personal Savings and any grant available)\
				To find out more about the grants available for your scheme, visit https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/new/schemes-and-grants/cpf-housing-grants-for-hdb-flats/single-singapore-citizen-scheme\
				\n\nPlease enter a whole number",
				reply_markup=mark)
			bot.register_next_step_handler(msg, whatsalary)
		elif scheme == "jss":
			joint2 = "On my own"
			msg = bot.send_message(chat_id, "How much funds do you have available? (Include your CPF OA savings, Personal Savings and any grant available)\
				To find out more about the grants available for your scheme, visit https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/new/joint-singles-scheme-or-orphans-scheme\
				\n\nPlease enter a whole number",
				reply_markup=mark)
			bot.register_next_step_handler(msg, whatsalary)
		elif scheme == "ncs":
			joint2 = "With a partner"
			msg = bot.send_message(chat_id, "How much funds do you have available? (Include your CPF OA savings, Personal Savings and any grant available)\
				To find out more about the grants available for your scheme, visit https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/new/non-citizen-spouse-scheme\
				\n\nPlease enter a whole number",
				reply_markup=mark)
			bot.register_next_step_handler(msg, whatsalary)
		elif scheme == "public" or scheme == "ff":
			joint2 = "With a partner"
			msg = bot.send_message(chat_id, "How much funds do you have available? (Include your CPF OA savings, Personal Savings and any grant available)\
				To find out more about the grants available for your scheme, visit https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/new/first-timer-applicants\
				\n\nPlease enter a whole number",
				reply_markup=mark)
			bot.register_next_step_handler(msg, whatsalary)

	elif message.text =="No":
		msg = bot.send_message(chat_id, "Are you buying a home on your own or with a partner?", reply_markup=m.type_markup)
		bot.register_next_step_handler(msg, grant)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whatjoint)

def grant(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	response_ls = ["On my own","With a partner"]
	mark = types.ReplyKeyboardRemove(selective=False)
	if message.text in response_ls:
		global joint2
		joint2 = message.text
		msg = bot.send_message(chat_id, "How much funds do you have available? (Include your CPF OA savings, Personal Savings and any grant available)\
				To find out more about the grants available, visit https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/new/cpf-housing-grants-for-hdb-flats\
				\n\nPlease enter a whole number",
				reply_markup=mark)
		bot.register_next_step_handler(msg, whatsalary)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, grant)


def whatsalary(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	if message.text.isdigit():
		global funds
		funds = int(message.text)
		r.hmset(message.chat.id,{"lastupdated":d.today(),"savings1":funds}) # Money saved for house of the first person

		msg = bot.send_message(chat_id, "What is your gross monthly income?\n\nPlease enter a whole number")
		bot.register_next_step_handler(msg, whatcom)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whatsalary)


def whatcom(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	if message.text.isdigit():
		global income1
		income1 = int(message.text)
		r.hmset(message.chat.id,{"lastupdated":d.today(),"income1":income1}) #Monthly income of the first person

		msg = bot.send_message(chat_id, "What is your monthly financial commitments and living expenses? (Eg. Car loans, credit card loans, personal loans.)\
			\n\nPlease enter a whole number")
		bot.register_next_step_handler(msg, assess_afford)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whatcom)

def assess_afford(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	if message.text.isdigit():
		global com1
		global affordability
		com1 = int(message.text)
		r.hmset(message.chat.id,{"lastupdated":d.today(),"f_commitment1":com1}) #Saving the financial commitment of the 1st person

		if joint2 == "On my own":
			affordability = assessing_afford(chat_id)
			bot.send_message(chat_id, "Your maximum affordability calculated is ${}.\
				For a better reflection of your affordability, do consult a bank regarding loans available for you :)".format(affordability))
			bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")
		else:
			msg = bot.send_message(chat_id, "How much funds does your partner have available? (Include CPF OA savings & Personal Savings)\
			\n\nPlease enter a whole number")
			bot.register_next_step_handler(msg, whatsalary2)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, assess_afford)

def assessing_afford(chat_id):
	# To calculate max affordability, we take the smaller of the two values calculated. The first value is obtained via the assumption of
	# 30% Mortage Servicing Ratio. The second value is obtained via the assumption of 75% Loan to Value ratio.
	if joint2 == "On my own":
		value_1 = (income1 - com1)*12*25*0.3 + funds
		value_2 = funds/2.5*10
	elif joint2 == "With a partner":
		value_1 = (income1 + income2 - com1 - com2)*12*25*0.3 + funds + funds2
		value_2 = (funds+funds2)/2.5*10
	final = min(value_1,value_2)
	return int(final)


def whatsalary2(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	if message.text.isdigit():
		global funds2
		funds2 = int(message.text)
		r.hmset(message.chat.id,{"lastupdated":d.today(),"savings2":funds2}) # Money saved for House of the second person

		msg = bot.send_message(chat_id, "What is your partner's gross monthly income? Please enter a whole number")
		bot.register_next_step_handler(msg, whatcom2)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whatsalary2)

def whatcom2(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	if message.text.isdigit():
		global income2
		income2 = int(message.text)
		r.hmset(message.chat.id,{"lastupdated":d.today(),"income2":income2}) #Monthly income of the second person
		msg = bot.send_message(chat_id, "What is your partner's monthly financial commitments and living expenses? \
			(Eg. Car loans, credit card loans, personal loans.) Please enter a whole number")
		bot.register_next_step_handler(msg, assess_afford2)
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, whatcom2)


def assess_afford2(message):
	chat_id = message.chat.id
	bot.send_chat_action(chat_id, 'typing')
	if message.text.isdigit():
		global com2
		global affordability
		com2 = int(message.text)
		r.hmset(message.chat.id,{"lastupdated":d.today(),"f_commitment2":com2}) #Saving the financial commitment of the second person

		affordability = assessing_afford(chat_id)
		bot.send_message(chat_id, "Your maximum affordability calculated is ${}.\
				For a better reflection of your affordability, do consult a bank regarding loans available for you :)".format(affordability))
		bot.send_message(chat_id, "If you would like me to do other things for you, just enter '/start'! :)")
	else:
		msg = bot.send_message(chat_id, "I am sorry, I didn't quite catch that... Please try again")
		bot.register_next_step_handler(msg, assess_afford2)


##====================================================
## Property Search
##====================================================

def nextItemListing(call):
	global counter, messageStorage
	nextMessage = messageStorage[counter]

	keyboard = types.InlineKeyboardMarkup()
	nextButton = types.InlineKeyboardButton(text='Next', callback_data='next')
	previousButton = types.InlineKeyboardButton(text='Previous', callback_data='previous')
	favButton = types.InlineKeyboardButton(text='Favorite', callback_data='fav')

	if counter == len(messageStorage)-1:
		keyboard.add(previousButton)
		keyboard.row(favButton)
	elif counter == 0:
		keyboard.add(nextButton)
		keyboard.row(favButton)
	else:
		keyboard.add(previousButton, nextButton)
		keyboard.row(favButton)


	bot.edit_message_text(chat_id = call.message.chat.id,
						  message_id=call.message.message_id, text=str(nextMessage), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)  # The other inline button calls
def callback_inline(call):
	global counter, sort
	selections = ['hdb-1', 'hdb-2','hdb-3','hdb-4','hdb-5', 'condo', 'landed']
	if call.message:  # Processes only buttons from messages
		if call.data == 'hdb':
			print('User has picked HDB')
			pickHDBroom(call)

		elif call.data in selections:
			print('Picking District')
			print('User has picked a {}-room flat'.format(getDistrict(call)))
			global propertyTypeSelection, propertyTypeIdentifier

			if call.data == 'hdb-1':
				propertyTypeSelection = 'HDB: 1 Room Flat'
				propertyTypeIdentifier = 'hdb-1'
				r.hmset(call.message.chat.id,{"lastupdated":d.today(),"property_Type":propertyTypeSelection}) #Save the property type

			if call.data == 'hdb-2':
				propertyTypeSelection = 'HDB: 2 Room Flat'
				propertyTypeIdentifier = 'hdb-2'
				r.hmset(call.message.chat.id,{"lastupdated":d.today(),"property_Type":propertyTypeSelection}) #Save the property type

			if call.data == 'hdb-3':
				propertyTypeSelection = 'HDB: 3 Room Flat'
				propertyTypeIdentifier = 'hdb-3'
				r.hmset(call.message.chat.id,{"lastupdated":d.today(),"property_Type":propertyTypeSelection}) #Save the property type

			if call.data == 'hdb-4':
				propertyTypeSelection = 'HDB: 4 Room Flat'
				propertyTypeIdentifier = 'hdb-4'
				r.hmset(call.message.chat.id,{"lastupdated":d.today(),"property_Type":propertyTypeSelection}) #Save the property type

			if call.data == 'hdb-5':
				propertyTypeSelection = 'HDB: 5 Room Flat'
				propertyTypeIdentifier = 'hdb-5'
				r.hmset(call.message.chat.id,{"lastupdated":d.today(),"property_Type":propertyTypeSelection}) #Save the property type

			if call.data == 'condo':
				propertyTypeSelection = 'Condominium'
				propertyTypeIdentifier = 'condo'
				r.hmset(call.message.chat.id,{"lastupdated":d.today(),"property_Type":propertyTypeSelection}) #Save the property type

			if call.data == 'landed':
				propertyTypeSelection = 'Landed Property'
				propertyTypeIdentifier = 'landed'
				r.hmset(call.message.chat.id,{"lastupdated":d.today(),"property_Type":propertyTypeSelection}) #Save the property type

			getDistrict(call)

		elif call.data == 'district1' or call.data == 'district2' or call.data == 'district3':
			computeDistrict(call)
			askBudget(call)

		elif call.data == 'next':
			counter += 1
			nextItemListing(call)

		elif call.data == 'previous':
			counter -= 1
			nextItemListing(call)

		elif call.data == 'fav':
			print(call)
			if len(favouriteList)<=1:
				favouriteList.append(call.message.text)
			else:
				bot.send_message(call.message.chat.id, 'You have a reached a maximum of 2 favourites. Enter /info to view and clear your favourited apartments.')
			print(favouriteList)

		elif call.data == 'addr' or call.data == 'price' or call.data == 'size' or call.data == 'psf':
			sort = call.data
			finalisedPreference(call)


def getSort(message):
	keyboard=types.InlineKeyboardMarkup()
	addressButton = types.InlineKeyboardButton(text='Sort by Ascending Address Name', callback_data='addr')
	priceButton = types.InlineKeyboardButton(text='Price', callback_data='price')
	sizeButton = types.InlineKeyboardButton(text='Size', callback_data='size')
	psfButton = sizeButton = types.InlineKeyboardButton(text='Price per Square Feet', callback_data='psf')

	keyboard.row(addressButton)
	keyboard.row(priceButton)
	keyboard.row(sizeButton)
	keyboard.row(psfButton)
	bot.send_message(message.chat.id, 'Choose your preference', reply_markup=keyboard)

def getPropertyType(message):
	keyboard = types.InlineKeyboardMarkup()
	buttonHDB = types.InlineKeyboardButton(text='HDB', callback_data='hdb')
	buttonCondo = types.InlineKeyboardButton(text='Condo',callback_data='condo')
	buttonLanded = types.InlineKeyboardButton(text='Landed',callback_data='landed')


	keyboard.add(buttonHDB, buttonCondo, buttonLanded)
	bot.send_message(message.chat.id, 'What is the type of property?', reply_markup=keyboard)

def pickHDBroom(call):
	keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text='1 Room', callback_data='hdb-1')
	button2 = types.InlineKeyboardButton(text='2 Room', callback_data='hdb-2')
	button3 = types.InlineKeyboardButton(text='3 Room', callback_data='hdb-3')
	button4 = types.InlineKeyboardButton(text='4 Room', callback_data='hdb-4')
	button5 = types.InlineKeyboardButton(text='5 Room', callback_data='hdb-5')

	keyboard.add(button1, button2, button3, button4, button5)
	bot.edit_message_text(chat_id=call.message.chat.id,
				  message_id=call.message.message_id, text='How many rooms?', reply_markup=keyboard)

def getDistrict(call):
	keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text='Core Central Districts', callback_data='district1')
	button2 = types.InlineKeyboardButton(text='Rest of Central Region', callback_data='district2')
	button3 = types.InlineKeyboardButton(text='Outside Central Region', callback_data='district3')

	longtext= '''<b>Choose a District:\n\nCore Central Districts</b>\n
	D1 - Temasek Blvd, Raffles Link\n
	D2 - Anson, Tanjong Pagar\n
	D4 - Telok Blangah, Harbourfront\n
	D6 - High Street, Beach Road\n
	D7 - Middle Road, Golden Mile\n
	D9 - Orchard, Cairnhill, River Valley\n
	D10 - Bukit Timah, Holland Rd, Tanglin\n
	D11 - Watten Estate, Novena, Thomson\n\n
	<b>Rest of Central Region</b>\n
	D2 - Anson, Tanjong Pagar\n
	D3 - Queenstown, Tiong Bahru\n
	D7 - Middle Road, Golden Mile\n
	D8 - Little India\n
	D12 - Balestier, Toa Payoh, Serangoon\n
	D13 - Macpherson, Braddell\n
	D14 - Geylang, Eunos\n
	D15 - Katong, Joo Chiat, Amber Road\n\n
	<b>Outside Central Region</b>\n
	D5 - Pasir Panjang, Clementi\n
	D16 - Bedok, Upper East Coast\n
	D17 - Loyang, Changi\n
	D18 - Tampines, Pasir Ris\n
	D19 - Serangoon, Hougang, Punggol\n
	D20 - Bishan, Ang Mo Kio\n
	D21 - Upper Bukit Timah, Ulu Pandan\n
	D22 - Jurong\n
	D23 - Bukit Panjang, Choa Chu Kang\n
	D24 - Lim Chu Kang, Tengah\n
	D25 - Kranji, Woodgrove\n
	D26 - Upper Thomson, Springleaf\n
	D27 - Yishun, Sembawang\n
	D28 - Seletar'''
	keyboard.add(button1, button2, button3)

	print(call)
	print(call.data)
	bot.edit_message_text(chat_id=call.message.chat.id,
						  message_id=call.message.message_id, parse_mode='html',text=longtext, reply_markup=keyboard)

def computeDistrict(call):
	global districtCode, districtIdentifier

	if call.data == 'district1':
		districtIdentifier = '''Core Central Districts - inclusive of:\n\n
		D1 - Temasek Blvd, Raffles Link\n
		D2 - Anson, Tanjong Pagar\n
		D4 - Telok Blangah, Harbourfront\n
		D6 - High Street, Beach Road\n
		D7 - Middle Road, Golden Mile\n
		D9 - Orchard, Cairnhill, River Valley\n
		D10 - Bukit Timah, Holland Rd, Tanglin\n
		D11 - Watten Estate, Novena, Thomson\n
		'''
		districtCode = citi.districtFilter(1)
		r.hmset(call.message.chat.id,{"lastupdated":d.today(),"area":"Core Central Districts"}) #Save the area code

	if call.data == 'district2':
		districtIdentifier = '''Rest of Central Region - inclusive of:\n\n
		D2 - Anson, Tanjong Pagar\n
		D3 - Queenstown, Tiong Bahru\n
		D7 - Middle Road, Golden Mile\n
		D8 - Little India\n
		D12 - Balestier, Toa Payoh, Serangoon\n
		D13 - Macpherson, Braddell\n
		D14 - Geylang, Eunos\n
		D15 - Katong, Joo Chiat, Amber Road\n\n
		'''
		districtCode = citi.districtFilter(2)
		r.hmset(call.message.chat.id,{"lastupdated":d.today(),"area":"Rest of Central Region"}) #Save the area code


	if call.data == 'district3':
		districtIdentifier = '''Outside Central Region - inclusive of:\n\n
		D5 - Pasir Panjang, Clementi\n
		D16 - Bedok, Upper East Coast\n
		D17 - Loyang, Changi\n
		D18 - Tampines, Pasir Ris\n
		D19 - Serangoon, Hougang, Punggol\n
		D20 - Bishan, Ang Mo Kio\n
		D21 - Upper Bukit Timah, Ulu Pandan\n
		D22 - Jurong\n
		D23 - Bukit Panjang, Choa Chu Kang\n
		D24 - Lim Chu Kang, Tengah\n
		D25 - Kranji, Woodgrove\n
		D26 - Upper Thomson, Springleaf\n
		D27 - Yishun, Sembawang\n
		D28 - Seletar
		'''
		districtCode = citi.districtFilter(3)
		r.hmset(call.message.chat.id,{"lastupdated":d.today(),"area":"Outside Central Region"}) #Save the area code

def askBudget(call):
	bot.edit_message_text(chat_id=call.message.chat.id,
						  message_id=call.message.message_id,
						  text='Enter the minimum budget & maximum budget:\n(Example: 500000,600000)',
						  reply_markup=False)

def finalisedPreference(call):
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Your preference:\n\n1) {}\n2) Budget: ${} to ${}\n3) {} \n4) Sort by: {}'.format(propertyTypeSelection,
																				   minimum, maximum, districtIdentifier, sort)
				 +'\nEnter /searchnow to see our recommendations specially tailored for you!\n'+
				 'To update your preferences, enter /mypref\n'
				 , reply_markup=False)

@bot.message_handler(func=lambda message: True)
def logTextMessage(message):
	# split if they type 500000,600000
	if len(message.text.split(','))==2: #'1','2'

		global minimum, maximum, budget
		minimum = int(message.text.split(',')[0]) #'1,2' -> [1,2]
		maximum = int(message.text.split(',')[1])

		budget = (citi.budget(minimum,maximum)) #budget logged

		print('\n\n\n')
		r.hmset(message.chat.id,{"lastupdated":d.today(),"budget":[minimum,maximum]})
		print(r.hgetall(message.chat.id))
		redisData = r.hget(message.chat.id,"budget")
		print(redisData.decode('utf-8'))
		print('\n\n\n')

		print('Your budget = (minimum,maximum) = {},{}'.format(minimum,maximum))

		bot.send_message(message.chat.id, 'Enter /sort to indicate your search preference')





try:
	bot.infinity_polling(none_stop=True)

except Exception as err:
	logging.error(err)
	time.sleep(5)
	print ("Internet error!")

# bot.stop_polling()
