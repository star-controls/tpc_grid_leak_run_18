#!/usr/local/epics/modules/pythonIoc/pythonIoc

#set pythonIoc interpreter above

#import basic softioc framework
from softioc import softioc, builder

#import the the application
import tpc_grid_leak

#run the ioc
builder.LoadDatabase()
softioc.iocInit()

#start the application
tpc_grid_leak.loop_monit()

#put alarm limits
softioc.dbpf("tpc_grid_leak:12:00:mv.LOLO", "-120")
softioc.dbpf("tpc_grid_leak:12:00:mv.HIHI", "-110")
softioc.dbpf("tpc_grid_leak:12:01:mv.LOLO", "-120")
softioc.dbpf("tpc_grid_leak:12:01:mv.HIHI", "-110")

#start the ioc shell
softioc.interactive_ioc(globals())
