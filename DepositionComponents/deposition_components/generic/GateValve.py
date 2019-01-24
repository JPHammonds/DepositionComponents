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

VALVE_ALL_OPEN = 100.0
VALVE_ALL_CLOSED = 0.000

class GateValve(DepositionListDevice):
    VALVE_ALL_OPEN = 100.0
    VALVE_ALL_CLOSED = 0.000
    valve_position = FC(EpicsSignal, "{self.prefix}{self.position_read_pv_suffix}",
                             write_pv="{self.prefix}{self.position_write_pv_suffix}",
                             tolerance=0.5,
                             name='valve_position')
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
                 position_read_pv_suffix,
                 position_write_pv_suffix,
                 close_request_read_pv_suffix,
                 close_request_write_pv_suffix,
                 open_request_read_pv_suffix,
                 open_request_write_pv_suffix,
                 fully_open_read_pv_suffix,
                 fully_closed_read_pv_suffix,
                 **kwargs):
        self.position_read_pv_suffix = position_read_pv_suffix
        self.position_write_pv_suffix = position_write_pv_suffix
        self.close_request_read_pv_suffix = close_request_read_pv_suffix
        self.close_request_write_pv_suffix = close_request_write_pv_suffix
        self.open_request_read_pv_suffix = open_request_read_pv_suffix
        self.open_request_write_pv_suffix = open_request_write_pv_suffix
        self.fully_open_read_pv_suffix = fully_open_read_pv_suffix
        self.fully_closed_read_pv_suffix = fully_closed_read_pv_suffix
        
        super(GateValve, self).__init__(prefix, **kwargs)
        
    def close(self, group='gate_valves'):
        logger.info("Closing gate valve")
        yield from bps.abs_set(self.valve_position, \
                               VALVE_ALL_CLOSED, \
                               group=group)
         
    def open(self, position=VALVE_ALL_OPEN, \
                        group='gate_valves'):
        logger.info("Opening gate valve to position %f" % position)
        yield from bps.abs_set(self.valve_position, \
                               position, \
                               group=group)
        
    def is_open(self):
        return self.valve_position.get() > 0
    
    def is_fully_open(self):
        return self.fully_open.get() == 1
    
    def is_fully_closed(self):
        return self.fully_closed.get() == 1
    
    def status(self):
        logger.info("Position: %f" % self.valve_position.get())
        logger.info("Fully Open: %s" % self.fully_open.get())
        logger.info("Fully Closed: %s" % self.fully_closed.get())
