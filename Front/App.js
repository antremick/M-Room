// File: App.js
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import BuildingsListScreen from "./screens/BuildingsListScreen";
import RoomsListScreen from "./screens/RoomsListScreen";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
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
  );
}
