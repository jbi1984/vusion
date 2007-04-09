#!/usr/bin/env python

'''
          File: vusion/vusionerror.py
   Description: Error management interface for Vusion
       Licence: GNU General Public Licence 2.0
'''

import os,sys
import datetime

class vusionerror:
   notices = 0;
   def notice(self,module,desc):
      if self.notices == 1:
         timestamp = datetime.datetime.isoformat(datetime.datetime.now());
         print "[notice] [" + timestamp + "] Module: " + module + ", Message: " + desc;

   def warning(self,module,desc):
      timestamp = datetime.datetime.isoformat(datetime.datetime.now());
      print "[warning] [" + timestamp + "] Module: " + module + ", Message: " + desc;
   
   def fatal(self,module,desc):
      timestamp = datetime.datetime.isoformat(datetime.datetime.now());
      print "[FATAL ERROR] [" + timestamp + "] Module: " + module + ", Returned: " + desc;      
      sys.exit();
