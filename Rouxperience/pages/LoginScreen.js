import React from 'react'
import { useState } from 'react';
import { StyleSheet, Text, TextInput, View, TouchableOpacity } from 'react-native';
import { LoginStyles } from '../styles/LoginStyles';

export default function LoginScreen() {
    const [userName, setUserName] = useState('')
    const [password, setPassword] = useState('')
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
                <TouchableOpacity style={LoginStyles.button}>
                    <Text style={LoginStyles.buttonText}>Entrar</Text>
                </TouchableOpacity>
            </View>
        </View>
    )
}