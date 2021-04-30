//
//  PathFinder.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-28.
//

import Foundation
import SwiftUI



class PathNode: Equatable, Comparable, Hashable {
    
    let node: Node
    let parent: PathNode?
    let cost: Float
    let guessCost: Float
    
    init(node: Node, parent: PathNode?, cost: Float, guessCost: Float) {
        self.node = node
        self.parent = parent
        self.cost = cost
        self.guessCost = guessCost
    }
   
    func hash(into hasher: inout Hasher) {
        hasher.combine(node)
        hasher.combine(node.x)
        hasher.combine(node.y)
        hasher.combine(parent)
        hasher.combine(cost)
        hasher.combine(guessCost)
    }
    
    static func ==(lhs: PathNode, rhs: PathNode) -> Bool {
        return (lhs.node.x == rhs.node.x) && (lhs.node.y == rhs.node.y) && (lhs.node.Walkable == rhs.node.Walkable)
    }
    
    static func < (lhs: PathNode, rhs: PathNode) -> Bool {
        return (lhs.cost + lhs.guessCost) < (rhs.cost + rhs.guessCost)
    }
    
}

func backtrack(_ goalANode: PathNode) -> [Node] {
    var sol: [Node] = []
    var ANode = goalANode
    
    while (ANode.parent != nil) {
        sol.append(ANode.node)
        ANode = ANode.parent!
    }
    
    sol.append(ANode.node)
    
    return sol
}


func astar(from initialState: Node, to goal: Node, grid: [Node]) -> [Node]? {
    var pqueue = PriorityQueue(ascending: true, startingValues: [PathNode(node: initialState, parent: nil, cost: 0, guessCost: Float(initialState.guessCost(to: goal, grid: grid).count) )])
    var explored = Dictionary<Node, Float>()
    explored[initialState] = 0
    var ANodesSearched: Int = 0
    
    while let currentANode = pqueue.pop() {
        ANodesSearched += 1
          // we know if there are still items, we can pop one
        let currentState = currentANode.node
        
        if (currentState == goal) {
            print("Searched \(ANodesSearched) ANodes.")
            return backtrack(currentANode)
        }
        
        for child in currentState.getNeighbours(grid: grid) {
            
            // Checks if moving diagonal
            let checkA = (child.x == currentANode.node.x + 9.75 && child.y == currentANode.node.y + 9.75)
            let checkB = (child.x == currentANode.node.x + 9.75 && child.y == currentANode.node.y - 9.75)
            let checkC = (child.x == currentANode.node.x - 9.75 && child.y == currentANode.node.y + 9.75)
            let checkD = (child.x == currentANode.node.x - 9.75 && child.y == currentANode.node.y - 9.75)
            
            let newcost: Float
            
            if checkA || checkB || checkC || checkD {
                newcost = currentANode.cost + sqrt(2)
            } else {
                newcost = currentANode.cost + 1
            }
            
            //1 assumes a grid, there should be a cost function    FIX FIX FIX FIX
            if (explored[child] == nil) || (explored[child]! > newcost) {
                explored[child] = newcost
                pqueue.push(PathNode(node: child, parent: currentANode, cost: newcost, guessCost: Float(child.guessCost(to: goal, grid: grid).count) ))
            }
        }
    }
    
    return nil
}




/*
struct Waypointfinder {
    
    let map: [Node] = NodeGrid().Grid
    
    
    func pathfind(from start: Node, to goal: Node) -> [Node]{
        return drawLine(from: start, to: goal)
    }
    
    
    private func drawLine(from start: Node, to goal: Node) -> [Node] {
        
        let startXY: (CGFloat, CGFloat) = (start.x, start.y)
        let goalXY: (CGFloat, CGFloat) = (goal.x, goal.y)
        
        /*let cleanedMap: [Node] = map.filter({
            
        })*/
        
        var nodesCrossed: Int = 0
        var foundNodes: [Node] = []
        
        // Check if line crosses a node
        for i in 0..<map.count {
            print("Counting..")
            print(map[i])
            print(startXY)
            print(goalXY)
            if crossedChecker(startXY, goalXY, i) {
                nodesCrossed += 1
                foundNodes.append(map[i])
            }
        }
        
        print("Crossed \(nodesCrossed) nodes")
        return foundNodes
    }
    
    
    
    private func crossedChecker(_ startXY: (CGFloat, CGFloat), _ goalXY: (CGFloat, CGFloat), _ i: Int) -> Bool {
        
        let offset: CGFloat = (9.75 * sqrt(2)) / 2  /// Max possible distance to a nodes center
        let xDistance = startXY.0 - goalXY.0
        let yDistance = startXY.1 - goalXY.1
        
        
        
        
        
        return true
    }
    

}
///(map[i].x >= startXY.0 - distanceToNodeCenter && map[i].x <= startXY.0 + distanceToNodeCenter) && (map[i].y >= startXY.1 - distanceToNodeCenter && map[i].y <= startXY.1 + distanceToNodeCenter)

/*
 let checkA = (map[i].x >= startXY.0 - offset && map[i].y >= startXY.1 - offset)
 let checkB = (map[i].x <= startXY.0 + offset && map[i].y <= startXY.1 + offset)
 
 let checkC = (map[i].x >= goalXY.0 - offset && map[i].y >= goalXY.1 - offset)
 let checkD = (map[i].x <= goalXY.0 + offset && map[i].y <= goalXY.1 + offset)
 */

/*
 private func crossedCheckerOld(_ startXY: (CGFloat, CGFloat), _ goalXY: (CGFloat, CGFloat), _ i: Int) -> Bool {
     
     let offset: CGFloat = (9.75 * sqrt(2)) / 2  /// Max possible distance to a nodes center
     
     /// Checks explained visually in notes. Basically draws two parallel lines offset to se if it is possible that any nodes have been crossed
     let checkA = (map[i].x >= startXY.0 - offset && map[i].y >= startXY.1 - offset)
     let checkB = (map[i].x <= startXY.0 + offset && map[i].y <= startXY.1 + offset)
     
     let checkC = (map[i].x >= goalXY.0 - offset && map[i].y >= goalXY.1 - offset)
     let checkD = (map[i].x <= goalXY.0 + offset && map[i].y <= goalXY.1 + offset)
     
     return ((checkA && checkB) && checkC && checkD)
 }
 */


struct Pathfinder {
    
    let map: [Node] = NodeGrid().Grid
    
    
    func pathfind(from start: Node, to goal: Node) {
        
    }

}






/// Formulate a result path as an array from a goal ANode found in an astar search
///
/// - parameter startANode: The goal ANode found from an astar search.
/// - returns: An array containing the states to get from the start to the goal.


/// Find the shortest path from a start state to a goal state.
///
/// - parameter initialState: The state that we are starting from.
/// - parameter goalTestFn: A function that determines whether a state is the goal state.
/// - parameter successorFn: A function that finds the next states from a state.
/// - parameter heuristicFn: A function that makes an underestimate of distance from a state to the goal.
/// - returns: A path from the start state to a goal state as an array.

*/
