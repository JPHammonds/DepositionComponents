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

class DigitalGateValve(DepositionListDevice):    
    VALVE_ALL_OPEN = 100.0
    VALVE_ALL_CLOSED = 0.000
    close_request = FC(EpicsSignal, \
                      "{self.prefix}{self.close_request_read_pv_suffix}", \
                          write_pv="{self.prefix}{self.close_request_write_pv_suffix}", \
                          name='close_request')
    open_request = FC(EpicsSignal, \
                         "{self.prefix}{self.open_request_read_pv_suffix}", \
                         write_pv="{self.prefix}{self.open_request_write_pv_suffix}", \
                         name='open_request')
    fully_open = FC(EpicsSignal, \
                                 '{self.prefix}{self.fully_open_read_pv_suffix}', \
                                 name='fully_open')
    fully_closed = FC(EpicsSignal, \
                                 '{self.prefix}{self.fully_closed_read_pv_suffix}', \
                                 name='fully_closed')

    def __init__(self, prefix,
                 close_request_read_pv_suffix,
                 close_request_write_pv_suffix,
                 open_request_read_pv_suffix,
                 open_request_write_pv_suffix,
                 fully_open_read_pv_suffix,
                 fully_closed_read_pv_suffix,
                 **kwargs):
        self.close_request_read_pv_suffix = close_request_read_pv_suffix
        self.close_request_write_pv_suffix = close_request_write_pv_suffix
        self.open_request_read_pv_suffix = open_request_read_pv_suffix
        self.open_request_write_pv_suffix = open_request_write_pv_suffix
        self.fully_open_read_pv_suffix = fully_open_read_pv_suffix
        self.fully_closed_read_pv_suffix = fully_closed_read_pv_suffix
        
        super(DigitalGateValve, self).__init__(prefix, **kwargs)

