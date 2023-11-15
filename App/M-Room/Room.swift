//
//  Room.swift
//  M-Room
//
//  Created by Anthony Remick on 5/9/23.
//

import Foundation
import SwiftUI
import CoreLocation

struct Room: Hashable, Codable{
    
    var FacilityID: String
    var BuildingID: Int
    var CampusDescr: String
    var CampusCd: Int
    
    var ChrstcDescr254: String
    var Chrstc: Int
    var RmRecNbr: Int
    var ChrstcDescrShort: String
    var ChrstcDescr: String
    
    var RmInstSeatCnt: Int
    var BldDescr50: String
    var RmTyp: Int
    
    
    struct Meeting: Hashable, Codable{
        var MtgStartTime: String
        var MtgEndTime: String
        var MtgDate: String
        var MtgDescr: String
        var CampusMtgType: String
        var ContactMin: Int
    }
     
}
