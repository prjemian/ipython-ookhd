print(__file__)

"""test some ideas"""

class SseqRecord(Device):
    dol1 = Component(EpicsSignal, ".DOL1")
    dly1 = Component(EpicsSignal, ".DLY1")
    lnk1 = Component(EpicsSignal, ".LNK1")
    flnk = Component(EpicsSignal, ".FLNK")
    enable = Component(EpicsSignal, "Enable")
    enable_calc = Component(EpicsSignal, "EnableCalc")

"""
demo of how PSS shutter works

set open bit, PSS resets it a short time later

xxx:bit1 will act like OPEN bit
xxx:bit2 will act like CLOSE bit
There is no status bit
"""
RESET_DELAY_S = 1.0

bit1 = EpicsSignal("xxx:bit1", name="bit1")
bit2 = EpicsSignal("xxx:bit2", name="bit2")

calc1 = calcs.calc1
calc2 = calcs.calc2

sseq_enable = EpicsSignal("xxx:userStringSeqEnable", name="sseq_enable")
sseq1 = SseqRecord("xxx:userStringSeq1", name="sseq1")
sseq2 = SseqRecord("xxx:userStringSeq2", name="sseq2")

sseq_enable.put(1)

def initBitReset(bit, sseq, calc):
    """
    setting bit to 1 waits a short delay, then resets the bit
    """
    # FIXME: Why is this needed?  synApps question
    __calc_enable = EpicsSignal(calc.prefix+"EnableCalc", name="__calc_enable")
    __calc_enable.put(1)
    
    sseq.enable.put(1)
    sseq.enable_calc.put(1)
    
    calc.outn.put(bit.pvname)
    sseq.dol1.put(bit.pvname + " CP NMS")
    sseq.dly1.put(RESET_DELAY_S)
    sseq.lnk1.put(calc.channels.A.value.pvname + " CP NMS")
    sseq.flnk.put(calc.prefix)

try:
    initBitReset(bit1, sseq1, calc1)
    initBitReset(bit2, sseq2, calc2)
except Exception as exc:
    print(exc)
