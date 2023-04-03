from finite_state_machine import FiniteStateMachine
from finite_state_machine import State
from transition import Transition

class TrafficLight(State):
    def __init__(self, color:str):
        super().__init__()
        self.color = color
        
    def _do_entering_action(self) -> None:
        print(f'Entering {self.color} Light State')
    def _do_in_state_action(self) -> None:
        print(f'In {self.color} Light State')
    def _do_exiting_action(self) -> None:
        print(f'Exiting {self.color} Light State')

class TransitionToColor(Transition):
    def __init__(self, state) -> None:
        super().__init__(state)
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
    
class TrafficLights(FiniteStateMachine):
    def __init__(self):
        
        rl = TrafficLight('red')
        gl = TrafficLight('green')
        yl = TrafficLight('yellow')
        
        tg = TransitionToColor(gl)
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
    tl = TrafficLights()
    
    tl.start()