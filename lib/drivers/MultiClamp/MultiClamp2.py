# -*- coding: utf-8 -*-
from ctypes import *
import struct, os
from lib.util.clibrary import *
#from lib.util.CLibrary import *
#from PyQt4 import QtCore, QtGui

__all__ = ['MultiClamp']

## Load windows definitions
windowsDefs = winDefs()

# Load AxMultiClampMsg header
d = os.path.dirname(__file__)
axonDefs = CParser(
    os.path.join(d, 'AxMultiClampMsg.h'), 
    #replace={'MCCMSG_': ''},
    copyFrom=windowsDefs,
    cache=os.path.join(d, 'AxMultiClampMsg.h.cache'),
    #verbose=True
)

# Load telegraph definitions
teleDefs = CParser(
    os.path.join(d, 'MCTelegraphs.hpp'),
    copyFrom=windowsDefs,
    #replace={'MCTG_': ''},
    cache=os.path.join(d, 'MCTelegraphs.hpp.cache')
) 

##  Windows Messaging API 
#   provides RegisterWindowMessageA, PostMessageA, PeekMessageA, GetMessageA
#   See: http://msdn.microsoft.com/en-us/library/dd458658(VS.85).aspx
wmlib = CLibrary(windll.User32, teleDefs, prefix='MCTG_')

## Axon API (That's right, we have to use two different APIs to access one device. Cool, huh?)
axlib = CLibrary(windll.LoadLibrary(os.path.join(d, 'AxMultiClampMsg.dll')), axonDefs, prefix='MCCMSG_')

## Get window handle. Should be a long integer; may change in future windows versions.
#hWnd = struct.unpack('l', QtGui.QApplication.activeWindow().winId().asstring(4))

## register messages

#messages = [
    #'MCTG_OPEN_MESSAGE_STR',
    #'MCTG_CLOSE_MESSAGE_STR',
    #'MCTG_REQUEST_MESSAGE_STR',
    #'MCTG_BROADCAST_MESSAGE_STR',
    #'MCTG_RECONNECT_MESSAGE_STR',
    #'MCTG_ID_MESSAGE_STR',
#]
     
#msgIds = {}
#for m in messages:
    #msgIds[m] = wmlib.RegisterWindowMessageA(wmlib[m])


#def packSignalIDs(comPort, axoBus, channel):
    #return comPort | (axoBus << 8) | (channel << 16)


## open connection to specific clamp channel
#wmlib.PostMessageA(wmlib.HWND_BROADCAST, msgIds['MCTG_OPEN_MESSAGE_STR'], hWnd, packSignalIDs(3, 0, 1))

## poll for commander windows

## start thread for receiving messages

## for each message:
#if msg.cbData == wmlib.MC_TELEGRAPH_DATA.size() and msg.dwData == msgIds['MCTG_REQUEST_MESSAGE_STR']:
    #data = wmlib.MC_TELEGRAPH_DATA(msg.lpData)
    #if data.uComPortID == 3 and data.uAxoBusID == 0 and data.uChannelID == 1:
        ### message is the correct type, and for the correct channel
        #pass


## watch for reconnect messages

## close connection
#wmlib.PostMessageA(wmlib.HWND_BROADCAST, msgIds['MCTG_CLOSE_MESSAGE_STR'], hWnd, packSignalIDs(3, 0, 1))



## request an update
## careful -- does this disable automatic notification of changes?
#wmlib.PostMessageA(wmlib.HWND_BROADCAST, msgIds['MCTG_REQUEST_MESSAGE_STR'], hWnd, packSignalIDs(3, 0, 1))






class MultiClampChannel:
    """Class used to run MultiClamp commander functions for a specific channel.
    Uses most of the same functions as MultiClamp, but does not require the channel argument."""
    pass



