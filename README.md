# citihdb
Hackathon 2018

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.

Prerequisites
---------------
Follow the instructions in the various links attached to install them properly.
1. Python 3 (https://www.python.org/) -- one of the most powerful programming language
2. PyTelegrambotAPI (https://github.com/eternnoir/pyTelegramBotAPI) -- a sleek tool to host a Telegram bot
3. Request package (https://pypi.org/project/requests/)
4. BeautifulSoup4 (https://pypi.org/project/beautifulsoup4/) -- parsing HTML and XML documents; used for web scraping
5. Clone our repository!

## Running the tests
If you encountered any problems in the process, please refer to the top of this page under **Prerequisites** for possible missing dependencies.

### Running the server for us
1. Clone repository and save it in your Desktop (i.e. C:\Users\jem\citihdb)
2. If you have your own IDE or programmes to run python script file, you may do so at your own comfort. Or else, open up command prompt
(win key > search 'cmd' > enter)
3. Point your command prompt to the directory that contains our git repository by typing
```
C:\Users\jem>cd citihdb
C:\Users\jem\citihdb>
```
4. in cmd, type 'python citibot.py'. A prompt will appear in the command prompt. Once you see "____", your server is up and running.
5. Go to Telegram and search for @Citibot. Type /start command and follow the instructions given by our bot.

### Running the server with your own bot
1. Clone repository and save it in your Desktop (i.e. C:\Users\jem\citihdb)
2. If you have your own IDE or programmes to run python script file, you may do so at your own comfort. Or else, open up command prompt
(win key > search 'cmd' > enter)
![alt text](https://github.com/jeremyng123/citihack/blob/master/cmd%20in%20windows.png?raw=true)
3. Point your command prompt to the directory that contains our git repository by typing
```
C:\Users\jem>cd citihdb
C:\Users\jem\citihdb>
```
![alt text](https://github.com/jeremyng123/citihack/blob/master/cmd_cd.png?raw=true)
4. Follow the instructions at https://core.telegram.org/bots to learn how to create your own bot.

5. Once you have gotten your own bot Token (step 4), use your own favorite text editor (in our case, we use [Atom] (https://atom.io/)) and open up `CitiBot.py`.

6. Search for:
```
bot_token = "500756386:AAFPCzG-QX8Oa_Rd8AnJgBbZuCoGmB8p0Vp"
```
and replace the string stored in `bot_token` to your own bot Token.




### Authors
See Yi Jie - **Web scraping**, **UI & UX** of the Telegram Bot

Ashlyn - Research of HDB Schemes & coding of the **eligibility and affordability** portion.

Jeremy - **UI & UX** of Telegram Bot


## Acknowledgments
Hat tip to anyone whose code was used
Inspiration
etc
