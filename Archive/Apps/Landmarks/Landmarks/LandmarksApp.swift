//
//  LandmarksApp.swift
//  Landmarks
//
//  Created by Anthony Remick on 5/6/23.
//

import SwiftUI

@main
struct LandmarksApp: App {
    @StateObject private var modelData = ModelData()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(modelData)
        }
    }
}
