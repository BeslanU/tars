/**
 * TARS - Multi-Modal Summarization App
 * Main Application Entry Point
 * 
 * Features:
 * - Book content summarization (text paste or file upload)
 * - Video summarization (future)
 * - Audio summarization (future)
 */

import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

// Import screens
import BookSummaryScreen from './screens/BookSummaryScreen';
import VideoSummaryScreen from './screens/VideoSummaryScreen';
import AudioSummaryScreen from './screens/AudioSummaryScreen';
import HistoryScreen from './screens/HistoryScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

/**
 * Book Summarization Navigation Stack
 */
function BookStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: '#1e40af',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
          fontSize: 18,
        },
      }}
    >
      <Stack.Screen
        name="BookSummary"
        component={BookSummaryScreen}
        options={{ title: 'Book Summarizer' }}
      />
    </Stack.Navigator>
  );
}

/**
 * Video Summarization Navigation Stack
 */
function VideoStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: '#1e40af',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
          fontSize: 18,
        },
      }}
    >
      <Stack.Screen
        name="VideoSummary"
        component={VideoSummaryScreen}
        options={{ title: 'Video Summarizer' }}
      />
    </Stack.Navigator>
  );
}

/**
 * Audio Summarization Navigation Stack
 */
function AudioStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: '#1e40af',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
          fontSize: 18,
        },
      }}
    >
      <Stack.Screen
        name="AudioSummary"
        component={AudioSummaryScreen}
        options={{ title: 'Audio Summarizer' }}
      />
    </Stack.Navigator>
  );
}

/**
 * Main Application Component
 */
export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          headerShown: false,
          tabBarStyle: {
            backgroundColor: '#f3f4f6',
            borderTopColor: '#e5e7eb',
            borderTopWidth: 1,
          },
          tabBarLabelStyle: {
            fontSize: 12,
            fontWeight: '600',
          },
          tabBarActiveTintColor: '#1e40af',
          tabBarInactiveTintColor: '#9ca3af',
        }}
      >
        {/* Book Tab */}
        <Tab.Screen
          name="BooksTab"
          component={BookStack}
          options={{
            title: 'Books',
            tabBarLabel: 'Books',
            tabBarIcon: ({ color }) => (
              <Text style={{ fontSize: 20, color }}>📚</Text>
            ),
          }}
        />

        {/* Video Tab */}
        <Tab.Screen
          name="VideosTab"
          component={VideoStack}
          options={{
            title: 'Videos',
            tabBarLabel: 'Videos',
            tabBarIcon: ({ color }) => (
              <Text style={{ fontSize: 20, color }}>🎥</Text>
            ),
          }}
        />

        {/* Audio Tab */}
        <Tab.Screen
          name="AudioTab"
          component={AudioStack}
          options={{
            title: 'Audio',
            tabBarLabel: 'Audio',
            tabBarIcon: ({ color }) => (
              <Text style={{ fontSize: 20, color }}>🎙️</Text>
            ),
          }}
        />

        {/* History Tab */}
        <Tab.Screen
          name="HistoryTab"
          component={HistoryScreen}
          options={{
            title: 'History',
            tabBarLabel: 'History',
            tabBarIcon: ({ color }) => (
              <Text style={{ fontSize: 20, color }}>⏰</Text>
            ),
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

// Styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    backgroundColor: '#1e40af',
    paddingTop: 20,
    paddingBottom: 20,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  headerTitle: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#1e40af',
  },
  button: {
    backgroundColor: '#1e40af',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    marginVertical: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
