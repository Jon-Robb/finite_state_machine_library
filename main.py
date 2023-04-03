from finite_state_machine import FiniteStateMachine

if __name__ == '__main__':
    layout = FiniteStateMachine.Layout()
    fsm = FiniteStateMachine(layout=layout , unitialized=False)
    fsm.start()
    
    # list = [1,2,3, 3,3,3,3,3, 4,5]
    # print(next((x for x in list if x == 3), None))
    
    