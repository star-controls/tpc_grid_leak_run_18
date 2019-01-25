
from softioc import builder, alarm

class channel:
  #_____________________________________________________________________________
  def __init__(self, ibd, ichan, bdofs, com):
    #telnet to lecroy
    self.com = com
    #id of board
    self.ibd = ibd
    #id of this channel
    self.ichan = ichan
    #offset in board numbering
    self.bdofs = bdofs
    #PVs for the channel
    pvnam = "{0:02d}:{1:02d}:".format(self.ibd+self.bdofs, self.ichan)
    self.mc_pv = builder.aIn(pvnam+"mc", PREC=3)
    self.mv_pv = builder.aIn(pvnam+"mv", PREC=1, LLSV="MAJOR", HHSV="MAJOR", LOPR=-200., HOPR=0.)
    self.dv_pv = builder.aOut(pvnam+"dv", on_update=self.put_dv)
  #_____________________________________________________________________________
  def set_mc(self, val):
    #set measured current
    #print self.ibd, self.ichan, "mc:", val
    self.mc_pv.set(val)
  #_____________________________________________________________________________
  def set_mv(self, val):
    #set measured voltage
    #print self.ibd, self.ichan, "mv:", val
    self.mv_pv.set(val)
  #_____________________________________________________________________________
  def put_dv(self, val):
    #put demand voltage
    #print "dv:", self.ibd, self.ichan, val
    cmd = "ld s{0:d}.{1:d} dv {2:.1f}".format(self.ibd+self.bdofs, self.ichan, val)
    #print cmd
    self.com.put_cmd(cmd)
  #_____________________________________________________________________________
  def set_invalid(self):
    #set all readback PVs as invalid, to be used with watchdog timer
    self.mc_pv.set_alarm(alarm.INVALID_ALARM, alarm=alarm.UDF_ALARM)
    self.mv_pv.set_alarm(alarm.INVALID_ALARM, alarm=alarm.UDF_ALARM)

