#include <memory>

#include <chrono>

#include <cstdlib>

#include "tm_msgs/srv/send_script.hpp"

#include "rclcpp/rclcpp.hpp"

#include "tm_msgs/msg/sct_response.hpp"



using std::placeholders::_1;

using namespace std::chrono_literals;

int count=0;





bool send_cmd(std::string cmd, std::shared_ptr<rclcpp::Node> node, rclcpp::Client<tm_msgs::srv::SendScript>::SharedPtr client){

  auto request = std::make_shared<tm_msgs::srv::SendScript::Request>();

  request->id = "demo";

  request->script = cmd;

  while (!client->wait_for_service(1s)) {

    if (!rclcpp::ok()) {

      RCLCPP_ERROR_STREAM(rclcpp::get_logger("rclcpp"), "Interrupted while waiting for the service. Exiting.");

      return false;

    }

    RCLCPP_INFO_STREAM(rclcpp::get_logger("rclcpp"), "service not available, waiting again...");

  }





  auto result = client->async_send_request(request);

  // Wait for the result.



  if (rclcpp::spin_until_future_complete(node, result) ==

    rclcpp::FutureReturnCode::SUCCESS)

  {

    if(result.get()->ok){

      RCLCPP_INFO_STREAM(rclcpp::get_logger("rclcpp"),"OK");

    } else{

      RCLCPP_INFO_STREAM(rclcpp::get_logger("rclcpp"),"not OK");

    }

  } 

  else {

    RCLCPP_ERROR_STREAM(rclcpp::get_logger("rclcpp"), "Failed to call service");

  }

 return true;

}







class MinimalSubscriber : public rclcpp::Node

{

  public:

    MinimalSubscriber()

    : Node("demo_get_sct_response")

