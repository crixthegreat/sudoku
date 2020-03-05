#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2020/2/26 21:18:41

class Const():

    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value

const = Const()

const.GAME_CAPTION = 'Sudoku by Crix '
const.VERSION = 'v0.99'
const.WINDOW_WIDTH, const.WINDOW_HEIGHT = 600, 800
const.COLOR_RED = (255, 0, 0, 255)
const.COLOR_GREEN = (0, 255, 0, 255)
const.COLOR_BLUE = (0, 0, 255, 255)
const.COLOR_BLACK = (0, 0, 0, 255)
const.COLOR_WHITE = (255, 255, 255, 255)
const.COLOR_GRAY = (0, 0, 0, 155)
const.COLOR_YELLOW = (255, 255, 0, 200)
const.GAME_MODE = [(2, 2),(3, 2),(2, 3),(3, 3)]
const.GAME_SELECT_BOX_START_POS = (70, 690)

const.GAME_SELECT_BOX_IMAGE = 'pic/game_select_box.png'
const.CELL_IMAGE = 'pic/cell.png'
const.BG_IMAGE = 'pic/bg.png'
const.EXIT_IMAGE = 'pic/exit.png'
const.SOLVED_IMAGE = 'pic/solved.png'

const.TITLE_MUSIC_FILE = 'music/title.ogg'
const.MAIN_MUSIC_FILE = 'music/main.ogg'
const.SOLVED_MUSIC_FILE = 'music/solved.ogg'

const.GAME_STATUS_MENU = 'menu'
const.GAME_STATUS_MAIN = 'main'
const.GAME_STATUS_SOLVED = 'solved'
