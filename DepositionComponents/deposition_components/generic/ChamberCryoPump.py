'''
Created on Jan 23, 2019

@author: hammonds
'''
from deposition_components.DepositionListDevice import DepositionListDevice
from ophyd import (Component as Cpt, DynamicDeviceComponent as DDC,
                   FormattedComponent as FC)
from ophyd.signal import EpicsSignal

class ChamberCryoPump(DepositionListDevice):
    power_on = FC(EpicsSignal, '{self.prefix}{self.power_on_read_pv_suffix}',
               write_pv='{self.prefix}{self.power_on_write_pv_suffix}',
               name='power_on')
    exhaust_to_vp1 = FC(EpicsSignal,
                        '{self.prefix}{self.exhaust_read_pv_suffix}',
                        write_pv='{self.prefix}{self.exhaust_write_pv_suffix}',
                        name='exhaust_to_vp1')
    pressure = FC(EpicsSignal, "{self.prefix}{self.pressure_read_pv_suffix}",
                    name='pressure')
    temperature_status = FC(EpicsSignal,
                            "{self.prefix}{self.temp_status_read_pv_suffix}",
                            name='temperature_status')
    n2_purge = FC(EpicsSignal, "{self.prefix}{self.n2_purge_read_pv_suffix}",
              write_pv="{self.prefix}{self.n2_purge_write_pv_suffix}",
              name='n2_purge')

    def __init__(self, prefix,
                 power_on_read_pv_suffix,
                 power_on_write_pv_suffix,
                 exhaust_read_pv_suffix,
                 exhaust_write_pv_suffix,
                 pressure_read_pv_suffix,
                 temp_status_read_pv_suffix,
                 n2_purge_read_pv_suffix,
                 n2_purge_write_pv_suffix,
                 **kwargs):
        self.power_on_read_pv_suffix = power_on_read_pv_suffix
        self.power_on_write_pv_suffix = power_on_write_pv_suffix
        self.exhaust_read_pv_suffix = exhaust_read_pv_suffix
        self.exhaust_write_pv_suffix = exhaust_write_pv_suffix
        self.pressure_read_pv_suffix = pressure_read_pv_suffix
        self.temp_status_read_pv_suffix = temp_status_read_pv_suffix
        self.n2_purge_read_pv_suffix = n2_purge_read_pv_suffix
        self.n2_purge_write_pv_suffix = n2_purge_write_pv_suffix
        super(ChamberCryoPump, self).__init__(prefix, **kwargs)
        
    def is_cryo_on(self):
        return self.power_on.get() == 1
        
    def is_cryo_exhausting_to_vp1(self):
        return self.exhaust_to_vp1.get() == 1
    
#     def set(self):
#         '''
#         Turn the cryo pump on, but make sure that it is ready before turning 
#         it on and make sure that it is on before completion
#         '''