class MultiClamp:
    """Class used to interface with remote multiclamp server.
    Only one instance of this class should be created."""
    INSTANCE = None
    
    def __init__(self):
        if MultiClamp.INSTANCE is not None:
            raise Exception("Already created MultiClamp driver object; use MultiClamp.INSTANCE")
        self.handle = None
        
        self.connect()
        #self.findDevices()
        MultiClamp.INSTANCE = self
    
    def __del__(self):
        ## do other things to shut down driver?
        self.disconnect()
        MultiClamp.INSTANCE = None
    
    
        

    ### High-level driver calls
    
    def readParams(self, chan, params):
        """Reads multiple parameters from multiclamp.
        
        Arguments:
        chan -- Use the multiclamp device associated with this channel
        params -- List of parameters to request. 
                  Each parameter "SomeValue" must have a corresponding 
                  function "getSomeValue" in AxMultiClampMsg.h
        """
        res = {}
        for p in params:
            v = self.runFunction('get'+p, [chan])
            res[p] = v
        return res

    def setParams(self, chan, params):
        """Sets multiple parameters on multiclamp.
        
        Arguments:
        chan -- Use the multiclamp device associated with this channel
        params -- Dict of parameters to set. 
        """
        res = {}
        for p in params:
            #print "Setting", p, params[p]
            try:
                v = self.runFunction('set'+p, [chan, params[p]])
            except:
                printExc("Error while setting parameter %s=%s" % (p, str(params[p])))
            finally:
                res[p] = v
        return res
        
        
    def listDevices(self):
        """Return a list of strings used to identify devices on a multiclamp.
        These strings should be used to identify the same device across invocations."""
        
        devList = []
        for d in self.devices:
            d = d.copy()
            if MODELS.has_key(d['model']):
                d['model'] = MODELS[d['model']]
            else:
                d['model'] = 'UNKNOWN'
            ## Make sure the order of keys is well defined; string must be identical every time.
            strDesc = ",".join("%s:%s" % (k, d[k]) for k in ['model', 'sn', 'com', 'dev', 'chan'])  
            devList.append(strDesc) 
        return devList
    
    
    def setMode(self, chan, mode):
        """Set the mode of the multiclamp channel. Modes are 'ic', 'vc', and 'i=0'."""
        self.selectDev(chan)
        self.SetMode(mode)
    
    #def runFunction(self, func, args=(), maxResponse=1024):
        #"""Run a function on a remote multiclamp server. 
        
        #Function names are defined by the server and args must be a [list] of arguments. 
        #For most functions, the first argument will be a device ID number.
        #Example:
            #rtxi.runFunction('getPrimarySignalGain', [rtxi.getDeviceId(0)])
            
        #Always returns a list or raises exception if the server returned an error message.
        
        #Arguments:
        #maxResponse -- Maximum response length allowed
        #cache -- If true, skip 'set' commands and use cached values for 'get' commands (use with caution!)
        #"""
        
        #strArgs = map(lambda x: str(x), args)
        ##print "runFunction %s%s cache=%s" % (func, str(strArgs), str(cache))
        
        #cmd = "%s(%s)\n" % (func, ','.join(strArgs))
        #s.send(cmd)
        
        #resp = s.recv(maxResponse)
        #data = resp.rstrip('\0\n').split(',')
        #if func[:3] == 'get' and len(data) == 1:
            #raise Exception("get returned no data: %s = %s <%s>" % (cmd, resp, str(data)))
        #if data[0] == '0':
            #raise Exception('MultiClamp communication error: %s' % ', '.join(data[1:]))
        #else:
            ##print "runFunction", data[1:]
            #return data[1:]
                
    def getSignalInfo(self, chan, outputChan='Primary'):
        """Return a tuple (signalName, gain, units) for the current signal
        
        the outputChan argument defaults to 'Primary' and can be set to 'Secondary' instead.
        """
    #def getSignalInfo(self, devID, primary):
        #self.selectDev(devID)
        #model = self.devices[devID]['model']
        
        #priMap = ['PRI', 'SEC']
        
        #if primary == 0:
            #sig = self.getPrimarySignal(devID)
        #elif primary == 1:
            #sig = self.getSecondarySignal(devID)
        
        #mode = self.getMode(devID)
        #if mode == 'I=0':
            #mode = 'IC'
            
        ##print devID, model, mode, primary, sig
        #info = SIGNAL_MAP[model][mode][priMap[primary]][sig]
        #return list(info)
        
        
        (name, gain, units) = self.runFunction('get%sSignalInfo' % outputChan, [chan])
        xGain = float(self.runFunction('get%sSignalGain' % outputChan, [chan])[0])
        ## Silly workaround-- MC700A likes to tell us that secondary signal gain is 0
        if xGain < 1e-10:
                xGain = 1.0
        gain2 = float(gain) * xGain
        #print "%s gain = %f * %f = %f" % (outputChan, float(gain), float(xGain[0]), gain2)
        return (name, gain2, units)


    def stateDiff(self, state):
        """Compare the state of the multiclamp to the expected state (s1), return the keys that differ."""
        m = []
        for k in state.keys():
            v = state[k]
            if type(v) == bool:
                if (v and s2[k][0] != 'true') or (not v and s2[k][0] != 'false'):
                    m.append(k)
            elif type(v) == int:
                if v != int(s2[k][0]):
                    m.append(k)
            elif type(v) == float:
                if v - float(s2[k][0]) > 1e-30:
                    m.append(k)
        return m
    
    #def getNumDevices(self):
        #return len(self.devices)
    
    #def getDeviceInfo(self, devID):
        #if devID >= len(self.devices):
            #raise Exception("Device %d does not exist" % devID)
        #d = self.devices[devID]
        #if MODELS.has_key(d['model']):
            #model = MODELS[d['model']]
        #else:
            #model = 'UNKNOWN'
            
        #return [model, d['serial'], d['port'], d['device'], d['channel']]




    ################   Begin Low-level driver calls    ###########################
    
    def connect(self):
        """(re)create connection to commander."""
        if self.handle is not None:
            self.disconnect()
        (self.handle, err) = axlib.CreateObject()
        if self.handle == 0:
            self.handle = None
            self.raiseError("Error while initializing Axon library:", err)
        self.findDevices()
        
    def disconnect(self):
        """Destroy connection to commander"""
        if self.handle is not None:
            axlib.DestroyObject(self.handle)
            self.handle = None
    
    def findMultiClamp(self):
        if len(self.devices) == 0:
            fn = 'FindFirstMultiClamp'
        else:
            fn = 'FindNextMultiClamp'
            
        try:
            serial = create_string_buffer('\0'*16)
            ret = self.call(fn, pszSerialNum=serial, uBufSize=16)
        except:
            if sys.exc_info()[1][0] == 6000:  ## We have reached the end of the device list
                return None
            raise
        return {'sn': ret['pszSerialNum'], 'model': ret['puModel'], 'com': ret['puCOMPortID'], 'dev': ret['puDeviceID'], 'chan': ret['puChannelID']}
    
    def findDevices(self):
        self.devices = []
        while True:
            dev = self.findMultiClamp()
            if dev is None:
                break
            else:
                self.devices.append(dev)

    def selectDev(self, devID):
        if devID >= len(self.devices):
            raise Exception("Device %d does not exist" % devID)
        d = self.devices[devID]
        self.SelectMultiClamp(pszSerialNum=d['sn'], uModel=d['model'], uCOMPortID=d['com'], uDeviceID=d['dev'], uChannelID=d['chan'])


    def call(self, fName, *args, **kargs):   ## call is only used for functions that return a bool error status and have a pnError argument passed by reference.
        
        ## Perform value mapping for a few functions (SetMode, SetPrimarySignal, SetSecondarySignal)
        if fName in NAME_MAPS:
            if args[0] not in NAME_MAPS[fName]:
                raise Exception("Argument to %s must be one of %s" % (fName, NAME_MAPS[fName].keys()))
            args[0] = NAME_MAPS[fName][args[0]]
    
        ret = axlib('functions', fName)(self.handle, *args, **kargs)
        if ret() == 0:
            funcStr = "%s(%s)" % (fName, ', '.join(map(str, args) + ["%s=%s" % (k, str(kargs[k])) for k in kargs]))
            self.raiseError("Error while running function  %s\n      Error:" % funcStr, ret['pnError'])
            
        ## perform return value mapping for a few specific functions
        if fName in INV_NAME_MAPS:
            if ret[1] not in INV_NAME_MAPS[fName]:
                raise Exception("Return from %s was %s; expected one of %s." % (fName, ret[1], NAME_MAPS[fName].keys()))
            ret[1] = INV_NAME_MAPS[fName][ret[1]]
            
        return ret

    def __getattr__(self, attr):  ## shorthand for making function calls
            return lambda *args, **kargs: self.call(attr, *args, **kargs)
    
    def raiseError(self, msg, err):
        raise Exception(err, msg + " " + self.errString(err))

    def printError(self, msg, err):
        print msg + self.errString(err)

    def errString(self, err):
        try:
            return axlib.BuildErrorText(self.handle, err, create_string_buffer('\0'*256), 256)['sTxtBuf']
        except:
            sys.excepthook(*sys.exc_info())
            return "<could not generate error message>"

