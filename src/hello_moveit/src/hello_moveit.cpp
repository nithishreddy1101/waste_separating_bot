#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>

int main(int argc, char * argv[])
{
  // Initialize ROS and create the Node
  rclcpp::init(argc, argv);
    auto const node = std::make_shared<rclcpp::Node>(
        "hello_moveit",
        rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true)
    );

    // Create a ROS logger
    auto const logger = rclcpp::get_logger("hello_moveit");

     // ---- READ XYZ FROM ARGUMENTS ----
   if (argc < 4) {
      RCLCPP_ERROR(logger, "Usage: ros2 run pkg node X Y Z");
      return 1;
   }

   double x = std::stod(argv[1]);
   double y = std::stod(argv[2]);
   double z = std::stod(argv[3]);

    // Create the MoveIt MoveGroup Interface
    using moveit::planning_interface::MoveGroupInterface;
    auto move_group_interface = MoveGroupInterface(node, "manipulator");

    move_group_interface.setPoseReferenceFrame("base_link");

    // Set a target Pose
    auto const target_pose = [x, y, z]{
    geometry_msgs::msg::Pose msg;
    msg.orientation.y = 1.0;
    msg.position.x = x;
    msg.position.y = y;
    msg.position.z = z;

    return msg;
    }();

    move_group_interface.setPoseTarget(target_pose);

    // Create a plan to that target pose
    auto const [success, plan] = [&move_group_interface]{
    moveit::planning_interface::MoveGroupInterface::Plan msg;
    auto const ok = static_cast<bool>(move_group_interface.plan(msg));
    return std::make_pair(ok, msg);
    }();

// Execute the plan
if(success) {
  move_group_interface.execute(plan);
} else {
  RCLCPP_ERROR(logger, "Planning failed!");
}

  // Shutdown ROS
  rclcpp::shutdown();
  return 0;
}