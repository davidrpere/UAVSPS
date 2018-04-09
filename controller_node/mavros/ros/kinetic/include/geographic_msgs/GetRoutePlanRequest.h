// Generated by gencpp from file geographic_msgs/GetRoutePlanRequest.msg
// DO NOT EDIT!


#ifndef GEOGRAPHIC_MSGS_MESSAGE_GETROUTEPLANREQUEST_H
#define GEOGRAPHIC_MSGS_MESSAGE_GETROUTEPLANREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <uuid_msgs/UniqueID.h>
#include <uuid_msgs/UniqueID.h>
#include <uuid_msgs/UniqueID.h>

namespace geographic_msgs
{
template <class ContainerAllocator>
struct GetRoutePlanRequest_
{
  typedef GetRoutePlanRequest_<ContainerAllocator> Type;

  GetRoutePlanRequest_()
    : network()
    , start()
    , goal()  {
    }
  GetRoutePlanRequest_(const ContainerAllocator& _alloc)
    : network(_alloc)
    , start(_alloc)
    , goal(_alloc)  {
  (void)_alloc;
    }



   typedef  ::uuid_msgs::UniqueID_<ContainerAllocator>  _network_type;
  _network_type network;

   typedef  ::uuid_msgs::UniqueID_<ContainerAllocator>  _start_type;
  _start_type start;

   typedef  ::uuid_msgs::UniqueID_<ContainerAllocator>  _goal_type;
  _goal_type goal;




  typedef boost::shared_ptr< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> const> ConstPtr;

}; // struct GetRoutePlanRequest_

typedef ::geographic_msgs::GetRoutePlanRequest_<std::allocator<void> > GetRoutePlanRequest;

typedef boost::shared_ptr< ::geographic_msgs::GetRoutePlanRequest > GetRoutePlanRequestPtr;
typedef boost::shared_ptr< ::geographic_msgs::GetRoutePlanRequest const> GetRoutePlanRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> >::stream(s, "", v);
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
struct IsFixedSize< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "e56ac34268c6d575dabb30f42da4a47a";
  }

  static const char* value(const ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xe56ac34268c6d575ULL;
  static const uint64_t static_value2 = 0xdabb30f42da4a47aULL;
};

template<class ContainerAllocator>
struct DataType< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "geographic_msgs/GetRoutePlanRequest";
  }

  static const char* value(const ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "\n\
\n\
\n\
\n\
uuid_msgs/UniqueID network\n\
uuid_msgs/UniqueID start\n\
uuid_msgs/UniqueID goal\n\
\n\
\n\
================================================================================\n\
MSG: uuid_msgs/UniqueID\n\
# A universally unique identifier (UUID).\n\
#\n\
#  http://en.wikipedia.org/wiki/Universally_unique_identifier\n\
#  http://tools.ietf.org/html/rfc4122.html\n\
\n\
uint8[16] uuid\n\
";
  }

  static const char* value(const ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.network);
      stream.next(m.start);
      stream.next(m.goal);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GetRoutePlanRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::geographic_msgs::GetRoutePlanRequest_<ContainerAllocator>& v)
  {
    s << indent << "network: ";
    s << std::endl;
    Printer< ::uuid_msgs::UniqueID_<ContainerAllocator> >::stream(s, indent + "  ", v.network);
    s << indent << "start: ";
    s << std::endl;
    Printer< ::uuid_msgs::UniqueID_<ContainerAllocator> >::stream(s, indent + "  ", v.start);
    s << indent << "goal: ";
    s << std::endl;
    Printer< ::uuid_msgs::UniqueID_<ContainerAllocator> >::stream(s, indent + "  ", v.goal);
  }
};

} // namespace message_operations
} // namespace ros

#endif // GEOGRAPHIC_MSGS_MESSAGE_GETROUTEPLANREQUEST_H
