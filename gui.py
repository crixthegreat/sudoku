#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2020/2/27 13:06:52


'''MEMO

Now the game can use the 'cursor.png' as the mouse cursor.

This is done by modified the code of the Class Director
in the director.py in cocos. implemented on 2020/3/2

below the line of the orginal code:

    #: pyglet's window object
    self.window = window.Window(*args, **kwargs)

insert the following code:
    
    ## starts to insert code 
    ## crix's modification 2020/03/02
    ## add the mouse cursor support
    import os
    cursor_file = 'cursor.png'
    if os.path.exists(cursor_file):
        image = pyglet.image.load('cursor.png')
        cursor = pyglet.window.ImageMouseCursor(image, 0, image.height)
        self.window.set_mouse_cursor(cursor)
    ## end modification


MEMO END
'''


import cocos
import pyglet
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
from cocos import actions
from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

from const import const
from sudoku import Sudoku

class Audio(Sound):
    """The standard class for Audio
    """
    def __init__(self, file_name):
        super(Audio, self).__init__(file_name)


class Cell():
    '''Every cell in the table contains a sprite and a label
    '''
    def __init__(self, sprite, label):

        self.sprite = sprite
        self.label = label


class TableLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):

        super().__init__()

        self.game = None
        
        self.keys_pressed = set()

        self.game_status = const.GAME_STATUS_MENU
        
        self.game_mode = 3

        self.StartTimer = 0
        self.schedule(self.Timer_Refresh)
        self.TimePassed = 0

        mixer.init()
        self.title_music = Audio(const.TITLE_MUSIC_FILE)
        self.main_music = None
        self.solved_music = None

        self.title_music.play(-1)

        self.image = pyglet.resource.image(const.BG_IMAGE)

        self.Time_Label = cocos.text.Label('00:00',
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = const.COLOR_BLACK,
            x = 5, y = 780)

        self.Version_Label = cocos.text.Label(const.VERSION,
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = const.COLOR_BLACK,
            x = 550, y = 780)

        self.add(self.Time_Label)
        self.add(self.Version_Label)

        # for gif files
        #_anime = pyglet.image.load_animation(const.GAME_SELECT_BOX_IMAGE)
        #_bin = pyglet.image.atlas.TextureBin()
        #_anime.add_to_texture_bin(_bin)
        self.game_select_sprite = cocos.sprite.Sprite(const.GAME_SELECT_BOX_IMAGE,
                position = (const.GAME_SELECT_BOX_START_POS[0] + self.game_mode * int(600/len(const.GAME_MODE)), const.GAME_SELECT_BOX_START_POS[1]), 
                scale = 0.8)
        self.add(self.game_select_sprite)
        self.game_select_sprite.do(actions.Blink(20, 10))

        self.exit_button = cocos.sprite.Sprite(const.EXIT_IMAGE,
                position = (520, 781))
        self.add(self.exit_button)

        self.mouse_x = None
        self.mouse_y = None


    @property
    def selected_pos(self):
        return self._pos


    @selected_pos.setter
    def selected_pos(self, pos):

        row, column = pos
        if row<0:
            row = 0
        if row >= self.game.max_number:
            row = self.game.max_number - 1
        if column<0:
            column = 0
        if column >= self.game.max_number:
            column = self.game.max_number - 1
        
        self._pos = (row, column)
        self.last_cell_color = self.cells[row * self.game.max_number + column].sprite.color
        self.set_pos_color((row, column), const.COLOR_YELLOW)


    def Timer_Refresh(self, dt):

        if self.game_status == const.GAME_STATUS_MENU:
            if not(self.game_select_sprite.are_actions_running()):
                # blink infinitly
                self.game_select_sprite.do(actions.Blink(20, 10))
            return None
        elif self.game_status == const.GAME_STATUS_MAIN:
            self.game_select_sprite.stop()
            self.game_select_sprite.visible = True

            self.StartTimer += dt
            self.TimePassed += dt
            if self.StartTimer > 1:  # timer_interval
                self.Time_Label.element.text = str(int(self.TimePassed // 60)) + ' : ' + str(int(self.TimePassed % 60)) 
                self.StartTimer = 0


    def draw(self):

        self.image.blit(0,0)
        
    
    def on_mouse_motion(self, x, y, dx, dy):

        self.mouse_x, self.mouse_y = director.get_virtual_coordinates(x, y)

        if self.game_status == const.GAME_STATUS_MENU and  720 > self.mouse_y > 640:
            self.game_mode = int(self.mouse_x // (int(600/len(const.GAME_MODE))))
            self.game_select_sprite.position = (
                    const.GAME_SELECT_BOX_START_POS[0] + self.game_mode * int(600/len(const.GAME_MODE)), 
                        const.GAME_SELECT_BOX_START_POS[1])
            
        if self.game_status==const.GAME_STATUS_MAIN and self.mouse_y <= 600:

            row = self.game.max_number - int(self.mouse_y // (600/self.game.max_number)) - 1
            column = int(self.mouse_x // (600/self.game.max_number))
    
            if self.selected_pos != (row, column):
                last_pos = self.selected_pos
                self.set_pos_color(last_pos, self.last_cell_color)

                self.selected_pos = (row, column)
                
        if self.game_status != const.GAME_STATUS_MENU and 490<=self.mouse_x<=530 and 770<=self.mouse_y<=800:
            self.exit_button.scale = 1.2
        else:
            self.exit_button.scale = 1


    def on_mouse_press(self, x, y, buttons, modifiers):
        
        self.mouse_x, self.mouse_y = director.get_virtual_coordinates(x, y)
        if self.game_status == const.GAME_STATUS_MENU and  720 > self.mouse_y > 640:
            self.start_game(self.game_mode)

        if self.game_status== const.GAME_STATUS_MAIN and self.mouse_y <= 600:
            if buttons == 1:
                number = self.game.get_number(self.game.matrix, self.selected_pos)
                if number and number<self.game.max_number:
                        number += 1
                else:
                    number = 1
            elif buttons == 4:
                number = None

            self.game.set_number(self.selected_pos, number)
            self.update_table(self.selected_pos)

        if self.game_status != const.GAME_STATUS_MENU and 490<=self.mouse_x<=530 and 770<=self.mouse_y<=800:
            self.restart_game()

    def start_game(self, mode):
        self.game = Sudoku(const.GAME_MODE[mode][0], const.GAME_MODE[mode][1])

        max_number = self.game.max_number
        self.cells = []

        for _ in range(max_number * max_number):
            _sprite = cocos.sprite.Sprite(const.CELL_IMAGE, 
                    position=(_% max_number * int(600/max_number), 600 - _// max_number* int(600/max_number)), 
                    color=const.COLOR_WHITE[:3],
                    scale=0.3/max_number*9 ,
                    anchor=(0,200)
                    )
            _label = cocos.text.Label('',
                    font_size = 40/max_number*9,
                    font_name = 'Verdana',
                    bold = True,
                    color = const.COLOR_BLACK,
                    x = _%max_number*int(600/max_number) + int(100/max_number) ,
                    y = 600- _//max_number*int(600/max_number)- int(450/max_number),
                    )

            cell = Cell(_sprite, _label)
            self.cells.append(cell)

            self.add(_sprite)
            self.add(_label)
            

        self._pos = (-1, -1)
        self.last_cell_color = None

        self.game_initilise()
        
        self.main_music = Audio(const.MAIN_MUSIC_FILE)
        self.title_music.stop()
        self.main_music.play(-1)

        self.solved_sprite = None

    def restart_game(self):
        for _cell in self.cells:
            _cell.sprite.kill()
            _cell.label.kill()

        if self.solved_sprite:
            self.solved_sprite.kill()
            self.solved_sprite = None

        self.TimePassed = 0
        self.game_status = const.GAME_STATUS_MENU


    def on_key_press(self, key, modifiers):

        self.keys_pressed.add(key)

        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        
        #print(key_names, valid_input)

        _key = key_names[0]
        
        if self.game_status==const.GAME_STATUS_MAIN:
            valid_input = [str(number+1) for number in range(self.game.max_number)]
            if _key == 'SPACE':
                input_text = {'SPACE'}
            else:
                input_text = set(valid_input) & set(_key[-1])

            if input_text:
                _ = input_text.pop()
                number = int(_) if _ != 'SPACE' else None
                self.game.set_number(self.selected_pos, number)
                self.update_table(self.selected_pos)
        elif self.game_status == const.GAME_STATUS_SOLVED:
            if _key == 'SPACE':
                self.restart_game()


    def on_key_release(self, key, modifiers):

        self.keys_pressed.remove(key)


    def game_initilise(self):
        for row in range(self.game.max_number):
            if self.selected_pos[0] != -1:
                break
            for column in range(self.game.max_number):
                if not((row, column) in self.game.fixed_pos):
                    self.selected_pos = (row, column)
                    break

        for index, _cell in enumerate(self.cells):
            row = index // self.game.max_number
            column = index % self.game.max_number

            _number = self.game.get_number(self.game.matrix, (row, column))
            _number = str(_number) if _number else ''
            _cell.label.element.text = _number
            if _number:
                _cell.label.element.color = const.COLOR_GRAY
            else:
                _cell.label.element.bold = False

        self.game_status = const.GAME_STATUS_MAIN


    def set_pos_color(self, pos, color):

        row, column = pos
        self.cells[row * self.game.max_number + column].sprite.color = color[:3]


    def judge_the_matrix(self, pos):

        '''judge the matrix based the number modified in the pos
        1. judge the row
        2. judge the column
        3. judge the block

        RED - repeat numbers
        GREEN - full row/column/block completed
        '''
        
        repeat_number_list = set()
        row, column = pos
        number = self.game.get_number(self.game.matrix, pos)

        for _cell in self.cells:
            _cell.sprite.color = const.COLOR_WHITE[:3]
        # check the same row
        #   store all the numbers in the row
        number_in_the_row = []
        for _row in range(self.game.max_number):
            _number = self.game.get_number(self.game.matrix, (_row, column))
            if _number:
                number_in_the_row.append(_number)
                
        if len(set(filter(None, number_in_the_row))) == self.game.max_number:
            # color the full row when completed
            #print('number in the row:', number_in_the_row)
            for _row in range(self.game.max_number):
                self.set_pos_color((_row, column), const.COLOR_GREEN)
        else:
            #   set the color of the repeat numbers to RED
            for _row in range(self.game.max_number):
                _number = self.game.get_number(self.game.matrix, (_row, column))
                if _number and number_in_the_row.count(_number)>1:
                    self.set_pos_color((_row, column), const.COLOR_RED)
                else:
                    self.set_pos_color((_row, column), const.COLOR_WHITE)


        # check the same column
        #   store all the numbers in the column
        number_in_the_column = []
        for _column in range(self.game.max_number):
            _number = self.game.get_number(self.game.matrix, (row, _column))
            if _number:
                number_in_the_column.append(_number)

        if len(set(filter(None, number_in_the_column))) == self.game.max_number:
            #print('number in the column:', number_in_the_column)
            # color the full column when completed
            for _column in range(self.game.max_number):
                self.set_pos_color((row, _column), const.COLOR_GREEN)
        else:
            #   set the color of the repeat numbers to RED
            for _column in range(self.game.max_number):
                _number = self.game.get_number(self.game.matrix, (row, _column))
                if _number and number_in_the_column.count(_number)>1:
                    self.set_pos_color((row, _column), const.COLOR_RED)
                elif _column != column:
                    self.set_pos_color((row, _column), const.COLOR_WHITE)

        # check the same block
        block_no, _ = self.game.get_block_pos(pos)
        number_in_the_block = []
        for _number in self.game.matrix[block_no]:
            if _number:
                number_in_the_block.append(_number)

        if len(set(filter(None, number_in_the_block))) == self.game.max_number:
            #print('number in the block:', number_in_the_block)
            for index, _number in enumerate(self.game.matrix[block_no]):
                self.set_pos_color(self.game.get_matrix_pos(block_no, index), const.COLOR_GREEN)
        else:
            # set the color of the repeat numbers in the block to RED
            for index, _number in enumerate(self.game.matrix[block_no]):
                if _number and number_in_the_block.count(_number)>1:
                    self.set_pos_color(self.game.get_matrix_pos(block_no, index), const.COLOR_RED)
                elif row != self.game.get_matrix_pos(block_no, index)[0] and column != self.game.get_matrix_pos(block_no, index)[1]:
                    self.set_pos_color(self.game.get_matrix_pos(block_no, index), const.COLOR_WHITE)

        self.last_cell_color = self.cells[row * self.game.max_number + column].sprite.color
    

    def game_win(self):
        self.solved_music = Audio(const.SOLVED_MUSIC_FILE)
        self.main_music.stop()
        self.solved_music.play(-1)
        self.game_status = const.GAME_STATUS_SOLVED

        self.solved_sprite = cocos.sprite.Sprite(const.SOLVED_IMAGE, 
                position = (300, 450), scale = 1)
        self.add(self.solved_sprite)
        print('GAME SOLVED')


    def update_table(self, pos):
        
        if pos in self.game.fixed_pos:
            return None

        row, column = pos

        _number = self.game.get_number(self.game.matrix, pos)
        self.cells[row*self.game.max_number + column].label.element.text = str(_number) if _number else ''
        self.judge_the_matrix(pos)
        if not(_number):
            self.selected_pos = pos
        
        if self.game.judge_win():
            self.game_win()

