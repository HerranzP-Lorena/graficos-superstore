# 5 gráficos con Matplotlib, Seaborn y Streamlit — Ventas de Superstore

**Autora:** Lorena Herranz Pascual

**Enunciado:** elegir 5 gráficos y hacer un cuaderno que los muestre con **Matplotlib** y, en el mismo cuaderno, con **Seaborn**. Después, mostrar esos 5 gráficos en una página con **Streamlit**.

- 📓 **Cuaderno:** [`graficos_matplotlib_seaborn.ipynb`](graficos_matplotlib_seaborn.ipynb)
- 🌐 **Página de Streamlit:** _PEGAR AQUÍ EL ENLACE DE STREAMLIT_

## Los 5 gráficos

Tipos elegidos del cuaderno de clase `matplotlib.ipynb` (*Chart Chooser*), uno por familia, con su misma configuración de estilo.

| # | Gráfico | Familia | Matplotlib | Seaborn | Streamlit |
|---|---|---|---|---|---|
| 1 | Single Bar Chart | Comparación | `ax.barh` | `sns.barplot(estimator="sum")` | `st.bar_chart(horizontal=True)` |
| 2 | Line Chart | Cambio en el tiempo | `ax.plot` | `sns.lineplot` | `st.line_chart` |
| 3 | Scatter Chart | Relación | `ax.scatter` | `sns.scatterplot` | `st.scatter_chart` |
| 4 | Column Histogram | Distribución | `ax.hist` | `sns.histplot(discrete=True)` | `st.bar_chart` del recuento |
| 5 | Stacked Column Chart | Composición | `ax.bar(bottom=…)` | `sns.histplot(multiple="stack")` | `st.bar_chart(stack=True)` |

En la página de Streamlit cada gráfico tiene 3 pestañas: versión propia de Streamlit (interactiva), Matplotlib y Seaborn. También tiene filtros por región y por segmento de cliente.

## Datos

[Superstore Dataset — Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final): 9.994 líneas de pedido de una tienda de EE. UU. (2014–2017). Guardado como `datos/superstore.csv`; el archivo original se llama `Sample - Superstore.csv`.

## Estructura

```
├── graficos_matplotlib_seaborn.ipynb   # Cuaderno: cada gráfico en Matplotlib y en Seaborn
├── app.py                              # Página de Streamlit
├── datos/
│   └── superstore.csv                  # Datos de Kaggle
├── requirements.txt                    # Librerías que instala Streamlit Cloud
└── README.md
```

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```
