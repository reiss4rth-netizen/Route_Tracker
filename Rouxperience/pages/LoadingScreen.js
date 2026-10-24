import React from 'react'
import { Text, TouchableOpacity, View } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { LoadingStyles } from '../styles/LoadingStyles';

export default function LoadingScreen() {
    const navigation = useNavigation()
    return (
        <View style={LoadingStyles.container}>
            <View style={LoadingStyles.cloudsContainer}>
                <Text style={LoadingStyles.cloud}>☁️</Text>
                <Text style={LoadingStyles.cloud}>☁️</Text>
                <Text style={LoadingStyles.cloud}>☁️</Text>
            </View>
            <Text style={LoadingStyles.title}>Bienvenido a Rouxperience</Text>
            <View style={LoadingStyles.buttonsContainer}>
                <TouchableOpacity style={LoadingStyles.buttons} onPress={() => navigation.navigate('Login')}>
                    <Text style={LoadingStyles.textButton}>Iniciar sesión</Text>
                </TouchableOpacity>
                <TouchableOpacity style={LoadingStyles.buttons} onPress={() => navigation.navigate('Register')}>
                    <Text style={LoadingStyles.textButton}>Regístrate</Text>
                </TouchableOpacity>
            </View>
        </View>
    )
}
