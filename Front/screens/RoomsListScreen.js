// File: screens/RoomsListScreen.js
import React, { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator } from "react-native";
import AvailabilityBar from "./AvailabilityBar";

const ROOMS_URL = "http://127.0.0.1:5000/rooms";

export default function RoomsListScreen({ route }) {
  const { building } = route.params;

  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRooms();
  }, []);

  async function fetchRooms() {
    try {
      const response = await fetch(`${ROOMS_URL}`);
      const json = await response.json();
      // Filter only the rooms that belong to this building
      const buildingRooms = json.filter(
        (room) => room.building_id === building.id
      );
      setRooms(buildingRooms);
    } catch (error) {
      console.error("Error fetching rooms:", error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  if (rooms.length === 0) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
        <Text>No rooms found for {building.name}.</Text>
      </View>
    );
  }

  return (
    <FlatList
      data={rooms}
      keyExtractor={(item) => item.id.toString()}
      renderItem={({ item }) => (
        <View
          style={{ padding: 20, borderBottomWidth: 1, borderColor: "#ccc" }}
        >
          <Text style={{ fontWeight: "bold", marginBottom: 10 }}>
            {item.roomNum}
          </Text>
          {/* Render ONE availability bar for the current room */}
          <AvailabilityBar room={item} />
        </View>
      )}
    />
  );
}
