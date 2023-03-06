from finite_state_machine import FiniteStateMachine

if __name__ == '__main__':
    layout = FiniteStateMachine.Layout()
    fsm = FiniteStateMachine(layout=layout , unitialized=False)
    fsm.run()
    
    