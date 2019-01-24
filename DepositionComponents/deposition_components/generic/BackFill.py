'''
Created on Jan 23, 2019

@author: hammonds
'''
from deposition_components.DepositionListDevice import DepositionListDevice
from ophyd.signal import EpicsSignal
from ophyd.status import DeviceStatus
from ophyd import (Component as Cpt, DynamicDeviceComponent as DDC,
                   FormattedComponent as FC)

class BackFill(DepositionListDevice):
    ar_high_rate = FC(EpicsSignal,
                   '{self.prefix}{self.ar_high_rate_read_pv_suffix}',
                   write_pv='{self.prefix}{self.ar_high_rate_write_pv_suffix}',
                   name='ar_backfill_high_rate')
    ar_low_rate = FC(EpicsSignal,
                  '{self.prefix}{self.ar_low_rate_read_pv_suffix}',
                  write_pv='{self.prefix}{self.ar_low_rate_write_pv_suffix}',
                  name='ar_backfill_low_rate')
    overpressure = FC(EpicsSignal,
                      '{self.prefix}{self.overpressure_read_pv_suffix}',
                      write_pv=\
                         '{self.prefix}{self.overpressure_write_pv_suffix}',
                      name='overpressure') 
    
    def __init__(self, prefix,
                 ar_high_rate_read_pv_suffix,
                 ar_high_rate_write_pv_suffix,
                 ar_low_rate_read_pv_suffix,
                 ar_low_rate_write_pv_suffix,
                 overpressure_read_pv_suffix,
                 overpressure_write_pv_suffix,
                 **kwargs):
        self.ar_high_rate_read_pv_suffix = ar_high_rate_read_pv_suffix
        self.ar_high_rate_write_pv_suffix = ar_high_rate_write_pv_suffix
        self.ar_low_rate_read_pv_suffix = ar_low_rate_read_pv_suffix
        self.ar_low_rate_write_pv_suffix = ar_low_rate_write_pv_suffix
        self.overpressure_read_pv_suffix = overpressure_read_pv_suffix
        self.overpressure_write_pv_suffix = overpressure_write_pv_suffix
        super(BackFill, self).__init__(prefix, **kwargs)
        
    def set(self, rate):
        ''' 
        Set the backfill rate
        0 - Off
        1 - Low
        2 - High
        ''' 
        status = DeviceStatus()
        if rate < 0 or rate > 2:
            raise ValueError("Backfill value is expected to be one of 0-Off, "
                             "1-low, 2-high")
        elif rate == 0:
            self.ar_high_rate.set(0)
            self.ar_low_rate.set(0)
        elif rate == 1:
            self.ar_high_rate.set(0)
            self.ar_low_rate.set(1)
        elif rate == 2:
            self.ar_low_rate.set(0)
            self.ar_high_rate.set(1)
        return status._finished()

    
