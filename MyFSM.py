from FiniteStateMachine import FiniteStateMachine

class MyFSM(FiniteStateMachine):
    def __init__(self):
        
        
        layout = FiniteStateMachine.Layout()
        
        super().__init__(layout)
        
    def enter_state1(self):
        print("entering state 1")

    def exit_state1(self):
        print("exiting state 1")

    def update_state1(self):
        print("updating state 1")

    def transition1(self):
        print("transitioning from state 1 to state 2")
        return True

    def enter_state2(self):
        print("entering state 2")

    def exit_state2(self):
        print("exiting state 2")

    def update_state2(self):
        print("updating state 2")

    def transition2(self):
        print("transitioning from state 2 to state 1")
        return True
    
 # Add states to the layout here
        # -------------------------------------------------------------------------------------
        # layout.add_state("State1", self.enter_state1, self.exit_state1, self.update_state1)
        # self.add_state("State2", self.enter_state2, self.exit_state2, self.update_state2)
        # self.add_transition("State1", "State2", self.transition1)
        # self.add_transition("State2", "State1", self.transition2)
        # self.set_start("State1")
        