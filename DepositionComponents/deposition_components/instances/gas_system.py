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
from ophyd.ophydobj import Kind
from ophyd.status import DeviceStatus
import time
from _collections import OrderedDict

logger = logging.getLogger(__name__)

class MassFlowControl(DepositionListDevice):
    '''
    Device to describe a mass flow controller
    '''
    # kwarg name strings
    PURGE_TEXT = 'purge'
    LOW_LEVEL_VALUE_TEXT = 'low_level_value'
    SETTLE_TIME_TEXT = 'settle_time'
    
    LOW_LEVEL_DEFAULT_VALUE = 5.0
    VALVE_CLOSED_VALUE = 0
    VALVE_OPEN_VALUE = 1
    EPICS_PID_CONTROL_DISABLE = 0
    EPICS_PID_CONTROL_ENABLE = 1
    PLC_BYPASS_DISABLE = 0
    PLC_BYPASS_ENABLE = 1
    flow = FC(EpicsSignal, "{self.prefix}:plc:MFC_{self.instance_number}_IN",
               write_pv="{self.prefix}:plc:MFC_{self.instance_number}_OUT",
               put_complete=True,
                          kind=Kind.config)
    valve_on = FC(EpicsSignal, \
          "{self.prefix}:plc:MFC{self.instance_number}_RB",
          write_pv="{self.prefix}:plc:MFC{self.instance_number}_RC_On_OUT",
          kind=Kind.config,
          put_complete=True)
    plc_bypass = FC(EpicsSignal, \
            "{self.prefix}:plc:MFC{self.instance_number}_Manual_OUT",
            write_pv="{self.prefix}:plc:MFC{self.instance_number}_Manual_OUT",
            put_complete=True,
            kind=Kind.config)
    epics_pid_control = FC(EpicsSignal, \
               '{self.prefix}:userCalc1.{self.instance_letter}',
                write_pv='{self.prefix}:userCalc1.{self.instance_letter}' ,
                kind=Kind.config,
                put_complete=True)
    
    def __init__(self, *args, ch_name=None, mixerNumber=0, mixtureID="", \
                 flow=0, **kwargs):
        self.chName = ch_name
        self.mixtureID = mixtureID
        super(MassFlowControl, self).__init__(*args, **kwargs)
        # depos_sys.gun_selector.ps1_voltage
        
    def close_valve(self, group=None, wait=False):
        '''
        Close the valve that lets deposition gas into the system
        '''
        logger.info("closing valve mfc%d" % self.instance_number)
        yield from bps.abs_set(self.valve_on, self.VALVE_CLOSED_VALUE, \
                               group=group, wait=wait)
        
    def disable_epics_pid_control(self, group=None, wait=False):
        '''
        Disable EPICS PID control
        '''
        logger.info("disabling epics_pid_control mfc%d" % self.instance_number)
        yield from bps.abs_set(self.epics_pid_control, \
                               self.EPICS_PID_CONTROL_DISABLE, \
                               group=group, wait=wait)
        
    def disable_plc_bypass(self, group=None, wait=False):
        '''Disable the PLC bypass
        '''
        logger.info("disabling_plc_bypass mfc%d" % self.instance_number)
        yield from bps.abs_set(self.plc_bypass, \
                               self.PLC_BYPASS_DISABLE, \
                               group=group, wait=wait)
        
    def enable_epics_pid_control(self, group=None, wait=False):
        '''
        Enable EPICS PID control
        '''
        logger.info("enabling_epics_pid_control mfc%d" % self.instance_number)
        yield from bps.abs_set(self.epics_pid_control, \
                               self.EPICS_PID_CONTROL_ENABLE, \
                               group=group, wait=wait)
        
    def enable_plc_bypass(self, group=None, wait=False):
        '''
        Enable the PLC bypass
        '''
        logger.info("enabling pcl_bypass mfc%d" % self.instance_number)
        yield from bps.abs_set(self.plc_bypass, \
                               self.PLC_BYPASS_ENABLE, group=group, wait=wait)
        
    def open_valve(self, group=None, wait=False):
        '''
        Open the valve letting in Deposition gasses
        '''
        logger.info("enabling valve mfc%d" % self.instance_number)
        yield from bps.abs_set(self.valve_on, self.VALVE_OPEN_VALUE, \
                               group=group, wait=wait)

