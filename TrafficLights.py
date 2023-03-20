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

class RedToGreen(Transition):
    def __init__(self, next_state: TrafficLight('green') = None) -> None:
        super().__init__(next_state)
        self.count = 0 
    
    @property
    def is_transiting(self) -> bool:
        self.count += 1
        return self.count > 60
    
class GreenToYellow(Transition):
    def __init__(self, next_state: TrafficLight('yellow') = None) -> None:
        super().__init__(next_state)
        self.count = 0 
    
    @property
    def is_transiting(self) -> bool:
        self.count += 1
        return self.count > 60
    
class YellowToRed(Transition):
    def __init__(self, next_state: TrafficLight('red') = None) -> None:
        super().__init__(next_state)
        self.count = 0 
    
    @property
    def is_transiting(self) -> bool:
        self.count += 1
        return self.count > 60
    
class TrafficLights(FiniteStateMachine):
    def __init__(self):
        
        rl = TrafficLight('red')
        gl = TrafficLight('green')
        yl = TrafficLight('yellow')
        
        rtg = RedToGreen(gl)
        gty = GreenToYellow(yl)
        ytr = YellowToRed(rl)
        
        rl.add_transition(rtg)
        gl.add_transition(gty)
        yl.add_transition(ytr)
        
        layout = FiniteStateMachine.Layout()
        
        layout.initial_state = rl
        
        layout.add_states([layout.initial_state, gl, yl])
        
        super().__init__(layout)
        

if __name__ == "__main__":
    tl = TrafficLights()
    tl.run()