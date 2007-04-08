#!/usr/bin/env python

'''
          File: vusion/conifg.py
   Description: Config Parser's for:
                - Vusion main configuration files
                - Vusion Show files
       Licence: GNU General Public Licence 2.0
'''

import os, sys
import xml.dom.minidom
import ConfigParser as cfgparser
from xml.dom.minidom import Node
import vusionerror

class XMLParser:
   file = None;
   author = None;
   title = None;
   description = None;
   fullscreen = False;
   dimensions = (0,0);
   defaults = {};
   notes = {1 : {}, 2 : {}, 3 : {}, 4 : {}, 5 : {}, 6 : {}, 7 : {}, 8 : {}, 9 : {}, 10 : {}, 11 : {}, 12 : {}, 13 : {}, 14 : {},15 : {},16 : {}};
   cc = {1 : {}, 2 : {}, 3 : {}, 4 : {}, 5 : {}, 6 : {}, 7 : {}, 8 : {}, 9 : {}, 10 : {}, 11 : {}, 12 : {}, 13 : {}, 14 : {},15 : {},16 : {}};
   
   def __init__(self,file):
      if (os.path.exists(file) == False):
         v = vusionerror.vusionerror();
         v.fatal("Show","Cannot load Vusion show.");
      else:
         self.file = xml.dom.minidom.parse(file);
         
         # Meta Data
         for node in self.file.getElementsByTagName("metadata"):
            self.author = str(node.getElementsByTagName("author")[0].childNodes[0].data);
            self.title = str(node.getElementsByTagName("title")[0].childNodes[0].data);
            self.description = str(node.getElementsByTagName("description")[0].childNodes[0].data);
         
         # Dimensions
         for node in self.file.getElementsByTagName("dimensions"):
            self.fullscreen = {
               "true" : True,
               "false" : False
            }[node.getAttribute("fullscreen")];
            
            d = node.childNodes[0].data;
            self.dimensions = (int(d.split("x")[0]),int(d.split("x")[1]));
         
         # Defaults   
         for node in self.file.getElementsByTagName("default"):
            gamma = node.getElementsByTagName("gamma")[0];
            self.defaults["gamma"] = float(gamma.getAttribute("all")); 
         
            self.defaults["transition"] = int(node.getElementsByTagName("transition")[0].getAttribute("value"));
            
            for surface in node.getElementsByTagName("surface"): 
               if surface.getAttribute("n") == "a":
                  self.defaults["surface_a"] = (str(surface.getAttribute("type")),str(surface.getAttribute("file")));
               else:
                  self.defaults["surface_b"] = (str(surface.getAttribute("type")),str(surface.getAttribute("file")));
         
         # MIDI
         for node in self.file.getElementsByTagName("midi"):
            # Note On/Off commands
            for node2 in node.getElementsByTagName("note"):
                 self.notes[int(node2.getAttribute("c"))][int(node2.getAttribute("n"))] = str(node2.getAttribute("action"));
            
            # CC
            for node2 in node.getElementsByTagName("cc"):
               self.cc[int(node2.getAttribute("c"))][int(node2.getAttribute("n"))] = str(node2.getAttribute("change"));
      
      self.file = None;
               
class ConfigParser:
   midi = None;
   window = None;
   keyboard = {};
   live = {};
   video = {};
   
   def __init__(self,file):
      if (os.path.exists(file) == False):
         v = vusionerror.vusionerror();
         v.fatal("Config","Cannot load configuration file.");
      config = cfgparser.ConfigParser();
      config.readfp(open(file));
      
      self.window = bool(config.getboolean("Window","single_mode"));
      self.midi = int(config.get("MIDI","device"));
      self.keyboard = {
         str(config.get("Keyboard","viewer_live")) : 'live',
         str(config.get("Keyboard","viewer_video")) : 'video',
         str(config.get("Keyboard","viewer_image")) : 'image',
         str(config.get("Keyboard","viewer_surface")) : 'surface',
         str(config.get("Keyboard","viewer_play_pause")) : 'playpause',
         str(config.get("Keyboard","viewer_stop")) : 'stop',
         str(config.get("Keyboard","display_quit")) : 'quit',
         str(config.get("Keyboard","display_fullscreen")) : 'fullscreen'
      }
      self.live = {
         'driver': str(config.get("Live","driver")),
         'device': str(config.get("Live","device")),
         'input': str(config.get("Live","input")),
         'freq': str(config.get("Live","freq"))
      }
      self.video = {
         'driver': str(config.get("Video","driver")),
         'seek_seconds': str(config.get("Video","seek_seconds")),
         'play_audio': bool(config.getboolean("Video","play_audio")),
         'infinite_loop': bool(config.getboolean("Video","infinite_loop")),
         'auto_start': bool(config.getboolean("Video","auto_start"))
      }