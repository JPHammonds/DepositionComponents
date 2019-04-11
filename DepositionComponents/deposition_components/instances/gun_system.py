'''
Created on Jan 23, 2019

@author: hammonds
'''
import logging
from _collections import OrderedDict
from deposition_components.DepositionListDevice import DepositionListDevice
import bluesky.plan_stubs as bps
from ophyd.signal import EpicsSignal, Signal
from ophyd.ophydobj import Kind
from ophyd import (Component as Cpt, DynamicDeviceComponent as DDC,
                   FormattedComponent as FC)
from ophyd.status import DeviceStatus

logger = logging.getLogger(__name__)

NUMBER_OF_GUNS = 8

def _gun_fields(prefix, field_base, range_, **kwargs):
    defn = OrderedDict()
    
    for i in range_:
        suffix = '{field}{i}'.format(field=field_base, i=i)
        kwargs['instance_number'] = i
        defn['{}{}'.format(field_base, i)] = (Gun, prefix, \
                                              {'instance_number':i,
                                               'kind':Kind.normal})
    return defn


class Gun(DepositionListDevice):
    # Configure these as FormattedComponents
    relay_magnetron = FC(EpicsSignal, \
         "{self.prefix}:plc:Magnetron_{self.instance_number}_Power_RB",
          write_pv="{self.prefix}:plc:Mag{self.instance_number}_Pwr_Enable_OUT",
          name="relay_magnetron",
#          string=True,
          put_complete=True,
          kind=Kind.config)
    voltage_avg = FC(EpicsSignal,
                     "{self.prefix}:userAve{self.instance_number}.VAL",
                      name='voltage_avg',
                      kind=Kind.config)
    water_flow_cathode = FC(EpicsSignal, \
                        "{self.prefix}:userCalcOut1{self.instance_number}.VAL",
                         name="water_flow_cathode",
                         kind=Kind.config)
    mask_width = Cpt(Signal, value=40)
    zero_position = Cpt(Signal, value=0.0)
    coat_velocity = Cpt(Signal, value=75.0)
    travel_velocity = Cpt(Signal, value=75.0)
    high_position = Cpt(Signal, value=0.0)
    low_position = Cpt(Signal, value=0.0)

    def __init__(self, *args, ch_name=None, \
                 mask_width=40.0, zero_position=1000.0, \
                 sample_lower_extent=100.0, sample_upper_extent=250, \
                 coat_velocity=10.0, travel_velocity=15.0, \
                 overspray=45.0, **kwargs):
        self._ch_name = ch_name
#         self.mask_width = mask_width
#         self.zero_position = zero_positionbackfill
#         self.coat_velocity = coat_velocity
#         self.travel_velocity = travel_velocity
        super(Gun, self).__init__(*args, **kwargs)
