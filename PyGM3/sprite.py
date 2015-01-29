__author__ = 'Salvakiya'
import pyglet
from pyglet.gl import *


def texture_set_mag_filter_nearest(texture):
    # Temporary fix for blurry image
    glBindTexture(texture.target, texture.id)
    glTexParameteri(texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glBindTexture(texture.target, 0)


class _SpriteManager:
    sprite_image = []


def aadd(filename, xorg=0, yorg=0, batch=None):
    image = pyglet.resource.image(filename)
    _SpriteManager.graphics.append(pyglet.sprite.Sprite(image, xorg=xorg, yorg=yorg, batch=batch))


def add(file_name, img_number=0, img_rows=1, img_columns=-1, xorg=0, yorg=0, batch=None):
    final_image = None
    image = pyglet.resource.image(file_name)
    image.anchor_x = xorg
    image.anchor_y = yorg

    _SpriteManager.sprite_image.append(image)
    texture_set_mag_filter_nearest(image.get_texture())

    if img_number > 0:
        if img_columns is -1:
            final_image = pyglet.image.ImageGrid(image, 1, img_number).get_animation(.1, True)
        else:
            final_image = pyglet.image.ImageGrid(image, img_rows, img_columns).get_animation(.1, True)

    final_image.anchor_x = xorg
    final_image.anchor_y = yorg
    final_image = pyglet.sprite.Sprite(img=final_image, batch=batch)
    return final_image