__author__ = '\u03b5'
from functools import partial
from itertools import count
import weakref


class GM(object):
    def __init__(self):
        super(GM, self).__init__()
        self.ids = count()
        self.entities = {}

    def create(self, entity_fac, x=0, y=0, **kwargs):
        n = next(self.ids)
        entity = entity_fac(gm=self, e_id=n, x=x, y=y, **kwargs)
        self.entities[n] = entity
        return entity


class EntityAttribute(object):
    def __init__(self, attr_name):
        super(EntityAttribute, self).__init__()
        self.attr_name = attr_name
        self.weaks = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        try:
            return self.weaks[instance]()
        except KeyError:
            raise AttributeError(self.attr_name)

    def __set__(self, instance, value):
        self.weaks[instance] = weakref.ref(
            value, partial(self.deleted, weakref.ref(instance)))

    def deleted(self, instance_r, ref):
        inst = instance_r()
        if inst is not None:
            inst.communicating_entity_destroyed(self.attr_name)


class GameObject(object):
    def __init__(self, gm, e_id, x, y):
        self.gm = gm
        self.e_id = e_id
        self.x = x
        self.y = y

    def __repr__(self):
        return '<{0} #{1} at x={2} y={3}>'.format(
            type(self).__name__, self.e_id, self.x, self.y)

    def communicating_entity_destroyed(self, attr_name):
        print("Oh noes, we are venting through {0}!".format(attr_name))

    def destroy(self):
        del self.gm.entities[self.e_id]


class Bridge(GameObject):
    left_door = EntityAttribute('left_door')


class EscapePodsRoom(GameObject):
    right_door = EntityAttribute('right_door')


def main():
    game = GM()
    bridge = game.create(Bridge, 0, 0)
    pods = game.create(EscapePodsRoom, -1, 0)
    bridge.left_door = pods
    pods.right_door = bridge
    print(bridge.left_door)
    pods.destroy()
    del pods
    print(bridge.left_door)

main()