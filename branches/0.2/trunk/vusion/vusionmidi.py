#!/usr/bin/env python

'''
          File: vusion/vusionmidi.py
   Description: Handles the MIDI interface for Vusion
       Licence: GNU General Public Licence 2.0
'''

import time, pypm, array, math
import vusionerror

class VusionMIDI:
   notes = None;
   MidiIn = None;
   parent = None;
   v = vusionerror.vusionerror();
   
   def __init__(self,parent,device,notes,cc):
      pypm.Initialize();
      pypm.CountDevices();
      self.MidiIn = pypm.Input(device);
      self.parent = parent;
      self.notes = notes;
      self.cc = cc;

   def terminate(self):
      pypm.Terminate()

   def listen(self):
      while self.MidiIn.Poll():
         MidiData = self.MidiIn.Read(1);

         self.v.notice("MIDI In","channel: " + str(MidiData[0][0][0]) + " note:" + str(MidiData[0][0][1]) + " value: " + str(MidiData[0][0][2])); 

         # Note Data
         try:
            action = self.notes[MidiData[0][0][0] - 143][MidiData[0][0][1]];
            print action;
            if action.split("(")[0] == "quit":
               self.parent.quit();
            elif action.split("(")[0] == "live.capture_video":
               self.parent.live.capture_video();
            elif action.split("(")[0] == "video.control_playpause":
               self.parent.video.control_playpause(action.split("(")[1].replace(")","").replace("?",str(self.parent.surfaces[self.parent.trigger.surface][1])));
            elif action.split("(")[0] == "video.control_stop":
               self.parent.video.control_stop(action.split("(")[1].replace(")","").replace("?",str(self.parent.surfaces[self.parent.trigger.surface][1])));
            elif action.split("(")[0] == "video.control_seek_forward":
               self.parent.video.control_seek_forward(action.split("(")[1].replace(")","").replace("?",str(self.parent.surfaces[self.parent.trigger.surface][1])));
            elif action.split("(")[0] == "video.control_seek_backward":
               self.parent.video.control_seek_backward(action.split("(")[1].replace(")","").replace("?",str(self.parent.surfaces[self.parent.trigger.surface][1])));
            elif action.split("(")[0] == "trigger.live":
               self.parent.trigger.live(action.split("(")[1].replace(")",""));
            elif action.split("(")[0] == "trigger.video":
               self.parent.trigger.video(action.split("(")[1].replace(")",""));
            elif action.split("(")[0] == "trigger.image":
               self.parent.trigger.live(action.split("(")[1].replace(")",""));
            elif action.split("(")[0] == "trigger.select_surface_a":
               self.parent.trigger.select_surface_a();
            elif action.split("(")[0] == "trigger.select_surface_b":
               self.parent.trigger.select_surface_b();
         except KeyError:
            pass;
            
         # CC Data
         try:
            action = self.cc[MidiData[0][0][0] - 175][MidiData[0][0][1]];
            if action == "transition":
               self.parent.transition(MidiData[0][0][2]);
            elif action == "gamma":
               self.parent.gamma_all(MidiData[0][0][2])
         except KeyError:
            pass;