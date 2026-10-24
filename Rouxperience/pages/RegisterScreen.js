import React from 'react'
import { useState } from 'react';
import { StyleSheet, Text, TextInput, View, TouchableOpacity } from 'react-native';
import { RegisterStyles } from '../styles/RegisterStyles';

export default function RegisterScreen() {
    const [userName, setUserName] = useState('')
    const [password, setPassword] = useState('')
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    return (
        <View style={RegisterStyles.container}>
            <View style={RegisterStyles.form}>
                <Text style={RegisterStyles.title}>Regístrate</Text>
                <TextInput
                    style={RegisterStyles.formControl}
                    placeholder='Nombre'
                    placeholderTextColor="#aaa"
                    value={name}
                    autoCapitalize='none'
                    onChangeText={setName}
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
                <TouchableOpacity style={RegisterStyles.button}>
                    <Text style={RegisterStyles.buttonText}>Entrar</Text>
                </TouchableOpacity>
            </View>
        </View>
    )
}