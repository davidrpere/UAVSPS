
"use strict";

let HilActuatorControls = require('./HilActuatorControls.js');
let Waypoint = require('./Waypoint.js');
let GlobalPositionTarget = require('./GlobalPositionTarget.js');
let OverrideRCIn = require('./OverrideRCIn.js');
let HilControls = require('./HilControls.js');
let RadioStatus = require('./RadioStatus.js');
let Mavlink = require('./Mavlink.js');
let ActuatorControl = require('./ActuatorControl.js');
let Altitude = require('./Altitude.js');
let OpticalFlowRad = require('./OpticalFlowRad.js');
let VFR_HUD = require('./VFR_HUD.js');
let ParamValue = require('./ParamValue.js');
let Vibration = require('./Vibration.js');
let CommandCode = require('./CommandCode.js');
let AttitudeTarget = require('./AttitudeTarget.js');
let BatteryStatus = require('./BatteryStatus.js');
let RCIn = require('./RCIn.js');
let HilStateQuaternion = require('./HilStateQuaternion.js');
let ADSBVehicle = require('./ADSBVehicle.js');
let ManualControl = require('./ManualControl.js');
let RCOut = require('./RCOut.js');
let HilSensor = require('./HilSensor.js');
let PositionTarget = require('./PositionTarget.js');
let Thrust = require('./Thrust.js');
let CamIMUStamp = require('./CamIMUStamp.js');
let HomePosition = require('./HomePosition.js');
let WaypointList = require('./WaypointList.js');
let HilGPS = require('./HilGPS.js');
let State = require('./State.js');
let ExtendedState = require('./ExtendedState.js');
let FileEntry = require('./FileEntry.js');

module.exports = {
  HilActuatorControls: HilActuatorControls,
  Waypoint: Waypoint,
  GlobalPositionTarget: GlobalPositionTarget,
  OverrideRCIn: OverrideRCIn,
  HilControls: HilControls,
  RadioStatus: RadioStatus,
  Mavlink: Mavlink,
  ActuatorControl: ActuatorControl,
  Altitude: Altitude,
  OpticalFlowRad: OpticalFlowRad,
  VFR_HUD: VFR_HUD,
  ParamValue: ParamValue,
  Vibration: Vibration,
  CommandCode: CommandCode,
  AttitudeTarget: AttitudeTarget,
  BatteryStatus: BatteryStatus,
  RCIn: RCIn,
  HilStateQuaternion: HilStateQuaternion,
  ADSBVehicle: ADSBVehicle,
  ManualControl: ManualControl,
  RCOut: RCOut,
  HilSensor: HilSensor,
  PositionTarget: PositionTarget,
  Thrust: Thrust,
  CamIMUStamp: CamIMUStamp,
  HomePosition: HomePosition,
  WaypointList: WaypointList,
  HilGPS: HilGPS,
  State: State,
  ExtendedState: ExtendedState,
  FileEntry: FileEntry,
};