#         self.sample_lower_extent = sample_lower_extent
#         self.sample_upper_extent = sample_upper_extent
#         self.overspray = overspray
#         self.high_position.put(self.zero_position.value - \
#                                self.sample_upper_extent - \
#                                self.mask_width.value / self.overspray)
#         self.low_position.put(self.zero_position.value - \
#                               self.sample_lower_extent - \
#                               self.mask_width.value / self.overspray)
#         
#         self.travel_velocity.put(travel_velocity)
#         self.coat_velocity.put(coat_velocity)
#         self.mask_width.put(mask_width)
#         self.zero_position.put(zero_position)
        self.set_travellimits(mask_width, zero_position, \
                              sample_lower_extent, sample_upper_extent, \
                              coat_velocity, travel_velocity, \
                              overspray)
        
        logger.debug("dir(self %s" % dir(self))
        
    def coat_layers(self, motor, number_of_layers):
        logger.info("gun number %d, Motor %s" % (self.instance_number, motor))
        for l in number_of_layers:
            yield from bps.mv(motor.velocity, self.coat_velocity)
            yield from bps.mv(motor, self.high_position.value)
            yield from bps.sleep(.1)
            yield from bps.mv(motor, self.low_position.value)

    def home(self, motor, speed=0):
        if speed == 0:
            speed = self.travel_velocity
        logger.info("gun %d, motor, motor: %s, speed" % \
                    (self.instance_number, motor, speed))
        yield from bps.mv(motor.velocity, speed)
        yield from motor.mv(self.zero_position.value)

    def goToLowPosition(self, motor, speed=0):
        if speed == 0:
            speed = self.travel_velocity
        logger.info("gun %d, motor, motor: %s, speed" % \
                    (self.instance_number, motor, speed))
        yield from bps.mv(motor.velocity, speed)
        yield from motor.mv(self.low_position.value)

    def goToHighPosition(self, motor, speed=0):
        if speed == 0:
            speed = self.travel_velocityinstance_number
        logger.info("gun %d, motor, motor: %s, speed" % \
                    (self.instance_number, motor, speed))
        yield from bps.mv(motor.velocity, speed)
        yield from motor.mv(self.high_position.value)
        
    def set_travellimits(self, \
                         mask_width=40.0, zero_position=1000.0, \
                         sample_lower_extent=100.0, sample_upper_extent=250, \
                         coat_velocity=10.0, travel_velocity=15.0, \
                         overspray=45.0):
        self.sample_lower_extent = sample_lower_extent
        self.sample_upper_extent = sample_upper_extent
        self.overspray = overspray
        self.high_position.put(self.zero_position.value - \
                               self.sample_upper_extent - \
                               self.mask_width.value / self.overspray)
        self.low_position.put(self.zero_position.value - \
                              self.sample_lower_extent - \
                              self.mask_width.value / self.overspray)
        self.travel_velocity.put(travel_velocity)
        self.coat_velocity.put(coat_velocity)
        self.mask_width.put(mask_width)
        self.zero_position.put(zero_position)
        
        
    def enable(self):
        # logger.info("gun number %d" % d)
        yield from bps.abs_set(self.relay_magnetron, True)     

    def disable(self):
        # logger.info("gun number %d" % d)
        yield from bps.abs_set(self.relay_magnetron, False)     


class GunSelector(DepositionListDevice):
    DISABLE_TEXT = 0
    ENABLE_TEXT = 1
    PS_LOW_LEVEL_TEXT = 'ps_low_level'
    GUN_DISABLE_VAL = 0
    current_active_gun = FC(EpicsSignal, "{self.prefix}:userCalcOut10.A",
                            name="current_active_gun",
                            put_complete=True)
    power_on = FC(EpicsSignal, "{self.prefix}:plc:MPS1_Magnetron_Power_RB",
                     write_pv="{self.prefix}:plc:MPS1_Mag_Pwr_On_OUT",
                     name="mps1_power_on",
                     string=True,
                     put_complete=True)
    mps1_enable_output = FC(EpicsSignal, "{self.prefix}:ION:1:set_enable.PROC",
                        name="mps1_enable_output",
                        # string=True,backfill
                        put_complete=True)
    mps1_disable_output = FC(EpicsSignal, "{self.prefix}:ION:1:set_disable.PROC",
                         name="mps1_disable_output",
                         # string=True,
                         put_complete=True)
    ps1_voltage = FC(EpicsSignal, "{self.prefix}:userCalc8",
                     write_pv="{self.prefix}:userCalc5.A",
                     name="ps1_ps_voltage",
                     string=True,
                     put_complete=True)
    ps1_current = FC(EpicsSignal, "{self.prefix}:userCalc10",
                     write_pv="{self.prefix}:userCalc7.A",
                     name="ps1_ps_current",
                     string=True,
                     put_complete=True)
    ps1_power = FC(EpicsSignal, "{self.prefix}:userCalc9",
                   write_pv="{self.prefix}:userCalc6.A",
                   name="ps1_ps_power",
                   string=True,
                   put_complete=True)
    mps1_voltage = FC(EpicsSignal, "{self.prefix}:ION:1:target_voltage_sp_rd",
                     write_pv="{self.prefix}:ION:1:voltage",
                     name="mps1_ps_voltage",
                     string=True,
                     put_complete=True)
    mps1_current = FC(EpicsSignal, "{self.prefix}:ION:1:target_current_sp_rd",
                     write_pv="{self.prefix}:ION:1:current",
                     name="mps1_ps_current",
                     string=True,
                     put_complete=True)
    mps1_power = FC(EpicsSignal, "{self.prefix}:ION:1:target_power_sp_rd",
                   write_pv="{self.prefix}:ION:1:power",
                   name="mps1_ps_power",
                   string=True,
                   put_complete=True)
    mps1_voltage_rbv = FC(EpicsSignal, "{self.prefix}:ION:1:volts_rd",
                     name="mps1_ps_voltage_rbv",
                     string=True,
                     put_complete=True)
    mps1_current_rbv = FC(EpicsSignal, "{self.prefix}:ION:1:amps_rd",
                     name="mps1_ps_current_rbv",
                     string=True,
                     put_complete=True)
    mps1_power_rbv = FC(EpicsSignal, "{self.prefix}:ION:1:watts_rd",
                   name="mps1_ps_power_rbv",
                   string=True,
                   put_complete=True)
    guns = DDC(_gun_fields('', 'gun', range(1, 9)))
