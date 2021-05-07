//
//  GridTest.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-26.
//


import SwiftUI

struct GridView: View {
    
    // Each step is 9.75
    /*
     TOP LEFT THREE
     
     (0.0, 131.0, 9.75, 9.75)
     (9.75, 131.0, 9.75, 9.75)
     (19.5, 131.0, 9.75, 9.75)
     
     */
    
    @State var useAstar: Bool = false
    
    let rects: [CGRect] = [
        CGRect(x: 0.0, y: 131.0, width: 9.75, height: 9.75),
        CGRect(x: 9.75, y: 131.0, width: 9.75, height: 9.75),
        CGRect(x: 19.5, y: 131.0, width: 9.75, height: 9.75),
    ]
    
    @State var nodes: [Node] = NodeGrid().Grid
    
    @State var currentNode: Node = Node(x: 87.75, y: 589.25, Walkable: true)
    
    @State var path: [Node] = []
    
    @State var unwalkable: [Node] = []
    
    @State var intro = false
    
    @State var generating = false
    
    let loading = Loading()
    
    //let waypointFinder = Waypointfinder()
    
    let mqtt = SMCEMQTT()
    
    var body: some View {
        
        ZStack {
            ZStack{
                
                ForEach(nodes, id: \.id) { node in
                    Rectangle()
                        .onTapGesture {
                            /* PATHFINDING */
                            //showGenerating()
                            
                            //print("\(node.x), \(node.y),")
                            
                            print("Generating route...")
                            
                            path = []
                            
                            if useAstar {
                            // This astar; wonky paths, crashes sometimes
                                path = astar(from: currentNode, to: node, grid: nodes)!
                                path = path.reversed()
                            } else {
                            // This one is fast, but can't find all paths
                                
                                path = currentNode.pathfindTo(node, pathSoFar: [], grid: nodes, sizeSoFar: 0)
                            }
                            
                            
                            
                            
                            
                                
                            //currentNode.color = Color.yellow
                            
                            
                            
                            //path = currentNode.pathFindBetter(from: currentNode, target: node)
                            
                            
                            //print(path)
                            //generateRotations(path: path)
                            //unwalkable.append(node)
                            //path.append(node)
                        }
                        
                        .foregroundColor(node.Walkable ? node.color.opacity(0.1) : Color.red.opacity(0.2))
                        .border(Color.white.opacity(0.1))
                        .frame(width: 9.75, height: 9.75)
                        //.position(x: intro ? node.x : node.x + UIScreen.main.bounds.width, y: intro ? node.y : node.y)
                        .position(x: intro ? node.x : node.x, y: intro ? node.y : node.y - UIScreen.main.bounds.height) // <--- THIS ONE LOOKS SICK
                        //.position(x: intro ? node.x : (node.x - 196) * UIScreen.main.bounds.width, y: intro ? node.y : node.y)
                        //.position(x: node.x , y: node.y)
                        //.opacity(intro ? 1 : 0)
                        //.scaleEffect(intro ? 1 : 0)
                        //.animation(Animation.easeOut(duration: 1.5 + Double.random(in: 0...1) + 0.005 * Double(node.x)))
                        .animation(Animation.easeOut(duration: 1.5 + 0.005 * Double(abs(node.x - 195)) + 0.005 * Double(abs(node.y - 433.25)) ))
                        .onAppear() {
                            DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                                intro = true
                            }
                        }
                }
                
                
                
                ForEach(path, id: \.id) { node in
                    Rectangle()
                        .foregroundColor(node.Walkable ? Color.green.opacity(0.8) /*node.color*/ : Color.red.opacity(0.5))
                        .frame(width: 9.75, height: 9.75)
                        .position(x: node.x, y: node.y)

                }
                
                ForEach(unwalkable, id: \.id) { node in
                    Rectangle()
                        .foregroundColor(Color.red.opacity(0.5))
                        .frame(width: 9.75, height: 9.75)
                        .position(x: node.x, y: node.y)

                }
                
                /* TESTING
                VStack {
                    Spacer()
                    Text("Print unwalkable")
                        .onTapGesture {
                            
                            for i in 0..<unwalkable.count {
                                print("(\(unwalkable[i].x),\(unwalkable[i].y)),")
                            }
                            
                        }
                        .padding()
                    Text("Undo")
                        .onTapGesture {
                            
                            unwalkable = unwalkable.dropLast()
                            
                        }
                        .padding()
                    
                }*/
                
                if generating {
                    VStack {
                        loading
                            .offset(y: 60)
                            
                        Spacer()
                    }.transition(.move(edge: .top))
                    .animation(.spring())
                }
                
                
                
                
                
            }
            .offset(x: 4.875, y: -50)
            
            
            VStack {
                Spacer()
                HStack {
                    
                    ZStack {
                        Circle()
                            .frame(width: 40, height: 40)
                            .foregroundColor(color(30, 30, 30))
                            .overlay(Circle()
                                        .strokeBorder(path.count == 0 ? Color.red : Color.green, lineWidth: 3))
                        
                        Image(systemName: "point.fill.topleft.down.curvedto.point.fill.bottomright.up")
                            .foregroundColor(.white)
                    }
                    .onTapGesture {
                        if path.count > 0 {
                            
                            mqtt.publishCommands(commands: generateCommands(initialState: Command(direction: "RIGHT", rotation: 0), path: path))
                        } else {
                            print("Path is empty")
                        }
                    }
                    
                    Spacer()
                    
                    ZStack {
                        Circle()
                            .frame(width: 40, height: 40)
                            .foregroundColor(color(30, 30, 30))
                            .overlay(Circle()
                                        .strokeBorder(useAstar ? Color.green : Color.red, lineWidth: 3))
                        
                        Text("A  ")
                            .foregroundColor(.white)
                        
                        Image(systemName: "star.fill")
                            .font(.system(size: 8, weight: .light))
                            .foregroundColor(.white)
                            .offset(x: 6, y: -5)
                    }
                    .onTapGesture {
                        useAstar.toggle()
                    }
                    
                }
                .padding(.horizontal)
            }
            
            
            
        }
    }
    
    
    func showGenerating() {
        
        generating = true
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
            generating = false
        }
        
    }
    
    
    private func generateRotations(path: [Node]) {
        let STEP: CGFloat = 9.75
        for i in 0..<(path.count - 1) {
            
            let currentX = path[i].x
            let currentY = path[i].y
            
            let nextX = path[i+1].x
            let nextY = path[i+1].y
            
            if nextX == currentX + STEP && nextY == currentY {
                // RIGHT
                print("RIGHT")
            } else if nextX == currentX + STEP && nextY == currentY - STEP {
                // TOP RIGHT
                print("TOP RIGHT")
            } else if nextX == currentX && nextY == currentY - STEP {
                // TOP
                print("TOP")
            } else if nextX == currentX - STEP && nextY == currentY - STEP {
                // TOP LEFT
                print("TOP LEFT")
            } else if nextX == currentX - STEP && nextY == currentY {
                // LEFT
                print("LEFT")
            } else if nextX == currentX - STEP && nextY == currentY + STEP {
                // BOTTOM LEFT
                print("BOTTOM LEFT")
            }  else if nextX == currentX && nextY == currentY + STEP {
                // BOTTOM
                print("BOTTOM")
            } else if nextX == currentX + STEP && nextY == currentY + STEP {
                // BOTTOM RIGHT
                print("BOTTOM RIGHT")
            } else {
                print("NO DIRECTION")
            }
            
            
            
            
        }
        
        
    }

    
    
    func buildNodes() {
        var x: CGFloat = 0.0
        
        
        while x < 300 {
            var y: CGFloat = 131.0
            while y < 600 {
                if Int.random(in: 0...5) == 0 {
                    print("Node(x: \(x), y: \(y), Walkable: false),")
                } else {
                    print("Node(x: \(x), y: \(y), Walkable: true),")
                }
                y = y + 9.75
            }
            x = x + 9.75
        }
    }
    
    
}


struct Loading: View {
    
    var body: some View {
        HStack {
            
            Text("Generating")
                .foregroundColor(.white)
                .padding(.trailing)
            
            ProgressView()
        }
        .padding()
        .background(Capsule().foregroundColor(color(30, 30, 30)))
    }
    
}


/*
struct GridTest_Previews: PreviewProvider {
    static var previews: some View {
        GridView().preferredColorScheme(.dark)
    }
}*/


/*
 Node(Position: CGRect(x: 0.0, y: 131.0, width: 9.75, height: 9.75), Walkable: true),
 Node(Position: CGRect(x: 0.75, y: 131.0, width: 9.75, height: 9.75), Walkable: true),
 Node(Position: CGRect(x: 19.5, y: 131.0, width: 9.75, height: 9.75), Walkable: true)
 */
