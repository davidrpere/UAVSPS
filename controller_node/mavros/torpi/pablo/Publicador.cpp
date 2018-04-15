#include <zmq.hpp> 
#include <stdio.h> 
#include <stdlib.h> 
#include <time.h> 
#include <iostream> 
#include <fstream> 
#include <iosfwd> 
#include <raspicam/raspicam.h> 
#include<unistd.h> 
#include <ctime>
int main () {
    zmq::context_t context (1);
    zmq::socket_t publisher (context, ZMQ_PUB);
    publisher.bind("tcp://127.0.0.1:8080");
	
	raspicam::RaspiCam Camera; //Cmaera object
    //Open camera
    std::cout<<"Opening Camera..."<<std::endl;
    if ( !Camera.open()) {std::cerr<<"Error opening camera"<<std::endl;return -1;}
    //wait a while until camera stabilizes
    std::cout<<"Sleeping for 3 secs"<<std::endl;
    usleep(3000000);
    //capture std:: cout <<"hola"<< std::endl;
    Camera.grab();
    //allocate memory
    unsigned char *data=new unsigned char[ Camera.getImageTypeSize ( raspicam::RASPICAM_FORMAT_RGB )];
    std::cout << *data << std::endl;
    //extract the image in rgb format
    
    Camera.retrieve ( data,raspicam::RASPICAM_FORMAT_RGB );//get camera image
    
	
	int id=1;
	while(1){
    	int size=0;
		size=sizeof(*data)+sizeof(id)+1;
		zmq::message_t message(size);
    	snprintf((char *) message.data(), size ,"%i %s",id, data);
    	publisher.send(message);
	}
    return 0;
}
