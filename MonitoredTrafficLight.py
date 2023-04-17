


from Condition import TimedCondition
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
    
class MonitoredTrafficLights(FiniteStateMachine):
    def __init__(self):
        
        c1 = TimedCondition(10000)
        
        rl = MonitoredTrafficLight('red')
        gl = MonitoredTrafficLight('green')
        yl = MonitoredTrafficLight('yellow')
        
        tg = TransitionToColor(gl, c1)
    
        ty = TransitionToColor(yl)
        tr = TransitionToColor(rl)
        
        rl.add_transition(tg)
        gl.add_transition(ty)
        yl.add_transition(tr)
        
        layout = FiniteStateMachine.Layout()
        layout.add_states([rl, gl, yl])  
        layout.initial_state = rl
        
        super().__init__(layout=layout, unitialized = False)
        

if __name__ == "__main__":
    mtl = MonitoredTrafficLights()
    
    mtl.start()