    {

      subscription_ = this->create_subscription<tm_msgs::msg::SctResponse>(

      "sct_response", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));     

    }

  private:   

   void topic_callback(const tm_msgs::msg::SctResponse::SharedPtr msg) const

    {

      RCLCPP_INFO_STREAM(this->get_logger(),"SctResponse: id is = " << msg->id << ", script is " << msg->script);

      std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("demo_send_script");

      rclcpp::Client<tm_msgs::srv::SendScript>::SharedPtr client =

  node->create_client<tm_msgs::srv::SendScript>("send_script");

      std::string cmd_default_position = "PTP(\"JPP\",-90,0,90,0,90,0,-93,200,0,false)"; // default

      //placeset1 -94.2,25.63,32.54,31.83,90,-4

      //place1    -94.2,17.11,77.89,-5,89.96,-4.21

      //pickset1 -46.08,-15.69,78.25,27.46,90.06,43.94

      //pick1 -45.99,-22.03,115.86,-3.82,90,43.97

      

      

      std::string cmd_placeset_position1 = "PTP(\"JPP\",-94.2,25.63,32.54,31.83,90,-4,60,200,0,false)"; 

     std::string cmd_place_position1 = "PTP(\"JPP\",-94.2,17.11,77.89,-5,89.96,-4.21,60,200,0,false)"; 

  std::string cmd_pickset_position1 = "PTP(\"JPP\",-46.08,-15.69,78.25,27.46,90.06,43.94,60,200,0,false)"; 

  std::string cmd_pick_position1 = "PTP(\"JPP\",-45.99,-22.03,115.86,-3.82,90,43.97,60,200,0,false)";

      //placeset2 -87.26,20.62,39.56,29,90,2.79

      //place2    -87.24,13,82.84,-6.57,89.96,2.75

      //pickset2 -55.84,-1.17,66.28,24.89,89.97,34.19

      //pick2 -56.22,-4.73,103.10,-8.37,89.93,33.76

  

 std::string cmd_placeset_position2 = "PTP(\"JPP\",-87.26,20.62,39.56,29,90,2.79,60,200,0,false)"; 

 std::string cmd_place_position2 = "PTP(\"JPP\",-87.24,13,82.84,-6.57,89.96,2.75,60,200,0,false)"; 

 std::string cmd_pickset_position2 = "PTP(\"JPP\",-55.84,-1.17,66.28,24.89,89.97,34.19,60,200,0,false)"; 

  std::string cmd_pick_position2 = "PTP(\"JPP\",-56.22,-4.73,103.10,-8.37,89.93,33.76,60,200,0,false)"; 

  

  //pickskuBOX1 -86.35,9.15,140.94,30.91,-05.45,-91

  //pickskuBOX2 -83,0,137.6,46,-82,-91

  //HoldSKUBox  -83,4.55,138,38,-82,-91

  //LiftSKUBox  -84,-15.7,116.6,79.8,-83,-91

  //MoveSKUBox  -84,-15.7,116.6,79.8,-171,-91

  //PlaceSKUBox  -84,9.81,136.65,42.6,-172,-99

  std::string cmd_pickSKUBOX1 = "PTP(\"JPP\",-86.35,9.15,140.94,30.91,-5,-91,60,200,0,false)";

  std::string cmd_pickSKUBOX2 = "PTP(\"JPP\",-83,0,137.6,46,-82,-91,60,200,0,false)";

  std::string cmd_HoldSKUBOX = "PTP(\"JPP\",-83,4.55,138,38,-82,-91,60,200,0,false)";

  std::string cmd_LiftSKUBOX = "PTP(\"JPP\",-84,-15.7,116.6,79.8,-83,-91,60,200,0,false)";

  std::string cmd_MoveSKUBOX = "PTP(\"JPP\",-84,-15.7,116.6,79.8,-171,-91,60,200,0,false)";

  std::string cmd_PlaceSKUBOX = "PTP(\"JPP\",-84,9.81,136.65,42.6,-172,-99,60,200,0,false)";

  

  std::string cmd = "ScriptExit()";

      if(msg->script=="Listen2"){

      RCLCPP_INFO_STREAM(rclcpp::get_logger("rclcpp"),"LISTEN2DETECTED"); //go to pickup position

      if(count==0){ //go to pick position and pick

      send_cmd(cmd_pickset_position1,node,client); 

      send_cmd(cmd_pick_position1,node,client); 

      send_cmd(cmd, node, client);

      count++;

      }

      else if(count==2){ //second item

      send_cmd(cmd_placeset_position1,node,client);  

      send_cmd(cmd_pickset_position2,node,client);  

      send_cmd(cmd_pick_position2,node,client);      

      send_cmd(cmd, node, client);

      count++;

      }

      else if(count==4){

      send_cmd(cmd_placeset_position1,node,client);  

      send_cmd(cmd_pickSKUBOX1,node,client);

      send_cmd(cmd_pickSKUBOX2,node,client);

      send_cmd(cmd_HoldSKUBOX,node,client);               

      send_cmd(cmd, node, client);

      count++;

	}

      else if(count==6){

      send_cmd(cmd_pickset_position1,node,client); 

      }

      }

      else if(msg->script=="Listen3"){

      RCLCPP_INFO_STREAM(rclcpp::get_logger("rclcpp"),"LISTEN3DETECTED"); //go to place position

      if(count==1){ //go to place position and place

      send_cmd(cmd_pickset_position1,node,client); 

      send_cmd(cmd_placeset_position1,node,client); 

      send_cmd(cmd_place_position1,node,client); 

      send_cmd(cmd, node, client);

      count++;

      }

      else if(count==3){

      send_cmd(cmd_pickset_position2,node,client);  

      send_cmd(cmd_placeset_position1,node,client);  

      send_cmd(cmd_placeset_position2,node,client);  

      send_cmd(cmd_place_position2,node,client);   

      send_cmd(cmd, node, client);

      count++;

      }

      else if(count==5){

      send_cmd(cmd_LiftSKUBOX,node,client); 

      send_cmd(cmd_MoveSKUBOX,node,client);

      send_cmd(cmd_PlaceSKUBOX,node,client);    

      send_cmd(cmd, node, client);

      count++;   

      }

      }

      else if(msg->script=="Listen1"){

      send_cmd(cmd, node, client);

      }

}

    rclcpp::Subscription<tm_msgs::msg::SctResponse>::SharedPtr subscription_;



};







int main(int argc, char * argv[])

{

  rclcpp::init(argc, argv);

  std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("demo_send_script");

  rclcpp::Client<tm_msgs::srv::SendScript>::SharedPtr client =

  node->create_client<tm_msgs::srv::SendScript>("send_script");

  //std::string cmd_default_position = "PTP(\"JPP\",-90,0,90,0,90,0,35,200,0,false)"; // default

  std::string cmd_default_position = "PTP(\"JPP\",-80,0,80,0,80,0,35,200,0,false)";

  std::string cmd_pick_position = "PTP(\"JPP\",-90,25,90,-25,90,0,35,200,0,false)"; // pick

  std::string cmd_place_position = "PTP(\"JPP\",-90,-10,132,-34,97,0,35,200,0,false)"; // place

  std::string cmd = "ScriptExit()";

  send_cmd(cmd_default_position, node, client);

  send_cmd(cmd, node, client);

 rclcpp::spin(std::make_shared<MinimalSubscriber>());

  rclcpp::shutdown();

  return 0;



}