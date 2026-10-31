import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

export const loginService = async(username, password) => {
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Error al iniciar sesión.');
        }
        await AsyncStorage.setItem('userToken', data.token);
        return data;
    } catch (error) {
        throw error;
    }
};

export const registerService = async (name, username, email, password) => {
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({name, username, email, password})
        });
        const data = await response.json()
        if (!response.ok) {
            throw new Error (data.error || 'Error al registrar usuari.')
        }
        await AsyncStorage.setItem('userToken', data.token);
        return data;
    } catch (error) {
        throw error;
    }
}

export const getMyProfileService = async () => {
    try {
        const token = await AsyncStorage.getItem('userToken');
        if (!token) {
            throw new Error('Acción no autorzada')
        }
        const response = await fetch(`${API_URL}/me`, {
            method: 'GET', 
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Error al obtener el perfil')
        }
        return data;
    } catch (error) {
        throw error;
    }
};

export const deleteUserService = async (userId) => {
    try {
        const token = await AsyncStorage.getItem('userToken')
        if (!token) {
            throw new Error ('Accion no autorizada');
        }
        const response = await fetch(`${API_URL}/user/${userId}`, {
            method: 'DELETE', 
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json()
        if (!response.ok) {
            throw new Error('data.error' || 'Error al eliminar usuario')
        }
        return data;
    } catch (error) {
        throw error;
    }
}