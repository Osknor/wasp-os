# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Oskar Norinder
import wasp
import math
import random
food2 = (
    b'\x02'
    b'\x05\x05'
    b'@lC\x03\x80\xbb\x83\x01\x8a\x01\x83\x01'
)
class SnakeApp():
    NAME = 'Snake'

    def __init__(self):

        self.sz = 2
        self.sz2 = (self.sz*2+1)
        self._restarted = True
        self.gm = False
        self._moving = False

    def foreground(self):
        self._logic()
        wasp.system.request_tick(200)
        wasp.system.request_event(wasp.EventMask.TOUCH | wasp.EventMask.SWIPE_UPDOWN | wasp.EventMask.SWIPE_LEFTRIGHT)

    def tick(self, ticks):
        if not self.gm:
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
        if self.gm:
            self._restarted = True
            self._moving = False
            self.gm = False
    def _logic(self):
        """Draw the next frame."""
        size = 2
        if self._restarted:
            self._dir = [1,0]
            self._rl = True
            self._pos = []
            for i in range(4,0,-1):
                self._pos.append([i,22,False])
            self.food = random.choice([x for x in range(46*46) if not [x % 46,math.floor(x/46)] in self._pos])
            draw.blit(food2, (sz2)+ (food % 46)*(sz2),(sz2)+ (math.floor(food/46))*(sz2))
            for pos in big_pos:
                draw.fill(0xffff,(sz2)+ pos[0]*(sz2),(sz2)+ pos[1]*(sz2),sz2,sz2)
            self._restarted = False
        if self._moving:
            newHead = [self._pos[0][0]+self._dir[0],self._pos[0][1]+self._dir[1],False]
            for i in [newHead[0],newHead[1]]:
                if i < 1 or i > 45:
                    self.gm = True
                    break
            for pos in self._pos:
                if newHead[0] == pos[0] and newHead[1] == pos[1]:
                    self.gm = True
            if self.gm:
                wasp.watch.drawable.string("Game Over",30,110)
            else:
                self._update(newHead)

    def _update(self,newHead):
        draw = wasp.watch.drawable
        last = self._pos.pop()
        if [(self.food % 46),(math.floor(self.food/46))] == [newHead[0],newHead[1]]:
            newHead[2] = True
            self.food = None
        if newHead[2]:
            draw.fill(0xffff,(self.sz2)+ newHead[0]*(self.sz2)-1,(self.sz2)+ newHead[1]*(self.sz2)-1,self.sz2+2,self.sz2+2)
        else:
            draw.fill(0xffff,(self.sz2)+ newHead[0]*(self.sz2),(self.sz2)+ newHead[1]*(self.sz2),self.sz2,self.sz2)
        if last[2]:
            draw.fill(None,(self.sz2)+ last[0]*(self.sz2)-1,(self.sz2)+ last[1]*(self.sz2)-1,self.sz2+2,self.sz2+2)
            draw.fill(0xffff,(self.sz2)+ last[0]*(self.sz2),(self.sz2)+ last[1]*(self.sz2),self.sz2,self.sz2)
            last[2] = False
            self._pos.append(last)
        else:
            draw.fill(None,(self.sz2)+ last[0]*(self.sz2),(self.sz2)+ last[1]*(self.sz2),self.sz2,self.sz2)
        if not self.food:
            self.food = random.choice([x for x in range(46*46) if not [x % 46,math.floor(x/46)] in ([newHead] + self._pos)])
            draw.blit(food2, (self.sz2)+ (self.food % 46)*(self.sz2),(self.sz2)+ (math.floor(self.food/46))*(self.sz2))
        self._pos = [newHead] + self._pos
class Hack:
    def _restart(sz,sz2,food,big_pos):
        draw = wasp.watch.drawable
        draw.fill()
        draw.fill(0xffff,sz,sz,240-sz*2,(sz2)-sz) 
        draw.fill(0xffff,sz,sz,(sz2)-sz,240-sz*2)
        draw.fill(0xffff,240-(sz2),sz,sz+1,240-sz*2)
        draw.fill(0xffff,sz,240-(sz2),240-sz*2,sz+1)
        draw.blit(food2, (sz2)+ (food % 46)*(sz2),(sz2)+ (math.floor(food/46))*(sz2))
        for pos in big_pos:
            draw.fill(0xffff,(sz2)+ pos[0]*(sz2),(sz2)+ pos[1]*(sz2),sz2,sz2)