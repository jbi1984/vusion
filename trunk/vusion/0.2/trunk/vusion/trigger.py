#!/usr/bin/env python

'''
          File: vusion/trigger.py
   Description: Handle triggering of video files with the MIDI Controller.
       Licence: GNU General Public Licence 2.0
'''

import vusionerror

class Trigger:
   surface = 'A';
   parent = None;
   rect = None;
   
   def __init__(self,parent):
      self.parent = parent;

   def _rect(self,rect):
      self.rect = rect;
      
   def select_surface_a(self):
      self.surface = 'A';
      print 'selected surface A';
      
   def select_surface_b(self):
      self.surface = 'B';
      print 'selected surface B';
      
   def live(self,index):
      i = self.parent.live.createSurface(index);
      self.destroy();
      self.parent.surfaces[self.surface] = ("live",i);

   def video(self,file):
      i = self.parent.video.createSurface(file,self.parent.surface[self.surface],self.rect);
      self.destroy();
      self.parent.surfaces[self.surface] = ("video",i);
      
   def image(self,file):
      i = self.parent.image.createSurface(file);
      self.destroy();
      self.parent.surfaces[self.surface] = ("image",i);

   def destroy(self,surface=None):
      if surface == None:
         surface = self.surface;

      if self.parent.surfaces[surface][0] == "live":
         self.parent.live.destroySurface(self.parent.surfaces[surface][1]);
      if self.parent.surfaces[surface][0] == "video":
         self.parent.video.destroySurface(self.parent.surfaces[surface][1]);
      if self.parent.surfaces[surface][0] == "image":
         self.parent.image.destroySurface(self.parent.surfaces[surface][1]);
