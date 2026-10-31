import { StyleSheet } from "react-native";

export const ProfileStyles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f5',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    center: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    card: {
        backgroundColor: '#fff',
        width: '100%',
        padding: 20,
        borderRadius: 10,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    },
    title: {
        fontSize: 22,
        fontWeight: 'bold',
        marginBottom: 20,
        textAlign: 'center',
        color: '#333',
    },
    infoContainer: {
        marginBottom: 20,
    },
    label: {
        fontSize: 14,
        color: '#888',
        marginTop: 10,
    },
    value: {
        fontSize: 18,
        fontWeight: '600',
        color: '#222',
    },
    successText: {
        marginTop: 20,
        color: 'green',
        fontSize: 14,
        textAlign: 'center',
        fontWeight: '500',
    },
    button: {
        backgroundColor: '#ff5c5c',
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
    },
    buttonText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
    },
    image: {
        height: 100,
        width: 100
    }
});