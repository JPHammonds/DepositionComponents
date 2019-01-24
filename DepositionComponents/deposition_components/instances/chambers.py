'''
Created on Jan 23, 2019

@author: hammonds
'''
from deposition_components.DepositionListDevice import DepositionListDevice
from ophyd import (Component as Cpt, DynamicDeviceComponent as DDC,
                   FormattedComponent as FC)
from ophyd.ophydobj import Kind
from deposition_components.generic.ChamberCryoPump import ChamberCryoPump
from deposition_components.generic.ColdCathodeGauge import ColdCathodeGauge
from deposition_components.generic.GateValve import GateValve
from deposition_components.generic.BackFill import BackFill
from ophyd.signal import EpicsSignal

class LandingChamber(DepositionListDevice):
    '''
    Device to describe the landing chamber
    '''
    cryo_substitutions = {'power_on_read_pv_suffix': ':plc:CP1_Landing_Chamber_Cryo_Pump_RB',
                         'power_on_write_pv_suffix': ':plc:CP1_LC_Cryo_Pump_Off_OUT',
                         'exhaust_read_pv_suffix': ':plc:CP1_Exhaust_to_VP1_RB',
                         'exhaust_write_pv_suffix':':plc:CP1_Exhaust_VP1_On_OUT',
                         'pressure_read_pv_suffix': ':plc:Cryo_Pump_1_ok_IN',
                         'temp_status_read_pv_suffix': ':plc:Cryo_Pump_1_ok_IN',
                         'n2_purge_read_pv_suffix': ':plc:N2_Purge_to_CP1_RB',
                         'n2_purge_write_pv_suffix': ':plc:N2_Purge_CP1_OUT',
                         'kind': Kind.normal}
    cryo_pump = Cpt(ChamberCryoPump, '', **cryo_substitutions)
#     ccg_power_on = FC(EpicsSignal, "{self.prefix}:plc:Landing_Chamber_CCG1_RB",
#                   write_pv = "{self.prefix}:plc:LC_CCG1_Enable_OUT",
#                   name = 'ccg_power_on',
#                   put_complete=True)
#     ccg_pressure = FC(EpicsSignal,
#                       '{self.prefix}:plc:CCG_1_IN',
#                       name='ccg_pressure')
    ccg_substitutions = {'power_on_read_pv_suffix': ':plc:Landing_Chamber_CCG1_RB',
                         'power_on_write_pv_suffix': ':plc:LC_CCG1_Enable_OUT',
                         'pressure_read_pv_suffix': ':plc:CCG_1_IN',
                         'kind': Kind.normal }
    ccg = Cpt(ColdCathodeGauge, '', **ccg_substitutions)
    gate_valve_substitutions = {'position_read_pv_suffix': ':plc:GV_1_Pos_IN',
                                 'position_write_pv_suffix': ':plc:GV_1_Pos_OUT',
                                 'close_request_read_pv_suffix': ':plc:Landing_Chamber_Cryo_GV1_CLOSED_RB',
                                 'close_request_write_pv_suffix':':plc:LC_Cryo_GV1_Close_OUT',
                                 'open_request_read_pv_suffix': ':plc:Landing_Chamber_Cryo_GV1_OPEN_RB',
                                 'open_request_write_pv_suffix':':plc:LC_Cryo_GV1_Open_OUT',
                                 'fully_open_read_pv_suffix': ':plc:LC_GV1_DoorOpen_IN',
                                 'fully_closed_read_pv_suffix': ':plc:LC_GV1_DoorClosed_IN',
                                 'kind': Kind.normal}
    gate_valve = Cpt(GateValve, "", **gate_valve_substitutions)

    
