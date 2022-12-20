import logging
log = logging.getLogger(__name__)
from events import *

class InputFactory:
    def __init__(self, event_func):
        self.event_func = event_func

    def StandardButton(self, key):
        return StandardButton(self.event_func, key)
    def TwoButtonAxis(self, threshold, pos_key, neg_key):
        return TwoButtonAxis(self.event_func, threshold, pos_key, neg_key)
    def MouseAxis(self, axis, _max, wrap):
        return MouseAxis(self.event_func, axis, _max, wrap)
    def MouseWheelButton(self, value):
        return MouseWheelButton(self.event_func, value)
    def MultiButton(self, value):
        return MultiButton(self.event_func, value)
#    def RepeatingButton(self, value):
#        return StandardMultiButton(self.event_func, value)
    def KeySequenceButton(self, value):
        return KeySequenceButton(self.event_func, value)



class Input:
    def __init__(self, event_func, key):
        self.state = 0
        self.key = key
        self.event_func = event_func
        pass

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def _emit_event(self, ev):
        self.event_func(ev)

class StandardButton(Input):
    """Sends events when state changes"""
    def set_state(self, state):
        if state != self.state:
            ev = PressEvent if state else ReleaseEvent
            self._emit_event(ev(self.key))
            self.state = state


class MultiButton(Input):
    """Sends a sequence of key presses when state changes"""
    def __init__(self, event_func, key_list):
        super().__init__(event_func, None)
        self.key_list = key_list

    def set_state(self, state):
        if state != self.state:
            ev = PressEvent if state else ReleaseEvent
            for key in self.key_list:
                self._emit_event(ev(key))
            self.state = state

class TwoButtonAxis(Input):
    """Sends one event for positive, one event for negative"""
    def __init__(self, event_func, threshold, pos_key, neg_key):
        super().__init__(event_func, None)
        self.tick_mod = 10 #every 10 ticks
        self.pos_key = pos_key
        self.neg_key = neg_key
        self.threshold = threshold

    def set_state(self, state):
        if self.state == 0:
            if state > self.threshold:
                if self.pos_key is None:
                    return
                self.state = 1
                self._emit_event(PressEvent(key=self.pos_key))
            elif state < (-1*self.threshold):
               
