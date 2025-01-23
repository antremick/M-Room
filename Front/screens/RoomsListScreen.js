// File: screens/RoomsListScreen.js
import React, { useEffect, useState } from "react";
import { View, StyleSheet, FlatList } from "react-native";
import { ActivityIndicator, Text, Card, Searchbar } from "react-native-paper";
import AvailabilityBar from "./AvailabilityBar";

const ROOMS_URL = "http://127.0.0.1:5000/rooms";

export default function RoomsListScreen({ route }) {
  const { building } = route.params;

  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);

  // State for search text
  const [searchQuery, setSearchQuery] = useState("");

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

  // If still loading from the API
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator animating={true} size="large" />
      </View>
    );
  }

  // If no rooms at all for this building
  if (rooms.length === 0) {
    return (
      <View style={styles.loadingContainer}>
        <Text variant="bodyLarge">No rooms found for {building.name}.</Text>
      </View>
    );
  }

  // Derive displayed rooms based on search
  const displayedRooms = rooms.filter((r) =>
    r.roomNum.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // If displayedRooms is empty, user typed something that doesn't match any room
  // You can optionally show a small message or just show an empty list

  return (
    <View style={styles.container}>
      {/* Explanation message */}
      <Text style={styles.infoText}>
        Times in <Text style={{ color: "red", fontWeight: "bold" }}>red</Text>{" "}
        indicate a meeting starts at that half-hour.
      </Text>

      {/* Searchbar from React Native Paper */}
      <Searchbar
        placeholder="Search rooms..."
        onChangeText={(text) => setSearchQuery(text)}
        value={searchQuery}
        style={styles.searchbar}
      />

      {/* Render a filtered list of rooms */}
      <FlatList
        data={displayedRooms}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => (
          <Card style={styles.card}>
            <Card.Title title={item.roomNum} titleStyle={styles.cardTitle} />
            <Card.Content>
              <AvailabilityBar room={item} />
            </Card.Content>
          </Card>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  infoText: {
    marginBottom: 6,
    marginHorizontal: 8,
    fontSize: 14,
  },
  container: {
    flex: 1,
    padding: 8,
  },
  listContent: {
    paddingBottom: 16,
  },
  searchbar: {
    marginBottom: 10,
  },
  card: {
    marginBottom: 10,
  },
  cardTitle: {
    fontWeight: "bold",
  },
});
