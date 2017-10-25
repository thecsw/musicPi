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
listall = """Music archive."""

for i in range(0, len(a)):
    audio = MP3('Music/{}'.format(a[i]))
    length = audio.info.length
    print('{}.{}'.format(i, a[i]))
    print('Length - {} secs'.format(length))
    listall = listall + '\n{}.{}'.format(i, a[i])
    
def sms(ID, str):
        bot.sendMessage(ID, str)
    
def reply(ID, msgID, str):
        bot.sendMessage(ID, str, None, None, None, msgID)
    
def handle(msg):
    user_id = msg['chat']['id']
    msg_id = msg['message_id']
    command = msg['text'].encode('utf-8')
    
    if command == '/help':
        sms(user_id, listall)
        return
    
    q.insert(0, command)
    print('Inserted new song - {}'.format(a[int(command)]))
    print('Total queue size - {}'.format(len(q)))
    reply(user_id, msg_id, 'Song - {} has been inserted into the queue.\n\
Your place in the queue - {}'.format(
    a[int(command)],
    len(q)
    ))
    
MessageLoop(bot, handle).run_as_thread()
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
        if empty == False:
            print('Queue is empty. Nothing to play')
            empty = True
        time.sleep(1)
