#!/bin/bash

curl -X POST \
  -H "Content-Type: application/json" \
  -d '[
    {
      "BldDescrShort": "Building Name",
      "shortname": "BLDG",
      "FacilityID": "BLDG101",
      "Meetings": [
        {
          "MtgDate": "06-02-2024",
          "MtgStartTime": "09:30 AM",
          "MtgEndTime": "06:00 PM"
        }
      ]
    }
  ]' \
  https://mroom-api-c7aef75a74b0.herokuapp.com/import_data 