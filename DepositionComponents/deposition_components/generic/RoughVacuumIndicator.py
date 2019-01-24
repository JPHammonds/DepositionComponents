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

class RoughVacuumIndicator(DepositionListDevice):
     
#     def set(self, value):
#         '''need to set this up to turn the gauge on and off but provide protections
#         needed such as watching the pressure on another less accurate gauge 
#         to ensure low enough pressure that we dont damage the gauge
#         '''
    def __init__(self, prefix, **kwargs):
        super(RoughVacuumIndicator, self).__init__(prefix, **kwargs)
