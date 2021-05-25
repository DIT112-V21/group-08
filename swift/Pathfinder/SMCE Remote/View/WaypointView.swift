//
//  WaypointView.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-28.
//

import SwiftUI

struct WaypointView: View {
    
    let waypoints: [Waypoint] = [
    
        Waypoint(x: 321.75, y: 209.0),
        Waypoint(x: 243.75, y: 501.5),
        Waypoint(x: 243.75, y: 677.0),
        Waypoint(x: 126.75, y: 657.5),
        Waypoint(x: 39.0, y: 521.0),
        Waypoint(x: 117.0, y: 374.75),
        Waypoint(x: 39.0, y: 189.5),
        Waypoint(x: 175.5, y: 179.75),
        Waypoint(x: 87.75, y: 589.25)
       
    
    ]
    
    
    var body: some View {
        ZStack {
            /*
            Image("map")
                .resizable()
                .offset(y: -13)*/
            
            Path { path in
                path.move(to: CGPoint(x: 39.0, y: 521.0))
                path.addLine(to: CGPoint(x: 39.0, y: 189.5))
                path.addLine(to: CGPoint(x: 175.5, y: 179.75))
                path.addLine(to: CGPoint(x: 285.5, y: 179.75)) // MID POINT
                path.addLine(to: CGPoint(x: 321.75, y: 209.0))
                path.addLine(to: CGPoint(x: 243.75, y: 501.5))
                path.addLine(to: CGPoint(x: 235.75, y: 601.5)) // MID POINT
                path.addLine(to: CGPoint(x: 243.75, y: 677.0))
                path.move(to: CGPoint(x: 126.75, y: 657.5))
                path.addLine(to: CGPoint(x: 87.75, y: 589.25))
                path.addLine(to: CGPoint(x: 243.75, y: 501.5))
                path.move(to: CGPoint(x: 87.75, y: 589.25))
                path.addLine(to: CGPoint(x: 39.0, y: 521.0))
                path.addLine(to: CGPoint(x: 117.0, y: 374.75))
                path.addLine(to: CGPoint(x: 175.5, y: 179.75))
            }
            .stroke(color(30, 30, 30), lineWidth: 5)
            //.offset(y: -50)
            
            ForEach(waypoints, id: \.id) { waypoint in
                SingleWaypointView(x: waypoint.x, y: waypoint.y)
            }//.offset(y: -50)
            
            
        }
        
    }
}

struct SingleWaypointView: View {
    
    let x: CGFloat
    let y: CGFloat
    
    let size: CGFloat = 30
    
    @State var size1: CGFloat = 30
    
    @State var opacity1 = 1.0

    
    var body: some View {
        ZStack {
            
            Circle()
                .strokeBorder(Color.green, lineWidth: 2)
                .frame(width: size1, height:size1)
                .opacity(0.8)
                .opacity(opacity1)
            
            Circle()
                .foregroundColor(color(30, 30, 30))
                .frame(width: size, height: size)
                
            
            Circle()
                .strokeBorder(Color.green, lineWidth: 3)
                .frame(width: size, height:size)
  
            Circle()
                .foregroundColor(.green)
                .frame(width: 0.3 * size, height: 0.3 * size)
        }
        .onTapGesture {
            animateCircles()
        }
        .position(x: x, y: y)
    }
    
    func animateCircles() {
        
        print(x, y)
        
        withAnimation(Animation.linear(duration: 2).repeatForever(autoreverses: false)) {
            size1 = size1 + 30
            opacity1 = 0
        }
        /*
        DispatchQueue.main.asyncAfter(deadline: .now() + 7.5) {
            size1 = size
            opacity1 = 1
        }*/
        
    }
    
}

/*
 DispatchQueue.main.asyncAfter(deadline: .now() + 7.5) {
             hasTimeElapsed = true
         }
 */


struct WaypointView_Previews: PreviewProvider {
    static var previews: some View {
        WaypointView().preferredColorScheme(.dark)
    }
}
