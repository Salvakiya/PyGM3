__author__ = 'Salvakiya'
import instance


class step_controller:
    @staticmethod
    def delta_update(dt):
        run_step(dt)

    @staticmethod
    def update(dt):
        dt = .1
        run_step(dt)


def run_step(dt):
    # broke a rule and we access protected member
    for value in instance._InstanceController.entity.values():
        value.event_step_core(delta_time=dt)


# Define a class inherit from an exception type
class CustomError(Exception):
    def __init__(self, arg):
        # Set some exception infomation
        self.msg = arg

