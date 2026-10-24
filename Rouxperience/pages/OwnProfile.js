import React, { useState, useEffect } from 'react';
import { Text, View, ActivityIndicator, TouchableOpacity, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getMyProfileService } from '../services/userServices';
import { ProfileStyles } from '../styles/ProfileStyles'

export default function OwnProfileScreen() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigation = useNavigation();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const data = await getMyProfileService();
                setUser(data);
            } catch (error) {
                Alert.alert("Sesión expirada o inválida", error.message);
                navigation.replace('Login');
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, []);

    const handleLogout = async () => {
        await AsyncStorage.removeItem('userToken');
        navigation.replace('Login');
    };

    if (loading) {
        return (
            <View style={ProfileStyles.center}>
                <ActivityIndicator size="large" color="#0000ff" />
                <Text>Cargando perfil...</Text>
            </View>
        );
    }

    return (
        <View style={ProfileStyles.container}>
            <View style={ProfileStyles.card}>
                <Text style={ProfileStyles.title}>¡Perfil Verificado! 🎉</Text>
                
                {user ? (
                    <View style={ProfileStyles.infoContainer}>
                        <Text style={ProfileStyles.label}>Nombre:</Text>
                        <Text style={ProfileStyles.value}>{user.name}</Text>

                        <Text style={ProfileStyles.label}>Username:</Text>
                        <Text style={ProfileStyles.value}>@{user.username}</Text>

                        <Text style={ProfileStyles.label}>Correo electrónico:</Text>
                        <Text style={ProfileStyles.value}>{user.email}</Text>
                        
                        <Text style={ProfileStyles.successText}>
                            ✅ Conexión con el backend exitosa. El token JWT funciona correctamente.
                        </Text>
                    </View>
                ) : (
                    <Text>No se encontraron datos del usuario.</Text>
                )}

                <TouchableOpacity style={ProfileStyles.button} onPress={handleLogout}>
                    <Text style={ProfileStyles.buttonText}>Cerrar Sesión</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}