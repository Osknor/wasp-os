# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Oskar Norinder



import wasp
import icons
import math
import random


demo_icon = (
    b'\x02'
    b'`@'
    b'.\xc1?\x1f\xc3?\x1d\xc5?\x1b\xc7?\x19\xc9?\x17'
    b'\xcb?\x16\xcc?\x10\xc1\x06\xc8\x06\xc1?\n\xc4\x06\xc4'
    b'\x06\xc3?\n\xc6\x0c\xc6?\x08\xc9\x08\xc8?\x08\xc7\x0c'
    b'\xc7?\x06\xc6\x06\xc4\x06\xc5?\x06\xc4\x05\xc9\x06\xc3?'
    b'\x06\xc1\x06\xce\x05\xc2?\n\xd2?\x0c\xd7?\x08\xdc?'
    b'\x05\xdc\x05\xc18\xc3\x05\xd7\x06\xc38\xc5\x06\xd2\x05\xc6'
    b'8\xc7\x06\xce\x05\xc88\xca\x05\xc9\x06\xca8\xcc\x06\xc4'
    b'\x06\xcc8\xce\x0b\xcf8\xd0\x08\xd08\xce\x0b\xcf8\xcc'
    b'\x06\xc4\x06\xcc8\xc9\x06\xc9\x06\xca8\xc7\x06\xcd\x06\xc8'
    b'8\xc5\x06\xd2\x06\xc58\xc3\x05\xd7\x06\xc3>\xdb\x06\xc1'
    b'<\xe08\xc2\x06\xdf\x07\xc12\xc3\x06\xdb\x06\xc42\xc6'
    b'\x06\xd6\x06\xc54\xc7\x06\xd1\x06\xc84\xca\x05\xcd\x06\xc9'
    b'6\xcb\x06\xc8\x05\xcc6\xcd\x06\xc3\x06\xcd7\xd0\n\xcf'
    b'8\xd0\x08\xd08\xce\x05\xc1\x06\xcd:\xca\x06\xc5\x06\xcb'
    b':\xc8\x06\xca\x05\xc8<\xc5\x05\xcf\x06\xc5<\xc3\x05\xd3'
    b'\x06\xc2?\x04\xd8?\x07\xdc?\x05\xdb?\x08\xd7?\r'
    b'\xd2?\x11\xce?\x15\xc9?\x1a\xc5?\x1d\xc3?\x1e\xc3'
    b'?\x1e\xc3?\x1e\xc3?\x1e\xc3?\x1e\xc3?\x1e\xc3?'
    b'Q'
)
colors = (
        0xf800, # red
        0xffe0, # yellow
        0x07e0, # green
        0xffff, # white
        0x07ff, # cyan
        0x001f, # blue
        0xf81f, # magenta
    )

class Hack:
    """wasptool uses class (starting in column 0) as a clue for chunk at a
    time transmission. Hence we use fake classes to demark places it is safe
    to split an evaluation.
    """
    pass


class BounceApp():
    """Application for that classic DVD screen saver thing that bounces around on the screen changing color.

    """
    NAME = 'Bounce'
    ICON = demo_icon

    def __init__(self):
        self._color = 0
        self._i = 0
        self._dir = None
        self._pos = [50,50]
        self._last = [int(round(self._pos[0]*2+20)),int(round(self._pos[1]*2+20))]
        self._moving = False

    def foreground(self):
        """Draw the first frame and establish the tick."""
        self._draw()
        wasp.system.request_tick(200)
        wasp.system.request_event(wasp.EventMask.TOUCH | wasp.EventMask.SWIPE_UPDOWN | wasp.EventMask.SWIPE_LEFTRIGHT)

    def tick(self, ticks):
        """Handle the tick."""
        self._draw()
        wasp.system.keep_awake()
        #self._dir = None

    def swipe(self, event):
        """Notify the application of a touchscreen swipe event."""
        if not self._moving:
            if event[0] == wasp.EventType.DOWN:
                angle = 0.25*math.pi
            elif event[0] == wasp.EventType.LEFT:
                angle = 0.75*math.pi
            elif event[0] == wasp.EventType.UP:
                angle = 1.25*math.pi
            elif event[0] == wasp.EventType.RIGHT:
                angle = 1.75*math.pi
            direc = random.random()
            self._dir = [math.cos(direc*0.5*math.pi+angle),math.sin(direc*0.5*math.pi+angle)]
            self._moving = True

    def touch(self, event):
        if self._moving:
            self._moving = False
        else:
            self._dir = None
            self._color += 1
            if self._color >= len(colors):
                self._color = 0
    

    def _draw(self):
        """Draw the next frame."""
        draw = wasp.watch.drawable
        size = 10
        if self._moving:
            if self._dir == None:
                draw.fill()
                direc = random.random()
                self._dir = [math.cos(direc*2*math.pi),math.sin(direc*2*math.pi)]
            if self._pos[0]+self._dir[0] > 100 or self._pos[0]+self._dir[0] < 0:
                self._dir[0] *= -1
                self._color += 1
                if self._color >= len(colors):
                    self._color = 0
            if self._pos[1]+self._dir[1] > 100 or self._pos[1]+self._dir[1] < 0:
                self._dir[1] *= -1
                self._color += 1
                if self._color >= len(colors):
                    self._color = 0

            self._pos[0] += self._dir[0]*3
            self._pos[1] += self._dir[1]*3

            draw.fill(None,self._last[0]-size,self._last[1]-size,size*2+1,size*2+1)
            self._last = [int(round(self._pos[0]*2+20)),int(round(self._pos[1]*2+20))]
            draw.fill(colors[self._color],self._last[0]-size,self._last[1]-size,size*2+1,size*2+1)
        else:
            if self._dir == None:
                draw.fill()
                direc = random.random()
                self._dir = [math.cos(direc*2*math.pi),math.sin(direc*2*math.pi)]
                draw.fill(colors[self._color],self._last[0]-size,self._last[1]-size,size*2+1,size*2+1)