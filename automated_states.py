from state_machine import State
from field import Field

class idle(State):
    def on_event(self, event):
        if event == 'start':
            return drive()
        if event == 'safety':
            return safety()
        return self

class drive(State):
    def on_event(self, event):
        if event == 'harvest':
            return harvest()
        if event == 'plant':
            return plant()
        if event == 'stop':
            return idle()
        if event == 'edge':
            return edgeDetection()
        if event == 'obstacle':
            return obstacleDetection()
        if event == 'safety':
            return safety()
        if event == 'continue':
            return drive()
        return self

class harvest(State):
    def on_event(self, event):
        if event == 'drive':
            return drive()
        if event == 'stop':
            return idle()
        if event == 'edge':
            return edgeDetection()
        if event == 'obstacle':
            return obstacleDetection()
        if event == 'safety':
            return safety()
        if event == 'continue':
            return drive()
        return self

class plant(State):
    def on_event(self, event):
        if event == 'drive':
            return drive()
        if event == 'stop':
            return idle()
        if event == 'edge':
            return edgeDetection()
        if event == 'obstacle':
            return obstacleDetection()
        if event == 'safety':
            return safety()
        if event == 'continue':
            return drive()
        return self

class obstacleDetection(State):
    def on_event(self, event):
        if event == 'drive':
            return drive()
        if event == 'harvest':
            return harvest()
        if event == 'plant':
            return plant()
        if event == 'stop':
            return safety()
        if event == 'safety':
            return safety()
        return self

class edgeDetection(State):
    def on_event(self, event):
        if event == 'drive':
            return drive()
        if event == 'harvest':
            return harvest()
        if event == 'plant':
            return plant()
        if event == 'stop':
            return idle()
        if event == 'safety':
            return safety()
        return self

class safety(State):
    def on_event(self, event):
        return self