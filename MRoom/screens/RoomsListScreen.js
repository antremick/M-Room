import React, { useEffect, useState, useContext } from "react";
import { View, StyleSheet, FlatList } from "react-native";
import {
  ActivityIndicator,
  Text,
  Card,
  Searchbar,
  SegmentedButtons,
  IconButton,
} from "react-native-paper";
import AvailabilityBar from "./AvailabilityBar";
import { AuthContext } from "../contexts/AuthContext";

const ROOMS_URL =
  "https://mroom-staging-031597615ed8.herokuapp.com/rooms";
const FAVORITES_URL = "https://mroom-api-c7aef75a74b0.herokuapp.com/favorites/rooms";

export default function RoomsListScreen({ route }) {
  const { building } = route.params;
  const [rooms, setRooms] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedFloor, setSelectedFloor] = useState("all");
  const { user } = useContext(AuthContext);

  // Extract floor number from room number (e.g., "1100" -> "1")
  const getFloorNumber = (roomNum) => {
    const match = roomNum.match(/^\d/);
    return match ? match[0] : null;
  };

  // Get unique floor numbers from rooms
  const getFloorOptions = () => {
    const floors = new Set(
      rooms.map((room) => getFloorNumber(room.roomnum)).filter(Boolean)
    );
    return ["all", ...Array.from(floors)].map((floor) => ({
      value: floor,
      label: floor === "all" ? "All Floors" : `Floor ${floor}`,
    }));
  };

  useEffect(() => {
    fetchRooms();
    if (user) {
      fetchFavorites();
    }
  }, [user]);

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

  async function fetchFavorites() {
    try {
      const response = await fetch(FAVORITES_URL, {
        headers: {
          Authorization: `Bearer ${user.token}`,
        },
      });
      const json = await response.json();
      setFavorites(json.map((r) => r.id));
    } catch (error) {
      console.error("Error fetching favorites:", error);
    }
  }

  async function toggleFavorite(roomId) {
    if (!user) return;

    try {
      if (favorites.includes(roomId)) {
        await fetch(`${FAVORITES_URL}/${roomId}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${user.token}`,
          },
        });
        setFavorites(favorites.filter((id) => id !== roomId));
      } else {
        await fetch(FAVORITES_URL, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${user.token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ room_id: roomId }),
        });
        setFavorites([...favorites, roomId]);
      }
    } catch (error) {
      console.error("Error toggling favorite:", error);
    }
  }

  const displayedRooms = rooms.filter((r) => {
    const matchesSearch = r.roomnum
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    const matchesFloor =
      selectedFloor === "all" || getFloorNumber(r.roomnum) === selectedFloor;
    return matchesSearch && matchesFloor;
  });

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

      <SegmentedButtons
        value={selectedFloor}
        onValueChange={setSelectedFloor}
        buttons={getFloorOptions()}
        style={styles.floorPicker}
      />

      <FlatList
        data={displayedRooms}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => (
          <Card style={styles.card}>
            <Card.Title
              title={item.roomnum}
              titleStyle={styles.cardTitle}
              right={(props) => (
                <IconButton
                  {...props}
                  icon={favorites.includes(item.id) ? "heart" : "heart-outline"}
                  onPress={() => toggleFavorite(item.id)}
                  disabled={!user}
                />
              )}
            />
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
  floorPicker: {
    marginHorizontal: 10,
    marginBottom: 10,
  },
});