class _MULTICLAMP:
    MC_CREATED = False
    
    #def __init__(self):
        #if _MULTICLAMP.MC_CREATED:
            #raise Exception("Will not create another object instance--use the pre-existing MULTICLAMP object.")
        #self.mc = windll.AxMultiClampMsg
        ##_MULTICLAMP.MC_CREATED = True
        
        #errCode = c_int(0)
        #self.handle = self._call('MCCMSG_CreateObject', byref(errCode))
        #if self.handle == 0:
            #raise Exception("Error %d creating MC object", errCode.value)
        #self.findDevices()
    
    #def __del__(self):
        #self.__class__.MC_CREATED = False

    def __getattr__(self, attr):
        """Easy function-calling convention."""
        attr = attr[0].upper() + attr[1:]
        if attr[0] != "_" and hasattr(self.mc, 'MCCMSG_' + attr):
            return lambda *args: self.call(attr, *args)
        else:
            raise Exception("No name '%s' found" % attr)

    def call(self, fn, devID, arg=None):
        """Run a function from the DLL. """
        func = "MCCMSG_" + fn
        fsig = FUNCTIONS[func]
        #print fn, devID, arg
        self.selectDev(devID)
        unmap = False
        unref = False
        unbool = False
        
        if len(fsig[2]) < 3:
            arg = []
        else:
            if f[:3].lower() == 'get':
                if arg is not None:
                    raise Exception("Too many arguments to function %s" % f)
                unref = True
                if fsig[2][1][0] == 'double':
                    ref = c_double(0)
                    arg = byref(ref)
                elif fsig[2][1][0] == 'BOOL':
                    ref = c_int(0)
                    arg = byref(ref)
                    unbool = True
                elif fsig[2][1][0] == 'UINT':
                    ref = c_uint(0)
                    arg = byref(ref)
                    unmap = True
            else:
                if arg is None:
                    raise Exception("Missing argument %s for function %s" % (fsig[2][1][2], f))
                if fsig[2][1][0] == 'double':
                    arg = c_double(arg)
                elif fsig[2][1][0] == 'BOOL':
                    if arg:
                        print "Interpreting parameter as c_int(1)"
                        arg = c_int(1)
                    else:
                        print "Interpreting parameter as c_int(0)"
                        arg = c_int(0)
                elif fsig[2][1][0] == 'UINT':
                    arg = c_uint(self.nameToInt(arg, f))
        
        errCode = c_int(0)
        args = (self.handle, arg, byref(errCode))
        
        #if len(args) != len(fsig[2]):
            #raise Exception("Function %s takes %d args, %d given" % (f, len(fsig[2])-2, len(args)-2))
        
        ret = self._call(func, *args)
        #print "Call %s%s returned %s" % (func, str(args), str(ret))
        if ret == 0:
            raise Exception(errCode.value, self.error(errCode))
            
        ## Rediculous workaround--700A likes to claim it's secondary signal gain is 0
        if func == 'MCCMSG_GetSecondarySignalGain' and self.devices[devID]['model'] == HW_TYPE_MC700A:
            return 1
            
        if unref:
            if unmap:
                return self.intToName(ref.value, f)
            elif unbool:
                return ref.value == 1
            else:
                return ref.value
        else:
            return None
        
    #def _call(self, func, *args):
        #try:
            #return getattr(self.mc, func)(*args)
        #except:
            #print func, args
            #raise
        
    #def error(self, errCode):
        #buf = create_string_buffer('\0' * 256)
        #try:
            #self._call('MCCMSG_BuildErrorText', self.handle, errCode, buf, c_int(256))
            #return str(buf.value)
        #except:
            #raise
            ##raise Exception("Error getting error message :(")


        
    #def selectDev(self, devID):
        #if devID >= len(self.devices):
            #raise Exception("Device %d does not exist" % devID)
        #d = self.devices[devID]
        #erNum = c_uint(0)
        #ret = self._call('MCCMSG_SelectMultiClamp', self.handle, c_uint(d['model']), c_char_p(d['serial']), c_uint(d['port']), c_uint(d['device']), c_uint(d['channel']), byref(erNum))
        #if ret == 0:
            #raise Exception(erNum.value, self.error(erNum))
        
    def nameToInt(self, name, fn):
        return NAME_MAPS[fn][name]
        
    def intToName(self, num, fn):
        return INV_NAME_MAPS[fn][num]
        
    #def getNumDevices(self, *args):
        #if len(args) > 0:
            #raise Exception("getNumDevices takes no arguments")
        #return len(self.devices)
    
    #def getDeviceInfo(self, devID):
        #if devID >= len(self.devices):
            #raise Exception("Device %d does not exist" % devID)
        #models = {
            #HW_TYPE_MC700A: 'MC700A',
            #HW_TYPE_MC700B: 'MC700B'
        #}
        #d = self.devices[devID]
        #if models.has_key(d['model']):
            #model = models[d['model']]
        #else:
            #model = 'UNKNOWN'
            
        #return [model, d['serial'], d['port'], d['device'], d['channel']]
        
    #def getSignalInfo(self, devID, primary):
        #self.selectDev(devID)
        #model = self.devices[devID]['model']
        
        #priMap = ['PRI', 'SEC']
        
        #if primary == 0:
            #sig = self.getPrimarySignal(devID)
        #elif primary == 1:
            #sig = self.getSecondarySignal(devID)
        
        #mode = self.getMode(devID)
        #if mode == 'I=0':
            #mode = 'IC'
            
        ##print devID, model, mode, primary, sig
        #info = SIGNAL_MAP[model][mode][priMap[primary]][sig]
        #return list(info)
        
    
    
    def setSignalByName(self, devID, signal, primary):
        self.selectDev(devID)
        model = self.devices[devID]['model']
        
        priMap = ['PRI', 'SEC']
        
        mode = self.getMode(devID)
        if mode == 'I=0':
            mode = 'IC'
            
        sig = None
        sigMap = SIGNAL_MAP[model][mode][priMap[primary]]
        for k in sigMap:
            if sigMap[k][0] == signal:
                sig = k
        if sig is None:
            raise Exception("Signal name '%s' not found" % signal)
        if primary == 0:
            self.setPrimarySignal(devID, sig)
        elif primary == 1:
            self.setSecondarySignal(devID, sig)

    def getPrimarySignalInfo(self, devID):
        return self.getSignalInfo(devID, 0)

    def getSecondarySignalInfo(self, devID):
        return self.getSignalInfo(devID, 1)

    def setPrimarySignalByName(self, devID, signal):
        return self.setSignalByName(devID, signal, 0)

    def setSecondarySignalByName(self, devID, signal):
        return self.setSignalByName(devID, signal, 1)


