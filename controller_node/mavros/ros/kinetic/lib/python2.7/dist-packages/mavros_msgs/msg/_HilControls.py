# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from mavros_msgs/HilControls.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import std_msgs.msg

class HilControls(genpy.Message):
  _md5sum = "698148349c3a2e5720afcae2d934acca"
  _type = "mavros_msgs/HilControls"
  _has_header = True #flag to mark the presence of a Header object
  _full_text = """# HilControls.msg
#
# ROS representation of MAVLink HIL_CONTROLS
# (deprecated, use HIL_ACTUATOR_CONTROLS instead)
# See mavlink message documentation here:
# https://pixhawk.ethz.ch/mavlink/#HIL_CONTROLS

std_msgs/Header header
float32 roll_ailerons
float32 pitch_elevator
float32 yaw_rudder
float32 throttle
float32 aux1
float32 aux2
float32 aux3
float32 aux4
uint8 mode
uint8 nav_mode

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id
"""
  __slots__ = ['header','roll_ailerons','pitch_elevator','yaw_rudder','throttle','aux1','aux2','aux3','aux4','mode','nav_mode']
  _slot_types = ['std_msgs/Header','float32','float32','float32','float32','float32','float32','float32','float32','uint8','uint8']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       header,roll_ailerons,pitch_elevator,yaw_rudder,throttle,aux1,aux2,aux3,aux4,mode,nav_mode

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(HilControls, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.header is None:
        self.header = std_msgs.msg.Header()
      if self.roll_ailerons is None:
        self.roll_ailerons = 0.
      if self.pitch_elevator is None:
        self.pitch_elevator = 0.
      if self.yaw_rudder is None:
        self.yaw_rudder = 0.
      if self.throttle is None:
        self.throttle = 0.
      if self.aux1 is None:
        self.aux1 = 0.
      if self.aux2 is None:
        self.aux2 = 0.
      if self.aux3 is None:
        self.aux3 = 0.
      if self.aux4 is None:
        self.aux4 = 0.
      if self.mode is None:
        self.mode = 0
      if self.nav_mode is None:
        self.nav_mode = 0
    else:
      self.header = std_msgs.msg.Header()
      self.roll_ailerons = 0.
      self.pitch_elevator = 0.
      self.yaw_rudder = 0.
      self.throttle = 0.
      self.aux1 = 0.
      self.aux2 = 0.
      self.aux3 = 0.
      self.aux4 = 0.
      self.mode = 0
      self.nav_mode = 0

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_3I().pack(_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs))
      _x = self.header.frame_id
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_8f2B().pack(_x.roll_ailerons, _x.pitch_elevator, _x.yaw_rudder, _x.throttle, _x.aux1, _x.aux2, _x.aux3, _x.aux4, _x.mode, _x.nav_mode))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      if self.header is None:
        self.header = std_msgs.msg.Header()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs,) = _get_struct_3I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.header.frame_id = str[start:end].decode('utf-8')
      else:
        self.header.frame_id = str[start:end]
      _x = self
      start = end
      end += 34
      (_x.roll_ailerons, _x.pitch_elevator, _x.yaw_rudder, _x.throttle, _x.aux1, _x.aux2, _x.aux3, _x.aux4, _x.mode, _x.nav_mode,) = _get_struct_8f2B().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_3I().pack(_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs))
      _x = self.header.frame_id
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_8f2B().pack(_x.roll_ailerons, _x.pitch_elevator, _x.yaw_rudder, _x.throttle, _x.aux1, _x.aux2, _x.aux3, _x.aux4, _x.mode, _x.nav_mode))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      if self.header is None:
        self.header = std_msgs.msg.Header()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs,) = _get_struct_3I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.header.frame_id = str[start:end].decode('utf-8')
      else:
        self.header.frame_id = str[start:end]
      _x = self
      start = end
      end += 34
      (_x.roll_ailerons, _x.pitch_elevator, _x.yaw_rudder, _x.throttle, _x.aux1, _x.aux2, _x.aux3, _x.aux4, _x.mode, _x.nav_mode,) = _get_struct_8f2B().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_3I = None
def _get_struct_3I():
    global _struct_3I
    if _struct_3I is None:
        _struct_3I = struct.Struct("<3I")
    return _struct_3I
_struct_8f2B = None
def _get_struct_8f2B():
    global _struct_8f2B
    if _struct_8f2B is None:
        _struct_8f2B = struct.Struct("<8f2B")
    return _struct_8f2B
