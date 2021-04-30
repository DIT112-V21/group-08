//
//  ContentView.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-19.
//

import SwiftUI
import CocoaMQTT

struct ContentViewOld : View {

    
    // START : 22,405
    // To tree : 44.163
    // Total : 48,381
    
    // Width is about 48,381 - 22,405 = 25,976
    
    // So offset is 390 (UI.width) / 2600 (rounded up) = 0.15 (this is pretty good)
    
    
    
    //@State var targetPos: CGPoint = CGPoint(x: 0.0, y: 0.0)

    
    // map width = 536cm + 1132cm
    // UIScreen.main.bounds.width / 1132 = 0.34452296819787986 <- WRONG
    // UIScreen.main.bounds.width = 390
    // So 1 cm in SMCE is
    
    @State var offsetX: CGFloat = 86 - UIScreen.main.bounds.width / 2
    @State var offsetY: CGFloat = 575 - UIScreen.main.bounds.height / 2
    @State var newPoint: CGPoint = CGPoint(x: 86, y: 555)
    
    @State var oldOffsetX: CGFloat = 86 - UIScreen.main.bounds.width / 2
    @State var oldOffsetY: CGFloat = 575 - UIScreen.main.bounds.height / 2
    @State var oldPoint: CGPoint = CGPoint(x: 86, y: 515)

    //@State var rotation: Double = 90
    
    @Binding var offsetmqtt: Double
    
    @Binding var rotationmqtt: Double
    
    var body: some View {
        ZStack {
            Image("map")
                .resizable()
                .offset(y: -15)
                .gesture(
                    DragGesture(minimumDistance: 0, coordinateSpace: .global)
                        .onChanged { value in
                            //self.position = value.location
                            print(value.location)
                            updatePos(value.location)
                        }
                        .onEnded { _ in
                           
                        }
                )
            
            Circle()
                .frame(width: 15, height: 15)
                //.rotationEffect(.degrees(rotation))
                .offset(x: offsetX + (CGFloat((offsetmqtt * (rotationmqtt))) * 0.15), y: offsetY + (CGFloat((offsetmqtt * (1 - rotationmqtt)))))
                .animation(Animation.linear(duration: 1))
            
            /* WORKING BUT IDK IF IT LOOKS GOOD
            Path { path in
                path.move(to: CGPoint(x: oldPoint.x, y: oldPoint.y - 40))
                path.addLine(to: CGPoint(x: newPoint.x, y: newPoint.y - 40))
            }
            .stroke()*/
            
            /*HStack { Testing circle
                Spacer()
                VStack {
                    Spacer()
                    Circle()
                        .frame(width: 40, height: 40)
                        .onTapGesture {
                            
                    }
                }
            }*/
                
        }
    }
    
    // TODO: Distribute offset from ArduinoMQTT by looking at gyroscope angle (eg 45 degrees 50-50 split on x and y)
    
    func updatePos(_ point: CGPoint){
        oldPoint = newPoint
        oldOffsetX = offsetX
        oldOffsetY = offsetY
        
        newPoint = point
        offsetX = point.x - UIScreen.main.bounds.width / 2
        offsetY = point.y - UIScreen.main.bounds.height / 2
        
        //print("Calc \(UIScreen.main.bounds.width / (1132))")
        print("WIDTH \(UIScreen.main.bounds.width)")
    }
    
    /*
    func rotate(_ point: CGPoint) {
        let adjacent = abs(oldOffsetX - point.x)
        let opposite = abs(oldOffsetY - point.y)
        
        let div = opposite / adjacent
        
        print("Adding \(100 * Double(atan(div))) degrees of rotation")
        
        rotation += 100 * Double(atan(div))
        print("Rotation: \(rotation)")
    }*/
    
    
}


/*
 Width: 374
 */




struct ContentViewOld_Previews: PreviewProvider {
    static var previews: some View {
        ContentViewOld(offsetmqtt: .constant(0), rotationmqtt: .constant(0))
            .preferredColorScheme(.dark)
    }
}

