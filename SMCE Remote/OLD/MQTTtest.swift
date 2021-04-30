//
//  MQTTtest.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-19.
//

import MapKit
import SwiftUI
import CocoaMQTT


struct Drone {
    var coordinate: CLLocationCoordinate2D
    var distance: UInt8
    var direction: UInt8
}

//
struct MQTTtest: View {
    @State public var region = MKCoordinateRegion(center: CLLocationCoordinate2D(latitude: 34.0000, longitude: -86.0000), span: MKCoordinateSpan(latitudeDelta: 0.001, longitudeDelta: 0.001))
    
    @State private var trackingMode = MapUserTrackingMode.follow
    
    @State private var safety = false
    
    @State private var showingSheet = false
    
    @State public var Connection:Bool = false
    
    var Bee: Drone = Drone(coordinate: .init(latitude: 34.0010, longitude: -86.0010), distance: 10, direction: 180)
    
    
    let mqttClient = CocoaMQTT(clientID: "testerman", host: "localhost", port: 1883)
    
    var body: some View {
        
        
        VStack {
            HStack{
                Text("Beer Bee")
                
                Spacer()
                Button(action: {
                    self.mqttClient.username="user"
                    self.mqttClient.password="password"
                    self.mqttClient.keepAlive=60
                    self.mqttClient.connect()
                    self.Connection.toggle()
                    
                    }, label: {
                        Text(Connection ? "Disconnect":"Connect")
                    })
            }

            Spacer()
            // Content Here
            
            
            HStack(alignment: .center) {
                Toggle(isOn: $safety) {
                    //action here
                }
                .toggleStyle(SwitchToggleStyle(tint: Color.red))

                Button("Main") {
                    self.mqttClient.publish("/", withString: "hello world!")
                }
                Spacer()
            }
            
            Button("Hold") {
                self.mqttClient.subscribe("/")
                self.mqttClient.didReceiveMessage = { mqtt, message, id in
                    print("Message received in topic \(message.topic) with payload \(message.string!)")
                }
            }
            
            
        }
        
       
    }
}



struct MQTTtest_Previews: PreviewProvider {
    static var previews: some View {
        MQTTtest()
            .preferredColorScheme(.dark)
    }
}
