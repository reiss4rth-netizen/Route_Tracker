import React from 'react'
import { useState } from 'react';
import { StyleSheet, Text, TextInput, View, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { registerService } from '../services/userServices';
import { RegisterStyles } from '../styles/RegisterStyles';

export default function RegisterScreen() {
    const [userName, setUserName] = useState('')
    const [password, setPassword] = useState('')
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const navigate = useNavigation()

    const handleRegister = async () => {
        try {
            const response = await registerService(name, userName, email, password);
            alert(response.message)
            navigate.replace('OwnProfile')
        } catch (error) {
            alert(error.message)
        }
    }

    return (
        <View style={RegisterStyles.container}>
            <View style={RegisterStyles.form}>
                <Text style={RegisterStyles.title}>Regístrate</Text>
                <TextInput
                    style={RegisterStyles.formControl}
                    placeholder='Nombre'
                    placeholderTextColor="#aaa"
                    value={name}
                    autoCapitalize='words'
                    onChangeText={setName}
                />
                <TextInput
                    style={RegisterStyles.formControl}
                    placeholder='Username'
                    placeholderTextColor="#aaa"
                    value={userName}
                    autoCapitalize='none'
                    onChangeText={setUserName}
                />
                <TextInput
                    style={RegisterStyles.formControl}
                    placeholder='E-mail'
                    placeholderTextColor="#aaa"
                    value={email}
                    autoCapitalize='none'
                    onChangeText={setEmail}
                />
                <TextInput
                    style={RegisterStyles.formControl}
                    placeholder='Password'
                    placeholderTextColor="#aaa"
                    value={password}
                    secureTextEntry= {true}
                    autoCapitalize='none'
                    onChangeText={setPassword}
                />
                <TouchableOpacity style={RegisterStyles.button} onPress={handleRegister}>
                    <Text style={RegisterStyles.buttonText}>Entrar</Text>
                </TouchableOpacity>
            </View>
        </View>
    )
}