class PlanarChamber(DepositionListDevice):
    '''
    Device to describe the Planar chamberpower_on_write_pv_suffix
    '''
    cryo_substitutions = {
        'power_on_read_pv_suffix': ':plc:CP2_Planar_Chamber_Cryo_Pump_RB',
        'power_on_write_pv_suffix': ':plc:CP2_PC_Cryo_Pump_Off_OUT',
        'exhaust_read_pv_suffix': ':plc:CP2_Exhaust_to_VP1_RB',
        'exhaust_write_pv_suffix':':plc:CP2_Exhaust_VP1_On_OUT',
        'pressure_read_pv_suffix': ':plc:Cryo_Pump_2_ok_IN',
        'temp_status_read_pv_suffix': ':plc:Cryo_Pump_2_ok_IN',
        'n2_purge_read_pv_suffix': ':plc:N2_Purge_to_CP2_RB',
        'n2_purge_write_pv_suffix': ':plc:N2_Purge_CP2_OUT',
        'kind': Kind.normal}

    cryo_pump = Cpt(ChamberCryoPump, '', **cryo_substitutions)
    gate_valve_substitutions = {
        'position_read_pv_suffix': ':plc:GV_2_Pos_IN',
         'position_write_pv_suffix': ':plc:GV_2_Pos_OUT',
         'close_request_read_pv_suffix': ':plc:Planar_Chamber_Cryo_GV2_CLOSED_RB',
         'close_request_write_pv_suffix':':plc:LC_Cryo_GV2_Close_OUT',
         'open_request_read_pv_suffix': ':plc:Planar_Chamber_Cryo_GV2_OPEN_RB',
         'open_request_write_pv_suffix':':plc:LC_Cryo_GV2_Open_OUT',
         'fully_open_read_pv_suffix': ':plc:RC_GV2_Open_IN',
         'fully_closed_read_pv_suffix': ':plc:RC_GV2_Closed_IN',
         'kind': Kind.normal}
    gate_valve = Cpt(GateValve, '', **gate_valve_substitutions)
#     gate_valve = DDC(gate_valve_config)

            
class RoundChamber(DepositionListDevice):
    '''
    Device to describ the Round Chamber
    '''
    cryo_substitutions = {
        'power_on_read_pv_suffix': ':plc:CP3_Round_Chamber_Cryo_Pump_RB',
        'power_on_write_pv_suffix': ':plc:CP3_RC_Cryo_Pump_Off_OUT',
        'exhaust_read_pv_suffix': ':plc:CP3_Exhaust_to_VP1_RB',
        'exhaust_write_pv_suffix':':plc:CP3_Exhaust_VP1_On_OUT',
        'pressure_read_pv_suffix': ':plc:Cryo_Pump_3_ok_IN',
        'temp_status_read_pv_suffix': ':plc:Cryo_Pump_3_ok_IN',
        'n2_purge_read_pv_suffix': ':plc:N2_Purge_to_CP3_RB',
        'n2_purge_write_pv_suffix': ':plc:N2_Purge_CP3_OUT',
        'kind': Kind.normal}
    cryo_pump = Cpt(ChamberCryoPump, '', **cryo_substitutions)
    gate_valve_substitutions = {'position_read_pv_suffix': ':plc:GV_3_Pos_IN',
        'position_write_pv_suffix': ':plc:GV_3_Pos_OUT',
        'close_request_read_pv_suffix': ':plc:Round_Chamber_Cryo_GV3_CLOSED_RB',
        'close_request_write_pv_suffix':':plc:LC_Cryo_GV3_Close_OUT',
        'open_request_read_pv_suffix': ':plc:Round_Chamber_Cryo_GV3_OPEN_RB',
                                 'open_request_write_pv_suffix':':plc:LC_Cryo_GV3_Open_OUT',
                                 'fully_open_read_pv_suffix': ':plc:PC_GV3_Open_IN',
                                 'fully_closed_read_pv_suffix': ':plc:PC_GV3_Closed_IN',
                                 'kind': Kind.normal}
    gate_valve = Cpt(GateValve, '', **gate_valve_substitutions)