#     this does not work because guns is not fully defined here.  need to do __init__
#     logger.debug("guns %s" % guns)

    def __init__(self, *args, **kwargs):
        logger.error("__init__ for GunSelector")
        prefix = args[0]
        self.number_of_guns = NUMBER_OF_GUNS
        super(GunSelector, self).__init__(*args, **kwargs)
        
        
    def _enable_gun(self, gun_number, ps_low_level=5.0):
        '''
        Method to enable a specified gun.  This method is meant to be used
        combined with the set method instead of being used by a script itself.
        Note it uses object set methods more directly.  This returns status 
        instead of returning an iterable as needed by other methods used         :param purge: logical to determine if this se

        directly in scripts.
        :param gun_number: Specifies the gun number to be enabled 
        :param ps_low_level: ensures that no gun magnetrons are changed
        until the power supply is below this level
        :rtype: DeviceStatus
        '''
        done_status = DeviceStatus(self)
        # Before enabling the relay
        self.mps1_enable_output.set(self.ENABLE_TEXT)
        self.mps1_enable_output.set(self.DISABLE_TEXT)
        current_active_gun = int(self.current_active_gun.get())
#        gun_to_enable = self.guns.__getattr__("gun%d" % gun_number)
        gun_to_enable = self.guns.__getattribute__("gun%d" % gun_number)
        if current_active_gun != 0:
