#!/usr/bin/env python
import RPi.GPIO as GPIO
import sys
import vlc
import glob
import time
import signal

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.output(7,True)

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }
hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '-'  }
fp = open('/dev/hidraw0', 'rb')

## Play MP3 Files
music_folder = "/home/pi/jukebox/library/"
music = None

mlp = vlc.MediaListPlayer()
mp = vlc.MediaPlayer()
mlp.set_media_player(mp)

def vlcEvent(event):
   print "vlcEvent: ", event.type, event.u

mlp_em = mlp.event_manager()
mlp_em.event_attach(vlc.EventType.MediaListPlayerNextItemSet, vlcEvent)
 
mp_em = mp.event_manager()
mp_em.event_attach(vlc.EventType.MediaPlayerEndReached, vlcEvent)
mp_em.event_attach(vlc.EventType.MediaPlayerMediaChanged, vlcEvent)

def play(title):
   mlp.stop()
   ml = vlc.MediaList()
   print "play: " + title
   album_path = music_folder + title
   print album_path
   files = glob.glob(album_path + "/*.m*")
   files.sort()
   for file in files:
      ml.add_media(file)
      print file

   mlp.set_media_list(ml)
   mlp.play()

def playChapter(title):
   print "play from chapter: " + title
   mlp.stop()
   ml = vlc.MediaList()
   album_path = music_folder + title.split("-")[0]
   print album_path
   jumpChapter = title.split("-")[1]
   print "chapter: " + jumpChapter
   files = glob.glob(album_path + "/*.m*")
   files.sort()
   album_path_length = len(album_path) + 1
   for file in files:
      file_name = file[album_path_length:]
      print "file: " + file_name
      if int(file_name[:2]) >= int(jumpChapter):
         ml.add_media(file)
         print "add: " + file
   mlp.set_media_list(ml)
   mlp.play()

## Scaning Barcode
ss = ""
shift = False

done = False

while True:
   try:
      ## Get the character from the HID
      buffer = fp.read(8)
      for c in buffer:
         if ord(c) > 0:

            ##  40 is carriage return which signifies
            ##  we are done looking for characters
            if int(ord(c)) == 40:
               #done = True
               if "CMD" in ss:
                  print ss
                  if ss == "CMD-NEXT":
                     print "next"
                     mlp.next()
                  if ss == "CMD-STOP":
                     print "stop"
                     mlp.stop()
                  if ss == "CMD-PLAY":
                     print "play"
                     mlp.play()
                  if ss == "CMD-PAUSE":
                     print "pause"
                     mlp.pause()
                  if ss == "CMD-PREV":
                     print "previous"
                     mlp.previous()
                  ss = ""
                  break;
               elif "-" in ss:
                  print "chapter scan: " + ss
                  playChapter(ss)
                  ss = ""
                  break;
               else:
                  play(ss)
                  ss = ""
                  break;

            ##  If we are shifted then we have to 
            ##  use the hid2 characters.
            if shift: 

               ## If it is a '2' then it is the shift key
               if int(ord(c)) == 2 :
                  shift = True

               ## if not a 2 then lookup the mapping
               else:
                  ss += hid2[ int(ord(c)) ]
                  shift = False

            ##  If we are not shifted then use
            ##  the hid characters

            else:

               ## If it is a '2' then it is the shift key
               if int(ord(c)) == 2 :
                  shift = True

               ## if not a 2 then lookup the mapping
               else:
                  ss += hid[ int(ord(c)) ]
          
   except KeyboardInterrupt:
      GPIO.cleanup()
      sys.exit()  
print ss