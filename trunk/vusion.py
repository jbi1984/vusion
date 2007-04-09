#!/usr/bin/env python2.4
import os, sys, pygame, array, time, Image, ImageChops, math, signal
import Numeric as N
import pygame.surfarray as surfarray
from pygame.time import *
from pygame.locals import *
from vusion import vusionerror, vusionmidi, live, video, image, trigger, config, gui

##############################################
#                                            #
#   Vusion 0.2  - Realtime Video Mixer       #
#   Created by Christopher Stranex           #
#   Under the GNU General Public Licence     #
#   Contact: chris@sa.web.za                 #
#                                            #
##############################################

'''
USAGE:   
   $ vusion show_file [cfg_file]
      show_file - Vusion XML Show file
      cfg_file - Vusion configuration file (default: /etc/vusion/vusion.conf)
   
   $ vusion --version
      Vusion version information
   
   $ vusion --configure
      Loads configuration GUI
      
   $ vusion-editor
      Loads XML Show GUI
      
   $ rmrf-software vusion [--uninstall | --upgrade]
      Loads the rm-rf Software Manager and shows vusion.      
'''

class Vusion:
   cfg = None
   show = None
   vmidi = None
   live = None
   video = None
   trigger = None
   image = None
   gui = None
   surfaces = { 'A' : (None,None), 'B' : (None,None) }
   surface = { 'A': None, 'B' : None, 'Screen' : None }
  
   def __init__(self):
      arg = sys.argv;
      if len(arg) > 2:
         # parse the non-default configuration file
         self.cfg = config.ConfigParser(arg[2]);
         self.show = config.XMLParser(arg[1]);
      else:
         # use the default configuration file
         self.cfg = config.ConfigParser("/etc/vusion/vusion.conf");
         self.show = config.XMLParser(arg[1]);

      # Load all Vusion modules
      self.vmidi = vusionmidi.VusionMIDI(self,self.cfg.midi,self.show.notes,self.show.cc);
      # Setup Live's interfaces
      intf = {};
      i = 0;
      for interface in self.cfg.live['device'].split(";"):
         intf[len(intf)] = (interface,self.cfg.live['input'].split(";")[i],self.cfg.live['freq'].split(";")[i]);         
         i=i+1; 
      self.live = live.Live(self.show.dimensions,self.cfg.video['driver'],intf);
      self.video = video.Video(self.show.dimensions,self.cfg.video['driver'],self.cfg.video['seek_seconds'],self.cfg.video['play_audio'],self.cfg.video['infinite_loop'],self.cfg.video['auto_start']);
      self.image = image.Image();
      
      self.trigger = trigger.Trigger(self);

      if self.cfg.window == False:
         # Load the gui for the other screen. This is done by calling gui
         self.gui = gui.PreviewGUI(self);
      
      pygame.init();
      pygame.display.set_caption("Vusion 0.2")
      pygame.display.set_icon(pygame.image.load('images/logo.png'));
      pygame.mouse.set_visible(False);
      pygame.mixer.quit();

      if self.show.fullscreen == True:
         self.surface['Screen'] = pygame.display.set_mode(self.show.dimensions,pygame.FULLSCREEN);
      else:
         self.surface['Screen'] = pygame.display.set_mode(self.show.dimensions);
      self.trigger._rect(pygame.Rect(self.surface['Screen'].get_rect()));

      self.surface['A'] = pygame.Surface(self.show.dimensions,0,24);
      self.surface['A'].fill((0,0,0))
      self.surface['A'].set_alpha(128);

      self.surface['B'] = pygame.Surface(self.show.dimensions,0,24);
      self.surface['B'].fill((0,0,0))
      self.surface['B'].set_alpha(128);
      
      # Read the default part of the show file and do:
      # setup default for surface a      
      self.trigger.select_surface_a();
      if self.show.defaults['surface_a'][0] == "live":
         self.trigger.live(self.show.defaults['surface_a'][1]);
      elif self.show.defaults['surface_a'][0] == "video":
         self.trigger.video(self.show.defaults['surface_a'][1]);
      else:
         self.trigger.image(self.show.defaults['surface_a'][1]);

      # setup default for surface b      
      self.trigger.select_surface_b();
      if self.show.defaults['surface_b'][0] == "live":
         self.trigger.live(self.show.defaults['surface_b'][1]);
      elif self.show.defaults['surface_b'][0] == "video":
         self.trigger.video(self.show.defaults['surface_b'][1]);
      else:
         self.trigger.image(self.show.defaults['surface_b'][1]);
         
      # default brightness + transition position
      self.transition(self.show.defaults['transition']);
      self.gamma_all(float(self.show.defaults['gamma'] * 14.285714286));


   def gamma_all(self,value):
      pygame.display.set_gamma(int(value*0.07));

   def transition(self,value):
      value = int(value*2);
      self.surface['A'].set_alpha(value);
      self.surface['B'].set_alpha(255-value);

   def quit(self):
      # Destroy active surfaces
      self.trigger.destroy('A');
      self.trigger.destroy('B');
      if self.gui != None:
         os.kill(self.gui.pid,signal.SIGTERM);
      pygame.display.quit();
      sys.exit(0);
 
   def main(self):
      # The main loop
      while True:
         # Prepare surface A and B
         for surface in self.surfaces:
            if self.surfaces[surface][0] == "live":
               self.surface[surface].blit(self.live.fetchFrame(self.surfaces[surface][1],self.surface[surface].get_alpha()),(0,0));
            if self.surfaces[surface][0] == "image":
               pos = self.image.fetchPosition(self.surfaces[surface][1]);
               self.surface[surface].blit(self.image.fetchFrame(self.surfaces[surface][1],self.surface[surface].get_alpha()),pos);
     
         # The Blitting section
         self.surface['Screen'].fill((255,255,255));
         self.surface['Screen'].blit(self.surface['A'],(0,0));
         self.surface['Screen'].blit(self.surface['B'],(0,0));
         pygame.display.flip();
         self.vmidi.listen();
         
         # check for key presses
         if self.gui != None:
            self.gui.keys();
         
if (__name__ == '__main__'):
    app = Vusion()
    app.main()
