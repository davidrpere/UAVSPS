// Generated by gencpp from file actionlib/TestRequestGoal.msg
// DO NOT EDIT!


#ifndef ACTIONLIB_MESSAGE_TESTREQUESTGOAL_H
#define ACTIONLIB_MESSAGE_TESTREQUESTGOAL_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace actionlib
{
template <class ContainerAllocator>
struct TestRequestGoal_
{
  typedef TestRequestGoal_<ContainerAllocator> Type;

  TestRequestGoal_()
    : terminate_status(0)
    , ignore_cancel(false)
    , result_text()
    , the_result(0)
    , is_simple_client(false)
    , delay_accept()
    , delay_terminate()
    , pause_status()  {
    }
  TestRequestGoal_(const ContainerAllocator& _alloc)
    : terminate_status(0)
    , ignore_cancel(false)
    , result_text(_alloc)
    , the_result(0)
    , is_simple_client(false)
    , delay_accept()
    , delay_terminate()
    , pause_status()  {
  (void)_alloc;
    }



   typedef int32_t _terminate_status_type;
  _terminate_status_type terminate_status;

   typedef uint8_t _ignore_cancel_type;
  _ignore_cancel_type ignore_cancel;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _result_text_type;
  _result_text_type result_text;

   typedef int32_t _the_result_type;
  _the_result_type the_result;

   typedef uint8_t _is_simple_client_type;
  _is_simple_client_type is_simple_client;

   typedef ros::Duration _delay_accept_type;
  _delay_accept_type delay_accept;

   typedef ros::Duration _delay_terminate_type;
  _delay_terminate_type delay_terminate;

   typedef ros::Duration _pause_status_type;
  _pause_status_type pause_status;


    enum { TERMINATE_SUCCESS = 0 };
     enum { TERMINATE_ABORTED = 1 };
     enum { TERMINATE_REJECTED = 2 };
     enum { TERMINATE_LOSE = 3 };
     enum { TERMINATE_DROP = 4 };
     enum { TERMINATE_EXCEPTION = 5 };
 

  typedef boost::shared_ptr< ::actionlib::TestRequestGoal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::actionlib::TestRequestGoal_<ContainerAllocator> const> ConstPtr;

}; // struct TestRequestGoal_

typedef ::actionlib::TestRequestGoal_<std::allocator<void> > TestRequestGoal;

typedef boost::shared_ptr< ::actionlib::TestRequestGoal > TestRequestGoalPtr;
typedef boost::shared_ptr< ::actionlib::TestRequestGoal const> TestRequestGoalConstPtr;

// constants requiring out of line definition

   

   

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::actionlib::TestRequestGoal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::actionlib::TestRequestGoal_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace actionlib

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'actionlib': ['/tmp/binarydeb/ros-kinetic-actionlib-1.11.9/obj-arm-linux-gnueabihf/devel/share/actionlib/msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::actionlib::TestRequestGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::actionlib::TestRequestGoal_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::actionlib::TestRequestGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::actionlib::TestRequestGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::actionlib::TestRequestGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::actionlib::TestRequestGoal_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::actionlib::TestRequestGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "db5d00ba98302d6c6dd3737e9a03ceea";
  }

  static const char* value(const ::actionlib::TestRequestGoal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xdb5d00ba98302d6cULL;
  static const uint64_t static_value2 = 0x6dd3737e9a03ceeaULL;
};

template<class ContainerAllocator>
struct DataType< ::actionlib::TestRequestGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "actionlib/TestRequestGoal";
  }

  static const char* value(const ::actionlib::TestRequestGoal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::actionlib::TestRequestGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n\
int32 TERMINATE_SUCCESS = 0\n\
int32 TERMINATE_ABORTED = 1\n\
int32 TERMINATE_REJECTED = 2\n\
int32 TERMINATE_LOSE = 3\n\
int32 TERMINATE_DROP = 4\n\
int32 TERMINATE_EXCEPTION = 5\n\
int32 terminate_status\n\
bool ignore_cancel  # If true, ignores requests to cancel\n\
string result_text\n\
int32 the_result    # Desired value for the_result in the Result\n\
bool is_simple_client\n\
duration delay_accept  # Delays accepting the goal by this amount of time\n\
duration delay_terminate  # Delays terminating for this amount of time\n\
duration pause_status  # Pauses the status messages for this amount of time\n\
";
  }

  static const char* value(const ::actionlib::TestRequestGoal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::actionlib::TestRequestGoal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.terminate_status);
      stream.next(m.ignore_cancel);
      stream.next(m.result_text);
      stream.next(m.the_result);
      stream.next(m.is_simple_client);
      stream.next(m.delay_accept);
      stream.next(m.delay_terminate);
      stream.next(m.pause_status);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct TestRequestGoal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::actionlib::TestRequestGoal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::actionlib::TestRequestGoal_<ContainerAllocator>& v)
  {
    s << indent << "terminate_status: ";
    Printer<int32_t>::stream(s, indent + "  ", v.terminate_status);
    s << indent << "ignore_cancel: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.ignore_cancel);
    s << indent << "result_text: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.result_text);
    s << indent << "the_result: ";
    Printer<int32_t>::stream(s, indent + "  ", v.the_result);
    s << indent << "is_simple_client: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.is_simple_client);
    s << indent << "delay_accept: ";
    Printer<ros::Duration>::stream(s, indent + "  ", v.delay_accept);
    s << indent << "delay_terminate: ";
    Printer<ros::Duration>::stream(s, indent + "  ", v.delay_terminate);
    s << indent << "pause_status: ";
    Printer<ros::Duration>::stream(s, indent + "  ", v.pause_status);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ACTIONLIB_MESSAGE_TESTREQUESTGOAL_H