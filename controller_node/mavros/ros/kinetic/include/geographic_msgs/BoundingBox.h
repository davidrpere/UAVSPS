// Generated by gencpp from file geographic_msgs/BoundingBox.msg
// DO NOT EDIT!


#ifndef GEOGRAPHIC_MSGS_MESSAGE_BOUNDINGBOX_H
#define GEOGRAPHIC_MSGS_MESSAGE_BOUNDINGBOX_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <geographic_msgs/GeoPoint.h>
#include <geographic_msgs/GeoPoint.h>

namespace geographic_msgs
{
template <class ContainerAllocator>
struct BoundingBox_
{
  typedef BoundingBox_<ContainerAllocator> Type;

  BoundingBox_()
    : min_pt()
    , max_pt()  {
    }
  BoundingBox_(const ContainerAllocator& _alloc)
    : min_pt(_alloc)
    , max_pt(_alloc)  {
  (void)_alloc;
    }



   typedef  ::geographic_msgs::GeoPoint_<ContainerAllocator>  _min_pt_type;
  _min_pt_type min_pt;

   typedef  ::geographic_msgs::GeoPoint_<ContainerAllocator>  _max_pt_type;
  _max_pt_type max_pt;




  typedef boost::shared_ptr< ::geographic_msgs::BoundingBox_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::geographic_msgs::BoundingBox_<ContainerAllocator> const> ConstPtr;

}; // struct BoundingBox_

typedef ::geographic_msgs::BoundingBox_<std::allocator<void> > BoundingBox;

typedef boost::shared_ptr< ::geographic_msgs::BoundingBox > BoundingBoxPtr;
typedef boost::shared_ptr< ::geographic_msgs::BoundingBox const> BoundingBoxConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::geographic_msgs::BoundingBox_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::geographic_msgs::BoundingBox_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace geographic_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'geographic_msgs': ['/tmp/binarydeb/ros-kinetic-geographic-msgs-0.5.2/msg'], 'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg'], 'uuid_msgs': ['/opt/ros/kinetic/share/uuid_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::geographic_msgs::BoundingBox_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::geographic_msgs::BoundingBox_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::geographic_msgs::BoundingBox_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::geographic_msgs::BoundingBox_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::geographic_msgs::BoundingBox_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::geographic_msgs::BoundingBox_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::geographic_msgs::BoundingBox_<ContainerAllocator> >
{
  static const char* value()
  {
    return "f62e8b5e390a3ac7603250d46e8f8446";
  }

  static const char* value(const ::geographic_msgs::BoundingBox_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xf62e8b5e390a3ac7ULL;
  static const uint64_t static_value2 = 0x603250d46e8f8446ULL;
};

template<class ContainerAllocator>
struct DataType< ::geographic_msgs::BoundingBox_<ContainerAllocator> >
{
  static const char* value()
  {
    return "geographic_msgs/BoundingBox";
  }

  static const char* value(const ::geographic_msgs::BoundingBox_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::geographic_msgs::BoundingBox_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# Geographic map bounding box. \n\
#\n\
# The two GeoPoints denote diagonally opposite corners of the box.\n\
#\n\
# If min_pt.latitude is NaN, the bounding box is \"global\", matching\n\
# any valid latitude, longitude and altitude.\n\
#\n\
# If min_pt.altitude is NaN, the bounding box is two-dimensional and\n\
# matches any altitude within the specified latitude and longitude\n\
# range.\n\
\n\
GeoPoint min_pt         # lowest and most Southwestern corner\n\
GeoPoint max_pt         # highest and most Northeastern corner\n\
\n\
================================================================================\n\
MSG: geographic_msgs/GeoPoint\n\
# Geographic point, using the WGS 84 reference ellipsoid.\n\
\n\
# Latitude [degrees]. Positive is north of equator; negative is south\n\
# (-90 <= latitude <= +90).\n\
float64 latitude\n\
\n\
# Longitude [degrees]. Positive is east of prime meridian; negative is\n\
# west (-180 <= longitude <= +180). At the poles, latitude is -90 or\n\
# +90, and longitude is irrelevant, but must be in range.\n\
float64 longitude\n\
\n\
# Altitude [m]. Positive is above the WGS 84 ellipsoid (NaN if unspecified).\n\
float64 altitude\n\
";
  }

  static const char* value(const ::geographic_msgs::BoundingBox_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::geographic_msgs::BoundingBox_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.min_pt);
      stream.next(m.max_pt);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct BoundingBox_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::geographic_msgs::BoundingBox_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::geographic_msgs::BoundingBox_<ContainerAllocator>& v)
  {
    s << indent << "min_pt: ";
    s << std::endl;
    Printer< ::geographic_msgs::GeoPoint_<ContainerAllocator> >::stream(s, indent + "  ", v.min_pt);
    s << indent << "max_pt: ";
    s << std::endl;
    Printer< ::geographic_msgs::GeoPoint_<ContainerAllocator> >::stream(s, indent + "  ", v.max_pt);
  }
};

} // namespace message_operations
} // namespace ros

#endif // GEOGRAPHIC_MSGS_MESSAGE_BOUNDINGBOX_H
