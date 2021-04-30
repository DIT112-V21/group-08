//
//  GridView.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-24.
//
/*
import SwiftUI

struct GridView: View {
    
    // Each step is 9.75
    let rects: [CGRect] = NoWalk().getRect()
    
    var body: some View {
        let columns = Array(repeating: GridItem(.flexible(minimum: 4, maximum: 10), spacing: 0), count: 40)

        
        ZStack {
            LazyVGrid(columns: columns, spacing: 0) {
                
                ForEach(1...2440, id: \.self) { item in
                    
                    InnerView(rects: rects)
                        .aspectRatio(1, contentMode: .fit)
                        .border(Color.white.opacity(0.1))
                        
                    
                    
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .center)
            .aspectRatio(1, contentMode: .fit)
            
            Text("Test").onTapGesture {
                
            }
            
        }
        
    }
}

struct InnerView: View {
    
    @State var color = Color.white.opacity(0.05)
    let rects: [CGRect]
    @State var walkable: Bool? = nil
    @State var position: CGRect? = nil
    
    var body: some View {
        
        GeometryReader { geo in
            Rectangle()
                .foregroundColor(rects.contains(geo.frame(in: .global)) ? Color.red.opacity(0.4) : color)
                .onTapGesture {
                    
                    print(geo.frame(in: .global))
                    
                    color = Color.red.opacity(0.4)
                    
                }
                .onAppear() {
                    walkable = rects.contains(geo.frame(in: .global))
                    position = geo.frame(in: .global)
                }
        }
        
    }   
}
/*
struct GridView_Previews: PreviewProvider {
    static var previews: some View {
        GridView().preferredColorScheme(.dark)
    }
}
*/
*/
