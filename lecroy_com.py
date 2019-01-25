
#telnet connection to lecroy power supply

import telnetlib
import time

class lecroy_com:
  #_____________________________________________________________________________
  def __init__(self, port):
    #commands queue
    self.queue = []
    #busy flags
    self.busy = False
    self.asyn = False
    self.in_put_cmd = False
    #open telnet connection at a given port
    self.tcom = telnetlib.Telnet()
    self.tcom.open("scserv.starp.bnl.gov", port)
    print self.put_cmd_sync("1450")
  #_____________________________________________________________________________
  def put_cmd(self, cmd=""):
    #asynchronous command
    if cmd != "": self.queue.append(cmd)
    #only one instance since now
    if self.in_put_cmd == True: return
    #lock the instance
    self.in_put_cmd = True
    #wait for synchronous command to finish
    while self.busy == True: time.sleep(0.1)
    #process the command queue
    while len(self.queue) > 0:
      #skip if synchronous command was issued
      if self.busy == True:
        break
      #raise asyn bysy flag
      self.asyn = True
      self.run_cmd(self.queue.pop(0))
      self.asyn = False
    #unlock the instance
    self.in_put_cmd = False
  #_____________________________________________________________________________
  def put_cmd_sync(self, cmd):
    #synchronous command, expected to run at regular intervals
    self.busy = True
    #wait for asynchronous command in proggress
    while self.asyn == True: time.sleep(0.1)
    #process the command, capture the response
    resp = self.run_cmd(cmd)
    #print resp
    self.busy = False
    #finish any asynchronous commands
    self.put_cmd()
    return resp
  #_____________________________________________________________________________
  def run_cmd(self, cmd):
    #put command to telnet
    cmd += "\r"
    for char in cmd:
      self.tcom.write(char)
      self.tcom.read_until(char)
    return self.tcom.read_until(">", 4).replace("\r\x0c", " ")
