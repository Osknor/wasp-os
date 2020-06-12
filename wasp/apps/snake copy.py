# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Oskar Norinder



import wasp
import math
import random


# 2-bit RLE, generated from /home/pi/Desktop/food2.png, 15 bytes
food2 = (
    b'\x02'
    b'\x05\x05'
    b'@lC\x03\x80\xbb\x83\x01\x8a\x01\x83\x01'
)



class Hack:
    """wasptool uses class (starting in column 0) as a clue for chunk at a
    time transmission. Hence we use fake classes to demark places it is safe
    to split an evaluation.
    """
    pass




class SnakeApp():
    """Application for classic snake game.

    """
    NAME = 'Snake'

    def __init__(self):

        self.food = []
        self.pos = []
        self.size = 2
        self.dir = None
        self.rl = True
        self.moving = False
        self.restart = True
        self.gameOver = False
        self.occ = []
        self.spaces = 230/(self.size*2+1)

    def foreground(self):
        """Draw the first frame and establish the tick."""
        self._draw()
        wasp.system.request_tick(200)
        wasp.system.request_event(wasp.EventMask.TOUCH | wasp.EventMask.SWIPE_UPDOWN | wasp.EventMask.SWIPE_LEFTRIGHT)

    def tick(self, ticks):
        """Handle the tick."""
        if not self.gameOver:
            self._draw()
            wasp.system.keep_awake()
        #self._dir = None

    def swipe(self, event):
        """Notify the application of a touchscreen swipe event."""
        if event[0] == wasp.EventType.DOWN and self.rl:
            self.dir = [0,-1]
            self.rl = False
        elif event[0] == wasp.EventType.LEFT and not self.rl:
            self.dir = [1,0]
            self.rl = True
        elif event[0] == wasp.EventType.UP and self.rl:
            self.dir = [0,1]
            self.rl = False
        elif event[0] == wasp.EventType.RIGHT and not self.rl:
            self.dir = [-1,0]
            self.rl = True

    def touch(self, event):
        if not self.moving:
            self.moving = True
        if self.gameOver:
            self.restart = True
            self.moving = False
            self.gameOver = False
    def _draw(self):
        """Draw the next frame."""
        draw = wasp.watch.drawable
        size = 2
        if self.restart:
            draw.fill()
            draw.fill(0xffff,self.size,self.size,240-self.size*2,(self.size*2+1)-self.size) 
            draw.fill(0xffff,self.size,self.size,(self.size*2+1)-self.size,240-self.size*2)
            draw.fill(0xffff,240-(self.size*2+1),self.size,self.size+1,240-self.size*2)
            draw.fill(0xffff,self.size,240-(self.size*2+1),240-self.size*2,self.size+1)
            self.dir = [1,0]
            self.rl = True
            self.pos = []
            self.occ = []
            for i in range(4,0,-1):
                self.pos.append([i,22,False])
                #self.occ.append()
            print(self.pos)
            self.food = random.choice([x for x in range(46*46) if not [x % 46,math.floor(x/46)] in self.pos])
            print(self.food)
            draw.blit(food2, (self.size*2+1)+ (self.food % 46)*(self.size*2+1),(self.size*2+1)+ (math.floor(self.food/46))*(self.size*2+1))
            for pos in self.pos:
                draw.fill(0xffff,(self.size*2+1)+ pos[0]*(self.size*2+1),(self.size*2+1)+ pos[1]*(self.size*2+1),self.size*2+1,self.size*2+1)
            self.restart = False
            #print("restart")
        if self.moving:
            newHead = [self.pos[0][0]+self.dir[0],self.pos[0][1]+self.dir[1],False]
            #print(newHead)
            for i in [newHead[0],newHead[1]]:
                if i < 1 or i > 45:
                    self.gameOver = True
                    break
            for pos in self.pos:
                if newHead[0] == pos[0] and newHead[1] == pos[1]:
                    self.gameOver = True
            if self.gameOver:
                draw.string("Game Over",30,110)
            else:
                last = self.pos.pop()
                if [(self.food % 46),(math.floor(self.food/46))] == [newHead[0],newHead[1]]:
                    print("bam!")
                    newHead[2] = True
                    self.food = None
                if newHead[2]:
                    draw.fill(0xffff,(self.size*2+1)+ newHead[0]*(self.size*2+1)-1,(self.size*2+1)+ newHead[1]*(self.size*2+1)-1,self.size*2+3,self.size*2+3)
                else:
                    draw.fill(0xffff,(self.size*2+1)+ newHead[0]*(self.size*2+1),(self.size*2+1)+ newHead[1]*(self.size*2+1),self.size*2+1,self.size*2+1)
                if last[2]:
                    draw.fill(None,(self.size*2+1)+ last[0]*(self.size*2+1)-1,(self.size*2+1)+ last[1]*(self.size*2+1)-1,self.size*2+3,self.size*2+3)
                    draw.fill(0xffff,(self.size*2+1)+ last[0]*(self.size*2+1),(self.size*2+1)+ last[1]*(self.size*2+1),self.size*2+1,self.size*2+1)
                    last[2] = False
                    self.pos.append(last)
                else:
                    draw.fill(None,(self.size*2+1)+ last[0]*(self.size*2+1),(self.size*2+1)+ last[1]*(self.size*2+1),self.size*2+1,self.size*2+1)
                if not self.food:
                    self.food = random.choice([x for x in range(46*46) if not [x % 46,math.floor(x/46)] in ([newHead] + self.pos)])
                    draw.blit(food2, (self.size*2+1)+ (self.food % 46)*(self.size*2+1),(self.size*2+1)+ (math.floor(self.food/46))*(self.size*2+1))
                self.pos = [newHead] + self.pos
                #self.occ = [math.floor((self.pos[0][0]+self.dir[0])/5)*math.floor((self.pos[0][1]+self.dir[1])/5)] + self.occ
                #print(self.pos)

            
