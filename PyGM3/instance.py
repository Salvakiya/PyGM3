__author__ = 'Salvakiya'
import weakref
from itertools import count


# this class keeps all of the variables of the instances
class _InstanceController:
    # dictionaries of all entities
    entity = {}
    entity_count = count()

    # list of all deactivated entities
    deactivated = []

    # dictionary of lists which contain entities of the type
    type_lists = {}

    def __init__(self):
        pass


# Game Maker Object is Entity
class Entity(object):
    def __init__(self, entity_id=-1, type_index=-1, x=0, y=0, **kwargs):
        self.entity_id = entity_id
        self.type_index = type_index
        self.x = x
        self.y = y
        self.sprite = None
        self.visible = True
        self._active = True
        self._destroyed = False
        self.alarm = {}

        self.event_create(**kwargs)
        self._cleanup_create()

    def _cleanup_create(self):
        pass


    def event_create(self, **kwargs):
        pass
        

    def event_destroy(self):
        # not complete
        self._active = False
        self._destroyed = True
        print(str(self.entity_id) + " was killed!")

    def event_draw(self):
        if self.sprite is not None and self.visible is True:
            #self.sprite.draw()
            self.sprite.x = self.x
            self.sprite.y = self.y
    
    def event_step(self):
        pass

    def event_step_core(self, delta_time=.1):
        # if we are not active do not preform
        if self._active is False:
            return

        # if we have alarms to iterate through
        # alarm usage is self.alarm[method_name] = steps_until_execution
        if self.alarm > 0:
            # create a list of alarms which we are finished with
            alarms_to_remove = []

            # iterate through the alarms
            for method_alarm in self.alarm:
                # tick down the alarm.
                self.alarm[method_alarm] -= 1 * (delta_time * 10)

                # if its time execute method
                if self.alarm[method_alarm] < 0:
                    perform = getattr(self, method_alarm)
                    perform()

                # if we did not reset the alarm when performing
                # prepare to remove the alarm
                if self.alarm[method_alarm] < 0:
                    alarms_to_remove.append(method_alarm)

            # remove the list of alarms
            for method_alarm in alarms_to_remove:
                self.alarm.pop(method_alarm)
        self.event_step()


def _create_type_list(entity_type):
    if entity_type.__name__ not in _InstanceController.type_lists:
        # create the list
        _InstanceController.type_lists[entity_type.__name__] = []

        # iterate through all objects to add to the list
        for entity in _InstanceController.entity.values():
            if entity.__class__.__name__ == entity_type.__name__:
                entity.type_index = len(_InstanceController.type_lists[entity_type.__name__])
                _InstanceController.type_lists[entity_type.__name__].append(entity.entity_id)
        return True
    else:
        return False


def destroy(destroy_id):
    if not isinstance(destroy_id, (int, long)):
        # print("warning! an instance is calling instance.destroy with a real reference to an entity")
        destroy_id = destroy_id.entity_id

    instance_to_destroy = _InstanceController.entity[destroy_id]
    instance_to_destroy.event_destroy()
    instance_name = instance_to_destroy.__class__.__name__
    if instance_name in _InstanceController.type_lists:
        # if this is the last instance of this type
        if len(_InstanceController.type_lists[instance_name]) <= 1:
            _InstanceController.type_lists.pop(instance_name)
        else:
            _InstanceController.type_lists[instance_name].pop(instance_to_destroy.type_index)

    _InstanceController.entity.pop(destroy_id)
    return None


def create(entity_type, x=0, y=0, **kwargs):
    assign_id = next(_InstanceController.entity_count)
    assign_type_id = -1

    if entity_type.__name__ in _InstanceController.type_lists:
        _InstanceController.type_lists[entity_type.__name__].append(assign_id)

        assign_type_id = len(_InstanceController.type_lists[entity_type.__name__])

    _InstanceController.entity[assign_id] = entity_type(x=x, y=y,
                                                        entity_id=assign_id,
                                                        type_index=assign_type_id,
                                                        **kwargs)

    return weakref.proxy(_InstanceController.entity[assign_id])

def number(entity_type):
    if entity_type.__name__ not in _InstanceController.type_lists:
        _create_type_list(entity_type)
    if entity_type.__name__ in _InstanceController.type_lists:
        return len(_InstanceController.type_lists[entity_type.__name__])

def identity(obj):
    if isinstance(obj, (int, long)):
        return weakref.proxy(_InstanceController.entity[obj])
    else:
        return obj


def exists(obj):
    for instance in _InstanceController.entity:
        if instance.entity_id == obj.entity_id:
            return True
        elif instance.__class__.__name__ == obj.__class__.__name__:
            return True

    # return False if nothing was found
    return False


def nearest(x, y, entity_type):
    if entity_type.__name__ not in _InstanceController.type_lists:
        _create_type_list(entity_type)

    tracking_distance = -1
    entity_id = -1
    # for value in InstanceController.type_lists[entity_type.__name__]:
     #    instance
