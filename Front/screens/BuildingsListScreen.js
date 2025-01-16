// File: screens/BuildingsListScreen.js
import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
} from "react-native";

// Replace with the URL to your Flask endpoint for building data
const BUILDINGS_URL = "http://127.0.0.1:5000/buildings";
// Or maybe something like 'https://myserver.com/buildings'

export default function BuildingsListScreen({ navigation }) {
  const [buildings, setBuildings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBuildings();
  }, []);

  async function fetchBuildings() {
    try {
      let response = await fetch(BUILDINGS_URL);
      let json = await response.json();
      setBuildings(json); // We assume your API returns a list of buildings
    } catch (error) {
      console.error("Error fetching buildings:", error);
    } finally {
      setLoading(false);
    }
  }

  function onBuildingPress(building) {
    // Navigate to RoomsListScreen and pass building info
    navigation.navigate("RoomsList", { building });
  }

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <FlatList
      data={buildings}
      keyExtractor={(item) => item.id.toString()}
      renderItem={({ item }) => (
        <TouchableOpacity
          onPress={() => onBuildingPress(item)}
          style={{ padding: 20, borderBottomWidth: 1, borderColor: "#ccc" }}
        >
          <Text style={{ fontSize: 16 }}>{item.name}</Text>
        </TouchableOpacity>
      )}
    />
  );
}

