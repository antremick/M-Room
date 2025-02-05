import React from "react";
import { View, StyleSheet, Image, Linking } from "react-native";
import { Text } from "react-native-paper";

export default function InfoScreen() {
  return (
    <View style={styles.container}>
      <Image
        source={require("../assets/logo.png")}
        style={styles.logo}
        resizeMode="contain"
      />
      <Text style={styles.description}>
        Welcome to MRoom! {"\n\n"}
        MRoom is your go-to app for finding open classrooms to study in on
        campus. New features including location services, table finders, Rick's
        line skips, and more coming soon!
        {"\n\n"}
        Happy to take any inquiries, feedback, or suggestions at {" "}
        <Text
          style={{ color: "#00274C", textDecorationLine: "underline" }}
          onPress={() => Linking.openURL("mailto:remickar@umich.edu")}
        >
          remickar@umich.edu
        </Text>
        {"\n\n"}
        MRoom is not an official U-M application and is not affiliated with U-M
        in any way.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    alignItems: "center",
    backgroundColor: "#fff",
  },
  logo: {
    width: 200,
    height: 80,
    marginTop: 40,
    marginBottom: 30,
  },
  description: {
    fontSize: 16,
    textAlign: "center",
    lineHeight: 24,
    color: "#333",
  },
});
