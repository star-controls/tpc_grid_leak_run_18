
from board import board
from channel import channel
from lecroy_com import lecroy_com
from watchdog import watchdog
import pandas
from softioc import builder, alarm

class mainframe:
  #_____________________________________________________________________________
  def __init__(self, port):
    #telnet communication to lecroy
    self.com = lecroy_com(port)
    #number of boards and channels per board
    self.nbd = 1
    self.nchan = 8
    #offset in board numbering
    self.bdofs = 12
    #list of board objects
    self.bdlist = []
    for ibd in range(self.nbd):
      self.bdlist.append(board(ibd, self.nchan, self.bdofs, self.com))
    #configuration file
    self.confnam = "config.csv"
    self.cframe = pandas.read_csv(self.confnam)
    #watchdog timer with 10 sec timeout
    self.wdt = watchdog(10, self.bdlist)
    self.wdt.start()
    #mainframe PVs
    self.hvstat_pv = builder.boolIn("hvstat", ZNAM="OFF", ONAM="ON")
    self.hvon_pv = builder.boolOut("hvon", ZNAM=0, ONAM=1, HIGH=0.1, initial_value=0, on_update=self.do_on)
    self.hvoff_pv = builder.boolOut("hvoff", ZNAM=0, ONAM=1, HIGH=0.1, initial_value=0, on_update=self.do_off)
    self.link_pv = builder.boolOut("link", ZNAM=0, ONAM=1, HIGH=0.7, initial_value=0)
  #_____________________________________________________________________________
  def do_on(self, val):
    #turn mainframe on
    if val == 0: return
    self.com.put_cmd("hvon")
    self.hvstat_pv.set(1)
  #_____________________________________________________________________________
  def do_off(self, val):
    #turn mainframe off
    if val == 0: return
    self.com.put_cmd("hvoff")
    self.hvstat_pv.set(0)
  #_____________________________________________________________________________
  def init_config(self):
    #initialize default values from config file
    for i in range(len(self.cframe)):
      ibd = self.cframe["board"][i]-self.bdofs
      ich = self.cframe["channel"][i]
      dv_val = self.cframe["dv"][i]
      self.bdlist[ibd].chlist[ich].dv_pv.set(dv_val)
  #_____________________________________________________________________________
  def get_values(self, resp, setfunc):
    #get monitored parameters from response list
    for ibd in range(self.nbd):
      for ich in range(self.nchan):
        val = float(resp.pop(0))
        setfunc(self.bdlist[ibd].chlist[ich], val)
  #_____________________________________________________________________________
  def do_read(self):
    #read measured current and voltage
    resp = self.com.put_cmd_sync("src mc mv").split(" ")
    #skip command echo and lecroy prompt (last item) in response list
    while resp.pop(0).find("mv") < 0:
      pass
    resp.pop()
    self.get_values(resp, channel.set_mc)
    self.get_values(resp, channel.set_mv)
    #print "done", len(resp)
    #read high voltage status
    hvresp = self.com.put_cmd_sync("hvstatus")
    #print hvresp
    if hvresp.find("HVOFF") >= 0:
      self.hvstat_pv.set(0)
    elif hvresp.find("HVON") >= 0:
      self.hvstat_pv.set(1)
    else:
      self.hvstat_pv.set_alarm(alarm.INVALID_ALARM, alarm=alarm.UDF_ALARM)
    #flash the heartbeat PV
    self.link_pv.set(1)
    #reset the watchdog timer
    self.wdt.reset()