class LoadlockChamber(DepositionListDevice):
    '''
    Device to describe the Load Lock chamber
    '''
    cryo_substitutions = {'power_on_read_pv_suffix': ':plc:CP4_Loadlock_Chamber_Cryo_Pump_RB',
                                 'power_on_write_pv_suffix': ':plc:CP4_LLC_Cryo_Pump_Off_OUT',
                                 'exhaust_read_pv_suffix': ':plc:CP4_Exhaust_to_VP1_RB',
                                 'exhaust_write_pv_suffix':':plc:CP4_Exhaust_VP1_On_OUT',
                                 'pressure_read_pv_suffix': ':plc:Cryo_Pump_4_ok_IN',
                                 'temp_status_read_pv_suffix': ':plc:Cryo_Pump_4_ok_IN',
                                 'n2_purge_read_pv_suffix': ':plc:N2_Purge_to_CP4_RB',
                                 'n2_purge_write_pv_suffix': ':plc:N2_Purge_CP4_OUT',
                                 'kind': Kind.normal}
    cryo_pump = Cpt(ChamberCryoPump, '', **cryo_substitutions)
#     ccg_power_on = FC(EpicsSignal, "{self.prefix}:plc:Loadlock_CCG2_RB",
#                    write_pv = "{self.prefix}:plc:LL_CCG2_Enable_OUT",
#                  name='power_on',
#                  put_complete=True)
#     ccg_pressure = FC(EpicsSignal,
#                       '{self.prefix}:plc:CCG_2_IN')
    ccg_substitutions = {'power_on_read_pv_suffix': ':plc:Loadlock_CCG2_RB',
                         'power_on_write_pv_suffix': ':plc:LL_CCG2_Enable_OUT',
                         'pressure_read_pv_suffix': ':plc:CCG_2_IN',
                         'kind' : Kind.normal}
    ccg = Cpt(ColdCathodeGauge, '', **ccg_substitutions)

    gate_valve_substitutions = {'position_read_pv_suffix': ':plc:GV_4_Pos_IN',
                                 'position_write_pv_suffix': ':plc:GV_4_Pos_OUT',
                                 'close_request_read_pv_suffix': ':plc:Loadlock_Chamber_Cryo_GV4_CLOSED_RB',
                                 'close_request_write_pv_suffix':':plc:LC_Cryo_GV4_Close_OUT',
                                 'open_request_read_pv_suffix': ':plc:Loadlock_Chamber_Cryo_GV4_OPEN_RB',
                                 'open_request_write_pv_suffix':':plc:LC_Cryo_GV4_Open_OUT',
                                 'fully_open_read_pv_suffix': ':plc:LL_GV4_Open_IN',
                                 'fully_closed_read_pv_suffix': ':plc:LL_GV4_Closed_IN',
                                 'kind': Kind.normal}
    gate_valve = Cpt(GateValve, '', **gate_valve_substitutions)
    backfill_substitutions = {
        'ar_high_rate_read_pv_suffix': ':plc:EOV3_Process_Argon_Hi_Backfill_RB',
        'ar_high_rate_write_pv_suffix': ':plc:LL_Ar_Hi_Bf_On_OUT',
        'ar_low_rate_read_pv_suffix': ':plc:Ar_Backfill_to_LL_RB',
        'ar_low_rate_write_pv_suffix': ':plc:Ar_Backfill_LL_On_OUT',
        'overpressure_read_pv_suffix': ':plc:Ar_Backfill_CC_On_OUT',
        'overpressure_write_pv_suffix': ':plc:Center_Chamber_Overpressure_RB',
        'kind': Kind.normal}
    backfill = Cpt(BackFill, '', **backfill_substitutions)
    exhaust_to_vp1 = FC(EpicsSignal, "{self.prefix}:plc:Loadlock_to_VP1_RB",
                         write_pv="{self.prefix}:plc:LL_VP1_On_OUT")
    door_seal = FC(EpicsSignal,
                   '{self.prefix}:plc:EOV4_Loadlock_Door_Seal_RB',
                   write_pv='{self.prefix}:plc:LL_Door_Seal_Open_OUT',
                   name='door_seal')
    pressure_1000t = FC(EpicsSignal,
                       '{self.prefix}:plc:PT_4_IN',
                       name='pressure_1000t')
    pressure_10t = FC(EpicsSignal, '{self.prefix}:plc:PT_4_IN',
                      name='pressure_10t')
    gv5_substitutions = {'position_read_pv_suffix': None,
                         'position_write_pv_suffix': None,
                         'close_request_read_pv_suffix': ':plc:Loadlock_Chamber_Cryo_GV5_CLOSED_RB',
                         'close_request_write_pv_suffix':':plc:LC_Cryo_GV5_Close_OUT',
                         'open_request_read_pv_suffix': ':plc:Loadlock_Chamber_Cryo_GV5_OPEN_RB',
                         'open_request_write_pv_suffix':':plc:LL_Cryo_GV5_Open_OUT',
                         'fully_open_read_pv_suffix': ':plc:LL_GV5_Open_IN',
                         'fully_closed_read_pv_suffix': ':plc:LL_GV5_Closed_IN',
                         'kind': Kind.normal}

    # gv5 = Cpt(GateValve, '', **gv5_substitutions)

    
