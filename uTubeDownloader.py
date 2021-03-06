#!/usr/bin/env python
# -*- coding: utf8 -*-

#______________________________________________________________________________________________________
#Name   : uTubeDownloader
#Licence: GPL3 (http://www.gnu.org/licenses/gpl.html), Youtube-dl have their recspective licence, please see their man page
#Author : John Skoteiniotis
#Email  : j0hnskot (at) gmail.com 
#Date   : 13-09-2011 (first release 9-9-2011)
#Version: 0.02
#Source Code: Everything below those comments is the sourcecode 
#Description:
#This simple script is a gui that will make the use of youtube-dl more user-friendly. 
#______________________________________________________________________________________________________

import os
import sys
import time
import subprocess
from threading import Thread
import pygtk
import glib
import gtk, gobject
pygtk.require('2.0')
import gtk

#Variables
playlist=False
quality="18"
url=""
z=""
onlySound=""
speedLimitEnabled=False
speedLimitEntry=gtk.Entry()
speedLimit="0"
downloading=False
progressLabel = gtk.Label("Loading..")
window = gtk.Window(gtk.WINDOW_TOPLEVEL)
entry = gtk.Entry()
isChannel=False
channelName=""
ifl=""
##



class uTubeDownloader:

    def iflOn(self ,widget , data=None):
        ##I Feel Lucky feature
        global ifl
        if ifl=="":
            ifl="ytsearch:"
        else:
            ifl=""

    def isChannelOn(self ,widget , data=None):
        global isChannel
        global channelName
        if isChannel==True:
            isChannel=False
            channelName=""
            print "if  " +channelName
        else:
            isChannel=True
            channelName="ytuser:"
            print "else   " +channelName


    def onlySoundOn(self ,widget , data=None):
        global onlySound

        if onlySound=="":
            onlySound="--extract-audio --audio-format \"vorbis\""

        else:
            onlySound=""


    def speedLimitEnabled(self ,widget , data=None):
        global speedLimitEnabled

        if speedLimitEnabled==False:
            speedLimitEnabled=True
        else:
            speedLimitEnabled=False
            speedLimit=0
    def isPlaylist(self, widget, data=None):

        global playlist

        if playlist==False:
            playlist=True
        else:
            playlist=False
        #print playlist

    def checkPlaylist(self):
        global url
        if -1!=url.find("list="):
            url=url[(url.find("list="))+5:(url.find("list="))+5+18]
        elif -1!=url.find("p="):
            url= url[(url.find("p="))+2:(url.find("p="))+2+18]
        else:
            print "its not a playlist"

    def setQuality(self, widget, data=None):
        global quality
        if data=="720p":
            quality="22"
        elif data=="1080p":
            quality="37"
        else:
            quality="18"

    def downloadStart(self,widget,data=None):
        global downloading
        if downloading!=True:
                downloadThread=Thread(target = self.download)
                downloadThread.start()
                downloadThread.join(1)
        else: 
                print "not ready"

    def download(self):
        
        global url
        global quality
        global playlist
        global downloading
        global speedLimitEnabled
        global speedLimit
        global channelName
        global onlySound
        print "Channel " + channelName

        if playlist==True:
            downloading=True
            self.checkPlaylist()
            if speedLimitEnabled==True:

                print "speedLimitEnabled"
                self.p=subprocess.Popen(["modules/youtube-dl "+onlySound+" -t --max-quality "+quality+" --rate-limit="+speedLimit+" www.youtube.com/view_play_list?p="+url],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            else:

                print "speedLimitNotEnabled"
                self.p=subprocess.Popen(["modules/youtube-dl "+onlySound+" -t --max-quality "+quality+" www.youtube.com/view_play_list?p="+url],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   
        else:
            global z
            downloading=True
            if speedLimitEnabled==True:
                self.p=subprocess.Popen(["modules/youtube-dl "+onlySound+" -t --max-quality "+quality+" "+"--rate-limit="+speedLimit+" \""+channelName+ifl+url+"\""],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                self.p=subprocess.Popen(["modules/youtube-dl "+onlySound+" -t --max-quality "+quality+" \""+channelName+ifl+url+"\""],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.makeProgressWindow()
        for line in iter(self.p.stdout.readline,""):
           global progressLabel
           global z
           z=line
           time.sleep(1)
           print z
           gobject.idle_add(self.updateProgressWindow)


    def updateProgressWindow(self):
        global progressLabel
        global z
        global downloading
        if downloading==True:
            if z.strip()!='1':
                progressLabel.set_text(z)
            elif z.strip()=='1' and playlist!=True:
                progressLabel.set_text("Download is complete. You can now close this window!")
                downloading=False;
    def makeProgressWindow(self):
        global window
        global z
        dialog = gtk.Dialog(title="Progress:", parent=window, flags=0, buttons=None)
        global progressLabel
        dialog.vbox.pack_start(progressLabel, True, True, 0)
        progressLabel.set_text("")
        progressLabel.show()
        dialog.show_all()

    def update(self, widget, data=None):

        subprocess.Popen(["modules/youtube-dl","-U"])


    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def speedLimitSet(self, widget, entry):
        global speedLimit
        speedLimit = speedLimitEntry.get_text()+"k"
        print speedLimitEntry.get_text()
        speedLimitEntry.set_text(speedLimitEntry.get_text())
        print speedLimit

    def enter_callback(self, widget, entry):
        global url
        url = entry.get_text()
        print entry.get_text()
        entry.set_text(entry.get_text())
        print url

    def __init__(self):
        global window
        
        window.set_size_request(640, 480)
        window.set_title("uTubeDownloader v0.04")
        window.set_border_width(10)
        vbox= gtk.VBox(False,10)
        window.add(vbox)
        vbox.show()
                
        #url box#
        global entry
        entry.set_max_length(0)
        entry.connect("changed", self.enter_callback, entry)
        entry.set_editable(True)
        entry.set_visibility(True)
        entry.select_region(0, len(entry.get_text()))
        vbox.pack_start(entry, True, True, 0)
        entry.show()

        playListButton = gtk.CheckButton("Playlist")
        playListButton.connect("toggled", self.isPlaylist, None)
        vbox.pack_start(playListButton, True, True, 2)
        playListButton.show()

        mp3Button = gtk.CheckButton("Only Sound")
        mp3Button.connect("toggled", self.onlySoundOn, None)
        vbox.pack_start(mp3Button, True, True, 2)
        mp3Button.show()

        channelButton = gtk.CheckButton("Channel")
        channelButton.connect("toggled", self.isChannelOn, None)
        vbox.pack_start(channelButton, True, True, 2)
        channelButton.show()

        iflButton = gtk.CheckButton("I feel Lucky!")
        iflButton.connect("toggled", self.iflOn, None)
        vbox.pack_start(iflButton, True, True, 2)
        iflButton.show()

        dlbutton = gtk.Button("Download")
        updateButton = gtk.Button("Αναβάθμηση του youtube-dl")
        dlbutton.connect("clicked", self.downloadStart, None)
        updateButton.connect("clicked", self.update, None)

        separator = gtk.HSeparator()
        vbox.pack_start(separator, False, True, 0)
        separator.show()

        vbox.add(dlbutton)
        vbox.add(updateButton)

        separator = gtk.HSeparator()
        vbox.pack_start(separator, False, True, 0)
        separator.show()
        #Quality buttons#
        Rbutton1 = gtk.RadioButton(None, "480p")
        Rbutton1.connect("toggled", self.setQuality, "480p")
        vbox.pack_start(Rbutton1, True, True, 0)
        Rbutton1.show()
        Rbutton2 = gtk.RadioButton(Rbutton1, "720p")
        Rbutton2.connect("toggled", self.setQuality, "720p")
        vbox.pack_start(Rbutton2, True, True, 0)
        Rbutton2.show()
        Rbutton3 = gtk.RadioButton(Rbutton1, "1080p")
        Rbutton3.connect("toggled", self.setQuality, "1080p")
        vbox.pack_start(Rbutton3, True, True, 0)
        Rbutton3.show()
        #SpeedLimit
        speedLimitButton = gtk.CheckButton("SpeedLimit")
        speedLimitButton.connect("toggled", self.speedLimitEnabled, None)
        vbox.pack_start(speedLimitButton, True, True, 2)
        speedLimitButton.show()
        global speedLimitEntry
        speedLimitEntry.set_max_length(10)
        speedLimitEntry.connect("changed", self.speedLimitSet, speedLimitEntry)
        speedLimitEntry.set_editable(True)
        speedLimitEntry.set_visibility(True)
        speedLimitEntry.select_region(0, len(speedLimitEntry.get_text()))
        vbox.pack_start(speedLimitEntry, True, True, 0)
        speedLimitEntry.show()
        
        dlbutton.show()
        #updateButton.show()
        window.show()
        gtk.gdk.threads_init()
    def main(self):

        gtk.main()
       

if __name__ == "__main__":
    downloader = uTubeDownloader()
    gtk.gdk.threads_enter()
    downloader.main()
    gtk.gdk.threads_leave()

