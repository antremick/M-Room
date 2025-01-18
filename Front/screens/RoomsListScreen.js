// File: screens/RoomsListScreen.js
import React, { useEffect, useState } from "react";
import { View, StyleSheet, FlatList } from "react-native";
import { ActivityIndicator, Text, Card } from "react-native-paper";
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
      const response = await fetch(ROOMS_URL);
      const data = await response.json();
      // Filter only rooms for this building
      const buildingRooms = data.filter(
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
    // Use Paper's ActivityIndicator
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator animating={true} size="large" />
      </View>
    );
  }

  if (rooms.length === 0) {
    // Use Paper's Text
    return (
      <View style={styles.loadingContainer}>
        <Text variant="bodyLarge">No rooms found for {building.name}.</Text>
      </View>
    );
  }

  return (
    <FlatList
      contentContainerStyle={styles.container}
      data={rooms}
      keyExtractor={(item) => item.id.toString()}
      renderItem={({ item }) => (
        <Card style={styles.card}>
          {/* Title for the room */}
          <Card.Title title={item.roomNum} titleStyle={styles.cardTitle} />
          {/* AvailabilityBar inside Card.Content */}
          <Card.Content>
            <AvailabilityBar room={item} />
          </Card.Content>
        </Card>
      )}
    />
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  container: {
    padding: 16,
  },
  card: {
    marginBottom: 16,
  },
  cardTitle: {
    fontWeight: "bold",
  },
});
