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

CCG_ON_VALUE = 1
CCG_OFF_VALUE = 0

class ColdCathodeGauge(DepositionListDevice):
    '''
    Device class to handle aspects of a cold cathode gauge
    '''
    ccg_power_on = FC(EpicsSignal,
                      "{self.prefix}{self.power_on_read_pv_suffix}",
                      write_pv="{self.prefix}{self.power_on_write_pv_suffix}",
                      name='ccg_power_on',
                      put_complete=True)
    ccg_pressure = FC(EpicsSignal,
                      '{self.prefix}{self.pressure_read_pv_suffix}',
                      name='ccg_pressure')

    def __init__(self, prefix,
                 power_on_read_pv_suffix,
                 power_on_write_pv_suffix,
                 pressure_read_pv_suffix,
                 **kwargs):
        '''
        initialize & grab keys used to complete pv names
        '''
        self.power_on_read_pv_suffix = power_on_read_pv_suffix
        self.power_on_write_pv_suffix = power_on_write_pv_suffix
        self.pressure_read_pv_suffix = pressure_read_pv_suffix
        super(ColdCathodeGauge, self).__init__(prefix, **kwargs)
        
    def disable(self, group='cathode_gauges'):
        '''
        Method to disable the gauge.  This will avoid gauge burnout at high 
        pressures
        '''
        logger.info("Disabling CCG")
        
        yield from bps.abs_set(self.ccg_power_on, CCG_OFF_VALUE, \
                               group=group)
        
    def enable(self, group='cathode_gauges'):
        '''
        Enable the gauge to place it in operating state
        '''
        logger.info("Disabling CCG")
        yield from bps.abs_set(self.ccg_power_on, CCG_ON_VALUE, \
                               group=group)

    
