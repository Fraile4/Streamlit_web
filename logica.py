import pandas as pd
import matplotlib.pyplot as plt

# Ruta del archivo CSV
CSV_FILE_PATH = './data/csv_final_web_tablo.csv'
CSV_LITTLE_FILE_PATH = './data/df_Small.csv'

# Cargar datos desde el archivo CSV
def cargar_datosTotal(index):
    df = pd.read_csv(CSV_FILE_PATH)
    df.set_index('Solicitud_id', inplace=True)
    
    # Filtrar el DataFrame para obtener un subconjunto más pequeño
    start_row = (index - 1) * 10 if index > 0 else 0
    end_row = index * 10
    df_small = df.iloc[start_row:end_row]
    
    # Guardar el DataFrame más pequeño en un nuevo archivo CSV
    df_small.to_csv(CSV_LITTLE_FILE_PATH, index=True)
    return df

def cargar_datosTotal2():
    df = pd.read_csv(CSV_FILE_PATH)
    df.set_index('Solicitud_id', inplace=True)
    
    return df


def cargar_datos():
    df = pd.read_csv(CSV_LITTLE_FILE_PATH)
    df.set_index('Solicitud_id', inplace=True)
    return df

def cargar_datosCliente(index):
    df = cargar_datos()
    df = df.loc[[index]]
    columns_to_select = ['Numero_tlf', 'Direccion']
    atraso = {
        1: 'Atraso de 1 mes',
        2: 'Atraso de 2 meses',
        3: 'Atraso de 3 meses',
        4: 'Atraso de 4 meses',
        5: 'Atraso de 5 meses',
        6: 'Atraso de 6 meses',
        7: 'Atraso de 7 meses o más',
        'atraso_1_29': 'Atraso de 1 mes',
        'atraso_30_59': 'Atraso de 2 meses',
        'atraso_60_89': 'Atrsa de 3 meses',
        'atraso_90_119': 'Atraso de 4 meses',
        'atraso_120_149': 'Atraso de 5 meses',
        'atraso_150_179': 'Atraso de 6 meses',
        'atraso_180_más': 'Ataso de 7 meses o más'
    }
    Total_Interecciones = len(eval(df.at[index, 'Interacciones']))
    interacciones = eval(df.loc[index, 'Interacciones'])
    Ultima_Interaccion = df.loc[index, 'Ultima_Interaccion_cat']
    atraso = df['Nivel_Atraso'].map(atraso).loc[index]

    existing_columns = [col for col in columns_to_select if col in df.columns]
    new_df = df[existing_columns]
    new_df['Total Interacciones'] = Total_Interecciones
    new_df['Ultima Interacción'] = Ultima_Interaccion
    new_df['Nivel Atraso'] = atraso
    return new_df

def mostrar_datosPaP(df):
    df = cargar_datos()
    columns_to_select = ['Numero_tlf', 'Direccion', 'Atendido']
    existing_columns = [col for col in columns_to_select if col in df.columns]
    new_df = df[existing_columns]
    new_df['Atendido'] = new_df['Atendido'].map({1: '✔️', 0: '❌'})

    #new_df = new_df.sample(n=min(10, len(new_df)))
    return new_df


def mostrar_datosCC(df):
    df = cargar_datos()
    columns_to_select = ['Numero_tlf', 'Atendido']
    existing_columns = [col for col in columns_to_select if col in df.columns]
    new_df = df[existing_columns]
    new_df['Atendido'] = new_df['Atendido'].map({1: '✔️', 0: '❌'})
    return new_df

def mostrar_datosAE():
    df = cargar_datos()
    columns_to_select = ['Numero_tlf', 'Interacciones']
    existing_columns = [col for col in columns_to_select if col in df.columns]
    new_df = df[existing_columns]
    return new_df

# Función para guardar datos en el archivo CSV
def guardar_datos(row, tp, resultado, promesa):
    # Mapear el tipo de gestión
    tipo_gestion_map = {
        'PaP': 'Gestión Puerta a Puerta',
        'CC': 'Call Center',
        'AE': 'Agencias Especializadas'
    }
    tp = tipo_gestion_map.get(tp, tp)
    
    # Nueva interacción
    nueva_interaccion = {
        'Tipo_Gestión': tp,
        'Resultado': resultado,
        'Promesa_Pago': promesa
    }
    
    # Cargar datos actuales
    df = cargar_datos()
    
    # Convertir la cadena JSON a una lista de diccionarios
    interacciones = eval(df.at[row, 'Interacciones'])
    
    # Añadir la nueva interacción
    interacciones.append(nueva_interaccion)
    
    # Convertir la lista de diccionarios de nuevo a una cadena JSON
    df.at[row, 'Interacciones'] = str(interacciones)

    # Cambiar la variable Atendido de 0 a 1
    df.at[row, 'Atendido'] = 1

    df.at[row, 'Ultima_Interaccion_cat'] = tp
    
    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(CSV_LITTLE_FILE_PATH, index=True)
    #modelo.ejecutar_proceso()

def añadir_incidencia(selected_row, incidencia):
    df = cargar_datos()
    
    # Convertir la cadena JSON a una lista de incidencias
    incidencias = eval(df.at[selected_row, 'Incidencia']) if 'Incidencia' in df.columns and pd.notna(df.at[selected_row, 'Incidencia']) else []
    
    # Añadir la nueva incidencia
    incidencias.append(incidencia)
    
    # Convertir la lista de incidencias de nuevo a una cadena JSON
    df.at[selected_row, 'Incidencia'] = str(incidencias)

    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(CSV_LITTLE_FILE_PATH, index=True)
    
    # Subir los cambios al archivo CSV grande
    #subir_cambios(df)
    #modelo.ejecutar_proceso()

def mostrar_incidencia(selected_row):
    df = cargar_datos()
    incidencias = eval(df.at[selected_row, 'Incidencia'])
    return '\n\r'.join([f"{i+1}. {incidencia}" for i, incidencia in enumerate(incidencias)])

def cargar_datosAtraso(selected_row):
    df = cargar_datos()
    atraso = df.loc[selected_row, 'Nivel_Atraso']
    
    # Contar la frecuencia de cada nivel de atraso
    atraso_counts = df['Nivel_Atraso'].value_counts()
    
    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    atraso_counts.plot(kind='bar', color='skyblue')
    plt.title('Distribución del Nivel de Atraso')
    plt.xlabel('Nivel de Atraso')
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    
    # Mostrar la gráfica
    return plt.show()


def subir_cambios(df):
    # Cargar el DataFrame grande y el pequeño
    df_total = cargar_datosTotal2()

    # Actualizar el DataFrame grande con los cambios del pequeño
    df_total.update(df)

    # Guardar el DataFrame grande actualizado en el archivo CSV
    df_total.to_csv(CSV_FILE_PATH, index=True)

