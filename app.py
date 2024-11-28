import streamlit as st
import pandas as pd

import auth
import menu
import logica as lg

# Configuración de la página
st.set_page_config(
    page_title="Dimex", 
    page_icon="./favicon.ico"  
)

st.title(':green[Dimex]')

if 'usuario' not in st.session_state:
    st.header(':orange[Login]')
    auth.generarLogin()
else:
    if st.session_state['usuario'] == 'admin':
        st.header(':orange[Registrar]')
        auth.generarRegistro()
    elif st.session_state['usuario'] == 'Dimex':
        st.header(':orange[Inicio]')
        if st.button('Ver tableros'):
            st.write('[Ir a Tableau](https://www.youtube.com/)')
    else:
        df = lg.cargar_datosTotal(st.session_state['index'])
        if st.session_state['puesto'] == 'PaP':
            st.header('Página de :orange[Gestión Puerta a Puerta]')
            st.subheader('Clientes del día:')
            data = lg.cargar_datos()
            st.write(lg.mostrar_datosPaP(data))
            #styled_data = data.style.apply(color_rows, axis=1)
            #st.write(styled_data)
        elif st.session_state['puesto'] == 'CC':
            st.header('Página de :orange[Call Center]')
            st.subheader('Clientes del día:') 
            data = lg.cargar_datos()
            st.write(lg.mostrar_datosCC(data))
            #styled_data = data.style.apply(color_rows, axis=1)
            #st.write(styled_data)
        elif st.session_state['puesto'] == 'AE':
            st.header('Página de :orange[Agencias Especializadas]')
            st.subheader('Clientes del día:')
            data = lg.cargar_datos()
            st.write(lg.mostrar_datosCC(data))
        st.session_state['Data'] = data

        #st.header('Página :orange[principal]')
        menu.generarMenu(st.session_state['usuario'])

        ''''''
        