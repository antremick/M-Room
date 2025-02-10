import React, { useState, useContext } from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Button, TextInput, Surface } from 'react-native-paper';
import { AuthContext } from '../contexts/AuthContext';

export default function AccountScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true);
  const { signIn, signUp, signOut, user } = useContext(AuthContext);

  const handleSubmit = async () => {
    if (isLogin) {
      await signIn(email, password);
    } else {
      await signUp(email, password);
    }
  };

  if (user) {
    return (
      <View style={styles.container}>
        <Surface style={styles.surface}>
          <Text style={styles.title}>Welcome, {user.email}</Text>
          <Button 
            mode="contained" 
            onPress={signOut}
            style={styles.button}
          >
            Sign Out
          </Button>
        </Surface>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.surface}>
        <Text style={styles.title}>{isLogin ? 'Sign In' : 'Create Account'}</Text>
        <TextInput
          label="Email"
          value={email}
          onChangeText={setEmail}
          mode="outlined"
          style={styles.input}
        />
        <TextInput
          label="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          mode="outlined"
          style={styles.input}
        />
        <Button 
          mode="contained" 
          onPress={handleSubmit}
          style={styles.button}
        >
          {isLogin ? 'Sign In' : 'Sign Up'}
        </Button>
        <Button 
          mode="text" 
          onPress={() => setIsLogin(!isLogin)}
          style={styles.switchButton}
        >
          {isLogin ? 'Need an account? Sign Up' : 'Have an account? Sign In'}
        </Button>
      </Surface>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  surface: {
    padding: 16,
    borderRadius: 8,
    elevation: 4,
  },
  title: {
    fontSize: 24,
    marginBottom: 16,
    textAlign: 'center',
  },
  input: {
    marginBottom: 12,
  },
  button: {
    marginTop: 8,
  },
  switchButton: {
    marginTop: 8,
  },
}); 