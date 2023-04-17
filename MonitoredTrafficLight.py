


from Condition import StateEntryDurationCondition, TimedCondition
from state import MonitoredState
from finite_state_machine import FiniteStateMachine
from transition import MonitoredTransition
# from Condition import 

class MonitoredTrafficLight(MonitoredState):
    def __init__(self, color:str):
        super().__init__()
        self.color = color
        
    def _do_entering_action(self) -> None:
        print(f'Entering {self.color} Light State')
    def _do_in_state_action(self) -> None:
        print(f'In {self.color} Light State')
    def _do_exiting_action(self) -> None:
        print(f'Exiting {self.color} Light State')

class TransitionToColor(MonitoredTransition):
    def __init__(self, state, condition=None) -> None:
        super().__init__(state, condition)
        self.count = 0 
        
    @property
    def is_transiting(self) -> bool:
        if self.count > 100:
            self.count = 0
            return True
        self.count += 1
        return self.count > 100

    def _do_transition_action(self) -> None:
        print(f'Transitioning to {self.next_state.color.capitalize()} Light State')
    
class StateDurationMonitoredTrafficLights(FiniteStateMachine):
    def __init__(self):
        
        # c1 = TimedCondition(1)
        # c2 = TimedCondition(2)
        # c3 = TimedCondition(3)
        
        
        rl = MonitoredTrafficLight('red')
        sc1 = StateEntryDurationCondition(1.0, rl)
        
        gl = MonitoredTrafficLight('green')
        sc2 = StateEntryDurationCondition(1.0, gl)
        
        yl = MonitoredTrafficLight('yellow')
        sc3 = StateEntryDurationCondition(1.0, yl)
        
        tg = TransitionToColor(gl, sc1)
        ty = TransitionToColor(yl, sc2)
        tr = TransitionToColor(rl, sc3)
        
        rl.add_transition(tg)
        gl.add_transition(ty)
        yl.add_transition(tr)
        
        layout = FiniteStateMachine.Layout()
        layout.add_states([rl, gl, yl])  
        layout.initial_state = rl
        
        super().__init__(layout=layout, unitialized = False)
        

if __name__ == "__main__":
    mtl = StateDurationMonitoredTrafficLights()
    mtl.start()