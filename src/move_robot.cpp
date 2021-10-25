#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <iostream> 
#include <moveit_msgs/msg/display_robot_state.hpp>
#include <moveit_msgs/msg/display_trajectory.hpp>

#include <moveit_msgs/msg/attached_collision_object.hpp>
#include <moveit_msgs/msg/collision_object.hpp>

#include "rclcpp/rclcpp.hpp"

void moveRobot(moveit::planning_interface::MoveGroupInterface *move_group, int select, float value);
static const rclcpp::Logger LOGGER = rclcpp::get_logger("move_group");
const double jump_threshold = 0.0;
const double eef_step = 0.01;
std::vector<geometry_msgs::msg::Pose> waypoints;
geometry_msgs::msg::Pose pose;

void moveRobot(moveit::planning_interface::MoveGroupInterface *move_group, int select, float value) {
  std::cout << "Planning" << std::endl;  
  switch (select) {
      case 1: 
        pose.position.x = value; 
        break; 
      case 2: 
        pose.position.y = value; 
        break; 
      case 3: 
        pose.orientation.x = value; 
        break; 
      case 4: 
        waypoints.push_back(pose); 
        break; 
      case 5: 
        moveit_msgs::msg::RobotTrajectory trajectory;
        double fraction = move_group->computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
        move_group->execute(trajectory);
        std::cout << "Executing" << std::endl;
        waypoints.clear();  
        break; 
  }
}
int main(int argc, char** argv) {
    std::cout << "init" << std::endl;  
    rclcpp::init(argc, argv);
    rclcpp::NodeOptions node_options;
    node_options.automatically_declare_parameters_from_overrides(true);
    auto move_group_node = rclcpp::Node::make_shared("move_group_interface", node_options);
    std::cout << "init 2" << std::endl; 
  // We spin up a SingleThreadedExecutor for the current state monitor to get information
  // about the robot's state.
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(move_group_node);
  std::thread([&executor]() { executor.spin(); }).detach();
  std::cout << "init 3" << std::endl; 
  static const std::string PLANNING_GROUP = "ur_manipulator";
  std::cout << "1" << std::endl; 
moveit::planning_interface::MoveGroupInterface move_group(move_group_node, PLANNING_GROUP); 
std::cout << "2" << std::endl; 
moveit::planning_interface::PlanningSceneInterface planning_scene_interface;
  // The :planning_interface:`MoveGroupInterface` class can be easily
  // setup using just the name of the planning group you would like to control and plan for.
  std::cout << "init 4" << std::endl; 
  // Raw pointers are frequently used to refer to the planning group for improved performance.
  const moveit::core::JointModelGroup* joint_model_group =
      move_group.getCurrentState()->getJointModelGroup(PLANNING_GROUP);
  move_group.clearPathConstraints();
  std::cout << "init 5" << std::endl; 
  moveit::core::RobotState start_state(*move_group.getCurrentState());
  move_group.setStartState(start_state);
  move_group.setPlanningTime(10.0); 
  std::cout << "init 5" << std::endl;
  moveRobot(&move_group, 1,1); 
  moveRobot(&move_group, 4,0); 
  moveRobot(&move_group, 5,0); 
  rclcpp::shutdown(); 
  return 0; 
}
