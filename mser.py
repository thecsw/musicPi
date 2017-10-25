#TODO:
#1. Make a variable to store the musics' destination/folder/directory
#2. Get rid of the mutagen, not needed. Became redundant
import os
import sys
import time
#Mutagen to get the length of mp3 files, not important!
from mutagen.mp3 import MP3
import telepot
from telepot.loop import MessageLoop
#Telegram bot key
key = ''
bot = telepot.Bot(key)
#THis is the queue that we will be storing everything
q = []
#So the app would send the QUEUE IS EMPTY n times, just once
empty = False
#The varibale to hold listing
a = os.listdir('Music')
#THis one will hold the archive, that will be outputed
listall = """Music archive."""
#List all music in the directory
for i in range(0, len(a)):
    audio = MP3('Music/{}'.format(a[i]))
    length = audio.info.length
    print('{}.{}'.format(i, a[i]))
    print('Length - {} secs'.format(length))
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
    #Insert from the tail
    q.insert(0, command)
    print('Inserted new song - {}'.format(a[int(command)]))
    print('Total queue size - {}'.format(len(q)))
    reply(user_id, msg_id, 'Song - {} has been inserted into the queue.\n\
Your place in the queue - {}'.format(
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
            audio = MP3('Music/{}'.format(a[int(song)]))
            length = audio.info.length
            print('Successfully popped song - {}'.format(a[int(song)]))
            print('Total queue size - {}'.format(len(q)))
            os.system('mpv --no-video Music/\'{}\''.format(
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