# Commented out JPH use set instead 2018-12-18        
#     def purge(self, leak_rate, low_check_value, group=None, wait=False):
#         '''
#         Purge the syestem.  This method should probably go away.  It is
#         intended to be replaved by the purge option on the "set" command
#         '''
#         logger.info("preparing to purging mfc %d")
#         done_status = DeviceStatus(self)
#         self.valve_on.set(self.VALVE_OPEN_VALUE)
#         self.plc_bypass.set(self.PLC_BYPASS_ENABLE)
#         self.epics_pid_control(self.EPICS_PID_CONTROL_DISABLE)
#         self.flow.set(leak_rate, group=group)
# 
#         def purge_done_cb(value, timestamp, **kwargs):
#             if value < low_check_value:
#                 logger.info("purge of mfc%d is completed" % self.instance_number)
#                 self.valve_on.set(self.VALVE_CLOSED_VALUE, group=group)
#                 self.flow.clear_sub(purge_done_cb)
#                 done_status._finished()
# 
#         self.flow.subscribe(purge_done_cb)
#         return done_status
    
    def set(self, flow_rate, **kwargs):
        '''
        sets the flow of the mass flow controller.  kwargs may contain 
        "purge" a boolean
        "low_level_value" - a float value
        if purge is true, then this will wait until the value of flow is less 
        than the low check value.  Once below the level, this returns a finished
        status.
        If purge is false, then it immediately returns a finished status.
        '''
        logger.info("preparing to set flow mfc %f" % flow_rate)
        settle_time = 5.0
        # override settle time
        if self.SETTLE_TIME_TEXT in kwargs:
            settle_time = kwargs[self.SETTLE_TIME_TEXT]
        # Create a status object with 5
        done_status = DeviceStatus(self, settle_time=5.0)
        start_time = time.time()
        if self.PURGE_TEXT in kwargs:
            purge = kwargs[self.PURGE_TEXT]
        else:
            purge = False
        if purge == True:
            logger.info('doing a purging set')
            self.valve_on.set(self.VALVE_OPEN_VALUE)
            self.plc_bypass.set(self.PLC_BYPASS_ENABLE)
            self.epics_pid_control.set(self.EPICS_PID_CONTROL_DISABLE)
            set_stat = self.flow.set(flow_rate)
            time.sleep(5)
            if self.LOW_LEVEL_VALUE_TEXT in kwargs:
                low_level_value = kwargs[self.LOW_LEVEL_VALUE_TEXT]
            else:
                low_level_value = self.LOW_LEVEL_DEFAULT_VALUE

            def purge_done_cb(value, timestamp, **kwargs):
                time_now = time.time()
                time_since_set = time_now - start_time
                if value < low_level_value:
                    logger.info("purge of mfc%d is completed. Flow = %f" % 
                                (self.instance_number, value))
                    self.flow.set(0.0)
                    self.valve_on.set(self.VALVE_CLOSED_VALUE)
                    self.flow.clear_sub(purge_done_cb) 
                    done_status._finished()

            self.flow.subscribe(purge_done_cb)
        else:
            logger.info('doing a normal set')
            self.flow.set(flow_rate)
            done_status._finished()
        return done_status
    
    def shutdown(self):
        '''
        prepare for shutdown after use
        '''
        yield from self.disable_epics_pid_control()
        yield from self.set_flow(0.0)
        yield from self.close_valve()
            

def _mfc_fields(prefix, field_base, range_, **kwargs):
    defn = OrderedDict()
    
    for i in range_:
        suffix = '{field}{i}'.format(field=field_base, i=i)
        # kwargs['instance_number'] = i
        # kwargs['instance_letter'] = chr(i+64)
        defn['{}{}'.format(field_base, i)] = \
            (MassFlowControl, prefix, {'instance_number':i, 'kind':Kind.normal})
    return defn


