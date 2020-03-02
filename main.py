#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2020/2/27 13:04:31


import cocos
import pyglet
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

from const import const
from gui import TableLayer


cocos.director.director.init(width = 600, height = 800, caption = const.GAME_CAPTION + const.VERSION, resizable = False)
Game = TableLayer()
main_scene = cocos.scene.Scene(Game)
cocos.director.director.run(main_scene)
