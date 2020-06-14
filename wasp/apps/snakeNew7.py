# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Oskar Norinder
import wasp
import random
import micropython
import array
import random
food1 = (
    b'\x02'
    b'\x05\x05'
    b'@lC\x03\x80\xbb\x83\x01\x8a\x01\x83\x01'
)
# 2-bit RLE, generated from /home/pi/Desktop/foood.png, 22 bytes
food2 = (
    b'\x02'
    b'\x07\x07'
    b'\x04@lB\x04B\x04\x807\x83\x03\x85\x02\x85\x02\x85'
    b'\x03\x83\x02'
)


@micropython.viper
def move_snake(snake, pos: int,newHead: int, length: int) -> int:
    b = ptr16(snake)
    b[(pos)%68] = newHead
    return int(b[(pos-length)%68])

@micropython.viper
def get_head(snake,pos: int) ->int:
    b = ptr16(snake)
    return int(b[pos%68])
@micropython.viper
def check_hit(board,pos: int) -> bool:
    b = ptr32(board)
    return bool(b[(pos%34)] & (1 << (pos // 34)))
    return False
@micropython.viper
def update_board(board,pos:int ,last: int,ignore: bool):
    b = ptr32(board)
    #print(pos,last,(pos//34),(pos % 34),1 << (pos % 34), b[(pos//34)])
    b[(pos%34)] |= (1 << (pos // 34))
    if not ignore:
        c = ptr32(board)
        c[(last%34)] ^= (1 << (last // 34))


class SnakeApp():
    """Application for classic snake game.

    """
    NAME = 'Snake'

    def __init__(self):
        self.board = array.array('I', [0] * 34 )
        self.snake = bytearray(136)
        self._size = 7
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
        draw.fill(0xffff,0,0,240,240) 
        draw.fill(0x0000,1,22,238,217)
        draw.fill(0xffff,1,22+7*15,7*4,7)
        self._dir = [1,0]
        self._rl = True
        self._restarted = False
        self._moving = False
        self._gameOver = False
        self.length = 4
        self.pos = 3
        for i in range(len(self.board)):
            self.board[i] = 0
        for i in range(4):
            move_snake(self.snake, i,15*34+i, 4)
            update_board(self.board,15*34+i,0,True)
        self._spawnFood()
        draw.blit(food2,1+7*(((self.food % 34) ) % 34) , 22+7*(((self.food//34)) % 31))
    def update(self):
        draw = wasp.watch.drawable
        if self._restarted:
            self._draw()
        if self._moving:
            head = get_head(self.snake,self.pos)
            self.pos += 1 
            newHead = (((head % 34) + self._dir[0]) % 34) +  34* (((head//34)+ self._dir[1]) % 31)
            draw.fill(0xffff,1+7*(((head % 34) + self._dir[0]) % 34),22+7*(((head//34)+ self._dir[1]) % 31),7,7)
            if check_hit(self.board,newHead):
                self._gameOver = True
                draw.string("Game Over",30,110)
            else:
                last = move_snake(self.snake,self.pos, newHead, self.length)
                #print(get_head(self.snake,self.pos))
                if self.food == newHead:
                    if self.length >= 67:
                        self._gameOver = True
                        draw.string("You Won! :)",30,110)
                    else:
                        update_board(self.board,newHead,last,True)
                        self._spawnFood()
                        draw.blit(food2,1+7*(((self.food % 34)) % 34) , 22+7*(((self.food//34)) % 31))
                        self.length += 1
                else:
                    update_board(self.board,newHead,last,False)
                    draw.fill(0x0000,1+7*((last % 34)  % 34),22+7*((last//34) % 31),7,7)


    def _spawnFood(self):
        trial = random.randrange(32*34)
        localCounter = 0
        while (True or localCounter < 100):
            if check_hit(self.board,trial):
                trial = (((trial % 34) + 2) % 34) +  34* (((trial//34)+ 7) % 31)
            else:
                break
        self.food = trial




