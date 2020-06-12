import wasp



class SetTimeApp():
    """Simple test application."""
    NAME = 'Set'
    def __init__(self):
        self.tests = ('Set time', 'Confirm')
        self.test = self.tests[0]
        self.newtime = (1,2,3)
#        self.oldtime = wasp.watch.rtc.get_localtime()
#        self.newtime = (self.oldtime[3], self.oldtime[4], self.oldtime[5])

    def foreground(self):
        """Activate the application."""
        self.on_screen = ( -1, -1, -1, -1, -1, -1 )
        self.draw()
        wasp.system.request_event(wasp.EventMask.TOUCH | wasp.EventMask.SWIPE_LEFTRIGHT)

    def background(self):
        """De-activate the application (without losing state)."""
        pass

    def sleep(self):
        return False

    def swipe(self, event):
        tests = self.tests
        i = tests.index(self.test) + 1
        if i >= len(tests):
            i = 0
        self.test = tests[i]
        self.draw()

    def touch(self, event):
        draw = wasp.watch.drawable
        if self.test == 'Set time':
            if event[1] < 80:
                cyph = 0
            elif event[1] > 160:
                cyph = 2
            else:
                cyph = 1
            if event[2] > 120:
                op = -1
            else:
                op = 1
            self.newtime = list(self.newtime)
            self.newtime[cyph] += op
            top = [12, 60, 60]
            self.newtime[cyph] *= (not (self.newtime[cyph] == top[cyph])) # 11+1=0
            self.newtime[cyph] += (self.newtime[cyph] < 0)*top[cyph] # 0-1 = 12
            self.newtime = tuple(self.newtime)
            
            draw.string("{}:{}:{}".format(self.newtime[0], self.newtime[1], self.newtime[2]), 0, 120, width=180)
            
        elif self.test == 'Confirm':
            wasp.watch.rtc.set_localtime((2020,1,1,self.newtime[0], self.newtime[1], self.newtime[2], 1, 1))

        return True

    def draw(self):
        """Redraw the display from scratch."""
        wasp.watch.display.mute(True)
        wasp.watch.drawable.fill()
        wasp.watch.drawable.string('{}'.format(self.test),
                0, 6, width=240)
        wasp.watch.display.mute(False)

