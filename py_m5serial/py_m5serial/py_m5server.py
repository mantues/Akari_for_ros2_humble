import rclpy
from py_tutorial_interfaces.srv import AddThreeInts
from rclpy.node import Node
from rclpy.action import ActionServer

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
from std_msgs.msg import Int32MultiArray

color_pair = ['BLACK','NAVY','DARKGREEN','DARKCYAN','MAROON','PURPLE','OLIVE',
                'LIGHTGREY','DARKGREY','BLUE','GREEN','CYAN','RED','MAGENTA',
                'YELLOW','WHITE','ORANGE','GREENYELLOW','PINK','RESET', 'RANDOM', 'SELECT']

text_pair = ['1.AKARI', '2.あかり', '3.灯り', '4.アカリ', '5.Akari', '6.akari', '7.灯']

# server
class m5server(Node):
    def __init__(self):
        super().__init__("m5_service")

        # create service OUT
        self._set_dout_srv = self.create_service(SetDout, 'set_dout_m5', self.set_dout_m5)
        self._set_pwmout_srv = self.create_service(SetPwmout, 'set_pwmout_m5', self.set_pwmout_m5)
        self._set_allout_srv = self.create_service(SetAllout, 'set_allout_m5', self.set_allout_m5)
        self._reset_allout_srv = self.create_service(Trigger, 'reset_allout_m5', self.reset_allout_m5)
        # create service DISPLAY
        self._set_display_color_srv = self.create_service(SetDisplayColor, 'set_display_color', self.set_display_color)
        self._set_display_text_srv = self.create_service(SetDisplayText, 'set_display_text', self.set_display_text)
        self._set_display_image_srv = self.create_service(SetDisplayImage, 'set_display_image', self.set_display_image)
        self._reset_m5_srv = self.create_service(Trigger, 'reset_m5', self.reset_m5)
        # create action service JOINTS
        self._move_joint_action_srv = ActionServer(self, MoveJoint, 'move_joints', self.move_joints)

        self.random_color = Color(
                red=random.randint(0, 255),
                green=random.randint(0, 255),
                blue=random.randint(0, 255),
            )

        # SETTING AKARI
        self.akari = AkariClient()
        self.joints = self.akari.joints
        self.m5 = self.akari.m5stack
        self.data = self.m5.get()

    # DISPLAY CALL BACK
    # callback
    def set_display_color(self, request, response):
        req_color = request.color
        self.get_logger().info('Change color : %s' % (str(req_color)))
        # set_display_color
        if req_color in color_pair:
            if req_color == 'RANDOM':
                self.m5.set_display_color(self.random_color)
                time.sleep(0.5)
                self.m5.set_display_text(text='RANDOM',
                    pos_x=Positions.CENTER, pos_y=Positions.CENTER, size=5,
                    text_color=Colors.WHITE, back_color=Colors.DARKGREY, refresh=False)
            elif req_color == 'RESET':
                self.m5.reset_m5()
            elif req_color == 'SELECT':
                r_color = request.color_var[0]
                g_color = request.color_var[1]
                b_color = request.color_var[2]
                color = Color(red=r_color, green=g_color, blue=b_color)
                self.m5.set_display_color(color)
                time.sleep(0.5)
                self.m5.set_display_text(text='SELECT',
                    pos_x=Positions.CENTER, pos_y=Positions.CENTER, size=5,
                    text_color=Colors.WHITE, back_color=Colors.DARKGREY, refresh=False)
            else:
                self.m5.set_display_color(Colors[req_color])
                time.sleep(0.5)
                self.m5.set_display_text(text=req_color,
                    pos_x=Positions.CENTER, pos_y=Positions.CENTER, size=5,
                    text_color=Colors.WHITE, back_color=Colors.DARKGREY, refresh=False)
            response.result = True
        else:
            self.m5.reset_m5()
            response.result = False
        return response

    # callback
    def set_display_text(self, request, response):
        req_text = request.text
        req_pos_x = request.pos_x
        req_pos_y = request.pos_y
        req_size = request.size
        req_text_color = request.text_color
        req_back_color = request.back_color
        req_refresh = request.refresh
        self.get_logger().info('Change text : %s Size: %s' % (str(req_text), str(req_size)))
        # set_display_text
        if req_text_color in color_pair:
            self.m5.set_display_text(
                text=req_text, pos_x=req_pos_x, pos_y=req_pos_y, size=req_size, text_color=Colors[req_text_color], back_color=Colors[req_back_color], refresh=req_refresh
            )
            response.result = True
        else:
            self.m5.reset_m5()
            response.result = False
        return response

    # callback
    def set_display_image(self, request, response):
        # display image on m5 screen
        filepath = request.filepath
        pos_x = request.pos_x
        pos_y = request.pos_y
        scale = request.scale
        self.m5.set_display_image(filepath, pos_x, pos_y, scale)
        response.result = True

        return response

    # callback
    def reset_m5(self, request, response):
        # reset m5 screen
        if request.trigger == "RESET":
            self.m5.reset_m5()
            self.get_logger().info('RESET M5 Stack')
            response.result = True
        else:
            self.get_logger().info('M5 Stack')
            response.result = False
        return response

    # OUT CALL BACK
    # callback
    def set_dout_m5(self, request, response):
        req_id = request.pin_id
        req_val = request.val
        # set m5 dout
        if -1 < req_id and req_id < 2:
            self.m5.set_dout(req_id, req_val)
            self.get_logger().info('PIN_ID: %s Valut: %s' % (str(req_id), str(req_val)))
            response.result = True
        else:
            self.get_logger().info('PIN_ID is NOT Corect (0-2 is OK): %s' % (str(req_id)))
            response.result = False
        return response

    # callback
    def set_pwmout_m5(self, request, response):
        req_id = request.pin_id
        req_val = request.val
        # set m5 dout
        if req_id == 0 and -1 < req_val < 256:
            self.m5.set_pwmout(req_id, req_val)
            self.get_logger().info('PIN_ID: %s Valut: %s' % (str(req_id), str(req_val)))
            response.result = True
        else:
            self.get_logger().info('PIN_ID: %s or Value: %s is NOT Corect (ID:0-2, Value:0-255)' % (str(req_id), str(req_val)))
            response.result = False
        return response

    # callback
    def set_allout_m5(self, request, response):
        req_dout0 = request.dout0_val
        req_dout1 = request.dout1_val
        req_pwmout0_val = request.pwmout0_val
        # set m5 dout
        if -1 < req_pwmout0_val < 256:
            self.m5.set_allout(dout0 = req_dout0, dout1 = req_dout1, pwmout0 = req_pwmout0_val)
            self.get_logger().info('Dout0: %s Dout1: %s PWM: %s' % (str(req_dout0), str(req_dout1), str(req_pwmout0_val)))
            response.result = True
        else:
            self.get_logger().info('PWM Value: %s is NOT Corect (0-255)' % (str(req_pwmout0_val)))
            response.result = False
        return response

    # callback
    def reset_allout_m5(self, request, response):
        # reset m5 allout
        if request.trigger == "RESETALLOUT":
            self.m5.reset_allout()
            self.get_logger().info('RESETALLOUT M5 Stack')
            response.result = True
        else:
            self.get_logger().info('M5 Stack')
            response.result = False
        return response

    # ACTION CALL BACK
    # callback
    def move_joints(self, action_msg):
        # enable servo
        self.joints.enable_all_servo()
        # feedback
        feedback = MoveJoint.Feedback()
        feedback.pos_pan = self.joints.get_joint_positions()['pan']
        feedback.pos_tilt = self.joints.get_joint_positions()['tilt']
        action_msg.publish_feedback(feedback)

        acc_pan = action_msg.request.acc_pan
        acc_tilt = action_msg.request.acc_tilt
        vel_pan = action_msg.request.vel_pan
        vel_tilt = action_msg.request.vel_tilt
        goal_pan = action_msg.request.goal_pan
        goal_tilt = action_msg.request.goal_tilt
        self.joints.move_joint_positions(pan=goal_pan,tilt=goal_tilt)
        self.get_logger().info('ACTION server pan: %s tilt: %s' % (str(goal_tilt), str(goal_pan)))
        action_msg.succeed()
        result = MoveJoint.Result()

        return result

def main(args=None):
    rclpy.init(args=args)

    # create service
    server = m5server()

    rclpy.spin(server)

    rclpy.shutdown()

if __name__ == "__main__":
    main()
