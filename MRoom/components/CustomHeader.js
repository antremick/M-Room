import React from "react";
import { View, Image, StyleSheet, SafeAreaView } from "react-native";
import { Text } from "react-native-paper";

export default function CustomHeader({ title = "Buildings", size = "large" }) {
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <Text
          style={[
            styles.title,
            size === "small" ? styles.smallText : styles.largeText,
          ]}
        >
          {title}
        </Text>
        <Image
          source={require("../assets/logo.png")}
          style={styles.logo}
          resizeMode="contain"
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    backgroundColor: "#fff",
  },
  container: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    height: 44,
    backgroundColor: "#fff",
    borderBottomWidth: 1,
    borderBottomColor: "#e0e0e0",
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#000",
    marginLeft: -8,
  },
  logo: {
    width: 100,
    height: 30,
    marginRight: -16,
  },
  largeText: {
    fontSize: 24,
  },
  smallText: {
    fontSize: 18,
  },
});