#init()

## Crapton of stuff to remember that is not provided by header files

def invertDict(d):
    return dict([(x[1], x[0]) for x in d.items()])

MODELS = {
    axlib.HW_TYPE_MC700A: 'MC700A',
    axlib.HW_TYPE_MC700B: 'MC700B'
}

MODE_LIST = {
    "vc": axlib.MODE_VCLAMP,
    "ic": axlib.MODE_ICLAMP,
    "i=0": axlib.MODE_ICLAMPZERO,
}
MODE_LIST_INV = invertDict(MODE_LIST) 

## Extract all signal names from library
PRI_OUT_MODE_LIST = {}
SEC_OUT_MODE_LIST = {}
for k in axlib['values']:
    if k[:11] == 'PRI_SIGNAL_':
        PRI_OUT_MODE_LIST[k[11:]] = axlib('values', k)
    elif k[:11] == 'SEC_SIGNAL_':
        SEC_OUT_MODE_LIST[k[11:]] = axlib('values', k)
PRI_OUT_MODE_LIST_INV = invertDict(PRI_OUT_MODE_LIST)
SEC_OUT_MODE_LIST_INV = invertDict(SEC_OUT_MODE_LIST)


NAME_MAPS = {
    'SetMode': MODE_LIST,
    'SetPrimarySignal': PRI_OUT_MODE_LIST,
    'SetSecondarySignal': SEC_OUT_MODE_LIST
}
INV_NAME_MAPS = {
    'GetMode': MODE_LIST_INV,
    'GetPrimarySignal': PRI_OUT_MODE_LIST_INV,
    'GetSecondarySignal': SEC_OUT_MODE_LIST_INV
}





