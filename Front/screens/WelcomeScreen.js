// File: screens/WelcomeScreen.js
import React from "react";
import { View, Text, Image, StyleSheet } from "react-native";
import { Button } from "react-native-paper";

export default function WelcomeScreen({ navigation }) {
  // Example next screen could be the main Buildings list
  function handleGetStarted() {
    navigation.navigate("BuildingsList");
  }

  return (
    <View style={styles.container}>
      {/* MRoom Logo */}
      <Image
        source={require("../assets/logo.png")}
        style={styles.logo}
        resizeMode="contain"
      />

      {/* App Description */}
      <Text style={styles.description}>
        Welcome to MRoom! {"\n\n"}
        MRoom helps you find open classrooms in your favorite buildings around campus.  {"\n\n"} Find study spots easy with MRoom!
      </Text>

      {/* “Get Started” Button */}
      <Button
        mode="contained"
        onPress={handleGetStarted}
        style={styles.button}
        labelStyle={styles.buttonLabel}
      >
        Get Started
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#fff",
  },
  logo: {
    width: 200,
    height: 80,
    marginBottom: 20,
  },
  description: {
    fontSize: 16,
    textAlign: "center",
    marginBottom: 30,
    color: "#333",
  },
  button: {
    width: 200,
    borderRadius: 6,
  },
  buttonLabel: {
    fontWeight: "bold",
    fontSize: 16,
  },
});
