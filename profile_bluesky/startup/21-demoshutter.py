print(__file__)

"""test a demo shutter"""

import threading

class ApsPssShutter(Device):
    """
    APS PSS shutter
    
    * shutters have separate bit PVs for open and close
    * set the bit, the shutter moves, and the bit resets a short time later
    * no indication that the shutter has actually moved from the bits
    """
    open_bit = Component(EpicsSignal, ":open")
    close_bit = Component(EpicsSignal, ":close")
    delay_s = 1.2
    valid_open_values = ["open",]   # lower-case strings ONLY
    valid_close_values = ["close",]
    
    def open(self):
        """open the shutter, interactive use"""
        self.open_bit.put(1)
    
    def close(self):
        """close the shutter, interactive use"""
        self.close_bit.put(1)
    
    def set(self, value, **kwargs):
        """open or close the shutter, BlueSky plan use"""
        # ensure numerical additions to lists are now strings
        self.valid_open_values = [str(i).lower() for i in self.valid_open_values]
        self.valid_close_values = [str(i).lower() for i in self.valid_close_values]

        acceptables = self.valid_open_values + self.valid_close_values
        if str(value).lower() not in acceptables:
            msg = "value should be one of " + " | ".join(acceptables)
            msg += " : received " + str(value)
            raise ValueError(msg)
        
        status = DeviceStatus(self)
        
        def move_shutter():
            if str(value).lower() in self.valid_open_values:
                self.open()     # no need to yield inside a thread
            elif str(value).lower() in self.valid_close_values:
                self.close()
        
        def run_and_delay():
            move_shutter()
            # sleep, since we don't *know* when the shutter has moved
            sleep(self.delay_s)
            status._finished(success=True)
        
        threading.Thread(target=run_and_delay, daemon=True).start()
        return status


class DemoShutter(ApsPssShutter):
    """variation of ApsPssShutter for testing"""
    open_bit = Component(EpicsSignal, bit1.pvname)
    close_bit = Component(EpicsSignal, bit2.pvname)


shtr = DemoShutter(name="shtr")

def planB():
    yield from abs_set(shtr, "open", wait=True)
    yield from abs_set(shtr, "close", wait=True)