## In order to properly interpret the output of getPrimarySignal and getSecondarySignal, 
## we also need to know the model and mode of the amplifier and translate via this table
## Note: Completely retarded. This should have been handled by the axon library

SIGNAL_MAP = {
    axlib.HW_TYPE_MC700A: {
        'VC': {
            'PRI': {
                "VC_MEMBPOTENTIAL": ("MembranePotential", 10.0, 'V'),
                "VC_MEMBCURRENT": ("MembraneCurrent", 0.5e9, 'A'),
                "VC_PIPPOTENTIAL": ("PipettePotential", 1.0, 'V'),
                "VC_100XACMEMBPOTENTIAL": ("100XACMembranePotential", 100., 'V'),
                "VC_AUXILIARY1": ("BathPotential", 1., 'V')
            },
            'SEC': {
                "VC_MEMBPOTENTIAL": ("MembranePlusOffsetPotential", 10.0, 'V'),
                "VC_MEMBCURRENT": ("MembraneCurrent", 0.5e9, 'A'),
                "VC_PIPPOTENTIAL": ("PipettePotential", 1., 'V'),
                "VC_100XACMEMBPOTENTIAL": ("100XACPipettePotential", 100., 'V'),
                "VC_AUXILIARY1": ("BathPotential", 1., 'V')
            }
        },
        'IC': {
            'PRI': {   ## Driver bug? Primary IC signals use VC values. Bah.
                "VC_PIPPOTENTIAL": ("MembranePotential", 1.0, 'V'),
                "VC_MEMBCURRENT": ("MembraneCurrent", 0.5e9, 'A'),
                "VC_MEMBPOTENTIAL": ("CommandCurrent", 0.5e9, 'A'),
                "VC_100XACMEMBPOTENTIAL": ("100XACMembranePotential", 100., 'V'),
                "VC_AUXILIARY1": ("BathPotential", 1., 'V')
            },
            'SEC': {
                "IC_CMDCURRENT": ("CommandCurrent", 0.5e9, 'A'),
                "IC_MEMBCURRENT": ("MembraneCurrent", 0.5e9, 'A'),
                "IC_MEMBPOTENTIAL": ("MembranePlusOffsetPotential", 1.0, 'V'),
                "IC_100XACMEMBPOTENTIAL": ("100XACMembranePotential", 100., 'V'),
                "IC_AUXILIARY1": ("BathPotential", 1., 'V')
            }
        }
    },
        
    axlib.HW_TYPE_MC700B: {
        'VC': {
            'PRI': {
                "VC_MEMBCURRENT": ("MembraneCurrent", 0.5e9, 'A'),
                "VC_MEMBPOTENTIAL": ("MembranePotential", 10.0, 'V'),
                "VC_PIPPOTENTIAL": ("PipettePotential", 1.0, 'V'),
                "VC_100XACMEMBPOTENTIAL": ("100XACMembranePotential", 100., 'V'),
                "VC_EXTCMDPOTENTIAL": ("ExternalCommandPotential", 50., 'V'),
                "VC_AUXILIARY1": ("Auxiliaryl", 1., 'V'),
                "VC_AUXILIARY2": ("Auxiliary2", 1., 'V')
            },
            'SEC': {
                "VC_MEMBCURRENT": ("MembraneCurrent", 0.5e9, 'A'),
                "VC_MEMBPOTENTIAL": ("MembranePotential", 10.0, 'V'),
                "VC_PIPPOTENTIAL": ("PipettePotential", 1.0, 'V'),
                "VC_100XACMEMBPOTENTIAL": ("100XACMembranePotential", 100., 'V'),
                "VC_EXTCMDPOTENTIAL": ("ExternalCommandPotential", 50., 'V'),
                "VC_AUXILIARY1": ("Auxiliaryl", 1., 'V'),
                "VC_AUXILIARY2": ("Auxiliary2", 1., 'V')
            }
        },
        'IC': {
            'PRI': {
                "IC_MEMBPOTENTIAL": ("MembranePotential", 10.0, 'V'),
                "IC_MEMBCURRENT": ("MembraneCurrent", 0.5e9, 'A'),
                "IC_CMDCURRENT": ("CommandCurrent", 0.5e9, 'A'),
                "IC_100XACMEMBPOTENTIAL": ("100XACMembranePotential", 100., 'V'),
                "IC_EXTCMDCURRENT": ("ExternalCommandCurrent", 2.5e9, 'A'),
                "IC_AUXILIARY1": ("Auxiliary1", 1., 'V'),
                "IC_AUXILIARY2": ("Auxiliary2", 1., 'V')
            },
            'SEC': {
                "IC_MEMBPOTENTIAL": ("MembranePotential", 10.0, 'V'),
                "IC_MEMBCURRENT": ("MembraneCurrent", 0.5e9, 'A'),
                "IC_PIPPOTENTIAL": ("PipettePotential", 1.0, 'V'),
                "IC_100XACMEMBPOTENTIAL": ("100XACMembranePotential", 100., 'V'),
                "IC_EXTCMDCURRENT": ("ExternalCommandCurrent", 2.5e9, 'A'),
                "IC_AUXILIARY1": ("Auxiliary1", 1., 'V'),
                "IC_AUXILIARY2": ("Auxiliary2", 1., 'V')
            }
        }
    }
}
    