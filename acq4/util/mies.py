from .igorpro import IgorBridge
from acq4.util import Qt


def __reload__(old):
    MIES._bridge = old['MIES']._bridge


class MIES(Qt.QObject):
    """Bridge for communicating with MIES (multi-patch ephys and pressure control in IgorPro)
    """
    _bridge = None

    @classmethod
    def getBridge(cls):
        """Return a singleton MIESBridge instance.
        """
        if cls._bridge is None:
            cls._bridge = MIES()
        return cls._bridge

    def __init__(self):
        super(MIES, self).__init__(parent=None)
        self.igor = IgorBridge()
        self._windowName = None

    def getClampState(self, hs):
        state = self.igor('FFI_GetClampState', self.getWindowName(), hs).result()
        mode = {0: 'VC', 1: 'IC', 2: 'I=0'}.get(state[-1], None)
        if mode is None:
            raise ValueError(f"Unknown clamp state: {state[-1]}")
        if mode == 'VC':
            # HoldingPotential       |                       | mV      |
            # RSCompChaining         |                       | On/Off  |
            # HoldingPotentialEnable |                       | On/Off  |
            # WholeCellCap           | 1 : On 0 : Off        | pF      |
            # WholeCellRes           |                       | MΩ      |
            # WholeCellEnable        | 1 : On 0 : Off        | On/Off  |
            # Correction             |                       | %       |
            # Prediction             |                       | %       |
            # RsCompEnable           |                       | On/Off  |
            # PipetteOffsetVC        | 1 : On 0 : Off        | mV      |
            # WholeCellCap           |                       | a.u.    |
            # ClampMode              | 0 : VC                |         |

            return {
                'HoldingPotential': state[0] * 1e-3,
                'RSCompChaining': bool(state[1]),
                'HoldingPotentialEnable': bool(state[2]),
                'WholeCellCap': state[3] * 1e-12,
                'WholeCellRes': state[4] * 1e6,
                'WholeCellEnable': bool(state[5]),
                'Correction': state[6],
                'Prediction': state[7],
                'RsCompEnable': bool(state[8]),
                'PipetteOffsetVC': state[9] * 1e-3,
                'WholeCellCap': state[10],
                'ClampMode': mode,
            }
        elif mode == 'IC':
            # BiasCurrent          |                       | pA      |
            # BiasCurrentEnable    |                       | On/Off  |
            # BridgeBalance        |                       | MΩ      |
            # BridgeBalanceEnable  | 1 : On 0 : Off        | On/Off  |
            # CapNeut              |                       | pF      |
            # CapNeutEnable        | 1 : On 0 : Off        | On/Off  |
            # AutoBiasVcom         |                       | mV      |
            # AutoBiasVcomVariance |                       | mV      |
            # AutoBiasIbiasmax     |                       | pA      |
            # AutoBiasEnable       | 1 : On 0 : Off        | On/Off  |
            # PipetteOffsetIC      |                       | mV      |
            # ClampMode            | 1 : IC                |         |

            return {
                'BiasCurrent': state[0] * 1e-12,
                'BiasCurrentEnable': bool(state[1]),
                'BridgeBalance': state[2] * 1e6,
                'BridgeBalanceEnable': bool(state[3]),
                'CapNeut': state[4] * 1e-12,
                'CapNeutEnable': bool(state[5]),
                'AutoBiasVcom': state[6] * 1e-3,
                'AutoBiasVcomVariance': state[7] * 1e-3,
                'AutoBiasIbiasmax': state[8] * 1e-12,
                'AutoBiasEnable': bool(state[9]),
                'PipetteOffsetIC': state[10] * 1e-3,
                'ClampMode': mode,
            }
        else:
            return {'ClampMode': mode}

    def selectHeadstage(self, hs):
        if hs != 0:
            raise NotImplementedError("Multiple headstages not currently implemented")
        return
        # return self.setCtrl("slider_DataAcq_ActiveHeadstage", hs)
    
    # def activateHeadstage(self, hs):
    #     return self.setCtrl(f"Check_DataAcqHS_0{hs}", True)
    def setHeadstageActive(self, hs, active: bool):
        return self.igor('FFI_SetHeadstageActive', self.getWindowName(), hs, 1 if active else 0)
    
    def isHeadstageActive(self, hs):
        value = self.getCtrlValue(f'Check_DataAcqHS_0{hs}')
        return value == '1'

    def enableTestPulse(self, enable:bool):
        """Enable/disable test pulse for all active headstages"""
        return self.igor('FFI_TestpulseMD', self.getWindowName(), 1 if enable else 0)

    # def getHolding(self, hs, mode):
    #     self.selectHeadstage(hs)
    #     if mode == "VC":
    #         val = float(self.getCtrlValue('setvar_DataAcq_Hold_VC')) / 1000
    #         enabled = self.getCtrlValue('check_DatAcq_HoldEnableVC') == '1'
    #     elif mode == "IC":
    #         val = float(self.getCtrlValue('setvar_DataAcq_Hold_IC')) / 1e12
    #         enabled = self.getCtrlValue('check_DatAcq_HoldEnable') == '1'
    #     return val, enabled

    def getHolding(self, headstage, mode):
        state = self.getClampState(headstage)
        if state['ClampMode'] != mode:
            return 0, False
            raise Exception("This is broken temporarily")
        key, scale = {'IC': ('BiasCurrent', 1e-12), 'VC': ('HoldingPotential', 1e-3)}[mode]
        return state[key] * scale, state[key+'Enable']

    # def setHolding(self, headstage, mode, value):
    #     self.selectHeadstage(headstage)
    #     if mode == "VC":
    #         ret = self.setCtrl('setvar_DataAcq_Hold_VC', value * 1000)
    #         if value != 0:
    #             ret = self.setCtrl('check_DatAcq_HoldEnableVC', True)
    #     else:
    #         ret = self.setCtrl('setvar_DataAcq_Hold_IC', value * 1e12)
    #         if value != 0:
    #             ret = self.setCtrl('check_DatAcq_HoldEnable', True)
    #     return ret

    def setHolding(self, headstage, mode, value):
        if mode == 'VC':
            return self.igor('FFI_SetHoldingPotential', self.getWindowName(), headstage, value * 1000)
        elif mode == 'IC':
            return self.igor('FFI_SetBiasCurrent', self.getWindowName(), headstage, value * 1e12)
        else:
            raise ValueError(f"Cannot set holding for mode '{mode}'")

    # def setClampMode(self, hs: int, value: str): # IC | VC | I=0
    #     rtn_value = None
    #     if value == "VC":
    #         rtn_value = self.setCtrl(f'Radio_ClampMode_{hs*2}', True)
    #     elif value == "IC":
    #         rtn_value = self.setCtrl(f'Radio_ClampMode_{hs*2+1}', True)
    #     elif value.lower() == "i=0":
    #         rtn_value = self.setCtrl(f'Radio_ClampMode_{hs*2+1}IZ', True)

    #     return rtn_value

    def setClampMode(self, headstage, mode):
        mode_n = {'VC': 0, 'IC': 1, 'I=0': 2}[mode]
        return self.igor('FFI_SetClampMode', self.getWindowName(), headstage, mode_n)

    # def getClampMode(self, hs): # IC | VC | I=0
    #     clamp_mode = None
    #     is_active: str = self.getCtrlValue(f'Radio_ClampMode_{hs*2}') # due to wonky control naming
    #     if is_active == "1":
    #         clamp_mode = "VC"
    #     else:
    #         is_active: str = self.getCtrlValue(f'Radio_ClampMode_{hs*2+1}')
    #         if is_active == "1":
    #             clamp_mode = "IC"
    #         else:
    #             is_active: str = self.getCtrlValue(f'Radio_ClampMode_{hs*2+1}IZ')
    #             if is_active == "1":
    #                 clamp_mode = "I=0"
    #     return clamp_mode

    def getClampMode(self, headstage):
        return self.getClampState(headstage)['ClampMode']

    def setAutoBias(self, headstage, value, enable):
        return self.igor('FFI_SetAutoBias', self.getWindowName(), headstage, value * 1000, 1 if enable else 0)

    # def setAutoBiasEnabled(self, headstage, value: bool):
    #     self.selectHeadstage(headstage)
    #     return self.setCtrl('check_DataAcq_AutoBias', value)

    # def getAutoBiasEnabled(self, headstage):
    #     self.selectHeadstage(headstage)
    #     value = self.getCtrlValue('check_DataAcq_AutoBias')
    #     return True if value == "1" else False
    def getAutoBiasEnabled(self, headstage):
        state = self.getClampState(headstage)
        if state != 'IC':
            return False
            raise Exception("this is broken for now")
        return state['AutoBiasEnable']
        
    # def setAutoBiasTarget(self, headstage, value):
    #     self.selectHeadstage(headstage)
    #     return self.setCtrl('setvar_DataAcq_AutoBiasV', value * 1000)
        
    def getAutoBiasTarget(self, headstage):
        state = self.getClampState(headstage)
        if state != 'IC':
            return 0
            raise Exception("this is broken for now")
        return state['AutoBiasVCom'] * 1e-3
    
    def getManualPressure(self, headstage) -> float:
        self.selectHeadstage(headstage)
        return float(self.getCtrlValue('setvar_DataAcq_SSPressure'))
    
    def setPressureAndSource(self, headstage, source, pressure):
        if source == 'user':
            self.selectHeadstage(headstage)
            return self.setCtrl("check_DataACq_Pressure_User", True)
        try:
            source_val = {'atmosphere': 0, 'regulator': 1}[source]
        except KeyError:
            raise ValueError(f"Invalid pressure source '{source}'")
        return self.igor('DoPressureManual', self.getWindowName(), headstage, source_val, pressure)

    def setHeadstageActive(self, hs, active):
        return self.setCtrl('Check_DataAcqHS_%02d' % hs, active)

    # def autoPipetteOffset(self, headstage):
    #     self.selectHeadstage(headstage)
    #     return self.setCtrl('button_DataAcq_AutoPipOffset_VC')

    # def autoBridgeBalance(self, headstage):
    #     self.selectHeadstage(headstage)
    #     return self.setCtrl('button_DataAcq_AutoBridgeBal_IC')

    # def autoCapComp(self, headstage):
    #     self.selectHeadstage(headstage)
    #     self.setCtrl('button_DataAcq_FastComp_VC')
    #     return self.setCtrl('button_DataAcq_SlowComp_VC')

    def autoPipetteOffset(self, headstage):
        self.igor('FFI_TriggerAutoClampControl', self.getWindowName(), headstage, 1)

    def autoCapComp(self, headstage):
        self.igor('FFI_TriggerAutoClampControl', self.getWindowName(), headstage, 2)

    def autoBridgeBalance(self, headstage):
        self.igor('FFI_TriggerAutoClampControl', self.getWindowName(), headstage, 3)


    def getLockedDevices(self):
        res = self.igor("GetListOfLockedDevices").result()
        return res.split(";")

    def setCtrl(self, name, value=None):
        """Set or activate a GUI control in MIES."""
        windowName = self.getWindowName()
        if value is None:
            return self.igor('PGC_SetAndActivateControl', windowName, name)
        else:
            return self.igor('PGC_SetAndActivateControlVar', windowName, name, value)
        
    def getCtrlValue(self, mies_ctrl_name):
        windowName = self.getWindowName()
        return self.igor('GetGuiControlValue', windowName, mies_ctrl_name).result()

    def getWindowName(self, ):
        if self._windowName is None:
            devices = self.getLockedDevices()
            for dev in devices:
                if dev != "":
                    self._windowName = devices[0]
        if self._windowName is None:
            raise Exception("No device locked in IGOR")
        return self._windowName

    def quit(self):
        self.igor.quit()


if __name__ == "__main__":
    from acq4.util import Qt
    import pyqtgraph as pg
    import sys


    class W(Qt.QWidget):
        def __init__(self, parent=None):
            super(W, self).__init__(parent=parent)
            self.mies = MIES.getBridge(True)
            self.mies.sigDataReady.connect(self.printit)
            self.b = Qt.QPushButton("stop", parent=self)
            self.b.clicked.connect(self.mies.quit)
            l = Qt.QVBoxLayout()
            l.addWidget(self.b)
            self.setLayout(l)

        def printit(self, data):
            print(data)


    app = pg.mkQApp()
    w = W()
    w.show()
    sys.exit(app.exec_())