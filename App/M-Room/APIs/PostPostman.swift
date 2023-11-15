//
//  PostPostman.swift
//  M-Room
//
//  Created by Anthony Remick on 5/16/23.
//

import Foundation

var APIGEE_BASE_URL = "https://gw.api.it.umich.edu"

var request = URLRequest(url: URL(string: "\(APIGEE_BASE_URL)/um/oauth2/token?grant_type=client_credentials&scope=classrooms")!,timeoutInterval: Double.infinity)

func process(){
    print("Function Ran")
    request.addValue("Basic e3tBUElHRUVfQVBQX0tFWX19Ont7QVBJR0VFX0FQUF9TRUNSRVR9fQ==", forHTTPHeaderField: "Authorization")

    request.httpMethod = "POST"

    let task = URLSession.shared.dataTask(with: request) { data, response, error in
      guard let data = data else {
        print(String(describing: error))
        return
      }
      print(String(data: data, encoding: .utf8)!)
      print(data)
        print("here")
    }
    
    
    print("here1")
    task.resume()
    print("here2")
}

//process()
