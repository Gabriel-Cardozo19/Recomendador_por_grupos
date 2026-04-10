import os
import pandas as pd
import streamlit as st

# -----------------------------------
# Configuración general
# -----------------------------------
st.set_page_config(
    page_title="Webshop | Cross-Selling",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------------
# Estilos
# -----------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #16325B;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #4F709C;
        margin-bottom: 1rem;
    }
    .big-card {
        background: linear-gradient(135deg, #EAF2FF, #F7FAFC);
        border: 1px solid #D9E2EC;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
    }
    .small-card {
        background-color: #F7FAFC;
        border: 1px solid #D9E2EC;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
        min-height: 120px;
    }
    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #102A43;
        margin-bottom: 8px;
    }
    .card-text {
        color: #486581;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Carga de datos
# -----------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "processed", "recomendaciones_modelo.csv")

    if not os.path.exists(data_path):
        st.error(f"No se encontró el archivo: {data_path}")
        st.stop()

    return pd.read_csv(data_path)

recomendaciones = load_data()

# -----------------------------------
# Columnas reales
# -----------------------------------
col_origen = "grupo_a"
col_reco = "grupo_b"
col_score = "score"
col_freq = "frecuencia"
col_ticket = "ticket_grupo_b"

# -----------------------------------
# Logo
# -----------------------------------
base_dir = os.path.dirname(os.path.dirname(__file__))
logo_path = os.path.join(base_dir, "app", "logo.png")

# -----------------------------------
# Diccionarios de negocio
# -----------------------------------
descripciones = {
    "Hogar": "Productos vinculados al hogar, decoración y confort, con potencial para compras complementarias.",
    "Recreación": "Categorías asociadas a familia, mascotas y estilo de vida recreativo.",
    "Tecnología": "Productos relacionados con electrónica, dispositivos y accesorios tecnológicos.",
    "Cuidado Personal": "Categorías de bienestar, higiene y consumo personal.",
    "Moda": "Productos vinculados a estilo, accesorios y consumo personal.",
    "Automotor": "Productos y accesorios asociados al vehículo.",
    "Viaje y accesorios": "Categorías vinculadas a movilidad, equipaje y viaje.",
    "Industria y construcción": "Herramientas y productos de uso técnico o funcional.",
    "Cultura y entretenimiento": "Categorías de lectura, música y ocio.",
    "Alimentos": "Productos de consumo alimenticio.",
    "Marketplace": "Grupo con menor participación relativa dentro del catálogo.",
    "other": "Grupo residual con menor volumen histórico."
}

# -----------------------------------
# Funciones helper
# -----------------------------------
def obtener_top_recomendaciones(grupo, top_k=5):
    return (
        recomendaciones[recomendaciones[col_origen] == grupo]
        .sort_values(col_score, ascending=False)
        .head(top_k)
        .copy()
    )

def mensaje_potencial(score_promedio):
    if score_promedio >= 0.60:
        return "Alta oportunidad comercial", "success"
    elif score_promedio >= 0.30:
        return "Oportunidad comercial media", "info"
    else:
        return "Oportunidad comercial acotada", "warning"

def insight_negocio(grupo_origen, grupo_recomendado):
    return (
        f"Los clientes que compran en {grupo_origen} también tienden a comprar en {grupo_recomendado}, "
        "lo que representa una oportunidad directa para aumentar el ticket promedio mediante cross-selling."
    )

def comparacion_promedio(df_total, df_grupo):
    promedio_catalogo = df_total[col_score].mean()
    promedio_grupo = df_grupo[col_score].mean() if not df_grupo.empty else 0

    if promedio_grupo > promedio_catalogo:
        return f"La fuerza de relación está por encima del promedio general del catálogo ({promedio_catalogo:.3f})."
    elif promedio_grupo < promedio_catalogo:
        return f"La fuerza de relación está por debajo del promedio general del catálogo ({promedio_catalogo:.3f})."
    else:
        return f"La fuerza de relación se encuentra alineada con el promedio general del catálogo ({promedio_catalogo:.3f})."

def fallback_popularidad(df, top_n=5):
    return (
        df.groupby(col_reco)[col_freq]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
        .rename(columns={
            col_reco: "Macrogrupo recomendado",
            col_freq: "Compras conjuntas"
        })
    )

def acciones_comerciales(grupo):
    base = {
        "Hogar": [
            ("🛒 Bundles", "Combinar productos complementarios para aumentar ticket."),
            ("🎯 Checkout", "Sugerencias cruzadas al momento de compra."),
            ("📢 Campañas", "Promociones enfocadas en consumo complementario.")
        ],
        "Tecnología": [
            ("🔌 Accesorios", "Impulsar ventas cruzadas de productos complementarios."),
            ("🎯 Upselling", "Sugerencias vinculadas a mejoras o extensiones de compra."),
            ("📢 Remarketing", "Campañas sobre categorías afines al interés del cliente.")
        ],
        "Recreación": [
            ("🎁 Combos", "Armar propuestas agrupadas para consumo recreativo."),
            ("🛍️ Checkout", "Sugerir compras adicionales por afinidad."),
            ("📢 Segmentación", "Campañas según estilo de vida y comportamiento.")
        ]
    }
    return base.get(grupo, [
        ("🛒 Bundles", "Probar combinaciones comerciales entre grupos relacionados."),
        ("🎯 Checkout", "Usar sugerencias cruzadas durante la compra."),
        ("📢 Campañas", "Activar promociones segmentadas por afinidad.")
    ])

# -----------------------------------
# Header
# -----------------------------------
logo_col, title_col = st.columns([1, 6])

with logo_col:
    if os.path.exists(logo_path):
        st.image(logo_path, width=85)

with title_col:
    st.markdown(
        '<div class="main-title">Recomendador de oportunidades de cross-selling</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Identificación de oportunidades comerciales entre macrogrupos para aumentar el ticket promedio</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# -----------------------------------
# Sidebar
# -----------------------------------
st.sidebar.header("Configuración")

grupos = sorted(recomendaciones[col_origen].dropna().unique())
grupo_seleccionado = st.sidebar.selectbox("Seleccionar macrogrupo origen", grupos)
top_k = st.sidebar.slider("Cantidad de recomendaciones", min_value=3, max_value=10, value=5)

if st.sidebar.button("Generar recomendación"):
    st.toast(f"Análisis generado para {grupo_seleccionado}")

# -----------------------------------
# Filtrado principal
# -----------------------------------
df_grupo = obtener_top_recomendaciones(grupo_seleccionado, top_k=top_k)

# -----------------------------------
# Métricas superiores
# -----------------------------------
metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric("Grupo analizado", grupo_seleccionado)

with metric2:
    if not df_grupo.empty:
        st.metric("Oportunidad principal", df_grupo.iloc[0][col_reco])
    else:
        st.metric("Oportunidad principal", "-")

with metric3:
    if not df_grupo.empty:
        st.metric("Fuerza de relación", f"{df_grupo[col_score].mean():.3f}")
    else:
        st.metric("Fuerza de relación", "0.000")

st.markdown("---")

# -----------------------------------
# Relación comercial detectada
# -----------------------------------
st.markdown("### Relación comercial detectada")
st.info(descripciones.get(grupo_seleccionado, "Grupo sin descripción cargada."))

# -----------------------------------
# Oportunidad principal sugerida
# -----------------------------------
if not df_grupo.empty:
    top_1 = df_grupo.iloc[0]
    texto_potencial, nivel = mensaje_potencial(df_grupo[col_score].mean())

    st.markdown(
        f"""
        <div class="big-card">
            <div class="card-title">Oportunidad principal sugerida</div>
            <div class="card-text">
                Para el macrogrupo <b>{grupo_seleccionado}</b>, la principal oportunidad detectada es <b>{top_1[col_reco]}</b>.<br><br>
                <b>Fuerza de relación:</b> {top_1[col_score]:.3f} &nbsp;&nbsp; | &nbsp;&nbsp;
                <b>Compras conjuntas:</b> {int(top_1[col_freq])} &nbsp;&nbsp; | &nbsp;&nbsp;
                <b>Ticket promedio asociado:</b> ${top_1[col_ticket]:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if nivel == "success":
        st.success(texto_potencial)
    elif nivel == "info":
        st.info(texto_potencial)
    else:
        st.warning(texto_potencial)
else:
    st.warning("No se encontraron recomendaciones para este macrogrupo.")

# -----------------------------------
# Principales oportunidades sugeridas
# -----------------------------------
st.markdown("### Principales oportunidades sugeridas")

if not df_grupo.empty:
    cards = st.columns(min(3, len(df_grupo.head(3))))

    for idx, (_, row) in enumerate(df_grupo.head(3).iterrows()):
        with cards[idx]:
            st.markdown(
                f"""
                <div class="small-card">
                    <div class="card-title">{row[col_reco]}</div>
                    <div class="card-text">
                        <b>Fuerza de relación:</b> {row[col_score]:.3f}<br>
                        <b>Compras conjuntas:</b> {int(row[col_freq])}<br>
                        <b>Ticket promedio:</b> ${row[col_ticket]:,.2f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------
# Detalle + Aplicación comercial
# -----------------------------------
left, right = st.columns([1.25, 1])

with left:
    st.markdown("### Detalle")
    if not df_grupo.empty:
        tabla = df_grupo[[col_reco, col_score, col_freq, col_ticket]].rename(columns={
            col_reco: "Macrogrupo recomendado",
            col_score: "Fuerza de relación",
            col_freq: "Compras conjuntas",
            col_ticket: "Ticket promedio"
        })
        tabla["Ticket promedio"] = tabla["Ticket promedio"].apply(lambda x: f"${x:,.2f}")
        st.dataframe(tabla, use_container_width=True)

with right:
    st.markdown("### Aplicación comercial")
    acciones = acciones_comerciales(grupo_seleccionado)

    cols_acciones = st.columns(3)
    for col, (titulo, desc) in zip(cols_acciones, acciones):
        with col:
            st.markdown(
                f"""
                <div class="small-card">
                    <div class="card-title">{titulo}</div>
                    <div class="card-text">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------
# Por qué esta relación importa
# -----------------------------------
st.markdown("### ¿Por qué esta relación importa?")
if not df_grupo.empty:
    st.success(insight_negocio(grupo_seleccionado, df_grupo.iloc[0][col_reco]))
    st.info(comparacion_promedio(recomendaciones, df_grupo))

    score_promedio = df_grupo[col_score].mean()
    st.markdown("### Nivel de oportunidad")
    st.progress(min(max(float(score_promedio), 0.0), 1.0))

# -----------------------------------
# Fallback si no hay recomendaciones
# -----------------------------------
if df_grupo.empty:
    st.markdown("### Alternativa sugerida")
    st.write(
        "Como no se detectaron relaciones suficientes para este grupo, se muestran opciones basadas en mayor volumen histórico de compras conjuntas."
    )
    fallback = fallback_popularidad(recomendaciones, top_n=5)
    st.dataframe(fallback, use_container_width=True)

# -----------------------------------
# Cierre
# -----------------------------------
st.markdown("---")
colA, colB = st.columns(2)

with colA:
    st.markdown("### ¿Qué aporta esta herramienta?")
    st.write(
        """
        Permite transformar datos históricos en oportunidades concretas de cross-selling, ayudando a:
        - identificar combinaciones con mayor potencial comercial
        - priorizar acciones para aumentar el ticket promedio
        - sostener decisiones de recomendación con evidencia de compra
        """
    )

with colB:
    st.markdown("### Próximos pasos")
    st.write(
        """
        Como evolución del proyecto, el sistema puede avanzar hacia:
        - recomendaciones más granulares
        - mayor nivel de personalización
        - integración con otras capas de activación comercial
        """
    )

st.markdown("---")
st.caption("Proyecto Webshop · Sprint 2 ")