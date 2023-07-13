#!/usr/bin/env python
# coding:utf-8

import rclpy
from rclpy.node import Node

from akari_msgs.msg import M5
from akari_msgs.srv import (SetAllout, SetDisplayColor,
                               SetDout, SetPwmout,
                               SetDisplayImage, SetDisplayText)

from akari_client import AkariClient
from akari_client.color import Color, Colors
from akari_client.position import Positions
import random
import time
import os
import sys


color_pair_text = ['BLACK','NAVY','DARKGREEN','DARKCYAN','MAROON','PURPLE','OLIVE',
                'LIGHTGREY','DARKGREY','BLUE','GREEN','CYAN','RED','MAGENTA',
                'YELLOW','WHITE','ORANGE','GREENYELLOW','PINK']

text_pair = ['1.AKARI', '2.あかり', '3.灯り', '4.アカリ', '5.Akari', '6.akari', '7.灯']
text_size = [3, 4, 5]

class m5client(Node):

    def __init__(self):
        super().__init__('m5client_text_node')
        # create client
        self.cli = self.create_client(SetDisplayText, 'set_display_text')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

        # create request
        self.req = SetDisplayText.Request()

        self.random_color = Color(
                red=random.randint(0, 255),
                green=random.randint(0, 255),
                blue=random.randint(0, 255),
            )


        self.akari = AkariClient()
        self.m5 = self.akari.m5stack
        self.data = self.m5.get()

    def send_request(self):
        #color_num = int(input())
        self.req.text = random.choice(text_pair)
        self.req.pos_x = 0
        self.req.pos_y = 0
        self.req.size = random.choice(text_size)
        self.req.text_color = random.choice(color_pair_text)
        self.req.back_color = random.choice(color_pair_text)
        self.req.refresh = False
        self.get_logger().info('Change color : %s' % (self.req))

        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main():
    rclpy.init()
    # create client
    client = m5client()
    # send request
    response = client.send_request()
    client.get_logger().info('Result: : %s' %(str(response.result)))
    client.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
