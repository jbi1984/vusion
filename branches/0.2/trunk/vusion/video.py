#!/usr/bin/env python

'''
          File: vusion/video.py
   Description: Video processing module for Vusion.
       Licence: GNU General Public Licence 2.0

   Drivers:
      pygame  - MPEG-1 Video Playback only

'''

import os
import pygame
import vusionerror

class Video:
   driver = "pygame";
   seekOffset = 2;
   playAudio = True;
   InfiniteLoop = False;
   AutoPlay = True;
   dimensions = (0,0);
   surfaces = {};
   
   def __init__(self,dimensions,driver,seekOffset,playAudio,loop,AutoPlay):
      self.dimensions = dimensions;
      self.seekOffset = float(seekOffset);
      self.playAudio = bool(playAudio);
      self.InfiniteLoop = int(loop);
      self.AutoPlay = bool(AutoPlay);
      
      try:
         self.driver = {
            "pygame" : "pygame"
         }
      except KeyError:
         v = vusionerror.vusionerror();
         v.warning("Video","Driver not supported, defaulting to pygame");
         self.driver = "pygame";
      
   def createSurface(self,video,surface,rect):
      if (os.path.exists(video) == False):
         v = vusionerror.vusionerror();
         v.warning("Video","Video specified does not exist");
         return False;
      else:
         self.surfaces[len(self.surfaces)] = pygame.movie.Movie(video);
         i = len(self.surfaces) - 1;
         self.surfaces[i].set_display(surface,rect);
         self.surfaces[i].stop();
         self.surfaces[i].rewind();
         if self.AutoPlay == True:
            if self.InfiniteLoop == True:
               self.surfaces[i].play(-1);
            else:
               self.surfaces[i].play();
         if self.playAudio == False:
            self.surfaces[i].set_volume(0.0);
         return i;

   def destroySurface(self,video):
      self.surfaces[video] = None;
      return True;


   # Seek forward in the video      
   def control_seek_forward(self,video):
      video = int(video);
      try:
         self.surfaces[video].skip(self.seekOffset);
      except KeyError:
         pass;
   
   # Seek backward in the video
   def control_seek_backward(self,video):
      video = int(video);
      try:
         seek = self.surfaces[video].get_time() - self.seekOffset;
         self.surfaces[video].rewind();
         self.surfaces[video].skip(seek);
      except KeyError:
         pass;
   
   # Play/pause the video
   def control_playpause(self,video):
      video = int(video);
      try:
         if self.surfaces[video].get_busy() == True:
            self.surfaces[video].pause();
         else:
            self.surfaces[video].play();
      except KeyError:
         pass;
   
   # Stop the video
   def control_stop(self,video):
      video = int(video);      
      try:
         self.surfaces[video].stop();
      except KeyError:
         pass;
