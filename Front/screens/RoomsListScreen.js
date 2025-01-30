import React, { useEffect, useState } from "react";
import { View, StyleSheet, FlatList } from "react-native";
import { ActivityIndicator, Text, Card, Searchbar } from "react-native-paper";
import AvailabilityBar from "./AvailabilityBar";

const ROOMS_URL = "https://mroom-api-c7aef75a74b0.herokuapp.com/rooms";

export default function RoomsListScreen({ route }) {
  const { building } = route.params;
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetchRooms();
  }, []);

  async function fetchRooms() {
    try {
      const response = await fetch(ROOMS_URL);
      const data = await response.json();
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
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator animating={true} size="large" />
      </View>
    );
  }

  if (rooms.length === 0) {
    return (
      <View style={styles.loadingContainer}>
        <Text variant="bodyLarge">No rooms found for {building.name}.</Text>
      </View>
    );
  }

  const displayedRooms = rooms.filter((r) =>
    r.roomnum.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <View style={styles.container}>
      <Text style={styles.headerText}>
        Times in <Text style={{ color: "red", fontWeight: "bold" }}>red</Text>{" "}
        indicate a room is busy for the next 30 minutes.
      </Text>

      <Searchbar
        placeholder="Search rooms..."
        onChangeText={(text) => setSearchQuery(text)}
        value={searchQuery}
        style={styles.searchbar}
        inputStyle={styles.searchbarInput}
      />

      <FlatList
        data={displayedRooms}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => (
          <Card style={styles.card}>
            <Card.Title title={item.roomnum} titleStyle={styles.cardTitle} />
            <Card.Content>
              <Text style={styles.availabilityLabel}>Availability:</Text>
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
  headerText: {
    fontSize: 16,
    textAlign: "center",
    marginTop: 15,
    marginBottom: 10,
    color: "#333",
  },
  container: {
    flex: 1,
    padding: 8,
  },
  listContent: {
    paddingBottom: 16,
  },
  searchbar: {
    margin: 10,
    marginBottom: 10,
    backgroundColor: "#fff",
    borderRadius: 24,
    elevation: 3, // Android shadow
    shadowColor: "#000", // iOS shadow
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  searchbarInput: {
    fontSize: 16,
  },
  card: {
    marginBottom: 10,
  },
  cardTitle: {
    fontWeight: "bold",
  },
  availabilityLabel: {
    fontSize: 16,
    color: "black",
    marginBottom: -16,
  },
});
