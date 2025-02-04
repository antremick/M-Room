import React, { useEffect, useState } from "react";
import { View, FlatList, StyleSheet, Text } from "react-native";
import { ActivityIndicator, Searchbar, List } from "react-native-paper";
import Fuse from "fuse.js";

const BUILDINGS_URL = "https://mroom-api-c7aef75a74b0.herokuapp.com/buildings";

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

      const fuseInstance = new Fuse(json, {
        keys: ["name", "short_name"],
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

  const displayedBuildings = (() => {
    if (!fuse || !searchText) return buildings;
    const results = fuse.search(searchText.trim());
    return results.map((r) => r.item);
  })();

  function onBuildingPress(building) {
    navigation.navigate("RoomsList", { building });
  }

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator animating={true} size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.headerText}>Tap on a Building to see rooms</Text>

      <Searchbar
        placeholder="Search buildings..."
        onChangeText={setSearchText}
        value={searchText}
        style={styles.searchbar}
        inputStyle={styles.searchbarInput}
      />

      <FlatList
        data={displayedBuildings}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <List.Item
            title={
              item.short_name && item.short_name !== ""
                ? `(${item.short_name}) ${item.name}`
                : item.name
            }
            onPress={() => onBuildingPress(item)}
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
  headerText: {
    fontSize: 16,
    textAlign: "center",
    marginTop: 15,
    marginBottom: 10,
    color: "#333",
  },
  loadingContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
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
  separator: {
    height: 1,
    backgroundColor: "#ccc",
    marginLeft: 15, // Removed the left margin so line extends fully
    marginRight: 15,
  },
});
