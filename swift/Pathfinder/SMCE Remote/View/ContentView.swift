//
//  MapView.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-27.
//

import SwiftUI
import SwiftUIVisualEffects

struct ContentView: View {
    
    @State var begin = false
    @State var showGrid = false
    @State var showWaypoint = false
    
    
    
    var body: some View {
        ZStack {
            
            Image("map")
                .resizable()
                .offset(y: -13)
            
            
            Rectangle()
                .foregroundColor(.black)
                .opacity(0.1)
                .blurEffect()
                .blurEffectStyle(.systemThinMaterialDark)
                .edgesIgnoringSafeArea(.all)
                .opacity(begin ? 0 : 1)
                .animation(Animation.easeOut(duration: 2))
            
            
            
            VStack {
                Image("smceLogo")
                    .resizable()
                    .scaledToFit()
                    .frame(width: UIScreen.main.bounds.width - 100)
                    .opacity(begin ? 0 : 1)
                    .animation(Animation.easeOut(duration: 1))
                
                if begin {
                    Spacer()
                }
                
                
                if !showWaypoint {
                    Button(action: {
                        begin.toggle()
                        showGrid.toggle()
                    }) {
                        ZStack{
                            Rectangle()
                                .foregroundColor(color(30, 30, 30))
                                .frame(width: 160, height: 50)
                                .cornerRadius(25)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 25)
                                        .strokeBorder(Color.gray.opacity(0.8), lineWidth: 1)
                                        .frame(width: 160, height: 50))
                            
                            
                            Text(begin ? "BACK" : "GRID")
                                .foregroundColor(.white)
                                .font(.system(size: 20, weight: .semibold))
                        }
                    }
                    .animation(.spring())
                }
                
                
                if !showGrid {
                    Button(action: {
                        begin.toggle()
                        showWaypoint.toggle()
                    }) {
                        ZStack{
                            Rectangle()
                                .foregroundColor(color(30, 30, 30))
                                .frame(width: 160, height: 50)
                                .cornerRadius(25)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 25)
                                        .strokeBorder(Color.gray.opacity(0.8), lineWidth: 1)
                                        .frame(width: 160, height: 50))
                            
                            
                            Text(begin ? "BACK" : "WAYPOINTS")
                                .foregroundColor(.white)
                                .font(.system(size: 20, weight: .semibold))
                        }
                    }
                    .animation(.spring())
                    .opacity(0)
                }
                
                
                
                if !begin {
                    Spacer()
                }
                
            }
            .padding(.top, UIScreen.main.bounds.width / 3)
            
            
            if showGrid {
                GridView()
            }
            
            if showWaypoint {
                WaypointView()
                    .offset(y: -50)
            }
            
            
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
