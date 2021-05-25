//
//  Command.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-05-04.
//

import Foundation
import SwiftUI


class Command {
    let direction: String
    let rotation: Int
    let distance: Float
    
    
    init(direction: String, rotation: Int) {
        self.direction = direction
        self.rotation = rotation
        self.distance = 0
    }
    
    init(direction: String, distance: Float) {
        
        if direction == "TOP RIGHT" || direction == "TOP LEFT" || direction == "BOTTOM RIGHT" || direction == "BOTTOM LEFT" {
            self.direction = direction
            self.distance = distance * sqrt(2)
            self.rotation = 0                   //MARK:  <-- This line may cause problems? If problems arise set rotation to nil or something like 1
        } else {
            self.direction = direction
            self.distance = distance
            self.rotation = 0
        }
    }
    
    func toString() {
        print("\(direction), distance: \(distance), rotation: \(rotation)")
    }
}


struct MQTTCommand {
    let type: String
    let value: Float
    
    
    func toString() {
        if type == "MOVE" {
            print("Car moved \(value)")
        }
        else {
            print("Car rotated to \(value)")
        }
    }
    
}


func generateCommands(initialState: Command, path: [Node]) -> [MQTTCommand] {
    var commands: [Command] = []
    var prevCommand: Command = initialState
    
    let STEP: CGFloat = 9.75
    
    for i in 0..<(path.count - 1) {
        
        let currentX = path[i].x
        let currentY = path[i].y
        
        let nextX = path[i+1].x
        let nextY = path[i+1].y
        
        
        
        var fdirection = ""
        var frotation = 0
        
        if nextX == currentX + STEP && nextY == currentY {
            // RIGHT
            //print("0")
            fdirection = "RIGHT"
            frotation = 0
            
        } else if nextX == currentX + STEP && nextY == currentY - STEP {
            // TOP RIGHT
            //print("315")
            fdirection = "TOP RIGHT"
            frotation = 315
            
        } else if nextX == currentX && nextY == currentY - STEP {
            // TOP
            //print("270")
            fdirection = "TOP"
            frotation = 270
            
        } else if nextX == currentX - STEP && nextY == currentY - STEP {
            // TOP LEFT
            //print("225")
            fdirection = "TOP LEFT"
            frotation = 225
            
        } else if nextX == currentX - STEP && nextY == currentY {
            // LEFT
            //print("180")
            fdirection = "LEFT"
            frotation = 180
            
        } else if nextX == currentX - STEP && nextY == currentY + STEP {
            // BOTTOM LEFT
            //print("135")
            fdirection = "BOTTOM LEFT"
            frotation = 135
            
        }  else if nextX == currentX && nextY == currentY + STEP {
            // BOTTOM
            //print("90")
            fdirection = "BOTTOM"
            frotation = 90
            
        } else if nextX == currentX + STEP && nextY == currentY + STEP {
            // BOTTOM RIGHT
            //print("45")
            fdirection = "BOTTOM RIGHT"
            frotation = 45
            
        } else {
            print("NO DIRECTION")
        }
        
        if prevCommand.direction == fdirection {
            commands.append(Command(direction: fdirection, distance: 9.75))
        } else {
            commands.append(Command(direction: fdirection, rotation: frotation))
            commands.append(Command(direction: fdirection, distance: 9.75))
        }
        
        prevCommand = Command(direction: fdirection, distance: 9.75)
        
        
    }
    
    return simplifyCommands(commands: commands)
}

private func simplifyCommands(commands: [Command]) -> [MQTTCommand] {
    
    var value: Float = 0
    var mqttCommands: [MQTTCommand] = []
    
    for i in 0..<(commands.count - 1) {
        if commands[i].distance == 0 {
            mqttCommands.append(MQTTCommand(type: "ROTATION", value: Float(commands[i].rotation)))
        }
        else if commands[i].direction == commands[i+1].direction {
            value = value + commands[i].distance
        }
        else {
            value = value + commands[i].distance
            mqttCommands.append(MQTTCommand(type: "MOVE", value: value))
            value = 0
        }
        
    }
    
    if commands[commands.count-1].distance == 0 {
        mqttCommands.append(MQTTCommand(type: "ROTATION", value: Float(commands[commands.count-1].rotation)))
    }
    else {
        value = value + commands[commands.count-1].distance
        mqttCommands.append(MQTTCommand(type: "MOVE", value: value))
        value = 0
    }
    
    for j in 0..<mqttCommands.count {
        mqttCommands[j].toString()
    }
    
    return mqttCommands
    
}
