 # -- coding: utf-8 --
"""myfile

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15e-V4gddIhN9kVunjOiHNkcsxjzHTuap
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu

# Configuración de la página de Streamlit
st.set_page_config(page_title="Deforestación en Áreas Naturales Protegidas", page_icon="🌳", initial_sidebar_state="expanded", layout='wide')

# Cargar datos
archivo = "Dataset_DeforestacionAnp_SERNANP.csv"
data = pd.read_csv(archivo)

# Configuración del menú
with st.sidebar:
    menu = option_menu(
        menu_title="Menú Principal",
        options=["Inicio", "Deforestación por año", "Causas de Deforestación", "Comparativo", "Zonificación", "Área Deforestada por ANP", "Conoce más"],
        icons=["house", "tree", "pie-chart", "bar-chart", "map", "globe", "info-circle"],
        menu_icon="menu-app",
        default_index=0
    )

# Sección: Inicio
if menu == "Inicio":
    st.title('Huellas de la deforestación')
    st.header("Rastreando el impacto de la pérdida forestal en Perú a través del tiempo")
    st.image("https://raw.githubusercontent.com/mcamilaa/streamlit_app/main/imagenes/defo_1.jpg", caption="Deforestación en áreas protegidas", use_column_width=False)
    st.write('La deforestación en Perú es un fenómeno alarmante que ha capturado la atención de ambientalistas, científicos y gobiernos por igual. Este país, hogar de una de las partes más ricas en biodiversidad del planeta, enfrenta una creciente amenaza debido a la tala indiscriminada de bosques, impulsada por actividades como la minería y la expansión urbana. En este caso, analizaremos un registro de monitoreo de la Deforestación en el ámbito de las Áreas Naturales, para dar conocimiento especificos sobre ello y generar un análisis.')
    st.write("El Registro de Monitoreo de la Deforestación en el ámbito de las Áreas Naturales Protegidas es una herramienta fundamental gestionada por el Servicio Nacional de Áreas Naturales Protegidas por el Estado (SERNANP) en Perú. Este organismo, adscrito al Ministerio del Ambiente, tiene como misión asegurar la conservación de las áreas protegidas del país, así como la diversidad biológica y el mantenimiento de sus servicios ambientales. A través de sistemas de información geográfica y técnicas de monitoreo biológico, SERNANP recopila y analiza datos sobre la deforestación y otros cambios en el uso del suelo dentro de estas áreas. Este registro no solo permite identificar las tendencias de pérdida de cobertura forestal, sino que también facilita la implementación de estrategias de conservación y gestión sostenible, contribuyendo así a la protección de los ecosistemas y a la mitigación de los efectos del cambio climático. La información obtenida es crucial para la toma de decisiones informadas y para el foralecimiento de las políticas ambientales en el país.")
    st.write("De tal forma, nos enfocaremos en el monitoreo de la deforestación dentro de las Áreas Naturales Protegidas. Examinaremos datos generales que ilustran la tasa de deforestación y las tendencias a lo largo del tiempo, así como las implicancias de estas pérdidas en la conservación de la biodiversidad.")

# Sección: Deforestación por año
if menu == "Deforestación por año":
    st.header("Área deforestada por año")
    st.write("El grafico a continuación nos permite analizar la perdida de áreas forestales en las ANP durante los años. De este modo, entenderemos la magnitud del problema que vive el Perú y apreciaremos los periodos de mayor cambio.")
    # Crear un filtro para seleccionar el año
    years = data['ANIO_REPORTE'].unique()
    selected_year = st.selectbox("Selecciona el año para mostrar el gráfico:", years)

    # Función para procesar y filtrar datos por año
    def procesar_datos_por_anio(data, anio):
        meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
        
        # Filtrar datos por año
        datos_anio = data[data['ANIO_REPORTE'] == anio]
        
        # Verifica si hay datos después del filtrado
        if datos_anio.empty:
            st.warning(f"No hay datos para el año seleccionado: {anio}")
            return pd.DataFrame(), pd.DataFrame()

        # Agrupar área deforestada por mes
        area_por_mes = datos_anio.groupby('MES_IMAG')['AREA_DEFO'].sum().reset_index()
        area_por_mes['MES_NOMBRE'] = area_por_mes['MES_IMAG'].map(meses)  # Mapear nombres de los meses
        
        return area_por_mes, datos_anio

    # Procesar datos para el año seleccionado
    data_anio, datos_filtrados = procesar_datos_por_anio(data, selected_year)

    # Verificar si hay datos antes de crear el gráfico
    if not data_anio.empty:
        # Colores para cada año
        color_map = {2021: 'orange', 2022: 'green', 2023: 'blue'}
        selected_color = color_map.get(selected_year, 'gray')

        # Crear gráfico con Plotly
        fig = px.line(data_anio, x='MES_NOMBRE', y='AREA_DEFO', title=f'Área deforestada por mes en {selected_year}')
        fig.update_traces(
            mode='lines+markers',
            marker=dict(symbol='circle', size=8, color=selected_color),
            line=dict(color=selected_color, width=2)
        )
        fig.update_layout(
            title=dict(
                text=f'Área deforestada por mes en {selected_year}',
                font=dict(size=20, color='darkblue')
            ),
            xaxis=dict(
                title='Mes',
                titlefont=dict(size=16, color='darkblue'),
                tickfont=dict(size=14, color='black'),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                title='Área Deforestada (ha)',
                titlefont=dict(size=16, color='darkblue'),
                tickfont=dict(size=14, color='black'),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified'
        )

        # Mostrar gráfico en Streamlit
        st.plotly_chart(fig)

        # Mostrar tabla de datos filtrados
        datos_filtrados.index = datos_filtrados.index + 1
        st.write(datos_filtrados[['MES_IMAG', 'ANIO_REPORTE', 'AREA_DEFO']])
        st.markdown("*La tabla muestra los datos de deforestación mensuales para el año seleccionado.*")
        st.info("Este gráfico ilustra la cantidad de área deforestada (en hectáreas) por mes en el año seleccionado.")
    else:
        st.warning("No hay datos suficientes para generar el gráfico.")
     

# Sección: Causas de Deforestación (Gráfico Interactivo)
if menu == "Causas de Deforestación":
    st.header("Causas de la Deforestación")
    st.write("La deforestación no es un fenómeno aleatorio; es impulsada por una combinación de factores humanos y naturales. Los cuales tienden a ser unos más comunes que otros. Entre las causas humanas más comunes se encuentran la agricultura, transporte, mineria y ocupación humana. Los cuales veremos a continuación")
    # Agrupación de datos por causa
    area_causa = data.groupby('DEFO_CAUSA')['AREA_DEFO'].sum().reset_index()
    area_causa = area_causa.sort_values('AREA_DEFO', ascending=False)  # Ordenar por área


    # Paleta de colores
    custom_colors = [
     "#6BAED6",  # Azul claro
     "#FDD835",  # Amarillo dorado
     "#A1D490",  # Verde suave
     "#FF6F61",  # Rojo coral
     "#9575CD"   # Morado
    ]

    # Crear gráfico de pastel interactivo con Plotly
    fig = px.pie(
        area_causa,
        values='AREA_DEFO',
        names='DEFO_CAUSA',
        title=' ',
        color_discrete_sequence=custom_colors,
        hole=0.3  # Gráfico de dona
    )
    
    # Personalizar la visualización de etiquetas
    fig.update_traces(
        textinfo='percent+label',
        hoverinfo='label+value+percent',
        textfont_size=14
    )

    # Configuración del diseño
    fig.update_layout(
        legend=dict(
            title='Causas',
            font=dict(size=14),
            bordercolor='lightgrey',
            borderwidth=1
        )
    )

    # Mostrar el gráfico interactivo en Streamlit
    st.plotly_chart(fig)

    # Tabla de datos
    st.write("Datos de causa de deforestación y área deforestada:")
    st.dataframe(area_causa)
   

# Sección: Comparativo
if menu == "Comparativo":
    st.header("Comparación entre Años")
    promedios = pd.DataFrame({
        "Año": ["2021", "2022", "2023"],
        "Promedio Mensual (ha)": [
            data[data['ANIO_REPORTE'] == 2021]['AREA_DEFO'].mean(),
            data[data['ANIO_REPORTE'] == 2022]['AREA_DEFO'].mean(),
            data[data['ANIO_REPORTE'] == 2023]['AREA_DEFO'].mean()
        ]
    })

    fig, ax = plt.subplots()
    ax.bar(promedios['Año'], promedios['Promedio Mensual (ha)'], color=['orange', 'green', 'blue'])
    ax.set_title('Promedio mensual de área deforestada (2021-2023)')
    ax.set_xlabel('Año')
    ax.set_ylabel('Área Deforestada (ha)')
    st.pyplot(fig)
    st.write(promedios)

# Sección: Zonificación
if menu == "Zonificación":
    st.header("Zonificación de Deforestación")
    st.write("El gráfico presentado a continuación ilustra la deforestación clasificada por diferentes tipos de zonificación en áreas naturales protegidas (ANP). Este análisis nos permite identificar las categorías más afectadas y evaluar cómo las actividades humanas o la falta de planificación contribuyen a la pérdida de cobertura forestal.")
    area_zonificacion = data.groupby("ZONIFI_ANP")['AREA_DEFO'].sum().reset_index()
    area_zonificacion = area_zonificacion.sort_values('AREA_DEFO', ascending=True)
    
    fig, ax = plt.subplots()
    ax.barh(area_zonificacion['ZONIFI_ANP'], area_zonificacion['AREA_DEFO'], color='teal')
    ax.set_title('Área deforestada por zonificación')
    ax.set_xlabel('Área Deforestada (ha)')
    st.pyplot(fig)
    st.dataframe(area_zonificacion.rename(columns={
        'ZONIFI_ANP': 'Zonificación',
        'AREA_DEFO': 'Área Deforestada (ha)'
    }))
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**1. Zona de Aprovechamiento Directo**")
        st.write("Áreas productivas con alta deforestación por agricultura y ganadería.")

    with col2:
        st.markdown("**2. Zona de Uso Especial**")
        st.write("Áreas protegidas, pero con deforestación ilegal.")

    with col3:
        st.markdown("**3. Zona Silvestre**")
        st.write("Territorios de conservación, afectados por minería y tala ilegal.")

    with col4:
        st.markdown("**4. No Zonificado**")
        st.write("Áreas sin regulación, vulnerables a la deforestación.")

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.markdown("**5. Zona de Recuperación**")
        st.write("Áreas en regeneración, aún afectadas por actividades humanas.")

    with col6:
        st.markdown("**6. Zona de Protección Estricta**")
        st.write("Áreas sin intervención, pero amenazadas por actividades ilegales.")

    with col7:
        st.markdown("**7. Zona de Uso Turístico y Recreativo**")
        st.write("Áreas turísticas que sufren daños por crecimiento desordenado.")

    with col8:
        st.markdown("**8. Zona Histórico Cultural**")
        st.write("Áreas patrimoniales, amenazadas por expansión agrícola y urbanización ilegal.")

# Sección: Área Deforestada por Categoría de ANP
if menu == "Área Deforestada por ANP":
    st.header("Área Deforestada por Categoría de ANP (2021-2023)")
    st.write("Las ANP si bien son protegidas por el estado, aún existe un sistema poco eficiente para lograr la cobertura total de protección de las regiones. Debido a que se siguen encontrando expuestas a peligros, en los gráficos a continuación veremos las áreas deforestadas separadas por categorias de ANP de las diversas partes del Perú.")
    # Filtrar datos para el periodo 2021-2023
    filtered_data = data[(data["ANIO_REPORTE"] >= 2021) & (data["ANIO_REPORTE"] <= 2023)].copy()

    # Limpieza de la columna "CATEGORIA" (quitar espacios y uniformar formato)
    filtered_data["CATEGORIA"] = filtered_data["CATEGORIA"].str.strip().str.title()

    # Verificar si hay datos después del filtrado
    if filtered_data.empty:
        st.warning("No se encontraron datos para el período 2021-2023.")
    else:
        # Agrupar datos por categoría y ANP, sumando el área deforestada
        sum_area_deforestation = filtered_data.groupby(["CATEGORIA", "ANP"])["AREA_DEFO"].sum().reset_index()

        # Obtener las categorías únicas
        categorias = sum_area_deforestation["CATEGORIA"].unique()

        # Combo box para seleccionar la categoría
        categoria_seleccionada = st.selectbox("Selecciona una categoría", categorias)

        # Filtrar datos por la categoría seleccionada
        categoria_data = sum_area_deforestation[sum_area_deforestation["CATEGORIA"] == categoria_seleccionada]

        # Verificar si hay datos para la categoría seleccionada
        if categoria_data.empty:
            st.warning(f"No hay datos para la categoría: {categoria_seleccionada}")
        else:
            # Crear gráfico de dispersión
            fig = px.scatter(
                categoria_data,
                x="ANP",
                y="AREA_DEFO",
                size="AREA_DEFO",
                color="ANP",
                hover_name="ANP",
                title=f"Área Deforestada (ha) en {categoria_seleccionada} (2021-2023)",
                labels={"ANP": "Área Natural Protegida", "AREA_DEFO": "Área Deforestada (ha)"},
                size_max=60,
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            # Mostrar gráfico en Streamlit
            st.plotly_chart(fig)

        # Mostrar información adicional
        st.markdown(f"*Mostrando datos para la categoría: {categoria_seleccionada}.*")
     
      # Diccionario con las descripciones de cada categoría
         descripciones = {
             "Bosque De Protección": """
             Áreas designadas para proteger suelos y recursos hídricos esenciales, actuando como barreras naturales contra procesos como la erosión, deslizamientos y sequías. Su manejo está enfocado en la preservación de ecosistemas y el control de actividades humanas que puedan afectar su equilibrio.
 
             **¿DE QUÉ MANERA AFECTA LA DEFORESTACIÓN?**  
             La pérdida de cobertura vegetal en estas áreas acelera la erosión, degrada los suelos y afecta el ciclo hidrológico, aumentando el riesgo de inundaciones y deslizamientos en comunidades cercanas.
             """,
             "Parque Nacional": """
             Espacios de gran extensión donde se conserva la diversidad biológica y paisajes de alto valor escénico. Las actividades están restringidas principalmente al ecoturismo, la educación ambiental y la investigación científica. Representan ecosistemas clave y son hábitats de especies endémicas o en peligro.
 
             **¿DE QUÉ MANERA AFECTA LA DEFORESTACIÓN?**  
             La tala afecta la biodiversidad, destruyendo hábitats esenciales y poniendo en peligro de extinción a especies únicas. Además, se pierde la capacidad de los bosques para regular el clima y almacenar carbono.
             """,
             "Reserva Comunal": """
             Áreas donde las comunidades indígenas o locales participan en la gestión y conservación de los recursos naturales. Buscan armonizar la protección de la biodiversidad con el uso tradicional sostenible, promoviendo actividades económicas como la recolección, pesca o ecoturismo, bajo un enfoque de respeto al entorno.
 
             **¿DE QUÉ MANERA AFECTA LA DEFORESTACIÓN?**  
             La destrucción de los ecosistemas compromete la disponibilidad de recursos para las comunidades, afectando su sustento y rompiendo el equilibrio entre actividades tradicionales y la conservación.
             """,
             "Reserva Nacional": """
             Zonas destinadas al uso sostenible de recursos naturales, como pesca, caza, recolección o forestación, siempre bajo una gestión adecuada para evitar el agotamiento. Su objetivo es conservar la biodiversidad y garantizar la sostenibilidad a largo plazo, permitiendo actividades económicas controladas.
 
             **¿DE QUÉ MANERA AFECTA LA DEFORESTACIÓN?**  
             La extracción descontrolada de madera y la expansión agrícola reducen la disponibilidad de recursos y alteran la capacidad de regeneración de los ecosistemas, afectando tanto a la biodiversidad como a las comunidades dependientes.
             """,
             "Santuario Histórico": """
             Áreas protegidas que albergan tanto riqueza cultural y arqueológica como biodiversidad significativa. Ejemplos notables son sitios con ruinas prehispánicas o lugares históricos rodeados de ecosistemas únicos, donde se combinan la conservación del patrimonio cultural y natural.
 
             **¿DE QUÉ MANERA AFECTA LA DEFORESTACIÓN?**  
             La tala ilegal y el cambio de uso del suelo degradan el entorno natural que complementa y protege los sitios históricos, afectando tanto el patrimonio cultural como la biodiversidad asociada.
             """,
             "Santuario Nacional": """
             Áreas que protegen ecosistemas frágiles o únicos con especies de flora y fauna de alto valor ecológico. Aquí, las actividades humanas están estrictamente limitadas para garantizar la conservación de los hábitats en su estado más natural posible.
 
             **¿DE QUÉ MANERA AFECTA LA DEFORESTACIÓN?**  
             En estos ecosistemas frágiles, cualquier pérdida de cobertura vegetal puede ser devastadora, eliminando especies vulnerables y alterando servicios ecosistémicos cruciales como la purificación del agua y la estabilidad del suelo.
             """,
             "Zonas Reservadas": """
             Espacios con características especiales que se encuentran en evaluación para definir su categoría definitiva dentro del Sistema Nacional de Áreas Protegidas. Mientras tanto, se aplican medidas provisionales de conservación para evitar impactos negativos y garantizar su protección.
 
             **¿DE QUÉ MANERA AFECTA LA DEFORESTACIÓN?**  
             La pérdida de bosques en estas áreas dificulta su evaluación y amenaza con destruir su valor antes de que puedan ser categorizadas. Esto pone en peligro tanto su biodiversidad como su potencial para la conservación.
             """
         }

        # Mostrar descripción según la categoría seleccionada
        if categoria_seleccionada in descripciones:
            st.markdown(descripciones[categoria_seleccionada])
        else:
            st.warning("No se encontró información adicional para esta categoría.")


# Sección: Conoce más
if menu == "Conoce más":
    st.header("¿Cómo ayudo a frenar la deforestación?")
    st.write("¡Conoce a SOSelva!")

    tab1, tab2, tab3 = st.tabs(["SOSelva", "Impacto Ambiental", "Cómo puedes ayudar"])

    # Pestaña 1: SOSelva
    with tab1:
        st.subheader("¿Qué es SOSelva?")
        st.write(
            "SOSelva es una iniciativa impulsada por el SERNANP y aliados estratégicos para "
            "proteger las áreas naturales protegidas de Perú, combatir la deforestación y promover "
            "el desarrollo sostenible."
        )
     
        st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center;">
            <img src="https://raw.githubusercontent.com/mcamilaa/streamlit_app/main/imagenes/soselva.jpeg" 
                 alt="SOSelva" style="width: 80%; max-width: 500px; height: auto; border-radius: 10px;">
        </div>
        """,
        unsafe_allow_html=True
    )

        st.markdown("### Acciones Principales de SOSelva:")
        st.write("""
        - Monitoreo de áreas naturales protegidas.
        - Promoción del turismo sostenible.
        - Desarrollo de actividades económicas sostenibles para comunidades locales.
        - Combate de delitos ambientales como el tráfico de fauna silvestre.
        """)
        st.markdown("### Aliados Estratégicos:")
        st.write("Profonanpe, SPDA, APECO, LATAM Airlines y otros.")
        
        st.info("Conoce más en el sitio oficial de [SERNANP](https://www.sernanp.gob.pe).")

    # Pestaña 2: Impacto Ambiental
    with tab2:
        st.subheader("Impacto Ambiental de la Deforestación")
        st.write(
            "La deforestación tiene consecuencias graves en la biodiversidad, el cambio climático "
            "y la sostenibilidad de las comunidades locales. Perú, al ser un país megadiverso, "
            "enfrenta desafíos significativos debido a la pérdida de cobertura forestal."
        )
        st.markdown("### Consecuencias principales:")
        st.write("""
        - Pérdida de hábitats para especies endémicas.
        - Incremento de emisiones de gases de efecto invernadero.
        - Erosión del suelo y pérdida de servicios ecosistémicos.
        """)
        st.image("https://raw.githubusercontent.com/mcamilaa/streamlit_app/refs/heads/main/imagenes/impacto.jpg", 
                 caption="Impacto de la deforestación en ecosistemas vulnerables", use_column_width=True)

    # Pestaña 3: Cómo puedes ayudar
    with tab3:
        st.subheader("¿Cómo puedes ayudar?")
        st.write(
            "La protección de nuestros bosques es una tarea colectiva. Aquí hay algunas maneras en las que puedes contribuir:"
        )
        st.markdown("### Opciones para contribuir:")
        st.write("""
        - 🌱 Participa como voluntario en programas de reforestación.
        - 💰 Apoya iniciativas como SOSelva mediante donaciones o difusión.
        - 📉 Reduce tu consumo de productos asociados con la deforestación (como madera ilegal).
        - 📢 Promueve el ecoturismo y las prácticas sostenibles.
        """)
        st.success("**Recuerda que** ¡Cada acción cuenta para proteger nuestras áreas naturales protegidas 😊!")

