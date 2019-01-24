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
from ophyd.status import DeviceStatus
logger = logging.getLogger(__name__)

class SealsPump(DepositionListDevice):
    power_on = FC(EpicsSignal,
                  '{self.prefix}{self.power_on_read_pv_suffix}',
                  write_pv='{self.prefix}{self.power_on_write_pv_suffix}',
                  name='power_on')
    
    def __init__(self, prefix,
                 power_on_read_pv_suffix,
                 power_on_write_pv_suffix,
                 **kwargs):
        self.power_on_read_pv_suffix = power_on_read_pv_suffix
        self.power_on_write_pv_suffix = power_on_write_pv_suffix
        super(SealsPump, self).__init__(prefix, **kwargs)
        
    def set(self, value, **kwargs):
        stat = DeviceStatus()
