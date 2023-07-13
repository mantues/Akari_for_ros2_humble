cmake_minimum_required(VERSION 3.8)
project(akari_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

find_package(ament_cmake_python REQUIRED)

# ADD dependencies
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rclpy REQUIRED)
find_package(rosidl_default_generators REQUIRED)
#find_package(py_m5serial REQUIRED)
set(srv_files
  "srv/SetAllout.srv"
  "srv/SetDisplayColor.srv"
  "srv/SetDisplayImage.srv"
  "srv/SetDisplayText.srv"
  "srv/SetDout.srv"
  "srv/SetPwmout.srv"
  "srv/Trigger.srv"
)
set(msg_files
  "msg/M5.msg"
)
set(action_files
  "action/MoveJoint.action"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${srv_files}
  ${msg_files}
  ${action_files}
  DEPENDENCIES builtin_interfaces std_msgs geometry_msgs
)
install(TARGETS
  DESTINATION lib/${PROJECT_NAME}/
)

  
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()
ament_export_dependencies(rosidl_default_runtime)
ament_package()
