//
//  Funcs.swift
//  SMCE Remote
//
//  Created by Adam Telles on 2021-04-19.
//

import Foundation
import SwiftUI

func gradient(colors: [Color], start: UnitPoint, stop: UnitPoint) -> LinearGradient {
    return LinearGradient(gradient: Gradient(colors: colors), startPoint: start, endPoint: stop)
}

// Returns a color based on RGB values
func color(_ r: Double, _ g: Double, _ b:Double) -> Color {
    return Color(red: r / 255, green: g / 255, blue: b / 255)
}

extension Double {
    func removeZerosFromEnd() -> String {
        let formatter = NumberFormatter()
        let number = NSNumber(value: self)
        formatter.minimumFractionDigits = 0
        formatter.maximumFractionDigits = 16 //maximum digits in Double after dot (maximum precision)
        return String(formatter.string(from: number) ?? "")
    }
}


// MQTT Commands

// Start server with terminal: /usr/local/sbin/mosquitto

// Start sketch

// In terminal write: mosquitto_pub -h 127.0.0.1 -t / -m "MESSAGE HERE"
// and it will show up in serial.

// To subscribe in terminal write: mosquitto_sub -h 127.0.0.1 -t /
