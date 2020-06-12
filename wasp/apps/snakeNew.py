# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Oskar Norinder
import wasp
import random
food2 = (
    b'\x02'
    b'\x05\x05'
    b'@lC\x03\x80\xbb\x83\x01\x8a\x01\x83\x01'
)
class SnakeApp():
    """Application for classic snake game.

    """
    NAME = 'Snake'

    def __init__(self):

        self._size = 2
        self._restarted = True
        self._gameOver = False
        self._moving = False

    def foreground(self):
        """Draw the first frame and establish the tick."""
        self._logic()
        wasp.system.request_tick(200)
        wasp.system.request_event(wasp.EventMask.TOUCH | wasp.EventMask.SWIPE_UPDOWN | wasp.EventMask.SWIPE_LEFTRIGHT)

    def tick(self, ticks):
        """Handle the tick."""
        if not self._gameOver:
            self._logic()
            wasp.system.keep_awake()

    def swipe(self, event):
        """Notify the application of a touchscreen swipe event."""
        if event[0] == wasp.EventType.DOWN and self._rl:
            self._dir = [0,-1]
            self._rl = False
        elif event[0] == wasp.EventType.LEFT and not self._rl:
            self._dir = [1,0]
            self._rl = True
        elif event[0] == wasp.EventType.UP and self._rl:
            self._dir = [0,1]
            self._rl = False
        elif event[0] == wasp.EventType.RIGHT and not self._rl:
            self._dir = [-1,0]
            self._rl = True

    def touch(self, event):
        if not self._moving:
            self._moving = True
        if self._gameOver:
            self._restarted = True
            self._moving = False
            self._gameOver = False
    def _logic(self):
        """Draw the next frame."""
        draw = wasp.watch.drawable
        size = 2
        if self._restarted:
            self._restart(draw)
        if self._moving:
            newHead = [self.pos[0][0]+self._dir[0],self.pos[0][1]+self._dir[1],False]
            for i in [newHead[0],newHead[1]]:
                if i < 1 or i > 45:
                    self._gameOver = True
                    break
            for pos in self.pos:
                if newHead[0] == pos[0] and newHead[1] == pos[1]:
                    self._gameOver = True
            if self._gameOver:
                draw.string("Game Over",30,110)
            else:
                self._update(draw,newHead)
    def _restart(self,draw):
        draw.fill()
        draw.fill(0xffff,self._size,self._size,240-self._size*2,(self._size*2+1)-self._size) 
        draw.fill(0xffff,self._size,self._size,(self._size*2+1)-self._size,240-self._size*2)
        draw.fill(0xffff,240-(self._size*2+1),self._size,self._size+1,240-self._size*2)
        draw.fill(0xffff,self._size,240-(self._size*2+1),240-self._size*2,self._size+1)
        self._dir = [1,0]
        self._rl = True
        self.pos = []
        self.occ = []
        for i in range(4,0,-1):
            self.pos.append([i,22,False])
        self.food = random.choice([x for x in range(46*46) if not [x % 46,(x//46)] in self.pos])
        draw.blit(food2, (self._size*2+1)+ (self.food % 46)*(self._size*2+1),(self._size*2+1)+ ((self.food//46))*(self._size*2+1))
        for pos in self.pos:
            draw.fill(0xffff,(self._size*2+1)+ pos[0]*(self._size*2+1),(self._size*2+1)+ pos[1]*(self._size*2+1),self._size*2+1,self._size*2+1)
        self._restarted = False
    def _update(self,draw,newHead):
        last = self.pos.pop()
        if [(self.food % 46),(self.food//46)] == [newHead[0],newHead[1]]:
            newHead[2] = True
            self.food = None
        if newHead[2]:
            draw.fill(0xffff,(self._size*2+1)+ newHead[0]*(self._size*2+1)-1,(self._size*2+1)+ newHead[1]*(self._size*2+1)-1,self._size*2+3,self._size*2+3)
        else:
            draw.fill(0xffff,(self._size*2+1)+ newHead[0]*(self._size*2+1),(self._size*2+1)+ newHead[1]*(self._size*2+1),self._size*2+1,self._size*2+1)
        if last[2]:
            draw.fill(None,(self._size*2+1)+ last[0]*(self._size*2+1)-1,(self._size*2+1)+ last[1]*(self._size*2+1)-1,self._size*2+3,self._size*2+3)
            draw.fill(0xffff,(self._size*2+1)+ last[0]*(self._size*2+1),(self._size*2+1)+ last[1]*(self._size*2+1),self._size*2+1,self._size*2+1)
            last[2] = False
            self.pos.append(last)
        else:
            draw.fill(None,(self._size*2+1)+ last[0]*(self._size*2+1),(self._size*2+1)+ last[1]*(self._size*2+1),self._size*2+1,self._size*2+1)
        if not self.food:
            self.food = random.choice([x for x in range(46*46) if not [x % 46,(x//46)] in ([newHead] + self.pos)])
            draw.blit(food2, (self._size*2+1)+ (self.food % 46)*(self._size*2+1),(self._size*2+1)+ (self.food//46)*(self._size*2+1))
        self.pos = [newHead] + self.pos