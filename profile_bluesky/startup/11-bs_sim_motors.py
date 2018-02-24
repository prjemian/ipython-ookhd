print(__file__)

"""bluesky simulated motors and detectors"""

from ophyd.sim import motor1, motor2, motor3
from ophyd.sim import det1, det2 
from bluesky.callbacks.fitting import PeakStats
from ophyd.sim import SynGauss

append_wa_motor_list(motor1, motor2, motor3)


# TODO: generalize this with ideas further below
class TunableAxisMixin_v1(object):
    """
    an axis should know how to tune itself
    """
    tune_start = -1
    tune_finish = 1
    tune_num = 11
    tune_time_s = 1
    tune_det = None
    std_stage_sigs = OrderedDict()
    tune_stage_sigs = OrderedDict()
    tune_peaks = None
    tune_ok = False
    tune_center = None
    
    def tune(self, det=None, start=None, finish=None, num=None, time=None, md=None):
        """
        tune this axis with the named detector in a single pass
        
        PARAMETERS

        det : obj
            detector object (must be provided on first use)
        start : float
            axis starting position
        finish : float
            axis ending position
        num : int
            number of steps
        time : float
            counting time (s) at each step
        md : dict
            scan metadata dictionary
        
        RAISES
        
        `ValueError` if cannot tune
        """
        self.tune_det = det or self.tune_det
        self.tune_start = start or self.tune_start
        self.tune_finish = finish or self.tune_finish
        self.tune_num = num or self.tune_num
        self.tune_time_s = time or self.tune_time_s
        self.tune_pretune_position = self.position
        
        if self.tune_det is None:
            msg = "Must supply a detector, none specified."
            raise ValueError(msg)
        
        # additional metadata
        if md is None:
            md = OrderedDict()
        md["tune_det"] = self.tune_det.name
        md["tune_axis"] = self.name
        md["tune_start"] = self.tune_start
        md["tune_finish"] = self.tune_finish
        md["tune_num"] = self.tune_num
        md["tune_time_s"] = self.tune_time_s

        # additional staging for tuning
        # use a class attribute as fallback in case restore is missed
        self.std_stage_sigs = self.stage_sigs
        self.stage_sigs.update(self.tune_stage_sigs)

        # stage the counting time
        det_time = self.tune_time_s
        # FIXME: stage or set?
        # yield from bps.mv(self.tune_det.exposure_time, self.tune_time_s)
        
        # prepare to get pl_MAX, pl_MIN, and PL_COM
        self.tune_peaks = PeakStats(x=self.name, y=self.tune_det.name)
        
        def peak_detected():
            """
            returns True if a peak was detected, otherwise False
            
            The default algorithm identifies a peak when the maximum
            value is four times the minimum value.  Change this routine
            by subclassing :class:`TuneAxis` and override :meth:`peak_detected`.
            """
            if self.tune_peaks is None:
                return False
            self.tune_peaks.compute()
            if self.tune_peaks.max is None:
                return False
            
            ymax = self.tune_peaks.max[-1]
            ymin = self.tune_peaks.min[-1]
            return ymax > 4*ymin        # this works for USAXS

        yield from bpp.subs_wrapper(
            bp.rel_scan(
                [self.tune_det], 
                self, 
                self.tune_start, 
                self.tune_finish, 
                self.tune_num, 
                md=md),
            self.tune_peaks
        )

        # restore standard staging
        self.stage_sigs = self.std_stage_sigs
        self.tune_time_s = det_time
        
        if peak_detected():
            self.tune_ok = True
            self.tune_center = self.tune_peaks.cen
            yield from bps.mv(self, self.tune_center)
        else:
            self.tune_ok = False
            self.tune_center = None
            yield from bps.mv(self, self.tune_pretune_position)
            msg = "tune {} v. {}: no tunable peak found"
            raise ValueError(msg.format(self.tune_det.name, self.name))


class TunableSynAxis_v1(ophyd.sim.SynAxis, TunableAxisMixin_v1): pass

motor4 = TunableSynAxis_v1(name='motor4')
det_gaussian = SynGauss('det1', motor4, 'motor4', center=.42, Imax=0.98e5, sigma=.127)


#------------------------------------------------------------------


""" more ideas on generalized tuning, allow customized tuning
Mixin
    # Mixin MUST not provide __init__() method, instead use self.tuner.config()
    self.tuner is set to instance of AxisTuner
    self.tune(md=md, **kwargs) calls self.tuner.tune(md=md, **kwargs)

class AxisTunerBase(object):
    ok = False
    center = None
    def tune(md=md, **kwargs): ...
    def config(**kwargs): ...
    def peak_detected(): ...


class UsaxsAxisTuner(AxisTunerBase):
    # implement algorithm from SPEC here

# TODO:  other BlueSky tuning algorithms

"""
