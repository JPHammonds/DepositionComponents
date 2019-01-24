'''
Created on Jan 23, 2019

@author: hammonds
'''

import logging
import bluesky.plan_stubs as bps
from ophyd import (Component as Cpt, DynamicDeviceComponent as DDC,
                   FormattedComponent as FC)
from deposition_components.DepositionListDevice import DepositionListDevice
from ophyd.signal import EpicsSignal
logger = logging.getLogger(__name__)

class VariableFrequencyDrivePump(DepositionListDevice):
    speed = FC(EpicsSignal,
                '{self.prefix}{self.speed_read_pv_suffix}',
                write_pv='{self.prefix}{self.speed_write_pv_suffix}',
                name='speed')
    n2_purge = FC(EpicsSignal, '{self.prefix}{self.n2_purge_read_pv_suffix}',
                   write_pv='{self.prefix}{self.n2_purge_write_pv_suffix}',
                   name='n2_purge')
    power_on = FC(EpicsSignal,
                   '{self.prefix}{self.power_on_read_pv_suffix}',
                   write_pv='{self.prefix}{self.power_on_write_pv_suffix}',
                   name='power_on')
    
    def __init__(self, prefix,
                 speed_read_pv_suffix,
                 speed_write_pv_suffix,
                 n2_purge_read_pv_suffix,
                 n2_purge_write_pv_suffix,
                 power_on_read_pv_suffix,
                 power_on_write_pv_suffix,
                  **kwargs):
        self.speed_read_pv_suffix = speed_read_pv_suffix
        self.speed_write_pv_suffix = speed_write_pv_suffix
        self.n2_purge_read_pv_suffix = n2_purge_read_pv_suffix
        self.n2_purge_write_pv_suffix = n2_purge_write_pv_suffix
        self.power_on_read_pv_suffix = power_on_read_pv_suffix
        self.power_on_write_pv_suffix = power_on_write_pv_suffix
        super(VariableFrequencyDrivePump, self).__init__(prefix, **kwargs)
