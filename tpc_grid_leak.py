
from softioc import builder
from mainframe import mainframe
import time
import threading

from datetime import datetime

builder.SetDeviceName("tpc_grid_leak")

#create mainframe object, set telnet port
mf = mainframe(9038)

#_____________________________________________________________________________
def do_monit():
  while True:
    time.sleep(3)
    #print "before: ", datetime.now()
    mf.do_read()
    #print "after: ", datetime.now()

#_____________________________________________________________________________
def loop_monit():
  #initialize lecroy mainframe from config file
  mf.init_config()
  #periodically read measured current and voltage
  tid = threading.Thread(target=do_monit)
  tid.start()

