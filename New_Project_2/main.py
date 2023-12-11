
import os

os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.animation import Animation
from dpeaDPi.DPiStepper import *
from time import sleep

from dpeaDPi.DPiComputer import *

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from pidev.Joystick import Joystick


from datetime import datetime

joy = Joystick(0, False)

dpiStepper = DPiStepper()
stepper_num = 0
steps = 1600
microstepping = 8
wait_to_finish_moving_flg = True
stepperStatus = dpiStepper.getStepperStatus(0)
time = datetime

dpiComputer = DPiComputer()


MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
BONUS_SCREEN_NAME = 'bonus'

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White



class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    stepper_num = 0
    gear_ratio = 1
    motorStepPerRevolution = 1600 * gear_ratio
    dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)
    speed_in_revolutions_per_sec = 1.0
    accel_in_revolutions_per_sec_per_sec = 2.0
    dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
    dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)

    directionToMoveTowardHome = 1  # 1 Positive Direction -1 Negative Direction
    homeSpeedInStepsPerSecond = speed_in_revolutions_per_sec / 2
    homeMaxDistanceToMoveInRevolutions = 3200

    dpiStepper.setMicrostepping(microstepping)
    speed_steps_per_second = 200 * microstepping
    accel_steps_per_second_per_second = speed_steps_per_second
    dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)
    dpiStepper.setSpeedInStepsPerSecond(1, speed_steps_per_second)
    dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)
    dpiStepper.setAccelerationInStepsPerSecondPerSecond(1, accel_steps_per_second_per_second)
    dpiStepper.setBoardNumber(0)

    dpiComputer.initialize()



    count = 0
    joystick_enabled = False
    direction_clockwise = True
    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("huzzah! it printed")
    def pressed2(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        self.count += 1
        self.ids.btn_2.text = str(self.count)


    def joystick(self, dt):

        print(joy.get_axis('x'), joy.get_axis('y'))
        print(joy.get_button_state(0))

        if joy.get_button_state(0) == True:
            self.ids.proj_label.text = "motor on"

        else:
            self.ids.proj_label.text = "motor off"


    @staticmethod
    def transition_forth():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.transition.direction = 'right'
        SCREEN_MANAGER.current = ADMIN_SCREEN_NAME

    @staticmethod
    def transition_forth2():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.transition.direction = 'right'
        SCREEN_MANAGER.current = BONUS_SCREEN_NAME

    def pressed3(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """

        if self.ids.proj_label.text == "motor on":

            self.ids.proj_label.text = "motor off"

            self.joystick_enabled = False

        elif self.ids.proj_label.text == "motor off":

            self.ids.proj_label.text = "motor on"

            anim = Animation(x=20, y=50, size=(80, 80), t='in_quad')
            anim += Animation(x=50, y=20, size=(200, 200), t='in_quad')
            anim += Animation(x=50, y=50, size=(20, 20), t='in_quad')
            anim.repeat = True
            anim.start(self.ids.img_btn)

            self.joystick_enabled = True

            Clock.schedule_interval(self.joystick, 0.1)
    def pressed4(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """


        if dpiStepper.initialize() == False:
             print("Communication with the DPiStepper board failed.")
        elif dpiStepper.initialize() == True:
             print("Communication with the DPiStepper board success")

        dpiStepper.enableMotors(True)

        print("Motor On")

        wait_to_finish_moving_flg = True
        dpiStepper.moveToRelativePositionInSteps(stepper_num, steps, wait_to_finish_moving_flg)

        if self.direction_clockwise == True:
            dpiStepper.moveToRelativePositionInSteps(stepper_num, steps, wait_to_finish_moving_flg)
        elif self.direction_clockwise == False:
             dpiStepper.moveToRelativePositionInSteps(stepper_num, -steps, wait_to_finish_moving_flg)

        print(f"Pos = {stepperStatus}")

    def pressed5(self):
            """
            Function called on button touch event for button with id: testButton
            :return: None
            """
            self.direction_clockwise = not self.direction_clockwise
            print(f"Direction = {self.direction_clockwise}")

    def pressed6 (self):
            """
            Function called on button touch event for button with id: testButton
            :return: None
            """
            dpiStepper.enableMotors(True)

            currentPosition = dpiStepper.getCurrentPositionInSteps(0)[1]
            print(f"Pos = {currentPosition}")

            dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)
            waitToFinishFlg = True
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 15, waitToFinishFlg)
            sleep(10)

            print(f"Pos = {currentPosition}")

            sleep(10)

            dpiStepper.speed_in_revolutions_per_sec = 5.0

            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 10, waitToFinishFlg)

            print(f"Pos = {currentPosition}")

            sleep(8)

            dpiStepper.moveToHomeInSteps(stepper_num, self.directionToMoveTowardHome, self.homeSpeedInRevolutionsPerSecond, self.homeMaxDistanceToMoveInRevolutions)

            print(f"Pos = {currentPosition}")

            dpiStepper.speed_in_revolutions_per_sec = 8.0

            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, -100, waitToFinishFlg)

            sleep(10)

            dpiStepper.moveToHomeInSteps(stepper_num, self.directionToMoveTowardHome, self.homeSpeedInRevolutionsPerSecond, self.homeMaxDistanceToMoveInRevolutions)

            print(f"Pos = {currentPosition}")
    def switch(self):



    def sliding(self):

            dpiStepper.setMicrostepping(microstepping)
            speed_steps_per_second = self.ids.proj_slider.value * microstepping
            accel_steps_per_second_per_second = speed_steps_per_second
            dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)
            dpiStepper.setSpeedInStepsPerSecond(1, speed_steps_per_second)
            dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)
            dpiStepper.setAccelerationInStepsPerSecondPerSecond(1, accel_steps_per_second_per_second)
    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.transition.direction = 'up'
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME


    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()
class BonusScreen(Screen):
    def __init__(self, **kwargs):

        Builder.load_file('BonusScreen.kv')

        super(BonusScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.transition.direction = 'up'
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME
"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(BonusScreen(name=BONUS_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
