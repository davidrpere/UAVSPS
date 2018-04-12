#include <cstdlib>

#include <ros/ros.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/CommandTOL.h>
#include <mavros_msgs/SetMode.h>


//Nuestras clases
#include "client_waypoints_fotos.h"
#include "publisher_gps_fotos.h"

int main(int argc, char **argv)
{

    std::string localhost_5557 = "tcp://*:5557";
    publisher_gps_fotos publisher("Grillito", localhost_5557);
    //IP+puerto propios, porque elegimos dónde publicar
    std::string ip_gcs = "tcp://192.168.0.10:5558";
    client_waypoints_fotos cliente("Pepito", ip_gcs);
    //IP+puerto del GCS para el cliente, que elige dónde escuchar

    //publisher.publish(500,500,500);
    //cliente.receive();

    int rate = 10;

    ros::init(argc, argv, "uavsps_guided");
    ros::NodeHandle n;

    ros::Rate r(rate);

    return 0;

    //Todo de aquí abajo es pseudocódigo

    bool obtenidos_waypoints = false;

    while(!obtenidos_waypoints)
    {
        /*
         * publisher.publish()
         *
         * if(cliente.waypoints_listos){
         *  std::vector<...> = cliente.getwaypoints
         *
         *  obtenidos_waypoints = true
         *  }
         *  else
         *  {
         *  sleep
         *  continue
         *  }
         * */
    }

    //cargo waypoints
    //armo sistema
    //activo modo guided
    //despego
    //while(1){
    // publisher.publishgps
    // if(waypoint_reached){
    //
    //  take_photo()
    //  publisher.publish_photo()
    //  if(next waypoint){}else return to home
    // }else{
    //   usleep 100 ms
    //  }
    //
    // }

    //Me suscribo a GPS y según o los obtengo llamo a publisher.publish en bucle
    //Espero a obtener mis waypoints mientras sigo publicando

    ////////////////////////////////////////////
    /////////////////GUIDED/////////////////////
    ////////////////////////////////////////////
    ros::ServiceClient cl = n.serviceClient<mavros_msgs::SetMode>("/mavros/set_mode");
    mavros_msgs::SetMode srv_setMode;
    srv_setMode.request.base_mode = 0;
    srv_setMode.request.custom_mode = "GUIDED";
    if(cl.call(srv_setMode)){
        ROS_ERROR("setmode send ok %d value:", srv_setMode.response.mode_sent);
    }else{
        ROS_ERROR("Failed SetMode");
        return -1;
    }

    ////////////////////////////////////////////
    ///////////////////ARM//////////////////////
    ////////////////////////////////////////////
    ros::ServiceClient arming_cl = n.serviceClient<mavros_msgs::CommandBool>("/mavros/cmd/arming");
    mavros_msgs::CommandBool srv;
    srv.request.value = true;
    if(arming_cl.call(srv)){
        ROS_ERROR("ARM send ok %d", srv.response.success);
    }else{
        ROS_ERROR("Failed arming or disarming");
    }

    /*
    ////////////////////////////////////////////
    /////////////////TAKEOFF////////////////////
    ////////////////////////////////////////////
    ros::ServiceClient takeoff_cl = n.serviceClient<mavros_msgs::CommandTOL>("/mavros/cmd/takeoff");
    mavros_msgs::CommandTOL srv_takeoff;
    srv_takeoff.request.altitude = 10;
    srv_takeoff.request.latitude = 0;
    srv_takeoff.request.longitude = 0;
    srv_takeoff.request.min_pitch = 0;
    srv_takeoff.request.yaw = 0;
    if(takeoff_cl.call(srv_takeoff)){
        ROS_ERROR("srv_takeoff send ok %d", srv_takeoff.response.success);
    }else{
        ROS_ERROR("Failed Takeoff");
    }
    */

    ////////////////////////////////////////////
    /////////////////DO STUFF///////////////////
    ////////////////////////////////////////////
    sleep(10);

    ////////////////////////////////////////////
    ///////////////////LAND/////////////////////
    ////////////////////////////////////////////
    ros::ServiceClient land_cl = n.serviceClient<mavros_msgs::CommandTOL>("/mavros/cmd/land");
    mavros_msgs::CommandTOL srv_land;
    srv_land.request.altitude = 10;
    srv_land.request.latitude = 0;
    srv_land.request.longitude = 0;
    srv_land.request.min_pitch = 0;
    srv_land.request.yaw = 0;
    if(land_cl.call(srv_land)){
        ROS_INFO("srv_land send ok %d", srv_land.response.success);
    }else{
        ROS_ERROR("Failed Land");
    }

    while (n.ok())
    {
        ros::spinOnce();
        r.sleep();
    }

    return 0;
}
