# Assign seperators
topSep = '|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|'
bottomSep ='|=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=\u05BE=|'
print('%s\n|Ignore any warnings that pop up                  |'% topSep)
print("|They don't affect the bot.                       |")


# OS Imports
import os
from os import sys

# Video Imports
import subprocess as sp
import numpy
#from scipy import ndimage, misc

# Reddit Imports
import configparser
import praw

#Other Imports
import re
import Helpers
import time
import datetime
def LPrint(value): return Helpers.LengthFixer(value.replace("\n",''))

# Setup
Setup = Helpers.Setup()
FFMPEG_BIN = Setup.FFMPEG()
r = praw.Reddit('Frozen Frame Grabber by /u/subconcussive')
config = configparser.ConfigParser()
config.read('settings.cfg')

try: # Try to Login
    username = config.get('AUTH', 'USERNAME')
except:
    try:
        import sys
        args = sys.argv[1:]
        dargs = args.split(" ")
        username = dargs[0]
    except:
        username = input("Enter Username: ")
        if username == '':
            raise ValueError()
try:
    password = config.get('AUTH', 'PASSWORD')
    if password == '':
        raise ValueError()
except:
    try:
        import sys
        args = sys.argv[1:]
        dargs = args.split(" ")
        password = dargs[1]
    except:
        password = input("Enter Password: ")
        if password == '':
            raise ValueError()
try:
    subR = config.get('SETTINGS', 'SUBREDDIT')
except:
    try:
        import sys
        args = sys.argv[1:]
        dargs = args.split(" ")
        subR = dargs[2]
    except:
        subR = input("Enter Subreddit: ")
        if subR == '':
            raise ValueError()
try:
    userID = config.get('AUTH', 'CLIENTID')
except:
    try:
        import sys
        args = sys.argv[1:]
        dargs = args.split(" ")
        userID = dargs[3]
    except:
        userID = input("Enter Imgur ClientId: ")
        if userID == '':
            raise ValueError()
try:
    userSecret = config.get('AUTH', 'CLIENTSECRET')
except:
    try:
        import sys
        args = sys.argv[1:]
        dargs = args.split(" ")
        userSecret = dargs[4]
    except:
        userSecret = input("Enter Imgur ClientSecret: ")
        if userSecret == '':
            raise ValueError()
r.login(username, password)
print('%s\n'% bottomSep)
#Now set some variables
already_done = []

