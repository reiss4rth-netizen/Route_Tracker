import { StyleSheet } from "react-native";

export const LoadingStyles = StyleSheet.create({
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
        fontSize: 48,
        fontWeight: 'bold',
        textAlign: 'center',
    },
    buttonsContainer: {
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        width: '100%',
        top: 40
    },
    buttons: {
        backgroundColor: '#4169E1',
        padding: 10,
        borderRadius: 8
    },
    textButton: {
        color: '#fdfdfd',
        fontSize: 15,
        fontWeight: 'bold'
    }
});
