// File: App.js
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

// 1) Import Paper Provider (and optionally a default theme)
import {
  Provider as PaperProvider,
  MD3LightTheme as DefaultTheme,
} from "react-native-paper";

import BuildingsListScreen from "./screens/BuildingsListScreen";
import RoomsListScreen from "./screens/RoomsListScreen";

// 2) (Optional) Create a custom theme to override colors, fonts, etc.
const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: "#6200ee",
    secondary: "#03dac6",
    // add or override more if you want
  },
};

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    // 3) Wrap everything in PaperProvider
    <PaperProvider theme={theme}>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="BuildingsList">
          <Stack.Screen
            name="BuildingsList"
            component={BuildingsListScreen}
            options={{ title: "Buildings" }}
          />
          <Stack.Screen
            name="RoomsList"
            component={RoomsListScreen}
            options={{ title: "Rooms" }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