while True:
    subreddit = r.get_subreddit(subR)
    numlimit = 15
    comments = subreddit.get_comments()
    for comment in comments:            
            if (comment.id in already_done):
                finished = True
            else:
                print(topSep)
                print(LPrint(comment.body))
                print(LPrint("Posted by: "+comment.author.name))
                if (('/u/'+username).upper() in comment.body.upper()):
                    # Example comment: '/u/FROZEN_BOT @time 34:38\nSee?'
                    reply = None
                    if '@' not in comment.body:
                        #malformed summons
                        if "time" in comment.body:
                            args = comment.body.split("time")[1:]#Try to parse it
                            if len(args) > 1:
                                reply = "Here's your screen grabs!\n\n"
                            else:
                                reply = "Here's your screen grab!\n\n"
                            counter = 0
                            for arg in args:
                                time = re.search(("([0-9]{1,2}:[0-9]{2}:[0-9]{2}|"
                                                 "[0-9]{1,2}:[0-9]{2}|"
                                                 "[0-9]{1,2})"),
                                                 arg).group(0)
                                if len(time) == len('HH:MM:ss'):
                                    _ = time
                                elif len(time) == len('H:MM:ss'):
                                    time = "0"+time
                                elif len(time) == len('MM:ss'):
                                    time = "00:"+time
                                elif len(time) == len('M:ss'):
                                    time = "0"+time
                                elif len(time) == len('ss'):
                                    time = "00:00:"+time
                                elif len(time) == len('s'):
                                    time = "00:00:0"+time
                                else:
                                    reply = ("ERROR: Malformed/Unparsable Request\n\nCorrect "
                                             "formatting is as follows:\n\n    <Any Text>"
                                             "/u/FROZEN_BOT @time HH:MM:SS\n\nYou can "
                                             "request multiple images at once by adding "
                                             "additional @time HH:MM:SS lines.\n\n"
                                             "^(I am a bot that grabs screenshots from"
                                             "Frozen, contact my [Owner/Caretaker]"
                                             "(https://ssl.reddit.com/u/subconcussive)")
                                    comment.reply(reply)
                                    already_done.append(comment.id)
                                    
                                image = Helpers.GetFrame(time, FFMPEG_BIN)
                                image.tofile('./Image.data')
                                pth='./Frozen'+str(counter)+'.png'
                                Helpers.ConvertToPNG(image,pth)
                                try:
                                    imgurURL = Helpers.UploadToImgur(pth, userID, userSecret)
                                    reply += "[Screen Grab at "+time+"]("+imgurURL+")\n\n"
                                except:
                                    print(LPrint('Something went wrong when uploading to imgur D:'))
                                    reply = ("Something went wrong when I tried to "
                                             "upload the image to imgur.\nPlease report this to "
                                             "my [Owner/Caretaker]"
                                             "(https://ssl.reddit.com/u/subconcussive)\n"
                                             "^(I am a bot that grabs screenshots from"
                                             "Frozen, contact my [Owner/Caretaker]"
                                             "(https://ssl.reddit.com/u/subconcussive)")
                                counter += 1
                        else:
                            reply = ("ERROR: Malformed/Unparsable Request\n\nCorrect "
                                     "formatting is as follows:\n\n    <Any Text>"
                                     "/u/FROZEN_BOT @time HH:MM:SS\n\nYou can "
                                     "request multiple images at once by adding "
                                     "additional @time HH:MM:SS lines.\n\n"
                                     "^(I am a bot that grabs screenshots from"
                                     "Frozen, contact my [Owner/Caretaker]"
                                     "(https://ssl.reddit.com/u/subconcussive)")
                            comment.reply(reply)
                            already_done.append(comment.id)
                    else:
                        args = comment.body.split('@')[1:]
                        if len(args) > 1:
                            reply = "Here's your screen grabs!\n\n"
                        else:
                            reply = "Here's your screen grab!\n\n"
                        counter = 0
                        for arg in args:
                            time = re.search(("([0-9]{1,2}:[0-9]{2}:[0-9]{2}|"
                                             "[0-9]{1,2}:[0-9]{2}|"
                                             "[0-9]{1,2})"),
                                             arg).group(0)
                            if len(time) == len('HH:MM:ss'):
                                _ = time
                            elif len(time) == len('H:MM:ss'):
                                time = "0"+time
                            elif len(time) == len('MM:ss'):
                                time = "00:"+time
                            elif len(time) == len('M:ss'):
                                time = "0"+time
                            elif len(time) == len('ss'):
                                time = "00:00:"+time
                            elif len(time) == len('s'):
                                time = "00:00:0"+time
                            else:
                                reply = ("ERROR: Malformed/Unparsable Request\n\nCorrect "
                                         "formatting is as follows:\n\n    <Any Text>"
                                         "/u/FROZEN_BOT @time HH:MM:SS\n\nYou can "
                                         "request multiple images at once by adding "
                                         "additional @time HH:MM:SS lines.\n\n"
                                         "^(I am a bot that grabs screenshots from"
                                         "Frozen, contact my [Owner/Caretaker]"
                                         "(https://ssl.reddit.com/u/subconcussive)")
                                comment.reply(reply)
                                already_done.append(comment.id)
                                
                            image = Helpers.GetFrame(time, FFMPEG_BIN)
                            image.tofile('./Image.data')
                            pth='./Frozen'+str(counter)+'.png'
                            Helpers.ConvertToPNG(image,pth)
                            try:
                                imgurURL = Helpers.UploadToImgur(pth, userID, userSecret)
                                reply += "[Screen Grab at "+time+"]("+imgurURL+")\n\n"
                            except:
                                print(LPrint('Something went wrong when uploading to imgur D:'))
                                reply = ("Something went wrong when I tried to "
                                         "upload the image to imgur.\n\nPlease report this to "
                                         "my [Owner/Caretaker]"
                                         "(https://ssl.reddit.com/u/subconcussive)\n\n"
                                         "^(I am a bot that grabs screenshots from"
                                         "Frozen, contact my [Owner/Caretaker]"
                                         "(https://ssl.reddit.com/u/subconcussive)")
                            counter += 1
                    #Check if the user has already commented in this thread
                    alreadyReplied = False
                    for commentReply in comment.replies:
                        try:
                            if (username.upper()==commentReply.author.name.upper()):
                                print(LPrint("One of my comments"))
                                print(LPrint("I've already commented in this thread"))
                                alreadyReplied = True
                            else:
                                _=1
                        except AttributeError:
                            _=1
                            #Someone Deleted this comment, I don't know if it was me.
                    if (not alreadyReplied) and (reply is not None) and (comment.id not in already_done):
                        try:
                            comment.reply(reply)
                        except:
                            import time
                            print(LPrint("Shit, I've hit the rate limit D:"))
                            time.sleep(600)
                            try:
                                comment.reply(reply)
                            except:
                                print(LPrint("Woah, I hit it again!"))
                                time.sleep(300)
                                try:
                                    comment.reply(reply)
                                except:
                                    print(LPrint("Skipping this one"))
                    else:
                        print(LPrint("Not replying to this comment"))
                                
                else:
                    print(LPrint("Not summoned on this comment"))
                
                print(bottomSep)
                already_done.append(comment.id)
    print("\n"+topSep)
    print(LPrint("Sleeping for a bit...")+'\n'+bottomSep)
    import time
    time.sleep(30)
    subreddit = None
    comments = None
    
# Seek and save as .RAW Logic
time = "00:34:33"
image = Helpers.GetFrame(time, FFMPEG_BIN)
image.tofile('./Image.data')
Helpers.ConvertToPNG(image)
