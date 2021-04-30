//
//  ContentView.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-21.
//

import SwiftUI

struct ContentViewNOTUSED: View {
    
    let mqtt = SMCEMQTT()
    
    @State var offsetX: CGFloat = 86 - UIScreen.main.bounds.width / 2
    @State var offsetY: CGFloat = 575 - UIScreen.main.bounds.height / 2
    
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
                            //updatePos(value.location)
                            getAngle(newPos: value.location)
                        }
                        .onEnded { _ in
                           
                        })
            
            //GridView()
            //GridView()
            
            
        }
    }
    
    func updatePos(_ point: CGPoint){
        
        mqtt.goForward(distance: (Double((point.x - UIScreen.main.bounds.width / 2) - offsetX)) / 0.15)
        offsetX = (point.x - UIScreen.main.bounds.width / 2)
        
        mqtt.waitStop()
        
        mqtt.goLeft90()
        
        mqtt.waitStop()
        
        mqtt.goForward(distance: abs(Double((point.y - UIScreen.main.bounds.height / 2) - offsetY)) / 0.15)
        offsetY = (point.y - UIScreen.main.bounds.width / 2)

    }
    
    
    func getAngle(newPos: CGPoint){
        let a = abs(offsetY - newPos.y)
        let b = abs(offsetX - newPos.x)
        
        let angle = atan(a / b)
        
        print("Angle: \(angle)")
    }
    
    
}

struct ContentViewNOTUSED_Previews: PreviewProvider {
    static var previews: some View {
        ContentViewNOTUSED()
    }
}
