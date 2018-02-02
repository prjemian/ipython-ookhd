print(__file__)

"""Set up default complex devices"""

import time
from ophyd import Component, Device, DeviceStatus
from ophyd import EpicsMotor, EpicsScaler
from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
from ophyd import PVPositioner, PVPositionerPC
from ophyd import AreaDetector, PcoDetectorCam
from ophyd import SingleTrigger, ImagePlugin, HDF5Plugin
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from bluesky.plan_stubs import mv, mvr, abs_set, wait

from APS_BlueSky_tools.devices import userCalcsDevice
# from APS_BlueSky_tools.synApps_ophyd import *


class MotorDialValuesDevice(Device):
    value = Component(EpicsSignalRO, ".DRBV")
    setpoint = Component(EpicsSignal, ".DVAL")


class MyEpicsMotorWithDial(EpicsMotor):
    dial = Component(MotorDialValuesDevice, "")


class ServoRotationStage(EpicsMotor):
    """extend basic motor support to enable/disable the servo loop controls"""
    
    # values: "Enable" or "Disable"
    servo = Component(EpicsSignal, ".CNEN", string=True)


class Motor_Shutter(Device):
    """
    a shutter, implemented with a motor
    
    USAGE::
        tomo_shutter = Motor_Shutter("2bma:m23", name="tomo_shutter")
        tomo_shutter.open()
        tomo_shutter.close()
        
        # or, when used in a plan
        def planA():
            yield from abs_set(tomo_shutter, "open", group="O")
            yield from wait("O")
            yield from abs_set(tomo_shutter, "close", group="X")
            yield from wait("X")
        def planA():
            yield from abs_set(tomo_shutter, "open", wait=True)
            yield from abs_set(tomo_shutter, "close", wait=True)
        def planA():
            yield from mv(tomo_shutter, "open")
            yield from mv(tomo_shutter, "close")
    """
    motor = Component(EpicsMotor, "")
    closed_position = 1.0
    open_position = 0.0
    _tolerance = 0.01
    
    def isopen(self):
        return abs(self.motor.position - self.open_position) <= self._tolerance
    
    def isclosed(self):
        return abs(self.motor.position - self.closed_position) <= self._tolerance
    
    def open(self):
        """move motor to BEAM NOT BLOCKED position, interactive use"""
        self.motor.move(self.open_position)
    
    def close(self):
        """move motor to BEAM BLOCKED position, interactive use"""
        self.motor.move(self.closed_position)

    def set(self, value, *, timeout=None, settle_time=None):
        """
        `set()` is like `put()`, but used in BlueSky plans

        Parameters
        ----------
        value : "open" or "close"
        timeout : float, optional
            Maximum time to wait. Note that set_and_wait does not support
            an infinite timeout.
        settle_time: float, optional
            Delay after the set() has completed to indicate completion
            to the caller

        Returns
        -------
        status : DeviceStatus
        """

        # using put completion:
        # timeout and settle time is handled by the status object.
        status = DeviceStatus(
            self, timeout=timeout, settle_time=settle_time)

        def put_callback(**kwargs):
            status._finished(success=True)

        if value.lower() == "open":
            pos = self.open_position
        elif value.lower() == "close":
            pos = self.closed_position
        else:
            msg = "value should be either open or close"
            msg + " : received " + str(value)
            raise ValueError(msg)
        self.motor.user_setpoint.put(pos, use_complete=True, callback=put_callback)

        return status
