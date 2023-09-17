## Team Members
The team consists of myself, [Nathaelle Fournier](https://github.com/SakyunBuns), [Quoc Huan](https://github.com/ArsenTigor), and [Andrzej Wisniowski](https://github.com/cryptoblivious). The project was part of a robotics class in which we had to create a finite state machine to control a robot. The robot was a GoPiGo3, and the finite state machine was implemented in python.

## FiniteStateMachine Library
Our work is estimated to be approximately 90% in line with the provided design. All requested elements have been implemented. However, we have encountered some minor issues in the management of lights for the robot's second task, which are yet to be resolved.

## Infrastructure
### C64Project
The C64Project class has been designed to perform several functions:

Robot integrity validation: This process confirms that all robot components are functioning correctly before deployment.
Robot startup management: This feature enables the robot to start up correctly.
Robot task management: This part allows the robot to execute the required tasks.
Application termination management: This feature ensures the application terminates correctly.  
### Robot
The Robot class has been designed to perform several functions:

Remote control management: This functionality allows remote control of the robot.
Range finder management: This section ensures the robot's ability to measure distances.
Eye color management (EyeBlinkers class): This provides the robot with the ability to change the color of its eyes, open and close them.
Headlight management: This functionality allows the robot to turn its headlights on and off.  
### Software Infrastructure
Our software is divided into three levels of abstraction. The first level offers a generic state machine with a plan, states, and transitions. The second level provides subclasses that add features closer to the actual requirements, and the third level controls a GoPiGo robot. This modular structure simplifies the addition of new tasks to the robot by merely adding a new state machine to its list of state machines.

## Other Abstraction Elements
A particularly noteworthy abstraction in our work involves the nested hierarchical structure we have established with our state and state machine classes. Indeed, this configuration resembles that of a mini operating system.

Each instance of our state class is capable of having a state machine. This means that, in our architecture, not only can a state machine possess multiple states, but also a state can itself possess another state machine. This nested hierarchy creates a complex structure that can be flexibly adjusted to meet the various requirements of our system.

This is similar to how an operating system manages processes and threads. Just as in our architecture, a process in an operating system can have multiple threads, and these threads can themselves spawn other processes or threads. This comparison highlights the power of our approach in terms of modularity and extensibility.

## Conclusion
We take pride in what we have achieved with this FiniteStateMachine library and how we have tackled the project's challenges. We are confident that the minor issues with light management could be easily resolved with a little more time.