class MainChamber(DepositionListDevice):
    '''
    Device to describe the center chamber
    '''
    landing_chamber = Cpt(LandingChamber, "")
    planar_chamber = Cpt(PlanarChamber, "")
    round_chamber = Cpt(RoundChamber, "")
    
    exhaust_to_vp1 = FC(EpicsSignal,
                        '{self.prefix}:plc:CC_Exhaust_to_VP1_RB',
                        write_pv='{self.prefix}:plc:CC_Exhaust_VP1_On_OUT',
                        name='exhaust_to_vp1')
    pt1_isolate = FC(EpicsSignal,
                     '{self.prefix}:plc:PT1_RB',
                     write_pv='{self.prefix}:plc:PT1_LC_On_OUT',
                     name='pt1_isolate')
    overpressure = FC(EpicsSignal,
                      '{self.prefix}:plc:Center_Chamber_Overpressure_RB',
                      write_pv='{self.prefix}:plc:CC_OverPress_Close_OUT',
                      name='overpressure') 
#     ar_backfill_high_rate = FC(EpicsSignal,
#                        '{self.prefix}:plc:EOV2_Loadlock_Argon_Hi_Backfill_RB',
#                        write_pv='{self.prefix}:plc:Process_Ar_Hi_Bf_On_OUT',
#                        name='ar_backfill_high_rate')
#     ar_backfill_low_rate = FC(EpicsSignal,
#                       '{self.prefix}:plc:Ar_Backfill_to_Center_RB',
#                       write_pv='{self.prefix}:plc:Ar_Backfill_CC_On_OUT',
#                       name='ar_backfill_low_rate')
    backfill_substitutions = {'ar_high_rate_read_pv_suffix': ':plc:EOV2_Loadlock_Argon_Hi_Backfill_RB',
                              'ar_high_rate_write_pv_suffix': ':plc:Process_Ar_Hi_Bf_On_OUT',
                              'ar_low_rate_read_pv_suffix': ':plc:Ar_Backfill_to_Center_RB',
                              'ar_low_rate_write_pv_suffix': ':plc:Ar_Backfill_CC_On_OUT',
                              'overpressure_read_pv_suffix': ':plc:Center_Chamber_Overpressure_RB',
                              'overpressure_write_pv_suffix': ':plc:CC_OverPress_Close_OUT',
                              'kind': Kind.normal}
    backfill = Cpt(BackFill, '', **backfill_substitutions)
    pressure_1000t = FC(EpicsSignal,
                        '{self.prefix}:plc:PT_2_IN',
                        name='pressure_1000t')    
