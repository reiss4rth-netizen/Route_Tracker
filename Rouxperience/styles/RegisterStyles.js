import { StyleSheet } from "react-native";

export const RegisterStyles = StyleSheet.create({
    container: {
        flex: 1, // Le indica a la vista que ocupe el 100% de la pantalla
        backgroundColor: '#87CEEB', // Azul cielo
        justifyContent: 'center', // Centra verticalmente el contenido
        alignItems: 'center', // Centra horizontalmente el contenido
    },
    title: {
        fontWeight: 'bold',
        fontSize: 24,
        marginBottom: 20
    },
    form: {
        backgroundColor: '#fcfcfc',
        padding: 20,
        width: '80%',
        marginHorizontal: 24,
        borderRadius: 10,
        justifyContent: 'center',
        alignItems: 'center'
    },
    formControl: {
        height: 40,
        width: '80%',                  
        backgroundColor: '#ffffff',   
        borderWidth: 1,            
        borderColor: '#ced4da',      
        borderRadius: 8,           
        paddingHorizontal: 12,      
        fontSize: 16,                
        color: '#212529',  
        marginBottom: 12        
    },
    button: {
        backgroundColor: '#27a2ff',
        width: 80,
        height: 40,
        borderRadius: 8,
        paddingVertical: 5,
        paddingHorizontal: 10,
        margin: 10,
        alignItems: 'center',
        justifyContent: 'center'
    },
    buttonText: {
        fontWeight: 'bold',   
        color: '#ffffff',
        fontSize: 16
    }
})