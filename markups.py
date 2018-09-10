from telebot import types




## source markup 
source_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
source_markup_b1 = types.KeyboardButton("Eligibility")
source_markup_b2 = types.KeyboardButton("Affordability")
source_markup.add(source_markup_b1,source_markup_b2)



#=================================
###### Eligibility
#=================================


## Marital Status
marital_markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
marital_markup_b1 = types.KeyboardButton("Single")
marital_markup_b2 = types.KeyboardButton("Married")
marital_markup_b3 = types.KeyboardButton("Divorced")
marital_markup_b4 = types.KeyboardButton("Widowed")
marital_markup.add(marital_markup_b1,marital_markup_b2,marital_markup_b3,marital_markup_b4)


## Age
age_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
age_markup_b1 = types.KeyboardButton("Under 21")
age_markup_b2 = types.KeyboardButton("Above 21 but below 35")
age_markup_b3 = types.KeyboardButton("Above 35 but below 55")
age_markup_b4 = types.KeyboardButton("Above 55")
age_markup.add(age_markup_b1,age_markup_b2,age_markup_b3,age_markup_b4)


## Citizenship
citi_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
citi_markup_b1 = types.KeyboardButton("Singaporean")
citi_markup_b2 = types.KeyboardButton("Permanent Resident")
citi_markup_b3 = types.KeyboardButton("Foreigner")
citi_markup.add(citi_markup_b1,citi_markup_b2,citi_markup_b3)


## Application
app_markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
app_markup_b1 = types.KeyboardButton("Single")
app_markup_b2 = types.KeyboardButton("Joint (Married)")
app_markup_b3 = types.KeyboardButton("Joint (Singles)")
app_markup_b4 = types.KeyboardButton("Joint (Fiance/Fiancee)")
app_markup.add(app_markup_b1,app_markup_b2,app_markup_b3,app_markup_b4)

## Citizenship2
citi2_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
citi2_markup_b1 = types.KeyboardButton("Singaporean")
citi2_markup_b2 = types.KeyboardButton("Permanent Resident")
citi2_markup_b3 = types.KeyboardButton("Foreigner")
citi2_markup.add(citi2_markup_b1,citi2_markup_b2,citi2_markup_b3)


#=================================
###### Affordability
#=================================

# Would you like to use your info from the Eligibility test?
info_markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
info_markup_b1 = types.KeyboardButton("Yes")
info_markup_b2 = types.KeyboardButton("No")
info_markup.add(info_markup_b1,info_markup_b2)

# Joint?
type_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
type_markup_b1 = types.KeyboardButton("On my own")
type_markup_b2 = types.KeyboardButton("With a partner")
type_markup.add(type_markup_b1,type_markup_b2)

#=================================
###### Information
#=================================

## What would you like to do?
info1_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
info1_markup_b1 = types.KeyboardButton("Assess my saved user profile")
info1_markup_b2 = types.KeyboardButton("Assess my favourited listings")
info1_markup_b3 = types.KeyboardButton("Clear my saved information")
info1_markup.add(info1_markup_b1,info1_markup_b2,info1_markup_b3)

## What do you want to clear
clearopt_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
clearopt_markup_b1 = types.KeyboardButton("User Profile")
clearopt_markup_b2 = types.KeyboardButton("Clear my favourited listings")
clearopt_markup.add(clearopt_markup_b1,clearopt_markup_b2)

## Are you sure you want to clear your saved information
sure_markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
sure_markup_b1 = types.KeyboardButton("Yes")
sure_markup_b2 = types.KeyboardButton("No")
sure_markup.add(sure_markup_b1,sure_markup_b2)
