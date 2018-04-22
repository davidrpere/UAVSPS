
"use strict";

let FileTruncate = require('./FileTruncate.js')
let FileOpen = require('./FileOpen.js')
let FileRead = require('./FileRead.js')
let ParamSet = require('./ParamSet.js')
let WaypointPush = require('./WaypointPush.js')
let StreamRate = require('./StreamRate.js')
let CommandLong = require('./CommandLong.js')
let CommandHome = require('./CommandHome.js')
let FileMakeDir = require('./FileMakeDir.js')
let CommandTriggerControl = require('./CommandTriggerControl.js')
let SetMode = require('./SetMode.js')
let FileRemove = require('./FileRemove.js')
let FileRename = require('./FileRename.js')
let FileChecksum = require('./FileChecksum.js')
let FileRemoveDir = require('./FileRemoveDir.js')
let CommandBool = require('./CommandBool.js')
let FileClose = require('./FileClose.js')
let WaypointPull = require('./WaypointPull.js')
let WaypointClear = require('./WaypointClear.js')
let ParamPush = require('./ParamPush.js')
let CommandInt = require('./CommandInt.js')
let ParamPull = require('./ParamPull.js')
let FileList = require('./FileList.js')
let ParamGet = require('./ParamGet.js')
let CommandTOL = require('./CommandTOL.js')
let WaypointSetCurrent = require('./WaypointSetCurrent.js')
let FileWrite = require('./FileWrite.js')

module.exports = {
  FileTruncate: FileTruncate,
  FileOpen: FileOpen,
  FileRead: FileRead,
  ParamSet: ParamSet,
  WaypointPush: WaypointPush,
  StreamRate: StreamRate,
  CommandLong: CommandLong,
  CommandHome: CommandHome,
  FileMakeDir: FileMakeDir,
  CommandTriggerControl: CommandTriggerControl,
  SetMode: SetMode,
  FileRemove: FileRemove,
  FileRename: FileRename,
  FileChecksum: FileChecksum,
  FileRemoveDir: FileRemoveDir,
  CommandBool: CommandBool,
  FileClose: FileClose,
  WaypointPull: WaypointPull,
  WaypointClear: WaypointClear,
  ParamPush: ParamPush,
  CommandInt: CommandInt,
  ParamPull: ParamPull,
  FileList: FileList,
  ParamGet: ParamGet,
  CommandTOL: CommandTOL,
  WaypointSetCurrent: WaypointSetCurrent,
  FileWrite: FileWrite,
};
