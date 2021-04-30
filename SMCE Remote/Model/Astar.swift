//
//  Astar.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-27.
//

//
//  astar.swift
//  SwiftPriorityQueue
//
//  Copyright (c) 2015-2019 David Kopec
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.
// This is an example of astar that uses SwiftPriorityQueue


class ANode<T: Hashable>: Comparable, Hashable {
    let state: T
    let parent: ANode?
    let cost: Float
    let heuristic: Float
    init(state: T, parent: ANode?, cost: Float, heuristic: Float) {
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
    }
    
    func hash(into hasher: inout Hasher) {
        hasher.combine(state)
        hasher.combine(parent)
        hasher.combine(cost)
        hasher.combine(heuristic)
    }
}

func < <T>(lhs: ANode<T>, rhs: ANode<T>) -> Bool {
    return (lhs.cost + lhs.heuristic) < (rhs.cost + rhs.heuristic)
}

func == <T>(lhs: ANode<T>, rhs: ANode<T>) -> Bool {
    return lhs === rhs
}

/// Formulate a result path as an array from a goal ANode found in an astar search
///
/// - parameter startANode: The goal ANode found from an astar search.
/// - returns: An array containing the states to get from the start to the goal.
func backtrack<T>(_ goalANode: ANode<T>) -> [T] {
    var sol: [T] = []
    var ANode = goalANode
    
    while (ANode.parent != nil) {
        sol.append(ANode.state)
        ANode = ANode.parent!
    }
    
    sol.append(ANode.state)
    
    return sol
}

/// Find the shortest path from a start state to a goal state.
///
/// - parameter initialState: The state that we are starting from.
/// - parameter goalTestFn: A function that determines whether a state is the goal state.
/// - parameter successorFn: A function that finds the next states from a state.
/// - parameter heuristicFn: A function that makes an underestimate of distance from a state to the goal.
/// - returns: A path from the start state to a goal state as an array.
func astar<T: Hashable>(_ initialState: T, goalTestFn: (T) -> Bool, successorFn: (T) -> [T], heuristicFn: (T) -> Float) -> [T]? {
    var frontier = PriorityQueue(ascending: true, startingValues: [ANode(state: initialState, parent: nil, cost: 0, heuristic: heuristicFn(initialState))])
    var explored = Dictionary<T, Float>()
    explored[initialState] = 0
    var ANodesSearched: Int = 0
    
    while let currentANode = frontier.pop() {
        ANodesSearched += 1
          // we know if there are still items, we can pop one
        let currentState = currentANode.state
        
        if goalTestFn(currentState) {
            print("Searched \(ANodesSearched) ANodes.")
            return backtrack(currentANode)
        }
        
        for child in successorFn(currentState) {
            let newcost = currentANode.cost + 1  //1 assumes a grid, there should be a cost function
            if (explored[child] == nil) || (explored[child]! > newcost) {
                explored[child] = newcost
                frontier.push(ANode(state: child, parent: currentANode, cost: newcost, heuristic: heuristicFn(child)))
            }
        }
    }
    
    return nil
}




/*
 class ANode<T: Hashable>: Comparable, Hashable {
     let state: T
     let parent: ANode?
     let cost: Float
     let heuristic: Float
     init(state: T, parent: ANode?, cost: Float, heuristic: Float) {
         self.state = state
         self.parent = parent
         self.cost = cost
         self.heuristic = heuristic
     }
     
     func hash(into hasher: inout Hasher) {
         hasher.combine(state)
         hasher.combine(parent)
         hasher.combine(cost)
         hasher.combine(heuristic)
     }
 }

 func < <T>(lhs: ANode<T>, rhs: ANode<T>) -> Bool {
     return (lhs.cost + lhs.heuristic) < (rhs.cost + rhs.heuristic)
 }

 func == <T>(lhs: ANode<T>, rhs: ANode<T>) -> Bool {
     return lhs === rhs
 }

 /// Formulate a result path as an array from a goal ANode found in an astar search
 ///
 /// - parameter startANode: The goal ANode found from an astar search.
 /// - returns: An array containing the states to get from the start to the goal.
 func backtrack<T>(_ goalANode: ANode<T>) -> [T] {
     var sol: [T] = []
     var ANode = goalANode
     
     while (ANode.parent != nil) {
         sol.append(ANode.state)
         ANode = ANode.parent!
     }
     
     sol.append(ANode.state)
     
     return sol
 }

 /// Find the shortest path from a start state to a goal state.
 ///
 /// - parameter initialState: The state that we are starting from.
 /// - parameter goalTestFn: A function that determines whether a state is the goal state.
 /// - parameter successorFn: A function that finds the next states from a state.
 /// - parameter heuristicFn: A function that makes an underestimate of distance from a state to the goal.
 /// - returns: A path from the start state to a goal state as an array.
 func astar<T: Hashable>(_ initialState: T, goalTestFn: (T) -> Bool, successorFn: (T) -> [T], heuristicFn: (T) -> Float) -> [T]? {
     var frontier = PriorityQueue(ascending: true, startingValues: [ANode(state: initialState, parent: nil, cost: 0, heuristic: heuristicFn(initialState))])
     var explored = Dictionary<T, Float>()
     explored[initialState] = 0
     var ANodesSearched: Int = 0
     
     while let currentANode = frontier.pop() {
         ANodesSearched += 1
           // we know if there are still items, we can pop one
         let currentState = currentANode.state
         
         if goalTestFn(currentState) {
             print("Searched \(ANodesSearched) ANodes.")
             return backtrack(currentANode)
         }
         
         for child in successorFn(currentState) {
             let newcost = currentANode.cost + 1  //1 assumes a grid, there should be a cost function
             if (explored[child] == nil) || (explored[child]! > newcost) {
                 explored[child] = newcost
                 frontier.push(ANode(state: child, parent: currentANode, cost: newcost, heuristic: heuristicFn(child)))
             }
         }
     }
     
     return nil
 }
 */