#             gun_current = self.guns.__getattr__("gun%d" % current_active_gun)
            gun_current = self.guns.__getattribute__("gun%d" % current_active_gun)
        logger.info("Enabling gun %d, current_active_gun %d" % \
              (gun_number, current_active_gun))
 
        def verify_ps1_voltage_cb(value, timestamp, **kwargs):
            value = float(value)
            logger.info("Waiting to reach low volt limit %f voltage %f " % \
                        (ps_low_level, value))
            if float(value) < float(ps_low_level):
                print("ps1 has been disabled")
                # Once the power supply goes below ps_low_level enable it
                if current_active_gun != 0:
                     
                    if gun_number != current_active_gun:
                        logger.info("Disabling gun %d which is already active" % \
                                    current_active_gun)
                        gun_current.relay_magnetron.set(self.DISABLE_TEXT)
                        self.current_active_gun.set(0)
                        logger.info("Enabling gun %d which was requested" % \
                                    gun_number)
                        gun_to_enable.relay_magnetron.set(self.ENABLE_TEXT)
                        self.current_active_gun.set(gun_number)
                    else:
                        logger.info("Enabling gun %d which is the current_active gun" % 
                                    gun_number)
                        gun_state = gun_to_enable.relay_magnetron.get()
                        if gun_state == self.ENABLE_TEXT:
                            logger.info("Gun is already enabled")
                        else:
                            logger.info("Gun %d is disabled need to enable it" % 
                                        gun_number)
                            gun_to_enable.relay_magnetron.set(self.ENABLE_TEXT)    
                        self.current_active_gun.set(gun_number)
                else:
                    gun_to_enable.relay_magnetron.set(self.ENABLE_TEXT)
                    self.current_active_gun.set(gun_number)
                     
                self.ps1_voltage.clear_sub(verify_ps1_voltage_cb)
                done_status._finished()
 
        # go into the waiting loop.
        self.ps1_voltage.subscribe(verify_ps1_voltage_cb)
        return done_status

    def _disable_all_guns(self, ps_low_level=5):
        '''
        Method to disable all of the guns.  This method is meant to be used
        combined with the set method instead of being used by a script itself.
        Note it uses object set methods more directly.  This returns status 
        instead of returning an iterable as needed by other methods used 
        directly in scripts.
        :param ps_low_level: ensures that no gun magnetrons are changed
        until the power supply is below this level
        return DeviceStatus
        '''
        logger.info("Disabling all guns")
        done_status = DeviceStatus(self)
 
        current_active_gun = self.current_active_gun.get()
        self.mps1_disable_output.set(self.ENABLE_TEXT)
        self.mps1_disable_output.set(self.DISABLE_TEXT)

        def verify_ps1_voltage_cb(value, timestamp, **kwargs):
            logger.debug("Waiting to reach low volt limit %f voltage %f " % \
                        (ps_low_level, float(value)))
            if float(value) < float(ps_low_level):
                logger.info("ps1 has been disabled")
                # Once the power supply goes below ps_low_level disable it
                for gun_index in range(1, 9):
                    gun_to_disable = self.guns.__getattribute__("gun%d" % gun_index)
                    gun_to_disable.relay_magnetron.set(self.DISABLE_TEXT)
                self.current_active_gun.set(0.0)
                logger.info("All guns are disabled")
                self.ps1_voltage.clear_sub(verify_ps1_voltage_cb)
                done_status._finished()
 
        self.ps1_voltage.subscribe(verify_ps1_voltage_cb)
        return done_status
            
    def mps1_enable(self):
        logger.debug("enable_power_supply")
        yield from bps.mv(self.mps1_enable_output, self.ENABLE_TEXT)
        yield from bps.mv(self.mps1_enable_output, self.DISABLE_TEXT)
    
        
    def mps1_power_on(self):
        logger.debug("mps1_power_on")
        yield from bps.mv(self.power_on, self.ENABLE_TEXT)
        
    def mps1_power_off(self):
        logger.debug("enable_power_on")
        yield from bps.mv(self.power_on, self.DISABLE_TEXT)
        
    def set(self, gun, **kwargs):
        ''' 
        Sets the active gun.  Before switching guns, need to ensure that the 
        no guns are receiving power above a threshold value.  The threshold 
        value may be set by including the keyword argument 'ps_low_level'.  
        If this is missing thentype filter text a value of 5V is used.  
        Gun number should be between 0 and 8.  If 0 is selected, then all 
        guns are disabled including the current active gun and the current
        active gun is set to 0.  
        Note that any attempt to switch guns will first ensure that the 
        output of the power supply has ramped below the threshold.  The 
        disable output signal is triggered to force the power supply to start
        ramping to zero.  No changes are made to the gun relay magnetrons are
        made until the voltage is below the threshold.  Also note, that after 
        the switching of guns, the gun voltage remains disabled.  The user code
        must enable the power supply output before using the gun.
        :param gun: gun number to activate.  Should be 1-8 for an actual gun or 
        0 to disable all guns
        :param ps_low_level
        
        '''
        logging.info ("Setting gun %d" % gun)
        if gun > 8 or gun < 0:
            raise(RuntimeError("Invalid gun selected gun number must be"
                               " between 0 & 8."))
        ps_low_level = 5.0
        # Check if the user has changed the ps_low_level which controls 
        # when relays can be switched.
        if self.PS_LOW_LEVEL_TEXT in kwargs:
            ps_low_level = kwargs[self.PS_LOW_LEVEL_TEXT]
        print (ps_low_level)
        if gun == 0:
            return self. _disable_all_guns()
        else:
            return self._enable_gun(gun, ps_low_level=ps_low_level)
    
