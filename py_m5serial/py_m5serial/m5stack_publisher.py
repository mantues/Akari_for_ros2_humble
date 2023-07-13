#!/usr/bin/env python
# coding:utf-8

import rclpy
from py_tutorial_interfaces.srv import AddThreeInts
from rclpy.node import Node

from akari_msgs.msg import M5
from akari_msgs.srv import (SetAllout, SetDisplayColor,
                               SetDout, SetPwmout,
                               SetDisplayImage, SetDisplayText)

from example_interfaces.srv import SetBool, Trigger
from akari_client import AkariClient
from akari_client.color import Color, Colors
from akari_client.position import Positions
import random
import time
import os
import sysfile:///home/kaz/ros2_ws/src/Akari_for_ros2_humble/py_m5serial/setup.py



class M5Publisher(Node):

    def __init__(self):
        super().__init__('M5Publisher')
        self.publisher_ = self.create_publisher(M5, '/M5stack', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.akari = AkariClient()
        self.m5 = self.akari.m5stack
        self.data = self.m5.get()

    def timer_callback(self):
        msg = M5()
        self.data = self.m5.get()
        msg.button_a = self.data["button_a"]
        msg.button_b = self.data["button_b"]
        msg.button_c = self.data["button_c"]
        msg.din0 = self.data["din0"]
        msg.din1 = self.data["din1"]
        msg.ain0 = self.data["ain0"]
        msg.dout0 = self.data["dout0"]
        msg.dout1 = self.data["dout1"]
        msg.temperature = self.data["temperature"]
        msg.brightness = self.data["brightness"]
        msg.pressure = self.data["pressure"]
        msg.general0 = self.data["general0"]
        msg.general1 = self.data["general1"]
        self.publisher_.publish(msg)
        if self.data["button_a"]:
            self.get_logger().info('Button A pressed!')


def main(args=None):
    rclpy.init(args=args)
    m5simple_publisher = M5Publisher()
    rclpy.spin(m5simple_publisher)
    m5simple_publisher.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
