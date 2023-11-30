from state_machine import State

class idle(State):
    def on_event(self, event):
        if event == 'start' or event == 'go':
            return drive()
        return self

class drive(State):
    def on_event(self, event):
        if event == 'harvest':
            return harvest()
        if event == 'plant':
            return plant()
        if event == 'stop' or event == 'pause':
            return idle()
        return self

class harvest(State):
    def on_event(self, event):
        if event == 'drive':
            return drive()
        if event == 'plant':
            return plant()
        if event == 'stop' or event == 'pause':
            return idle()
        return self

class plant(State):
    def on_event(self, event):
        if event == 'harvest':
            return harvest()
        if event == 'drive':
            return drive()
        if event == 'stop' or event == 'pause':
            return idle()
        return self

class turn(State):
    def on_event(self, event):
        return self

class speedControl(State):
    def on_event(self, event):
        return self

class obstacleDetection(State):
    def on_event(self, event):
        return self

class obstacleHit(State):
    def on_event(self, event):
        return self

class fieldData(State):
    def on_event(self, event):
        return self

class cropStatus(State):
    # Check if crops seem ready to harvest
    def on_event(self, event):
        return self

class cropFull(State):
    # Full on crops
    def on_event(self, event):
        return self

class cropEmpty(State):
    # No more crops to harvest
    def on_event(self, event):
        return self

# End of our states.