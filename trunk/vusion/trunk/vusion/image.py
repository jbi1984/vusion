#!/usr/bin/env python

'''
          File: vusion/video.py
   Description: Image displaying module for Vusion.
       Licence: GNU General Public Licence 2.0
'''

import os
import pygame
import vusionerror

class Image:
   surfaces = {};
        
   def createSurface(self,image):
      if (os.path.exists(image.split("?")[0]) == False):
         v = vusionerror.vusionerror();
         v.warning("Image","Image specified does not exist");
      else:
         if (len(image.split("?")) > 1):
            posx = int(image.split("?")[1].split("x")[0]);
            posy = int(image.split("?")[1].split("x")[1]);
            image = image.split("?")[0];
         else:
            posx = 0;
            posy = 0;
         self.surfaces[len(self.surfaces)] = (pygame.image.load(image),(posx,posy));
         return len(self.surfaces)-1;

   def fetchPosition(self,image):
      return self.surfaces[image][1];
   
   def fetchFrame(self,image,alpha):
      self.surfaces[image][0].set_alpha(alpha);
      return self.surfaces[image][0];
      
   def destroySurface(self,image):
      self.surfaces[image] = None;
      return True;   