print(__file__)

"""various detectors and other signals"""

from ophyd.scaler import ScalerCH
from APS_BlueSky_tools.examples import SynPseudoVoigt
import APS_BlueSky_tools.devices as APS_devices

noisy = EpicsSignalRO('xxx:userCalc1', name='noisy')
# scaler = EpicsScaler('xxx:scaler1', name='scaler')
scaler = ScalerCH("xxx:scaler1", name="scaler")
scaler.channels.chan04.chname.put("scint")
scaler.channels.chan07.chname.put("roi1")

scaler.match_names()
APS_devices.use_EPICS_scaler_channels(scaler)


synthetic_pseudovoigt = SynPseudoVoigt(
    'synthetic_pseudovoigt', m1, 'm1', 
    center=-1.5 + 0.5*np.random.uniform(), 
    eta=0.2 + 0.5*np.random.uniform(), 
    sigma=0.001 + 0.05*np.random.uniform(), 
    scale=1e5,
    bkg=0.01*np.random.uniform())

def tune_centroid_example():
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
