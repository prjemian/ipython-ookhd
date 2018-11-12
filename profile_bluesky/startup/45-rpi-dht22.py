print(__file__)

"""Raspberry Pi with DHT22 sensor running EPICS IOC"""

class DHT22Average(Device):
    average = Component(EpicsSignal, "")
    sdev = Component(EpicsSignal, ":sdev")

class RpiDHT22(Device):
    available = Component(EpicsSignal, "available")
    status = Component(EpicsSignal, "status")
    humidity = Component(EpicsSignal, "humidity")
    temperature = Component(EpicsSignal, "temperature")
    humidity_1m = Component(DHT22Average, "humidity:1m")
    humidity_15m = Component(DHT22Average, "humidity:15m")
    humidity_60m = Component(DHT22Average, "humidity:60m")
    temperature_1m = Component(DHT22Average, "temperature:1m")
    temperature_15m = Component(DHT22Average, "temperature:15m")
    temperature_60m = Component(DHT22Average, "temperature:60m")

try:
    rpi5bf5 = RpiDHT22("rpi5bf5:0:", name="rpi5bf5")
    # sd.monitors.append(rpi5bf5)
    # raise this now:
    #  ValueError: Subscription type not set and object rpi5bf5 of class RpiDHT22 has no default subscription set
except Exception as exc:
    print("Could not connect RPi sensor:", exc)
