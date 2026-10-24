import React from 'react'
import { StyleSheet, Text, View } from 'react-native';

export default function LoadingScreen() {
    return (
        <view style={styles.container}>
            <View style={Styles.cloudsContainer}>
                <Text style={StyleSheet.cloud}>☁️</Text>
                <Text style={styles.cloud}>☁️</Text>
                <Text style={styles.cloud}>☁️</Text>
            </View>
            <Text style={styles.title}>Bienvenido a Rouxperience</Text>
        </view>
    )
}

const styles = StyleSheet.create({
  container: {
    flex: 1, // Le indica a la vista que ocupe el 100% de la pantalla
    backgroundColor: '#87CEEB', // Azul cielo
    justifyContent: 'center', // Centra verticalmente el contenido
    alignItems: 'center', // Centra horizontalmente el contenido
  },
  cloudsContainer: {
    position: 'absolute', // Saca a las nubes del flujo central
    top: 60, // Distancia desde el borde superior de la pantalla
    flexDirection: 'row', // Coloca los elementos en fila (horizontal)
    width: '100%',
    justifyContent: 'space-evenly', // Reparte el espacio entre las nubes
  },
  cloud: {
    fontSize: 50,
  },
  title: {
    color: '#ffffff',
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
  }
});''