import os
import pandas as pd
import streamlit as st

# -----------------------------------
# Configuración general
# -----------------------------------
st.set_page_config(
    page_title="Webshop Recommender",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------------
# Estilos simples
# -----------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: #16325B;
    }
    .subtitle {
        font-size: 1rem;
        color: #4F709C;
        margin-bottom: 1.2rem;
    }
    .card {
        background-color: #F7FAFC;
        border: 1px solid #D9E2EC;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .card h4 {
        margin: 0 0 8px 0;
        color: #102A43;
    }
    .small-text {
        color: #486581;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Carga de datos (CORREGIDO)
# -----------------------------------
@st.cache_data
def load_data():
    path = "data/processed/recomendaciones_modelo.csv"
    return pd.read_csv(path)

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
# Header
# -----------------------------------
st.markdown('<div class="main-title">🛒 Sistema de recomendación por macrogrupos</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Demo funcional · Sprint 2 · Recomendaciones basadas en co-ocurrencia y valor económico</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# -----------------------------------
# Sidebar
# -----------------------------------
st.sidebar.header("Configuración de la demo")

grupos = sorted(recomendaciones[col_origen].dropna().unique())
grupo_seleccionado = st.sidebar.selectbox("Seleccionar grupo origen", grupos)
top_k = st.sidebar.slider("Cantidad de recomendaciones", min_value=3, max_value=10, value=5)

# -----------------------------------
# Filtrado
# -----------------------------------
df_grupo = (
    recomendaciones[recomendaciones[col_origen] == grupo_seleccionado]
    .sort_values(col_score, ascending=False)
    .head(top_k)
    .copy()
)

# -----------------------------------
# Resumen superior
# -----------------------------------
top1, top2, top3 = st.columns(3)

with top1:
    st.metric("Grupo origen", grupo_seleccionado)

with top2:
    st.metric("Recomendaciones mostradas", len(df_grupo))

with top3:
    if not df_grupo.empty:
        st.metric("Score promedio", round(df_grupo[col_score].mean(), 3))
    else:
        st.metric("Score promedio", 0)

st.markdown("---")

# -----------------------------------
# Cards principales
# -----------------------------------
st.subheader("Top recomendaciones")

if df_grupo.empty:
    st.warning("No hay recomendaciones disponibles para este grupo.")
else:
    card_cols = st.columns(min(3, len(df_grupo)))

    for idx, (_, row) in enumerate(df_grupo.head(3).iterrows()):
        with card_cols[idx]:
            st.markdown(
                f"""
                <div class="card">
                    <h4>{row[col_reco]}</h4>
                    <div class="small-text"><b>Score:</b> {round(row[col_score], 3)}</div>
                    <div class="small-text"><b>Frecuencia:</b> {row[col_freq]}</div>
                    <div class="small-text"><b>Ticket promedio:</b> {round(row[col_ticket], 2)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------
# Layout principal
# -----------------------------------
left, right = st.columns([1.4, 1])

with left:
    st.markdown("### Tabla completa")
    if not df_grupo.empty:
        st.dataframe(
            df_grupo[[col_reco, col_score, col_freq, col_ticket]],
            use_container_width=True
        )

with right:
    st.markdown("### Lectura rápida")
    if not df_grupo.empty:
        mejor_reco = df_grupo.iloc[0][col_reco]
        st.success(f"La recomendación principal para **{grupo_seleccionado}** es **{mejor_reco}**.")

        st.info(
            "El ranking combina señales de frecuencia de co-ocurrencia y valor económico del grupo recomendado."
        )

# -----------------------------------
# Gráfico
# -----------------------------------
if not df_grupo.empty:
    st.markdown("### Ranking visual")
    chart_df = df_grupo[[col_reco, col_score]].set_index(col_reco)
    st.bar_chart(chart_df)

# -----------------------------------
# Explicación del modelo
# -----------------------------------
st.markdown("---")
exp1, exp2 = st.columns(2)

with exp1:
    st.markdown("### ¿Qué hace el modelo?")
    st.write(
        """
        El sistema recomienda macrogrupos complementarios a partir de compras históricas.
        No se basa únicamente en popularidad, sino en relaciones detectadas entre grupos
        que tienden a aparecer juntos.
        """
    )

with exp2:
    st.markdown("### Limitaciones actuales")
    st.write(
        """
        - No hay personalización a nivel usuario.  
        - Algunos grupos tienen menor cobertura por baja frecuencia.  
        - El baseline supera al modelo en métricas tradicionales, pero el modelo aporta una lógica más orientada a negocio.
        """
    )

st.markdown("---")
st.caption("Proyecto Webshop · Sprint 2")