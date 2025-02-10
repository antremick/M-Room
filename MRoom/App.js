// File: App.js
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import {
  Provider as PaperProvider,
  MD3LightTheme as DefaultTheme,
} from "react-native-paper";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { AuthProvider } from "./contexts/AuthContext";
import AccountScreen from "./screens/AccountScreen";

import BuildingsListScreen from "./screens/BuildingsListScreen";
import RoomsListScreen from "./screens/RoomsListScreen";
import WelcomeScreen from "./screens/WelcomeScreen";
import InfoScreen from "./screens/InfoScreen";
import CustomHeader from "./components/CustomHeader";
import BuildingsMapScreen from "./screens/BuildingsMapScreen";

// 2) (Optional) Create a custom theme to override colors, fonts, etc.
const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: "#00274C",
    secondary: "#03dac6",
    // add or override more if you want
  },
};

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function HomeStack() {
  return (
    <Stack.Navigator
      initialRouteName="BuildingsList"
      screenOptions={{
        headerStyle: {
          backgroundColor: "#fff",
        },
        headerShadowVisible: true,
      }}
    >
      <Stack.Screen
        name="BuildingsList"
        component={BuildingsListScreen}
        options={{
          header: () => <CustomHeader size="large" />,
        }}
      />
      <Stack.Screen
        name="RoomsList"
        component={RoomsListScreen}
        options={({ route }) => ({
          header: () => (
            <CustomHeader
              title={`${
                route.params.building.short_name || route.params.building.name
              }`}
              size="small"
            />
          ),
        })}
      />
    </Stack.Navigator>
  );
}

function TabNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Home"
        component={HomeStack}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="home" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen
        name="Map"
        component={BuildingsMapScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="map" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen
        name="Account"
        component={AccountScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="account" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen
        name="Info"
        component={InfoScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons
              name="information"
              color={color}
              size={size}
            />
          ),
        }}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <PaperProvider theme={theme}>
        <NavigationContainer>
          <Stack.Navigator>
            <Stack.Screen
              name="Welcome"
              component={WelcomeScreen}
              options={{ headerShown: false }}
            />
            <Stack.Screen
              name="MainApp"
              component={TabNavigator}
              options={{ headerShown: false }}
            />
          </Stack.Navigator>
        </NavigationContainer>
      </PaperProvider>
    </AuthProvider>
  );
}
