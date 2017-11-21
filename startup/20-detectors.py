print(__file__)

from APS_BlueSky_tools.examples import SynPseudoVoigt
from ophyd import (EpicsScaler, EpicsSignal, EpicsSignalRO,
                   Device, DeviceStatus)
from ophyd import Component as Cpt
import time

aps_current = EpicsSignalRO("S:SRcurrentAI", name="aps_current")

## Beam Monitor Counts
#bs_bm2 = EpicsSignalRO('BL14B:Det:BM2', name='bs_bm2')
noisy = EpicsSignalRO('xxx:userCalc1', name='noisy')
scaler = EpicsScaler('xxx:scaler1', name='scaler')

synthetic_pseudovoigt = SynPseudoVoigt(
    'synthetic_pseudovoigt', m1, 'm1', 
    center=-1.5 + 0.5*np.random.uniform(), 
    eta=0.2 + 0.5*np.random.uniform(), 
    sigma=0.001 + 0.05*np.random.uniform(), 
    scale=1e5,
    bkg=0.01*np.random.uniform())

if False:
    RE(bp.tune_centroid(
        [synthetic_pseudovoigt], 
        'synthetic_pseudovoigt',
        m1, -5, 5, 1e-4, 
        step_factor=3,
        num=15,
        snake=True,
    ))
    RE(bp.scan([synthetic_pseudovoigt], m1, 
        m1.read()["m1"]["value"] - 3*synthetic_pseudovoigt.sigma,
        m1.read()["m1"]["value"] + 3*synthetic_pseudovoigt.sigma,
        20))
