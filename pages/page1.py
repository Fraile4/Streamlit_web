import streamlit as st
import pandas as pd

import auth
import logica as lg

# Configuración de la página
st.set_page_config(
    page_title="Dimex", 
    page_icon="./favicon.ico"  
)

auth.generarLogin()
if 'usuario' in st.session_state:
    st.header('Pagina para :blue[Añadir Interaccion]')
    
    # Cargar el DataFrame cada vez que se abre la página
    #if st.session_state['puesto'] == 'PaP':
    #    df = lg.mostrar_datosPaP()
    #else:
    #    df = lg.mostrar_datosCC()
    
    df = lg.cargar_datos()
    df = df[df['Atendido'] == 0]

    if df.empty:
        st.subheader(':red[No hay clientes disponibles para gestionar.]')
    else:
        # Agregar un selectbox para elegir una fila
        selected_row = st.selectbox('Seleccione una fila:', df.index)
        client_df = lg.cargar_datosCliente(selected_row)

        # Mostrar la foto correspondiente a la fila seleccionada y la fila en formato vertical en paralelo
        col1, col2 = st.columns(2)

        with col1:
            col0, col00, col000 = st.columns(3)
            with col00:
                foto_path = f"data/Fotos/{df.loc[selected_row, 'Foto']}"
                st.image(foto_path, caption='Foto del cliente', width=100)
                st.markdown("<br>" * 2, unsafe_allow_html=True)  # -- expuestos modo 
        
        with col2:
            #st.write('**Fila seleccionada:**')
            column_titles = {
                'Numero_tlf': 'Numero de teléfono',
                'Direccion': 'Dirección'
            }

            for column in client_df.columns:
                title = column_titles.get(column, column)  
                st.markdown(f"**:orange[{title}:]** {client_df.at[selected_row, column]}")
        
        col3, col4, col5 = st.columns(3)
        with col3:
            column_titles = {
                'Muy baja probabilidad de deterioro': 'Muy baja',
                'Baja probabilidad de deterioro': 'Baja',
                'Alta probabilidad de deterioro': 'Alta',
                'Muy alta probabilidad de deterioro': 'Muy alta'
            }
            title = column_titles.get(df.loc[selected_row, 'Categoria_Deterioro'], df.loc[selected_row, 'Categoria_Deterioro'])
            #st.metric(label="Probabilidad de deterioro", value=title, delta=-0.5, delta_color="inverse")
            st.metric(label="Probabilidad de deterioro", value=title)
        with col4:
            st.metric(label="Linea de credito", value=df.loc[selected_row, 'Linea credito'])
        with col5:
            capacidad_pago = df.loc[selected_row, 'capacidad_pago'] * 100
            st.metric(label="Capacidad de pago", value=f"{capacidad_pago:.2f}%")

        col6, col7 = st.columns(2)
        with col6:
            st.metric(label="Estatus de cuenta", value=df.loc[selected_row, 'Categoria_Estatus_Cuenta'])
        with col7:
            column_titles = {
                'Reestructura del Crédito': 'Reestructura',
            }
            title = column_titles.get(df.loc[selected_row, 'Original_Oferta_Cobranza'], df.loc[selected_row, 'Original_Oferta_Cobranza'])
            st.metric(label="Oferta de cobranza recomendada", value=title)


        
        if st.session_state['puesto'] != 'PaP':
            tab1, tab2 = st.tabs(["Distribución de gestiones", "Distribución en barras"])

            with tab1:
                import matplotlib.pyplot as plt

                # Datos para el gráfico de rueda
                labels = ['Gestión Puerta a Puerta', 'Agencias Especiales', 'Call Center']
                sizes = [
                    df['num_gestion_puerta_a_puerta'].sum(),
                    df['num_agencias_especiales'].sum(),
                    df['num_call_center'].sum()
                ]

                # Crear el gráfico de rueda
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Para que el gráfico sea un círculo

                # Mostrar el gráfico en Streamlit
                st.pyplot(fig)

            with tab2:
                import matplotlib.pyplot as plt

                # Datos para el gráfico de barras
                labels = ['Gestión Puerta a Puerta', 'Agencias Especiales', 'Call Center']
                sizes = [
                    df['num_gestion_puerta_a_puerta'].sum(),
                    df['num_agencias_especiales'].sum(),
                    df['num_call_center'].sum()
                ]

                # Crear el gráfico de barras con colores personalizados
                fig, ax = plt.subplots()
                colors = ['#FF5733', '#33FF57', '#3357FF']
                ax.bar(labels, sizes, color=colors)

                # Añadir etiquetas y título
                ax.set_ylabel('Número de gestiones')
                ax.set_title('Distribución de gestiones')
                ax.set_facecolor('#f0f0f0')  # Fondo del gráfico
                fig.patch.set_facecolor('#f0f0f0')  # Fondo de la figura

                # Añadir etiquetas de valor encima de las barras
                for i, v in enumerate(sizes):
                    ax.text(i, v + 0.5, str(v), ha='center', color='black')

                # Mostrar el gráfico en Streamlit
                st.pyplot(fig)

            col0, col00, col000 = st.columns(3)
            with col00:
                if st.button('Mandar SMS'):
                    st.info('SMS enviado exitosamente')

        # Botón para abrir el formulario de detalles del cliente
        with st.form(key='detalle_cliente_form', clear_on_submit=True):
            # Mostrar advertencia si 'Incidencia' no está vacía
            if df.loc[selected_row, 'Incidencia'] != '[]':
                st.warning(f"{lg.mostrar_incidencia(selected_row)}")

            st.write('**Interacción:**')
            # Selectboxes para resultado y promesa
            resultado = st.selectbox('Resultado de interacción:', ['Atendió cliente', 'Atendió un tercero', 'No localizado'])
            if resultado == 'Atendió cliente':
                promesa = st.selectbox('Promesa:', ['Si', 'No', 'None'])
            if resultado == 'Atendió un tercero':
                promesa2 = st.selectbox('Promesa:', ['None'])
            if resultado == 'No localizado':
                promesa3 = st.selectbox('Promesa:', ['None'])

            st.write('**Pago acordado:**')
            # Agregar un date_input para seleccionar la fecha
            fecha_interaccion = st.date_input('Fecha de pago acordada:')

            modelo_cobranza = st.selectbox('Seleccione el modelo de cobranza:', ['Reestructura del Crédito', 'Quita/ Castigo', 'Pago sin veneficio', 'Tus Pesos Valen Más'])
            pago_acordado = st.text_input('Pago acordado (pesos):', value='0')

            # Validar que el input solo contenga números
            if not pago_acordado.isdigit():
                st.error('El pago acordado debe ser un número válido.')
            else:
                pago_acordado = int(pago_acordado)
                st.write(f'Se cobraran {pago_acordado} pesos mexicanos, con la oferta de {modelo_cobranza}')
            # Botón de envío
            submit_button = st.form_submit_button(label='Guardar')

            # Lógica de guardado al enviar el formulario
            if submit_button:
                if 'puesto' in st.session_state:
                    lg.guardar_datos(selected_row, st.session_state['puesto'], resultado, promesa)
                    st.success('Datos guardados exitosamente')
                    #st.write("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)
                    #st.experimental.rerun()  # Recargar la página para actualizar la tabla
                else:
                    st.error('Error: puesto no definido en session_state')


