print(__file__)

"""test a demo shutter"""
from APS_BlueSky_tools.devices import ApsPssShutter

class DemoShutter(ApsPssShutter):
    """variation of ApsPssShutter for testing"""
    open_bit = Component(EpicsSignal, bit1.pvname)
    close_bit = Component(EpicsSignal, bit2.pvname)


shtr = DemoShutter(name="shtr")

def planB():
    yield from abs_set(shtr, "open", wait=True)
    yield from abs_set(shtr, "close", wait=True)
