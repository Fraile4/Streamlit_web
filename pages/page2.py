import streamlit as st

import auth
import logica as lg

# Configuración de la página
st.set_page_config(
    page_title="Dimex", 
    page_icon="./favicon.ico"  
)

auth.generarLogin()
if 'usuario' in st.session_state:
    st.header('Página para :red[Añadir Incidencia]')

    df = lg.cargar_datos()
    df = df[df['Atendido'] == 0]

    if df.empty:
        st.subheader(':red[No hay clientes disponibles para gestionar.]')
    else:
        col3, col4 = st.columns(2)

        with col3:
            selected_row = st.selectbox('Seleccione una fila:', df.index)

        with col4:
            col0, col00, col000 = st.columns(3)
            with col00:
                foto_path = f"data/Fotos/{df.loc[selected_row, 'Foto']}"
                st.image(foto_path, caption='Foto del cliente', width=100)
                st.markdown("<br>" * 1, unsafe_allow_html=True)  # -- expuestos modo 
        
        '''Incidencias actuales:'''
        # Mostrar advertencia si 'Incidencia' no está vacía
        if df.loc[selected_row, 'Incidencia'] != '[]':
            st.warning(f"{lg.mostrar_incidencia(selected_row)}")
        

        col1, col2 = st.columns(2)

        with col1:
            opcion = st.selectbox('Seleccione una opción a añadir:', ['Telefono', 'Dirección', 'Otro'])

        with col2:
            if opcion == 'Telefono':
                telefono = st.text_input("Añade el nuevo telefono:", value="", max_chars=15)
                if not telefono.isdigit():
                    if telefono != "":
                        st.warning("Por favor, ingrese solo números.")
            elif opcion == 'Dirección':
                textarea2 = st.text_area("Añade la nueva dirección:")
            elif opcion == 'Otro':
                textarea3 = st.text_area("Añade la incidencia:")

        #incidencia = st.text_area("Añadir incidencia:")
        incidencia = ""
        if st.button("Enviar"):
            if opcion == 'Telefono':
                incidencia = f"Teléfono añadido: {telefono}"
            elif opcion == 'Dirección':
                incidencia = f"Dirección añadida: {textarea2}"
            elif opcion == 'Otro':
                incidencia = f"{textarea3}"
            lg.añadir_incidencia(selected_row, incidencia)
            print(f"Incidencia añadida: {incidencia} seleccionada en la fila {selected_row}")
            st.write(f"Incidencia añadida: {incidencia}")