#!/usr/bin/env python

'''
          File: vusion/live.py
   Description: Handles realtime video
                captured from, for example, a tv card
                for Vusion
       Licence: GNU General Public Licence 2.0
'''

import pygame, Image, ImageChops, math
import vusionerror
# This must change later on and only be imported
# if v4l is selected but since only V4l is supported
# its okay for now.

import v4l

class Live:
   driver = "v4l";
   surfaces = {};
   interfaces = {0: ("/dev/video",1)};
   dimensions = (0,0);
   
   def __init__(self,dimensions,driver,interfaces):
      if len(interfaces) > 0:
         self.interfaces = interfaces;

      self.dimensions = dimensions;
       
      # Make sure its a proper driver
      try:
         self.driver = {
            'video4linux': "v4l",            
         }[driver];
      except KeyError:
         v = vusionerror.vusionerror();
         v.warning("Live","Driver not supported, defaulting to v4l");
         self.driver = "v4l";         

   def createSurface(self,interface):
      if self.driver == "v4l":
         # Setup the surface
         interface = int(interface);
         self.surfaces[len(self.surfaces)] = {0:v4l.video(self.interfaces[interface][0]),1:0};
         i = len(self.surfaces) - 1;
         # Setup v4l image
         self.surfaces[i][0].setupImage(self.dimensions[0],self.dimensions[1],v4l.VIDEO_PALETTE_YUV420P, v4l.VIDEO_PALETTE_RGB24);

         # Select the correct interface
         interfaces = self.interfaces[interface];
         self.surfaces[i][0].setChannel(int(interfaces[1]));
         
         if int(interfaces[1]) != 1:
            self.surfaces[i][0].setFrequency(int(interfaces[2]));
                     
         # Begin queueing frames
         self.surfaces[i][0].preQueueFrames();
         
         # Return surface number
         return i;
      else:
         return False;
      
   def fetchFrame(self,surface,alpha):
      if self.driver == "v4l":
         output = self.surfaces[surface][0].getImage(int(self.surfaces[surface][1]));
         #im = pygame.image.fromstring(output,self.dimensions,"RGB");
         im = pygame.image.frombuffer(output,self.dimensions,"RGB");
         im.set_alpha(alpha);
         self.surfaces[surface][1] = self.surfaces[surface][0].queueFrame();
         return im;
      else:
         return False;
      
   def destroySurface(self,surface):
      self.surfaces[surface] = None;
