import React, { useState, useEffect } from "react";
import { View, StyleSheet, Dimensions, Alert } from "react-native";
import MapView, { Marker } from "react-native-maps";
import * as Location from "expo-location";

const BuildingsMapScreen = () => {
  const [location, setLocation] = useState(null);
  const [buildings, setBuildings] = useState([]); // Will be populated from your API

  // Dummy building - Michigan Union
  const dummyBuilding = {
    id: 1,
    name: "Michigan Union",
    coordinate: {
      latitude: 42.274475,
      longitude: -83.742195,
    },
    description: "Student Union Building",
  };

  useEffect(() => {
    let locationSubscription;

    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        Alert.alert(
          "Permission denied",
          "Location permission is required to center the map."
        );
        return;
      }

      try {
        // Get initial location
        let currentLocation = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.High,
          maximumAge: 10000,
        });
        setLocation(currentLocation);

        // Subscribe to location updates
        locationSubscription = await Location.watchPositionAsync(
          {
            accuracy: Location.Accuracy.High,
            timeInterval: 10000,
            distanceInterval: 10,
          },
          (newLocation) => {
            setLocation(newLocation);
          }
        );
      } catch (error) {
        Alert.alert("Error", "Could not fetch location.");
      }
    })();

    // Cleanup subscription on unmount
    return () => {
      if (locationSubscription) {
        locationSubscription.remove();
      }
    };
  }, []);

  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        showsUserLocation={true}
        followsUserLocation={true}
        showsMyLocationButton={true}
        initialRegion={
          location
            ? {
                latitude: location.coords.latitude,
                longitude: location.coords.longitude,
                latitudeDelta: 0.01,
                longitudeDelta: 0.01,
              }
            : {
                // Default to Michigan Union area if location not available
                latitude: 42.274475,
                longitude: -83.742195,
                latitudeDelta: 0.01,
                longitudeDelta: 0.01,
              }
        }
      >
        {/* Show dummy building */}
        <Marker
          coordinate={dummyBuilding.coordinate}
          title={dummyBuilding.name}
          description={dummyBuilding.description}
        />
      </MapView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  map: {
    width: Dimensions.get("window").width,
    height: Dimensions.get("window").height,
  },
});

export default BuildingsMapScreen;
