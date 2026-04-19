# Sistema de Recomendacion por Venta Cruzada

Proyecto de ciencia de datos enfocado en el desarrollo de un sistema de recomendación para e-commerce, orientado a identificar relaciones de complementariedad entre categorías de productos y potenciar estrategias de cross-selling.

---

## Live Demo

👉 App interactiva: https://cross-selling-opportunities-recommender.streamlit.app/
👉 Dashboard (Power BI): https://app.powerbi.com/view?r=eyJrIjoiOTBhZDE5YjMtNjhhMy00NTM3LThmYmMtNGY1YTUzZWZlNDBlIiwidCI6IjU1MDNhYWMyLTdhMTUtNDZhZi1iNTIwLTJhNjc1YWQxZGYxNiIsImMiOjR9

---

## 🖥️ App Preview

![App Preview](images/app_preview.png)

---

## 💡 Business Problem

La plataforma no cuenta con un sistema que sugiera productos complementarios entre categorías relacionadas, lo que limita las oportunidades de venta cruzada y el incremento del ticket promedio.

---

## 📊 Exploratory Data Analysis (EDA)

Durante el análisis se identificaron los siguientes hallazgos:

- La mayoría de los pedidos contienen un solo producto → oportunidad de cross-selling  
- Existen diferencias significativas en el valor promedio entre categorías  
- Se detectaron patrones de co-compra entre grupos de productos  
- Algunas categorías presentan mayor potencial para aumentar el ticket promedio  

---

## 🧠 Methodology

El desarrollo se estructuró en las siguientes etapas:

### 🔹 Data Preparation (ETL)
- Integración de múltiples fuentes (orders, products, payments, reviews, customers)  
- Limpieza de datos  
- Construcción del dataset consolidado (`df_model`)  
- Agrupación de categorías en segmentos estratégicos  

### 🔹 Feature Engineering
- Relaciones de co-ocurrencia entre categorías  
- Frecuencia de compra conjunta  
- Incorporación del valor económico (ticket promedio)  
- Normalización de variables  

---

## 🤖 Models

### Modelo 1 – Baseline (Reglas)
- Basado en frecuencia de co-ocurrencia  
- Genera ranking de recomendaciones  
- Alta interpretabilidad  

### Modelo 2 – Machine Learning (Random Forest)
- Clasifica combinaciones de categorías  
- Utiliza variables económicas  
- Captura patrones más complejos  

---

## 📈 Results

- Accuracy: 0.66  
- Recall: 1.00  
- F1-score: 0.73  

El modelo prioriza la cobertura de oportunidades, funcionando como un MVP funcional.

---

## 📊 Insights

- Existen patrones claros de compra conjunta  
- No todas las combinaciones son igual de valiosas  
- El valor económico es clave en la recomendación  
- Es preferible recomendar más que perder oportunidades  

---

## 📌 Conclusion

El sistema desarrollado permite generar recomendaciones basadas en datos reales de compra, integrando frecuencia y valor económico.

Se trata de un MVP funcional que demuestra el potencial del uso de analítica para mejorar la experiencia del usuario y aumentar ingresos en e-commerce.

---

## 🛠️ Tech Stack

Python · Pandas · NumPy · Scikit-learn · Matplotlib · Seaborn · Streamlit · Power BI