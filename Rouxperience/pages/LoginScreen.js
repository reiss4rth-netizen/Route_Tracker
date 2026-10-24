import React from 'react'
import { useState } from 'react';
import { Text, TextInput, View, TouchableOpacity, Alert } from 'react-native';
import { loginService } from '../services/userServices';
import { useNavigation } from '@react-navigation/native';
import { LoginStyles } from '../styles/LoginStyles';

export default function LoginScreen() {
    const [userName, setUserName] = useState('')
    const [password, setPassword] = useState('')
    const navigation = useNavigation()

    const handleLogin = async () => {
        try {
            const data = await loginService(userName, password);
            console.log("Sesión iniciada exitosamente", data.message)
            navigation.replace('OwnProfile')
        } catch (error) {
            Alert.alert("Atención", error.message)
        }
    }
    return (
        <View style={LoginStyles.container}>
            <View style={LoginStyles.form}>
                <Text style={LoginStyles.title}>Inicia sesión</Text>
                <TextInput
                    style={LoginStyles.formControl}
                    placeholder='Username'
                    placeholderTextColor="#aaa"
                    value={userName}
                    autoCapitalize='none'
                    onChangeText={setUserName}
                />
                <TextInput
                    style={LoginStyles.formControl}
                    placeholder='Password'
                    secureTextEntry= {true}
                    placeholderTextColor="#aaa"
                    value={password}
                    autoCapitalize='none'
                    onChangeText={setPassword}
                />
                <TouchableOpacity style={LoginStyles.button} onPress={handleLogin}>
                    <Text style={LoginStyles.buttonText}>Entrar</Text>
                </TouchableOpacity>
            </View>
        </View>
    )
}