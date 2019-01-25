
from channel import channel

class board():
  #_____________________________________________________________________________
  def __init__(self, ibd, nchan, bdofs, com):
    #id of board
    self.ibd = ibd
    #number of channels
    self.nchan = nchan
    #channels on this board
    self.chlist = []
    for ich in range(self.nchan):
      self.chlist.append(channel(self.ibd, ich, bdofs, com))

