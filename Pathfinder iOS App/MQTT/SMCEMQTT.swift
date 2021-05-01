//
//  SMCEMQTT.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-21.
//

import Foundation
import CocoaMQTT
import SwiftUI


struct SMCEMQTT {
    
    let mqttClient = CocoaMQTT(clientID: "testerman", host: "localhost", port: 1883)
    var connected: Bool = false
    
    /*
    mutating func smceConnect() {
        mqttClient.username="user"
        mqttClient.password="password"
        mqttClient.keepAlive=60
        connected = mqttClient.connect()
    }*/
    
    init() {
        mqttClient.username="user"
        mqttClient.password="password"
        mqttClient.keepAlive=60
        connected = mqttClient.connect()
    }
    
    func customPublish(topic: String, message: String) {
        if connected {
            mqttClient.publish(topic, withString: message)
        } else {
            print("Could not publish message: \(message) to topic: \(topic)")
        }
    }
    
    func goForward() {
        mqttClient.publish("/", withString: "f")
    }
    func goBack() {
        mqttClient.publish("/", withString: "b")
    }
    func goLeft() {
        mqttClient.publish("/", withString: "l")
    }
    func goRight() {
        mqttClient.publish("/", withString: "r")
    }
    func stopCar() {
        mqttClient.publish("/", withString: "s")
    }
    
    func goForward(distance: Double) {
        mqttClient.publish("/", withString: "\(distance)")
    }
    
    func goLeft90() {
        mqttClient.publish("/", withString: "l90")
    }
    func goRight90() {
        mqttClient.publish("/", withString: "r90")
    }
    
    func waitStop() {
        mqttClient.publish("/", withString: "w")
    }
    
    
}
