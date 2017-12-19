#TODO:
#1. Make a variable to store the musics' destination/folder/directory DONE
#2. Get rid of the mutagen, not needed. Became redundant DONE
import os
import sys
import time
import telepot
from telepot.loop import MessageLoop
import config

#Telegram bot key
bot = telepot.Bot(config.key)
#THis is the queue that we will be storing everything
q = []
#So the app would send the QUEUE IS EMPTY n times, just once
empty = False
#The varibale to hold listing
a = os.listdir("/media/pi/MUSICPI")
#THis one will hold the archive, that will be outputed
listall = """Music archive."""
#List all music in the directory
for i in range(0, len(a)):
    print('{}.{}'.format(i, a[i]))
    listall = listall + '\n{}.{}'.format(i, a[i])

# Send message to user with their user ID
def sms(ID, str):
        bot.sendMessage(ID, str)

# Reply message to user with their user ID and to the message ID    
def reply(ID, msgID, str):
        bot.sendMessage(ID, str, None, None, None, msgID)

# Handling all new messages, like the getUpdates()
def handle(msg):
    user_id = msg['chat']['id']
    msg_id = msg['message_id']
    command = msg['text'].encode('utf-8')
    #Output the whole directory
    if command == '/help':
        sms(user_id, listall)
        return

    try:
        numba = int(command)
    except:
        sms(user_id, "Not a number!")
        return
        
    if int(command) > (len(a) - 1):
        print("Out of range!")
        sms(user_id, "Out of range, please enter values from 0 to {}".format(len(a)-1))
        return
    #Insert from the tail
    if a[int(command)] == "System Volume Information":
        sms(user_id, "A song, not a folder!")
        return
    q.insert(0, command)
    print('Inserted new song - {}'.format(a[int(command)]))
    print('Total queue size - {}'.format(len(q)))
    reply(user_id, msg_id, "Song - {} has been inserted into the queue.\n\
Your place in the queue - {}".format(
    a[int(command)],
    len(q)
    ))

#Checking for new messages
MessageLoop(bot, handle).run_as_thread()

#Now if the queue is bigger than 0, then pop the 0 element and start playing, repeat
while 1:
    if (len(q)>0):
        try:
            empty = False
            song = q.pop()
            print("Successfully popped song - {}".format(a[int(song)]))
            print("Total queue size - {}".format(len(q)))
            os.system("mpv --no-video /media/pi/MUSICPI/\"{}\"".format(
                a[int(song)]
            ))
        except:
            print('ERROR')
    else:
        #if it's empty
        if empty == False:
            print('Queue is empty. Nothing to play')
            empty = True
        time.sleep(1)
