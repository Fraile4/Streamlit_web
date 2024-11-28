import streamlit as st
import pandas as pd

# Constante para la ruta del archivo CSV de usuarios
USUARIOS_CSV_PATH = './data/usuarios.csv'

def generarMenu(usuario):
    """Genera el menú dependiendo del usuario

    Args:
        usuario (str): usuario utilizado para generar el menú
    """        
    with st.sidebar:
        # Cargamos la tabla de usuarios
        dfusuarios = pd.read_csv(USUARIOS_CSV_PATH)
        # Filtramos la tabla de usuarios
        dfUsuario =dfusuarios[(dfusuarios['usuario']==usuario)]
        # Cargamos el nombre del usuario
        nombre= dfUsuario['nombre'].values[0]
        #Mostramos el nombre del usuario
        st.write(f"Hola **:blue-background[{nombre}]** ")
        # Mostramos los enlaces de páginas
        st.page_link("app.py", label="Inicio", icon=":material/home:")
        st.subheader("Acciones")
        st.page_link("pages/page1.py", label="Interacción", icon=":material/group:")
        st.page_link("pages/page2.py", label="Aviso", icon=":material/sell:")
        st.subheader("Utilidades")
        st.page_link("pages/page3.py", label="ChatBot", icon="🤖")    
        # Botón para cerrar la sesión
        btnSalir=st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
            st.rerun()

