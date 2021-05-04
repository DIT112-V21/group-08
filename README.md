# group-08-Pathfinder
# What are we making?

We will endeavour to make a system to control the emulated car in the tool provided to us. We will write code for the emulated car to give it the capabilities we desire as well as create an interface with which to control the car.
The following is a list of the features of the system we plan to develop develop: \
      1: The car will be controllable using a joystick or "arrow key" like interface. \
      2: The car will be controllable with voice commands. \
      3: The car will be controllable via a map with pathfinding functionalities.
      
# Why are we making it? What problems does it solve?

By making the car be controllable with voice commands we hope to make it accessible to people unable to manually operate a computer and possibly more convenient. Autonomous navigation will make it much simpler for a user to move the car to a desired point. They can do so with many fewer inputs than if they were to steer the car themselves.

# How are we going to make it?

To build the system described above we are planning to use the following coding languages: Swift, Python and C++.

The reason we have chosen to use these different tools is to leverage the different strenghts of the utilized technologies as well as the individual strengths of our development team.

From a business standpoint we argue that these different interfaces are necessary for different users. Some drivers may want total control over the car, which is why we are enabling manual controls in our python application. Others may want a more hands off experience with voice control, also in python. Lastly, some passengers may want a layed back and fully autonomous driving experience, which is why we are implementing the pathfinding app in swift.

### Swift

We use Swift and SwiftUI to build the app which is responsible for presenting the map of the surrounding area as well as using pathfinding algorithms to find a path to the desired destination. Currently the app has two pathfinding algoriths, one that can quickly generate paths at the cost of them often being sub-optimal. And one that uses an a-star algorithm to generate the shortest path at the cost of it being slower to calculate. The app will then generate a set of instructions for the car to follow based on the calculated path. We may also implement a waypoint based system with predetermined routes between the different waypoints.

![alt-text](https://github.com/DIT112-V21/group-08/blob/readme-update/Pathfinder%20iOS%20App/Preview%20Content/Preview%20Assets.xcassets/DemoGIFs/NodeMap.gif) ![alt-text](https://github.com/DIT112-V21/group-08/blob/readme-update/Pathfinder%20iOS%20App/Preview%20Content/Preview%20Assets.xcassets/DemoGIFs/Astar.gif) ![alt-text](https://github.com/DIT112-V21/group-08/blob/readme-update/Pathfinder%20iOS%20App/Preview%20Content/Preview%20Assets.xcassets/DemoGIFs/Waypoints.gif)

### Python

Python will be used to develop our alternative user interface, responsible for manual controls as well as voice controlls.

### C++

C++ together with MQTT will be the bridge between our different interfaces and the car. Arduino code will be responsible for executing the various commands given to the car to perform.

# Development team:

- Adam Telles
- Ahmed Yasser
- Alex Nordin
- Axel Broberg	
- Erik Sjölund 	
- Hampus Erlandsson  
- Niklas Höglund   
