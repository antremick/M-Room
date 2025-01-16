//
//  ListGetPostman.swift
//  M-Room
//
//  Created by Anthony Remick on 5/16/23.
//

import Foundation

var AAPIGEE_BASE_URL = "https://gw.api.it.umich.edu"
var lg_request = URLRequest(url: URL(string: "\(AAPIGEE_BASE_URL)/um/aa/ClassroomList/Classrooms")!,timeoutInterval: Double.infinity)

func lg_process(){
    print("Function Ran")
    lg_request.addValue("{{Authorization}}", forHTTPHeaderField: "Authorization")
    lg_request.addValue("application/json", forHTTPHeaderField: "Accept")

    lg_request.httpMethod = "GET"
    let task = URLSession.shared.dataTask(with: lg_request) { data, response, error in
      guard let data = data else {
        print(String(describing: error))
        return
      }
      print(String(data: data, encoding: .utf8)!)
    }

    task.resume()
}

//lg_process()
