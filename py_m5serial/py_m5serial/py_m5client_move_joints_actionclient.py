#!/usr/bin/env python
# coding:utf-8

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from akari_msgs.msg import M5
from akari_msgs.srv import (SetAllout, SetDisplayColor,
                               SetDout, SetPwmout,
                               SetDisplayImage, SetDisplayText,
                               Trigger)
from akari_msgs.action import (MoveJoint)

from akari_client import AkariClient
from akari_client.color import Color, Colors
from akari_client.position import Positions
import random
import time
import os
import sys

class m5client(Node):

    def __init__(self):
        super().__init__('m5client_move_joints_action_client_node')
        # create action client
        self._action_client = ActionClient(self, MoveJoint, 'move_joints')

    def send_goal(self):
        goal_msg = MoveJoint.Goal()
        goal_pan = random.uniform(-1.0, 1.0)
        goal_tilt = random.uniform(-0.5, 0.5)
        acc_pan = 0.2
        acc_tilt = 0.2
        vel_pan = 0.2
        vel_tilt = 0.2
        goal_msg.goal_pan = goal_pan
        goal_msg.goal_tilt = goal_tilt
        goal_msg.acc_pan = acc_pan
        goal_msg.acc_tilt = acc_tilt
        goal_msg.vel_pan = vel_pan
        goal_msg.vel_tilt = vel_tilt
        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

        return self._action_client.send_goal_async(goal_msg)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.result))
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.pos_pan))
        self.get_logger().info('Received feedback: {0}'.format(feedback.pos_tilt))


def main():
    rclpy.init()
    # create client
    action_client = m5client()
    # send request
    future = action_client.send_goal()
    rclpy.spin_until_future_complete(action_client, future)


if __name__ == '__main__':
    main()
