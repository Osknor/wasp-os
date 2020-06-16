# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Oskar Norinder
import wasp
import random
import micropython
import fonts



# 2-bit RLE, generated from /home/pi/Desktop/Snake.png, 58 bytes
snake1 = (
    b'\x02'
    b'\n\n'
    b'\x02@\xacF\x03A\x80l\x86A\x01A\x82D\x82B'
    b'\x81B\x82B\x81B\x81A\x81B\x81A\x81B\x81A'
    b'\x81B\x81A\x81B\x81B\x82B\x81B\x82D\x82A'
    b'\x01A\x86A\x03F\x02'
)
# 2-bit RLE, generated from /home/pi/Desktop/food4.png, 26 bytes
food2 = (
    b'\x02'
    b'\n\n'
    b'\x05@lC\x06B\x07\x807\x84\x05\x86\x03\x88\x02\x88'
    b'\x02\x88\x03\x86\x05\x84\r'
)

@micropython.viper
def move_snake(snake, pos: int,newHead: int, length: int) -> int:
    b = ptr16(snake)
    b[(pos)%60] = newHead
    return int(b[(pos-length)%60])

@micropython.viper
def get_head(snake,pos: int) ->int:
    b = ptr16(snake)
    return int(b[pos%60])
@micropython.viper
def check_hit(board,pos: int) -> bool:
    b = ptr32(board)
    return bool(b[(pos%24)] & (1 << (pos // 24)))
    return False
@micropython.viper
def update_board(board,pos:int ,last: int,ignore: bool):
    b = ptr32(board)
    #print(pos,last,(pos//24),(pos % 24),1 << (pos % 24), b[(pos//24)])
    b[(pos%24)] |= (1 << (pos // 24))
    if not ignore:
        c = ptr32(board)
        c[(last%24)] ^= (1 << (last // 24))
class Hack:
    pass

class SnakeApp():
    """Application for classic Tetris game.

    """
    NAME = 'Tetris'

    def __init__(self):
        """ color 2bit  """
        self.board = bytearray(240)
        self.piece = bytearray(3)
        self._restarted = True
        self._gameOver = False
        self._moving = False
        self._rl = True
        self.length = 4
        self.pos = 3

    def foreground(self):
        self._draw()
        wasp.system.request_tick(160)
        wasp.system.request_event(wasp.EventMask.TOUCH | wasp.EventMask.SWIPE_UPDOWN | wasp.EventMask.SWIPE_LEFTRIGHT)

    def tick(self, ticks):
        if self._moving and not self._gameOver:
            wasp.system.keep_awake()
            self.update()
    def swipe(self, event):
        if event[0] == wasp.EventType.UP and self._rl:
            self._dir = [0,-1]
            self._rl = False
        elif event[0] == wasp.EventType.RIGHT and not self._rl:
            self._dir = [1,0]
            self._rl = True
        elif event[0] == wasp.EventType.DOWN and self._rl:
            self._dir = [0,1]
            self._rl = False
        elif event[0] == wasp.EventType.LEFT and not self._rl:
            self._dir = [-1,0]
            self._rl = True
    def touch(self, event):
        if not self._moving:
            self._moving = True
        elif self._gameOver:
            self._draw()
    def _draw(self):
        draw = wasp.watch.drawable
        draw.fill()
        draw.fill(0x02e2,0,0,240,20) 
        #draw.fill(0xffff,0,20+10*10,10*4,10)
        self._dir = [1,0]
        self._rl = True
        self._restarted = False
        self._moving = False
        self._gameOver = False
        self.length = 4
        self.pos = 3
        self.score = 0
        draw.set_font(fonts.fixel18)
        draw.set_color(0xffff,0x02E2)
        draw.string("Score: ", 10, 1,80)
        draw.string(str(self.score), 90, 1,20)
        for i in range(len(self.board)):
            self.board[i] = 0
        for i in range(4):
            move_snake(self.snake, i,10*24+i, 4)
            update_board(self.board,10*24+i,0,True)
            draw.blit(snake1, 10*i, 20+10*10)
        self._spawnFood()
        draw.blit(food2, 10*(((self.food % 24) ) % 24) , 20+10*(((self.food//24)) % 22))
    def update(self):
        draw = wasp.watch.drawable
        if self._restarted:
            self._draw()
        if self._moving:
            head = get_head(self.snake,self.pos)
            self.pos += 1 
            newHead = (((head % 24) + self._dir[0]) % 24) +  24* (((head//24)+ self._dir[1]) % 22)
            #draw.fill(0xffff, 10*(((head % 24) + self._dir[0]) % 24),20+10*(((head//24)+ self._dir[1]) % 22),10,10)
            draw.blit(snake1, 10*(((head % 24) + self._dir[0]) % 24) , 20+10*(((head//24)+ self._dir[1]) % 22))
            if check_hit(self.board,newHead):
                self._gameOver = True
                draw.reset()
                draw.string("Game Over",30,110)
            else:
                last = move_snake(self.snake,self.pos, newHead, self.length)
                if self.food == newHead:
                    if self.length >= 59:
                        self._gameOver = True
                        draw.reset()
                        draw.string("You Won! :)",30,110)
                    else:
                        update_board(self.board,newHead,last,True)
                        self._spawnFood()
                        draw.blit(food2, 10*(((self.food % 24)) % 24) , 20+10*(((self.food//24)) % 22))
                        self.length += 1
                else:
                    update_board(self.board,newHead,last,False)
                    draw.fill(0x0000, 10*((last % 24)  % 24),20+10*((last//24) % 22),10,10)
            if (self.length -4)*10 != self.score:
                self.score = 10*(self.length - 4)
                draw.set_color(0xffff,0x02E2)
                draw.set_font(fonts.fixel18)
                draw.string(str(self.score), 90, 1,20)


    def _spawnFood(self):
        trial = random.randrange((22*24)-1)
        localCounter = 0
        while (True or localCounter < 100):
            if check_hit(self.board,trial):
                trial = (((trial % 24) + 2) % 24) +  24* (((trial//24)+ 10) % 22)
            else:
                break
        self.food = trial