# ![](https://github.com/DIT112-V21/group-08/blob/master/GUI%20Pycharm/Car%20icon.png)Group-08 PathFinder 
![](https://github.com/DIT112-V21/group-08/blob/master/GUI%20Pycharm/Path%20Finder.png)
# Table of Contents
- [What are we making](https://github.com/DIT112-V21/group-08#what-are-we-making)
- [Why are we making it / What problems does it solve](https://github.com/DIT112-V21/group-08#why-are-we-making-it-what-problems-does-it-solve)
- [How are we going to make it](https://github.com/DIT112-V21/group-08#how-are-we-going-to-make-it)
- [Features Overview](https://github.com/DIT112-V21/group-08#features-overview)
- [Installation Guide(Set-up)](https://github.com/DIT112-V21/group-08/tree/master#installation-guideset-up)
- [User Manual](https://github.com/DIT112-V21/group-08/tree/master#user-manual)
- [Resources](https://github.com/DIT112-V21/group-08#resources)
- [Development Team](https://github.com/DIT112-V21/group-08#development-team)
# What are we making?

We will endeavour to make a system to control the emulated car in the tool provided to us. We will write code for the emulated car to give it the capabilities we desire as well as to create an interface with which to control the car remotely & safely.
The following is a brief list of the **Features** of the system we plan to develop develop: \
      1: The car will be controllable using manually via interface  & keyboard arrow keys. \
      2: The car will be controllable with smart voice commands. \
      3: The car will be controllable via a map with pathfinding functionalities.
      
# Why are we making it? What problems does it solve?

By making the car be controllable with voice commands we hope to make it accessible to people unable to manually operate a computer and possibly more convenient. Autonomous navigation will make it much simpler for a user to move the car to a desired point effectively. They can do so with many fewer inputs than if they were to steer the car themselves.
In adittion, currently with the panademic ravaging our world , it is sigificantly better to do more activities remotely with less risk of spreading viruses via human contacts or objects.

# How are we going to make it?

To build the system described above we are planning to use the following coding languages: **Swift**, **Python** and **C++**.

The reason we have chosen to use these different tools is to leverage the different strenghts of the utilized technologies as well as the individual strengths of our development team.

From a business standpoint we argue that these different interfaces are necessary for different users. Some drivers may want total control over the car, which is why we are enabling  manual controls in our python application & arrow keys control. Others may want a more hands off experience with voice control, also in python. Lastly, some passengers may want a layed back and fully autonomous driving experience, which is why we are implementing the pathfinding app in swift.

## Features Overview:

- [Basic & Advanced Obstacle Avoidance](https://github.com/DIT112-V21/group-08/wiki/Milestone-1:-Basic-Movement-&-Basic-Obstacle-Avoidance)

- [Mapping & Pathfinding capabilities](https://github.com/DIT112-V21/group-08/wiki/Milestone-2:-Mapping-&-Pathfinder-&-Advanced-Obstacle-Avoidance)

- [Controller Interface](https://github.com/DIT112-V21/group-08/wiki/Milestone-3:-Controller-Interface)

- [Manual & Voice control](https://github.com/DIT112-V21/group-08/wiki/Milestone-4:-Voice-Control)

### Swift

We use Swift and SwiftUI to build the app which is responsible for presenting the map of the surrounding area as well as using pathfinding algorithms to find a path to the desired destination. Currently the app has two pathfinding algoriths, one that can quickly generate paths at the cost of them often being sub-optimal. And one that uses an a-star algorithm to generate the shortest path at the cost of it being slower to calculate. The app will then generate a set of instructions for the car to follow based on the calculated path. We may also implement a waypoint based system with predetermined routes between the different waypoints.

![alt-text](https://github.com/DIT112-V21/group-08/blob/master/swift/Pathfinder/SMCE%20Remote/Preview%20Content/Preview%20Assets.xcassets/DemoGIFs/NodeMap.gif)
![alt-text](https://github.com/DIT112-V21/group-08/blob/master/swift/Pathfinder/SMCE%20Remote/Preview%20Content/Preview%20Assets.xcassets/DemoGIFs/Astar.gif) 

### Python

Python will be used to develop our alternative user interfaces, responsible for manual controls via an interface along with keyboard input, as well as smart voice recognition system to verbally deliver commands to the car and comprehend basic synonyms for driving.

![Main Window](https://github.com/DIT112-V21/group-08/blob/master/GUI%20Pycharm/Main%20window.png) 


![Voice Control Window](https://github.com/DIT112-V21/group-08/blob/master/GUI%20Pycharm/Voice%20Control%20Window.png) 


![Help Window](https://github.com/DIT112-V21/group-08/blob/master/GUI%20Pycharm/Help%20Window.png)


### C++

C++ together with MQTT will be the bridge between our various interfaces and the car(SMCE). Arduino code will be responsible for executing the several commands given to the car to perform accordingly.

## Installation Guide(Set-up):
There are a few things you need to set in place before kicking off:

- Download Arduino IDE
- Download SMCE-gd
- Download PyCharm
- Download Eclipse Mosquitto MQTT
- Clone the repository: https://github.com/DIT112-V21/group-08
- Install PyCharm Libraries
  - Click on "File" Top-Left
  - Select "Settings"
  - Click on the arrow line of "group-08"
  - Choose "Python Interpreter"
  - Press on the "+" button to add the libraries (packages)
- *Following instructions for MacOS only*
  - Install Xcode (also installs Swift and SwiftUI)
  - Open SMCE Remote.xcworkspace in Xcode and run the **iPhone 12 Pro** simulator. 
  > It is important to use the simulator for this specific device since other screen sizes may have visual errors (which may or may not be fixed eventually). If this part works fine then ignore the following instructions.
  - *If any CocoaPods issues arise* Install CocoaPods with following terminal commands
  > If using an Apple Silicon computer try adding *arch -x86_64* before each command.
    - **$ sudo gem install cocoapods**
    - *Navigate to xcode project directory*
    - **$ pod install**
  - *If any package dependencies issues arise*
    - In Xcode navigate to File > Swift Packages > Add Package Dependency
    - Select SMCE Remote as project
    - Paste this URL: https://github.com/lucasbrown/swiftui-visual-effects
    - Select master branch or latest release


![](https://github.com/DIT112-V21/group-08/blob/master/GUI%20Pycharm/Python%20Libraries.png)

## User Manual:
-
-
-
-
-
## Resources
### Sofware(Dependencies):
The following Software libraries, APIs and External services were used during the development of the PathFinder's Both Interfaces & General Functionalities:
- [Arduino IDE](https://www.arduino.cc/en/software)
- [SMCE-gd](https://github.com/ItJustWorksTM/smce-gd)
- [Smartcar Shield](https://platisd.github.io/smartcar_shield/index.html)
- [Swift](https://swift.org/download/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
  - PyCharm Libraries
- [DialogFlow API](https://cloud.google.com/dialogflow/es/docs)
- [Eclipse Mosquitto MQTT](https://mosquitto.org/download/)
- [C++](https://www.jetbrains.com/clion/?gclid=CjwKCAjwtJ2FBhAuEiwAIKu19nQfybBlmVgNuk8aOl7V7R__jwzHdAKu_jqeAhlLfO1aTcjLJXvwyRoCoK8QAvD_BwE&gclsrc=aw.ds)

# Development Team:

- [Adam Telles](https://github.com/adamtelles)
- [Ahmed Yasser](https://github.com/AhmedYasser-gu)
- [Alex Nordin](https://github.com/Alnor985)
- [Axel Broberg](https://github.com/AxelBroberg)
- [Erik Sjölund](https://github.com/esjolund)	
- [Hampus Erlandsson](https://github.com/BrutalFrost)  
- [Niklas Höglund](https://github.com/NiklasHoglund)   

