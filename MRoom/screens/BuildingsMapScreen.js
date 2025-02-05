import React from "react";
import { StyleSheet, View } from "react-native";
import MapView, { Marker } from "react-native-maps";

const BuildingsMapScreen = () => {
  // define a region to display initially (e.g., focus on the first building)
  const initialRegion = {
    latitude: 40.7128, // choose a default lat
    longitude: -74.006, // choose a default lon
    latitudeDelta: 0.05,
    longitudeDelta: 0.05,
  };

  const buildings = [
    {
      id: 1,
      name: "Building A",
      address: "123 Main St, Anytown, USA",
      latitude: 40.7128,
      longitude: -74.006,
    },
    {
      id: 2,
      name: "Building B",
      address: "456 Oak Ave, Somecity, USA",
      latitude: 34.0522,
      longitude: -118.2437,
    },
  ];

  return (
    <View style={styles.container}>
      <MapView style={styles.map} initialRegion={initialRegion}>
        {buildings.map((building) => (
          <Marker
            key={building.id}
            coordinate={{
              latitude: building.latitude,
              longitude: building.longitude,
            }}
            title={building.name}
            description={building.address}
            // (Optional) Add custom marker or info window styling
            // image={require('path/to/custom-marker.png')}
            // onCalloutPress={() => // navigate or open details}
          />
        ))}
      </MapView>
    </View>
  );
};

export default BuildingsMapScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    ...StyleSheet.absoluteFillObject,
  },
});
