//
//  MQTTView.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-19.
//

import SwiftUI
import CocoaMQTT

struct MQTTViewOld: View {
    
    
    // MQTT Commands

    // Start server with terminal: /usr/local/sbin/mosquitto

    // Start sketch

    // In terminal write: mosquitto_pub -h 127.0.0.1 -t / -m "MESSAGE HERE"
    // and it will show up in serial.

    // To subscribe in terminal write: mosquitto_sub -h 127.0.0.1 -t /

    
    
    let mqttClientDistance = CocoaMQTT(clientID: "testerman", host: "localhost", port: 1883)
    
    let mqttClientRotation = CocoaMQTT(clientID: "testerman2", host: "localhost", port: 1883)
    
    @State private var connected:Bool = false
    @State private var subbed:Bool = false
    
    @State var offset: Double = 0.0
    @State var rotation: Double = 0.0
    
    var body: some View {
        ZStack {
            
            
            if connected {
                ContentViewOld(offsetmqtt: $offset, rotationmqtt: $rotation)
            }
            
            
            
            
            VStack {
                ZStack {
                    
                    Button(action: {
                        mqttClientDistance.subscribe("/distance")
                        mqttClientDistance.didReceiveMessage = { mqtt, message, id in
                            print("Message received in topic \(message.topic) with payload \(message.string!)")
                            
                                offset = Double(message.string!)!
                            
                        }
                        
                        mqttClientRotation.subscribe("/rotation")
                        mqttClientRotation.didReceiveMessage = { mqtt, message, id in
                            print("Message received in topic \(message.topic) with payload \(message.string!)")
                            
                            let r = Double(message.string!)!
                            rotation = ((r + 180).truncatingRemainder(dividingBy: 360) / 360)
                            
                            print("rotation: \(rotation)")
                            
                                //offsetx = Double(message.string!)!
                            
                        }
                        
                        subbed.toggle()
                    }, label: {
                        if !subbed {
                        Text("Subscribe")
                            .foregroundColor(.white)
                            .font(.system(size: 24, weight: .semibold))
                            .padding()
                            .background(RoundedRectangle(cornerRadius: 25)
                                            .foregroundColor(connected ? .green : color(30, 30, 30))
                                            .overlay(RoundedRectangle(cornerRadius: 25)
                                                            .strokeBorder(Color.gray.opacity(0.3), lineWidth: 1)))
                        }/* else {
                            Text("Connected")
                                .foregroundColor(.white)
                                .font(.system(size: 24, weight: .semibold))
                                .opacity(0.3)
                        }*/
                    })
                    .opacity(!connected ? 0 : 1)
                    
                    
                    Button(action: {
                        if !connected { // Idk?
                            mqttClientDistance.username="user"
                            mqttClientDistance.password="password"
                            mqttClientDistance.keepAlive=60
                            
                            mqttClientRotation.username="user"
                            mqttClientRotation.password="password"
                            mqttClientRotation.keepAlive=60
                            
                            if mqttClientDistance.connect() && mqttClientRotation.connect() {
                                withAnimation(.linear){
                                    connected.toggle()
                                }
                            }
                        }
                        
                    }, label: {
                        if !connected {
                        Text("Connect")
                            .foregroundColor(.white)
                            .font(.system(size: 24, weight: .semibold))
                            .padding()
                            .background(RoundedRectangle(cornerRadius: 25)
                                            .foregroundColor(connected ? .green : color(30, 30, 30))
                                            .overlay(RoundedRectangle(cornerRadius: 25)
                                                            .strokeBorder(Color.gray.opacity(0.3), lineWidth: 1)))
                        }/* else {
                            Text("Connected")
                                .foregroundColor(.white)
                                .font(.system(size: 24, weight: .semibold))
                                .opacity(0.3)
                        }*/
                    })
                    .opacity(connected ? 0 : 1)
                    
                 
                    
                    
                }
                
                
                Button(action: {
                    mqttClientDistance.publish("/", withString: "f")
                }, label: {
                    Text("Go Forward")
                        .foregroundColor(.white)
                        .font(.system(size: 24, weight: .semibold))
                })
                
                Button(action: {
                    mqttClientDistance.publish("/", withString: "s")
                }, label: {
                    Text("Stop")
                        .foregroundColor(.white)
                        .font(.system(size: 24, weight: .semibold))
                })
                
                Button(action: {
                    mqttClientDistance.publish("/", withString: "b")
                }, label: {
                    Text("Go back")
                        .foregroundColor(.white)
                        .font(.system(size: 24, weight: .semibold))
                })
                
                Button(action: {
                    mqttClientDistance.publish("/", withString: "l")
                }, label: {
                    Text("Left")
                        .foregroundColor(.white)
                        .font(.system(size: 24, weight: .semibold))
                })
                
                Button(action: {
                    mqttClientDistance.publish("/", withString: "r")
                }, label: {
                    Text("Right")
                        .foregroundColor(.white)
                        .font(.system(size: 24, weight: .semibold))
                })
                
                /*Button("Hold") {
                    mqttClient.subscribe("/")
                    mqttClient.didReceiveMessage = { mqtt, message, id in
                        print("Message received in topic \(message.topic) with payload \(message.string!)")
                        if message.string != "f" && message.string != "s"{
                            offsetx = Double(message.string!)!
                        }
                    }
                }*/
                
            }

            
        }
    }
}

struct MQTTViewOld_Previews: PreviewProvider {
    static var previews: some View {
        MQTTViewOld().preferredColorScheme(.dark)
    }
}
