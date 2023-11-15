//
//  BuildingRow.swift
//  M-Room
//
//  Created by Anthony Remick on 5/14/23.
//

import SwiftUI

struct BuildingRow: View {
    @EnvironmentObject var modelData: ModelData
    
    var image: Image{Image("Ross")}
    //var w: CGFloat{200}
    //var h: CGFloat{100}
    
    var body: some View {
        HStack{
            VStack{
                Text(modelData.Rooms[0].CampusDescr)
                //Text(modelData.Rooms[0].name)
                Text("Available Rooms: 50")
            }
        }
        .frame(width: 100, height: 200)
        .background(image)
        .cornerRadius(100)
    }
}

struct BuildingRow_Previews: PreviewProvider {
    static var previews: some View {
        BuildingRow()
            .environmentObject(ModelData())
    }
}
