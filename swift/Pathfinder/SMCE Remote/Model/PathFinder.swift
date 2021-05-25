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
            
            
            if (explored[child] == nil) || (explored[child]! > newcost) {
                explored[child] = newcost
                pqueue.push(PathNode(node: child, parent: currentANode, cost: newcost, guessCost: Float(child.guessCost(to: goal, grid: grid).count) ))
            }
        }
    }
    
    return nil
}





