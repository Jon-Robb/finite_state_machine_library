


from Condition import StateEntryCountCondition, StateEntryDurationCondition, TimedCondition, AlwaysTrueCondition
from state import MonitoredState
from finite_state_machine import FiniteStateMachine
from transition import MonitoredTransition
# from Condition import 

class StateEntryDurationTrafficLight(MonitoredState):
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

    def _do_transition_action(self) -> None:
        print(f'Transitioning to {self.next_state.color.capitalize()} Light State')
        

class OgMonitoredTrafficLights(FiniteStateMachine):
    def __init__(self):

        
        gl = StateEntryDurationTrafficLight('green')
        yl = StateEntryDurationTrafficLight('yellow')
        rl = StateEntryDurationTrafficLight('red')
        
        condition_to_green = StateEntryDurationCondition(1.0, rl)
        condition_to_yellow = StateEntryDurationCondition(1.0, gl)
        condition_to_red = StateEntryDurationCondition(1.0, yl)
        
        
        transit_green = TransitionToColor(gl, condition_to_green)
        transit_yellow = TransitionToColor(yl, condition_to_yellow)
        transit_red = TransitionToColor(rl, condition_to_red)
        
        rl.add_transition(transit_green)
        gl.add_transition(transit_yellow)
        yl.add_transition(transit_red)
        
        layout = FiniteStateMachine.Layout()
        layout.add_states([rl, gl, yl])  
        layout.initial_state = rl
        
        super().__init__(layout=layout, unitialized = False)
    
class StateEntryMonitoredTrafficLights(FiniteStateMachine):
    def __init__(self):

        
        rl = StateEntryDurationTrafficLight('red')
        yl = StateEntryDurationTrafficLight('yellow')
        gl = StateEntryDurationTrafficLight('green')
        
        
        condition_to_yellow = StateEntryDurationCondition(1.0, rl)
        condition_to_red = StateEntryDurationCondition(1.0, yl)
        condition_to_green = TimedCondition(4)
        condition_in_green = AlwaysTrueCondition(inverse=True)
        
        tr = TransitionToColor(rl, condition_to_red)
        ty = TransitionToColor(yl, condition_to_yellow)
        rg = TransitionToColor(rl, condition_to_green)
        yg = TransitionToColor(yl, condition_to_green)
        ig = TransitionToColor(gl, condition_in_green)
        
        rl.add_transition(ty)
        # rl.add_transition(rg)
        yl.add_transition(tr)
        # yl.add_transition(yg)
        gl.add_transition(ig)
        
        layout = FiniteStateMachine.Layout()
        layout.add_states([rl, gl, yl])  
        layout.initial_state = rl
        
        super().__init__(layout=layout, unitialized = False)
        
        
class StateEntryCountMonitoredTrafficLights(FiniteStateMachine):
    def __init__(self):
    
        
        gl = StateEntryDurationTrafficLight('green')
        yl = StateEntryDurationTrafficLight('yellow')
        rl = StateEntryDurationTrafficLight('red')
        
        condition_to_green = StateEntryDurationCondition(1.0, rl)
        condition_to_yellow = StateEntryDurationCondition(1.0, gl)
        condition_to_red = StateEntryDurationCondition(1.0, yl)
        
        
        transit_green = TransitionToColor(gl, condition_to_green)
        transit_yellow = TransitionToColor(yl, condition_to_yellow)
        transit_red = TransitionToColor(rl, condition_to_red)
        
        transit_to_green_at_count_2 = TransitionToColor(rl, StateEntryCountCondition(2, gl, auto_reset=False))
        transit_to_green_at_count_2.add_transiting_action(lambda: print('DAGDGSDGSDGSDGSDGAWUEGHWIUGHIWUGHWIUGHWIUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWEIUGHWEIUGHWEIGUHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGHWIEUGKK'))
        
        rl.add_transition(transit_green)
        rl.add_transition(transit_to_green_at_count_2)
        gl.add_transition(transit_yellow)
        yl.add_transition(transit_red)
        
        layout = FiniteStateMachine.Layout()
        layout.add_states([rl, gl, yl])  
        layout.initial_state = rl
        
        super().__init__(layout=layout, unitialized = False)


# class RandomTrafficLights(FiniteStateMachine):
    

if __name__ == "__main__":
    
    # og_monitored = OgMonitoredTrafficLights()
    # og_monitored.start()
    
    secmtl = StateEntryCountMonitoredTrafficLights()
    secmtl.start()
    
    # semtl = StateEntryMonitoredTrafficLights()
    # semtl.start()