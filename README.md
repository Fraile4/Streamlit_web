# Proyecto Web de Dimex

Este proyecto es una aplicación web desarrollada como parte de un trabajo universitario para el curso de Analitica de Datos y Herramientas de Inteligencia Artificial en el TEC (Tecnologico de Monterrey). La aplicación tiene como objetivo proporcionar una plataforma en línea para la empresa Dimex, facilitando la gestión y visualización de sus clientes adeudados.

# Web App con Streamlit

Este es un pequeño proyecto para aprender a usar [Streamlit](https://streamlit.io/).

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/Fraile4/web_Streamlit.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd web_Streamlit
    ```
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4. Añade tu API_KEY en el archivo `config.py`:
    ```python
    API_KEY = 'YOUR API KEY'
    ```
   Para obtener el API_KEY, solicítalo en la web de [Groq](https://console.groq.com/keys).

5. Instala las dependencias de Google Cloud para Google Drive y Google Sheets:
    ```bash
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

6. Coloca las credenciales de la API de Google en la carpeta `data`:
    - Descarga el archivo `credentials.json` desde la consola de Google Cloud.
    - Guarda el archivo en la carpeta `data` dentro del directorio del proyecto.


## Uso

Para ejecutar la aplicación, usa el siguiente comando:
```bash
streamlit run app.py
```
