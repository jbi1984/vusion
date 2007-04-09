#!/usr/bin/env python

'''
          File: vusion/gui.py
   Description: Classes and functions related to the Preview Window for Vusion
       Licence: GNU General Public Licence 2.0
'''

import os, sys, time, signal
import pygame
from pygame.locals import *
import vusionerror, live, video, image, trigger, config, gui

class PreviewGUI:
   # Basically we are here to create a gtk window on the right. We forking the process here btw.
   display = None;
   parent = None;
   action = None;
   surface = {1: None, 2: None, 3: None};
   surfaces = {1: (None,None), 2: (None,None), 3: (None,None), 'active': (None,None)};
   pid = None;

   def __init__(self,parent):
      self.parent = parent;
      pid = os.fork();
      if pid:
         # Sleep so the user can move the mouse to where he wants. yes, we know its a little stupid but
         # hey.. sue us.
         self.pid = pid;
         time.sleep(5);
      else:
         # Child process
         self.pid = os.getpid();
         pygame.init();
         pygame.display.set_caption("Vusion 0.2 :: Preview Window")
         pygame.display.set_icon(pygame.image.load('images/logo.png'));
         pygame.mouse.set_visible(False);
         pygame.mixer.quit();
         self.surface[1] = pygame.Surface((320,240),0,24);
         self.surface[2] = pygame.Surface((320,240),0,24);
         self.surface[3] = pygame.Surface((320,240),0,24);
         self.surface[1].fill((255,0,0));
         self.surface[2].fill((0,255,0));
         self.surface[3].fill((0,0,255));
         self.display = pygame.display.set_mode((640,480));
         while 1:
            self.process_data();
            if self.surfaces[1][0] == "live":
               self.surface[1].blit(self.live.fetchFrame(self.surfaces[1][1],self.surface[1].get_alpha()),(0,0));
            if self.surfaces[2][0] == "live":
               self.surface[2].blit(self.live.fetchFrame(self.surfaces[2][1],self.surface[2].get_alpha()),(0,0));            
            if self.surfaces[3][0] == "live":
               self.surface[3].blit(self.live.fetchFrame(self.surfaces[3][1],self.surface[3].get_alpha()),(0,0));
               
            self.display.blit(self.surface[1],(0,0));
            self.display.blit(self.surface[2],(320,0));
            self.display.blit(self.surface[3],(320,240));
            pygame.display.flip();            

   def process_data(self):
      # Open /tmp/vusion.PID
      if os.path.exists("/tmp/vusion." + str(self.pid)):
         # read and do action
         action = file("/tmp/vusion." + str(self.pid),'r');
         for line in action:
            l = line.strip();
            if l.split(":")[0] == "surface":
               if int(l.split(":")[1]) < 4:
                  self.surfaces['active'] = int(l.split(":")[1]);
               else:
                  v = vusionerror.vusionerror();
                  v.warning('GUI','Surface out of range');
            if l.split(":")[0] == "live":            
               i = self.live.createSurface(int(l.split(":")[1]));
               self.surfaces[self.surfaces['active']] = ("live",i);
         action.close();
         action = file("/tmp/vusion." + str(self.pid),'w');
         action.write("");
         action.close();
         
   def toggle_fullscreen(self):
      if self.parent.show.fullscreen == True:
         self.parent.surface['Screen'] = pygame.display.set_mode(self.parent.show.dimensions);
         self.parent.show.fullscreen = False;      
      else:
         self.parent.surface['Screen'] = pygame.display.set_mode(self.parent.show.dimensions,pygame.FULLSCREEN);
         self.parent.show.fullscreen = True;
      self.parent.trigger._rect(pygame.Rect(self.parent.surface['Screen'].get_rect()));

   def doevent(self,action,value=-1):
      if action == 'fullscreen':
         self.toggle_fullscreen();
      elif action == 'quit':
         self.parent.quit();
         
      if value > -1:
         store = file("/tmp/vusion." + str(self.pid),'w');
         store.write(action + ':' + str(value));
         store.close();

   def keys(self):
      pygame.event.pump();
      events = pygame.event.get([pygame.KEYDOWN]);
      for event in events:
         # wtf do we do now?
         try:
            self.action = self.parent.cfg.keyboard[str(event.unicode)];
            self.doevent(self.action);
         except KeyError:
            try:
               if int(event.unicode) < 10:
                  self.doevent(self.action,event.unicode);
            except ValueError:
               pass;
      pygame.event.clear();
