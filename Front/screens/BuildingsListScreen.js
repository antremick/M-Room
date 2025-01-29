// File: screens/BuildingsListScreen.js
import React, { useEffect, useState } from "react";
import { View, FlatList, StyleSheet } from "react-native";
import { ActivityIndicator, Searchbar, List } from "react-native-paper";
import Fuse from "fuse.js";

// Replace with the URL to your Flask endpoint for building data
const BUILDINGS_URL = "https://mroom-api-c7aef75a74b0.herokuapp.com/buildings";
// const BUILDINGS_URL = "http://127.0.0.1:5000/buildings";


export default function BuildingsListScreen({ navigation }) {
  const [buildings, setBuildings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchText, setSearchText] = useState("");
  const [fuse, setFuse] = useState(null);

  useEffect(() => {
    fetchBuildings();
  }, []);

  async function fetchBuildings() {
    try {
      const response = await fetch(BUILDINGS_URL);
      const json = await response.json();
      setBuildings(json);

      // Initialize Fuse.js once we have our building data
      const fuseInstance = new Fuse(json, {
        keys: ["name"],
        threshold: 0.3,
        minMatchCharLength: 2,
      });
      setFuse(fuseInstance);
    } catch (error) {
      console.error("Error fetching buildings:", error);
    } finally {
      setLoading(false);
    }
  }

  // If there's no fuse instance or no search text, just show all buildings
  const displayedBuildings = (() => {
    if (!fuse || !searchText) return buildings;
    // Perform a fuzzy search
    const results = fuse.search(searchText.trim());
    // Extract the building items from Fuse results
    return results.map((r) => r.item);
  })();

  function onBuildingPress(building) {
    // Navigate to RoomsListScreen and pass building info
    navigation.navigate("RoomsList", { building });
  }

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        {/* Paper's ActivityIndicator for a Material look */}
        <ActivityIndicator animating={true} size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Paper's Searchbar instead of a regular TextInput */}
      <Searchbar
        placeholder="Search buildings..."
        onChangeText={setSearchText}
        value={searchText}
        style={styles.searchbar}
      />

      <FlatList
        data={displayedBuildings}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <List.Item
            title={item.name}
            // Optional: subtitle or description
            description="Tap to see rooms"
            onPress={() => onBuildingPress(item)}
            // Add left icon if you want
            left={(props) => <List.Icon {...props} icon="office-building" />}
          />
        )}
        ItemSeparatorComponent={() => <View style={styles.separator} />}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  searchbar: {
    margin: 10,
    marginBottom: 10,
    backgroundColor: "#91BAD6", // University of Michigan blue
  },
  separator: {
    height: 1,
    backgroundColor: "#ccc",
    marginLeft: 72, // space for left icon
  },
});