class GasMixer(DepositionListDevice):
    MIXED_RELAY_NAME_PATTERN = 'gm_relay_%dm'
    ARGON_RELAY_NAME_PATTERN = 'gm_relay_%da'
    RELAY_OPEN_TEXT = 'High'
    RELAY_CLOSE_TEXT = 'Low'
    gm_mfc_1_flow = FC(EpicsSignal, "{self.prefix}:LJT7:1:AI2",
                       write_pv="{self.prefix}:LJT7:1:AO7",
                       name='gm_mfc_1_flow')
    gm_mfc_2_flow = FC(EpicsSignal, "{self.prefix}:LJT7:1:AI3",
                       write_pv="{self.prefix}:LJT7:1:AO8",
                       name='gm_mfc_2_flow')
    gm_mfc_3_flow = FC(EpicsSignal, "{self.prefix}:LJT7:1:AI0",
                       write_pv="{self.prefix}:LJT7:1:AO2",
                       name='gm_mfc_3_flow')
    gm_mfc_1_purge = FC(EpicsSignal, "{self.prefix}:LJT7:1:DO0",
                     string=True)
    gm_mfc_2_purge = FC(EpicsSignal, "{self.prefix}:LJT7:1:DO1",
                     string=True)
    gm_mfc_3_purge = FC(EpicsSignal, "{self.prefix}:LJT7:1:DO8",
                     string=True)
    gm_pid2_fb_on = FC(EpicsSignal, "{self.prefix}:async_pid_slow2.FBON",
                       name="gm_pid2_fb_on",
                       string=True)
    gm_pid2_setpoint = FC(EpicsSignal, "{self.prefix}:async_pid_slow2.VAL",
                          name='gm_pid2_setpoint')
    gm_pid3_fb_on = FC(EpicsSignal, "{self.prefix}:async_pid_slow3.FBON",
                       name="gm_pid3_fb_on",
                       string=True)
    gm_pid3_setpoint = FC(EpicsSignal, "{self.prefix}:async_pid_slow3.VAL",
                          name='gm_pid3_setpoint')
    gm_relay_1a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO0",
                     name='gm_relay_1a',
                     string=True)
    gm_relay_1m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO1",
                     name='gm_relay_1m',
                     string=True)
    gm_relay_2a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO2",
                     name='gm_relay_2a',
                     string=True)
    gm_relay_2m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO3",
                     name='gm_relay_2m',
                     string=True)
    gm_relay_3a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO4",
                     name='gm_relay_3a',
                     string=True)
    gm_relay_3m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO5",
                     name='gm_relay_3m',
                     string=True)
    gm_relay_4a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO6",
                     name='gm_relay_4a',
                     string=True)
    gm_relay_4m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO7",
                     name='gm_relay_4m',
                     string=True)
    gm_relay_5a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO8",
                     name='gm_relay_5a',
                     string=True)
    gm_relay_5m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO9",
                     name='gm_relay_5m',
                     string=True)
    gm_relay_6a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO10",
                     name='gm_relay_6a',
                     string=True)
    gm_relay_6m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO11",
                     name='gm_relay_6m',
                     string=True)
    gm_relay_7a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO12",
                     name='gm_relay_7a',
                     string=True)
    gm_relay_7m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO13",
                     name='gm_relay_7m',
                     string=True)
    gm_relay_8a = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO14",
                     name='gm_relay_8a',
                     string=True)
    gm_relay_8m = FC(EpicsSignal, "{self.prefix}:LJT7:2:DO15",
                     name='gm_relay_8m',
                     string=True)

    mfcs = DDC(_mfc_fields('', 'mfc', range(1, 9)))
    
    def close_mfc_valves(self, mfc_names=None):
        '''
        Close the valves which feed deposition gas mixture to the deposition
        chamber
        '''
        logger.info("Closing valves for all MFCs")
        # if mfc_names is empty construct a list of all mfcs
        if mfc_names == None:
            mfc_names = self.mfcs.component_names
        # Loop over specified mfcs
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.close_valve(group='close_valves')
            logger.debug("mfc % s" % mfc)
        yield from bps.wait(group='close_valves')
        
    def close_mixed_gas_relays(self, relay_nums=None):
        '''
        Close off mixed gas from entering the chamber
        '''
        # if no valve list is specified then close all the valves.
        if relay_nums is None:
            relay_nums = range(1, 9)
        # loop over closing the selected valves
        for relay in relay_nums:
            relay_name = self.MIXED_RELAY_NAME_PATTERN % relay
            logger.info("closing relay %s" % relay_name)
            yield from bps.abs_set(self.__getattr__(relay_name), \
                                   self.RELAY_CLOSE_TEXT,
                                   group='close_mixed_gas_relays')
        yield from bps.wait(group='close_mixed_gas_relays')

    def close_argon_gas_relays(self, relay_nums=None):
        '''
        Close off the pure argon gas supply to the 
        '''
        if relay_nums is None:
            relay_nums = range(1, 9)
        logger.info("relay_nums %s" % relay_nums)
        for relay in relay_nums:
            relay_name = self.ARGON_RELAY_NAME_PATTERN % relay
            logger.info("closing relay %s" % relay_name)
            yield from bps.abs_set(self.__getattr__(relay_name), \
                                   self.RELAY_CLOSE_TEXT, \
                                   group='close_argon_gas_relays')
        yield from bps.wait(group='close_mixed_gas_relays')
        
    def disable_mfc_plc_bypass(self, mfc_names=None):
        logger.info("Disabling plc_bypass for all MFCs")
        if mfc_names == None:
            mfc_names = self.mfcs.component_names
        for mfc_name in self.mfcs.component_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.disable_plc_bypass(group='disable_plc_bypass')
            logger.debug("mfc % s" % mfc)
        yield from bps.wait(group='disable_plc_bypass')
        
    def disable_all_gm_pid_loops(self):
        logger.info("disable all gas mixer pid loops")
        yield from bps.mv(self.gm_pid2_setpoint, 0.000)
        yield from bps.mv(self.gm_pid3_setpoint, 0.000)
            
    def disable_mfc_epics_pid_control(self, mfc_names=None):
        logger.info("Disabling epics_pid_control for all MFCs")
        if mfc_names == None:
            mfc_names = self.mfcs.component_names
            
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.disable_epics_pid_control(group='disable_pid_control')
            logger.debug("mfc % s" % mfc)
        yield from bps.wait(group='disable_pid_control')
        
    def disable_all_gm_supply_flows(self):
        logger.info("Disabling all gas mixer supply flows")
        yield from bps.mv(self.gm_mfc_1_flow, 0.000)
        yield from bps.mv(self.gm_mfc_2_flow, 0.000)
        yield from bps.mv(self.gm_mfc_2_flow, 0.000)
        
    def enable_mfc_plc_bypass(self, mfc_names=None):
        logger.info("Enabling plc_bypass for all MFCs")
        if mfc_names == None:
            mfc_names = self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.enable_plc_bypass(group='enable_plc_bypass')
            logger.debug("mfc % s" % mfc)
        bps.wait(group='enable_bps_bypass')
            
    def enable_mfc_epics_pid_control(self, mfc_names=None):
        logger.info("enabling epics_pid_control for all MFCs")
        if mfc_names == None:
            mfc_names = self.mfcs.component_names
            
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.enable_epics_pid_control(group='enable_pid_control')
            logger.debug("mfc % s" % mfc)
        yield from bps.wait(group='enable_pid_control')
        
    def open_mixed_gas_relays(self, relay_nums=None):
        # if no relay_nums defined use them all.
        if relay_nums is None:
            relay_nums = range(1, 9)
        # Make sure to close all of the argon gas relays before opening the 
        # mixed gas relays
        yield from self.close_argon_gas_relays()
        # then finally open the mixed gas relayspurge of mfc%d is completed
        for relay in relay_nums:
            relay_name = self.MIXED_RELAY_NAME_PATTERN % relay
            yield from bps.abs_set(self.__getattr__(relay_name),
                                   self.RELAY_OPEN_TEXT,
                                   group='open_mixed_gas_relays')
        yield from bps.wait(group='open_mixed_gas_relays')
    
    def open_mfc_valves(self, mfc_names=None):
        logger.info("Opening valves for all MFCs")
        if mfc_names == None:
            mfc_names = self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from mfc.open_valve(group='open_valves')
            logger.debug("mfc % s" % mfc)
        yield from bps.wait('open_valves')
        
    def open_argon_gas_relays(self, relay_nums=None):
        # if no relay numbers are defined than use all of them
        if relay_nums is None:
            relay_nums = range(1, 9)
        # Make sure to close all of the mixed gas relays before openging these
        yield from self.close_mixed_gas_relays()
        # and now open the argon gas relays
        for relay in relay_nums:
            relay_name = self.ARGON_RELAY_NAME_PATTERN % relay
            yield from bps.abs_set(self.__getattr__(relay_name),
                                   self.RELAY_OPEN_TEXT,
                               group='open_argon_gas_relays')
        yield from bps.wait(group='open_argon_gas_relays')
    
    def set_mfc_flows(self, new_flow, mfc_names=None):
        if mfc_names == None:
            mfc_names = self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_name)
            yield from bps.abs_set(mfc, new_flow, group='set_flows', wait=True)
        yield from bps.wait('set_flows')        
        
    def purge_mfcs(self, mfc_names=None, leak_rate=25, low_value=5):
        
        if mfc_names == None:
            mfc_names = self.mfcs.component_names
        yield from self.close_argon_gas_relays()
        yield from self.close_mixed_gas_relays()
        for mfc_name in mfc_names:
            logger.info("Purging %s" % mfc_name)
            mfc = self.mfcs.__getattr__(mfc_name)
#             yield from mfc.open_valve()
#             yield from mfc.enable_plc_bypass()
#             yield from mfc.disable_epics_pid_control()
            kwargs = {'purge': True,
                      'low_check_value':low_value,
                      'group':'purge_mfcs'}
            yield from bps.abs_set(mfc, leak_rate, **kwargs)
#             yield from mfc.close_valve()
        # bps.sleep(30)
        yield from bps.wait(group='purge_mfcs')
        
    def shutdown(self):
        yield from self.disable_all_supply_flows()
        yield from self.disable_pid_loops()
        yield from self.close_mixed_gas_relays()
        yield from self.close_argon_gas_flows()
        mfc_names = self.mfcs.component_names
        for mfc_name in mfc_names:
            mfc = self.mfcs.__getattr__(mfc_names)
            yield from mfc.shutdown()
