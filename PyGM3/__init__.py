__author__ = "Salvakiya"
import pyglet
import core


class Resource:
    sprite_image = []
    sprite_count = 0
    pyglet.resource.path.append("../resources")
    pyglet.resource.reindex()

    def __init__(self):
        pass


def sprite_add(file_name, img_number=0, img_rows=1, img_columns=-1, x_orig=0, y_orig=0):
    final_image = None
    image = pyglet.resource.image(file_name)
    image.anchor_x = x_orig
    image.anchor_y = y_orig
    Resource.sprite_image.append(image)

    if img_number > 1:
        if img_columns is -1:
            final_image = pyglet.image.ImageGrid(image, 1, img_number).get_animation(.1, True)
        else:
            final_image = pyglet.image.ImageGrid(image, img_rows, img_columns).get_animation(.1, True)

    return final_image