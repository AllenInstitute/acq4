import glob
import sys

import serial
from acq4.devices.LightSource import LightSource
from acq4.util.HelpfulException import HelpfulException


class CoolLEDLightSource(LightSource):
    def __init__(self, dm, config, name):
        super(CoolLEDLightSource, self).__init__(dm, config, name)
        if "port" in config:
            self._port = config["port"]
        else:
            self._port = self._detectCoolLEDPort()
        self._devConn = serial.Serial(self._port, 38400, timeout=0)
        # self.addSource("A", {"active": True, "brightness": 100})
        # self.addSource("B", {"active": True, "brightness": 100})
        # self.addSource("C", {"active": True, "brightness": 100})
        # for name, config in self.sourceConfigs.items():
        #     self.setSourceBrightness(name, config["brightness"])
        #     self.setSourceActive(name, config["active"])
        self._readStatus()

    def _detectCoolLEDPort(self):
        if sys.platform.startswith("win"):
            ports = ["COM%s" % (i + 1) for i in range(10)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob("/dev/tty[A-Za-z]*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError("Unsupported platform")

        for port in ports:
            try:
                conn = serial.Serial(port, timeout=0.1)
                if conn.readline()[0:7] == b"CoolLED" or conn.readline() == 4:
                    conn.close()
                    return port
                elif conn.readline() == b"":
                    conn.write("XVER\n".encode("utf-8"))
                    out = conn.read(2000)
                    if out[0:7] == b"XFW_VER":
                        conn.close()
                        return port
                else:
                    conn.close()
            except (OSError, serial.SerialException):
                pass

        raise HelpfulException("Could not detect a CoolLED light source. Are the drivers installed?")

    def _readStatus(self):
        self._devConn.write("CSS?\n".encode("utf-8"))
        resp = self._devConn.readline().decode("utf-8")
        print(f"CoolLED resp: {resp}")
        self.sourceConfigs["A"]["active"] = (resp[5] == "N")
        self.sourceConfigs["A"]["brightness"] = int(resp[6:9])
        self.sourceConfigs["B"]["active"] = (resp[11] == "N")
        self.sourceConfigs["B"]["brightness"] = int(resp[12:15])
        self.sourceConfigs["C"]["active"] = (resp[17] == "N")
        self.sourceConfigs["C"]["brightness"] = int(resp[18:21])
        return self.sourceConfigs

    @staticmethod
    def _makeSetterCommand(channel, onOrOff, brightness):
        onOrOff = "N" if onOrOff else "F"
        return f"CSS{channel}S{onOrOff}{brightness:03d}\n".encode("utf-8")

    def quit(self):
        self._devConn.close()

    def sourceActive(self, name):
        return self._readStatus()[name]["active"]

    def setSourceActive(self, name, active):
        cmd = self._makeSetterCommand(name, active, self.getSourceBrightness(name))
        self._devConn.write(cmd)
        self.sourceConfigs[name]["active"] = active

    def getSourceBrightness(self, name):
        return self._readStatus()[name]["brightness"]

    def setSourceBrightness(self, name, percent):
        cmd = self._makeSetterCommand(name, percent > 0, percent)
        self._devConn.write(cmd)
