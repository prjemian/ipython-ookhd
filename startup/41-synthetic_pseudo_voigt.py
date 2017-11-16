print(__file__)


import ophyd.sim
from APS_BlueSky_tools.examples import SynPseudoVoigt

synthetic_pseudovoigt = SynPseudoVoigt(
    'synthetic_pseudovoigt', m1, 'm1', 
    center=-1.5 + 0.5*np.random.uniform(), 
    eta=0.2 + 0.5*np.random.uniform(), 
    sigma=0.001 + 0.05*np.random.uniform(), 
    scale=1e5,
    bkg=0.01*np.random.uniform())

#  RE(bp.scan([synthetic_pseudovoigt], m1, -2, 0, 219))
