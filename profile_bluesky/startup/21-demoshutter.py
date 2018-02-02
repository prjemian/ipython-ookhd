print(__file__)

"""test a demo shutter"""

import threading

class DemoShutter(Device):
    open_bit = Component(EpicsSignal, bit1.pvname)
    close_bit = Component(EpicsSignal, bit2.pvname)
    delay_s = 1.0
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
        self.valid_open_values = list(map(str.lower, map(str, self.valid_open_values)))
        self.valid_close_values = list(map(str.lower, map(str, self.valid_close_values)))
        
        status = DeviceStatus(self)
        print("start", status)
        
        def move_shutter():
            if str(value).lower() in self.valid_open_values:
                yield from mv(self.open_bit, 1)
            elif str(value).lower() in self.valid_close_values:
                yield from mv(self.close_bit, 1)
            else:
                acceptables = self.valid_open_values + self.valid_close_values
                msg = "value should be one of " + str(acceptables)
                msg += " : received " + str(value)
                raise ValueError(msg)
        
        def run_and_delay():
            print("run_and_delay", thread, status)
            move_shutter()
            #yield from sleep(self.delay_s)
            status._finished(success=True)
            print("thread complete", thread, status)
        
        thread = threading.Thread(target=run_and_delay, daemon=True)
        thread.start()
        print("thread started", thread, status)
        return status


shtr = DemoShutter(name="shtr")

def planB():
    yield from abs_set(shtr, "open", wait=True)
    yield from abs_set(shtr, "close", wait=True)
