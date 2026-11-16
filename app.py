# app.py — Página de Streamlit con los 5 gráficos de ventas de Superstore (datos de Kaggle)
# Ejecutar en local:   streamlit run app.py
#
# Cómo funciona Streamlit: lee este archivo de arriba abajo y "pinta" en la página web
# cada st.algo() que encuentra. Cada vez que el usuario toca un filtro, vuelve a ejecutar
# el script entero con el nuevo valor.
#
# Cada gráfico tiene 3 pestañas:
#   - Streamlit  → gráfico PROPIO de Streamlit (st.bar_chart, st.line_chart, st.scatter_chart): interactivo
#   - Matplotlib → la misma versión que en el cuaderno, mostrada con st.pyplot
#   - Seaborn    → la misma versión que en el cuaderno, mostrada con st.pyplot

from pathlib import Path          # Path: construir la ruta al CSV a partir de la carpeta de este archivo

import matplotlib.pyplot as plt   # matplotlib: la librería base que dibuja
import matplotlib.ticker as mtick # ticker: formato de los números de los ejes
import numpy as np                # numpy: posiciones de las columnas apiladas
import pandas as pd               # pandas: leer y filtrar los datos
import seaborn as sns             # seaborn: gráficos estadísticos sobre matplotlib
import streamlit as st            # streamlit: convierte el script en página web

# ---------------------------------------------------------------------------
# Configuración de la página (tiene que ser la primera llamada a st.)
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Superstore · 5 gráficos", page_icon="📊", layout="wide")

# ---------------------------------------------------------------------------
# Estilo: configuración del cuaderno de clase (matplotlib.ipynb)
# ---------------------------------------------------------------------------
SURFACE = "#fcfcfb"
TEXT, TEXT2, GRID = "#0b0b0b", "#52514e", "#e3e2de"
PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
    "text.color": TEXT, "axes.titlelocation": "left", "axes.titleweight": "semibold",
    "axes.titlesize": 12, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "axes.axisbelow": True, "grid.color": GRID, "grid.linewidth": 1,
    "lines.linewidth": 2, "lines.solid_capstyle": "round", "legend.frameon": False, "font.size": 10,
})


def xgrid(ax):   # rejilla solo vertical
    ax.grid(False)
    ax.grid(True, axis="x")


def ygrid(ax):   # rejilla solo horizontal
    ax.grid(False)
    ax.grid(True, axis="y")


miles = mtick.FuncFormatter(lambda v, pos: f"{v/1000:,.0f}k".replace(",", "."))   # 150000 → "150k"

# Traducciones (inglés → español)
CATEGORIAS = {"Furniture": "Muebles", "Office Supplies": "Material de oficina", "Technology": "Tecnología"}
SUBCATEGORIAS = {
    "Phones": "Teléfonos", "Chairs": "Sillas", "Storage": "Almacenaje", "Tables": "Mesas",
    "Binders": "Archivadores", "Machines": "Máquinas", "Accessories": "Accesorios", "Copiers": "Copiadoras",
    "Bookcases": "Estanterías", "Appliances": "Electrodomésticos", "Furnishings": "Decoración",
    "Paper": "Papel", "Supplies": "Suministros", "Art": "Material de dibujo", "Envelopes": "Sobres",
    "Labels": "Etiquetas", "Fasteners": "Grapas y clips",
}
REGIONES = {"West": "Oeste", "East": "Este", "Central": "Centro", "South": "Sur"}
SEGMENTOS = {"Consumer": "Particulares", "Corporate": "Empresas", "Home Office": "Oficina en casa"}
ORDEN_CAT = ["Tecnología", "Muebles", "Material de oficina"]
COLOR_CAT = dict(zip(ORDEN_CAT, PAL))   # cada categoría siempre con su color


# ---------------------------------------------------------------------------
# Carga y limpieza de datos (igual que en el cuaderno)
# ---------------------------------------------------------------------------
@st.cache_data   # guarda el resultado: el CSV se lee una vez, no en cada recarga de la página
def cargar_datos():
    ruta = Path(__file__).parent / "datos" / "superstore.csv"
    df = pd.read_csv(ruta, encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")
    df = df.dropna(subset=["Order Date", "Ship Date", "Category", "Sub-Category", "Customer ID", "Sales", "Profit"])
    df["Año"] = df["Order Date"].dt.year.astype(str)
    df["Días de envío"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Categoría"] = df["Category"].map(CATEGORIAS)
    df["Subcategoría"] = df["Sub-Category"].map(SUBCATEGORIAS)
    df["Región"] = df["Region"].map(REGIONES)
    df["Segmento"] = df["Segment"].map(SEGMENTOS)
    return df


def mostrar(fig):
    """Muestra una figura de matplotlib/seaborn en la página y la cierra para no gastar memoria."""
    st.pyplot(fig)
    plt.close(fig)


df = cargar_datos()

# ---------------------------------------------------------------------------
# Cabecera
# ---------------------------------------------------------------------------
st.title("📊 Ventas de Superstore — 5 gráficos")
st.caption(
    "Datos: Superstore Dataset (Kaggle) · Tipos de gráfico del cuaderno de clase (Chart Chooser) · "
    "Cada gráfico en Streamlit, Matplotlib y Seaborn · Lorena Herranz Pascual"
)

# ---------------------------------------------------------------------------
# Filtros (barra lateral)
# ---------------------------------------------------------------------------
st.sidebar.header("Filtros")
regiones = st.sidebar.multiselect("Región", sorted(df["Región"].unique()), default=sorted(df["Región"].unique()))
segmentos = st.sidebar.multiselect("Segmento de cliente", sorted(df["Segmento"].unique()),
                                   default=sorted(df["Segmento"].unique()))

datos = df[df["Región"].isin(regiones) & df["Segmento"].isin(segmentos)]   # filas que cumplen los dos filtros

if datos.empty:
    st.warning("No hay datos con esos filtros. Marca al menos una región y un segmento.")
    st.stop()   # detiene el script: no se dibuja nada más

# ---------------------------------------------------------------------------
# Indicadores
# ---------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Líneas de pedido", f"{len(datos):,}".replace(",", "."))
c2.metric("Ventas", f"{datos['Sales'].sum() / 1000:,.0f}k $".replace(",", "."))
c3.metric("Beneficio", f"{datos['Profit'].sum() / 1000:,.0f}k $".replace(",", "."))
c4.metric("Clientes", f"{datos['Customer ID'].nunique():,}".replace(",", "."))
st.divider()

# ===========================================================================
# 1 — Single Bar Chart
# ===========================================================================
st.header("1 · Single Bar Chart: ventas por subcategoría")
st.caption("Comparación estática. Barras ordenadas de mayor a menor; el eje empieza en 0.")

ventas_sub = (datos.groupby("Subcategoría", as_index=False)["Sales"].sum()
                   .sort_values("Sales", ascending=False))
tab_st, tab_mpl, tab_sns = st.tabs(["Streamlit", "Matplotlib", "Seaborn"])

with tab_st:   # lo que va dentro de este "with" aparece en la pestaña Streamlit
    st.bar_chart(ventas_sub, x="Subcategoría", y="Sales", horizontal=True,
                 sort="-Sales",                 # de mayor a menor ("-" = descendente)
                 color=PAL[0], x_label="Ventas ($)", y_label="", height=480)

with tab_mpl:
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(ventas_sub["Subcategoría"], ventas_sub["Sales"], color=PAL[0], height=0.55)
    ax.invert_yaxis()
    ax.bar_label(bars, labels=[f"{v/1000:.0f}k" for v in ventas_sub["Sales"]], padding=4, color=TEXT)
    ax.set_xlim(0, ventas_sub["Sales"].max() * 1.15)
    ax.xaxis.set_major_formatter(miles)
    xgrid(ax)
    ax.set_xlabel("Ventas ($)")
    ax.set_title("Ventas por subcategoría · Matplotlib")
    mostrar(fig)

with tab_sns:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=datos, x="Sales", y="Subcategoría", estimator="sum", errorbar=None,
                order=ventas_sub["Subcategoría"], color=PAL[0], width=0.55, ax=ax)
    ax.bar_label(ax.containers[0], labels=[f"{v/1000:.0f}k" for v in ventas_sub["Sales"]], padding=4, color=TEXT)
    ax.set_xlim(0, ventas_sub["Sales"].max() * 1.15)
    ax.xaxis.set_major_formatter(miles)
    xgrid(ax)
    ax.set(xlabel="Ventas ($)", ylabel="", title="Ventas por subcategoría · Seaborn")
    mostrar(fig)

# ===========================================================================
# 2 — Line Chart (muchos periodos)
# ===========================================================================
st.header("2 · Line Chart: ventas mensuales")
st.caption("Cambio en el tiempo, muchos periodos. Pasa el ratón por la línea (pestaña Streamlit) para ver cada mes.")

ventas_mes = datos.set_index("Order Date")["Sales"].resample("MS").sum().reset_index()   # suma por mes
tab_st, tab_mpl, tab_sns = st.tabs(["Streamlit", "Matplotlib", "Seaborn"])

with tab_st:
    st.line_chart(ventas_mes, x="Order Date", y="Sales", color=PAL[0], x_label="", y_label="Ventas ($)")

with tab_mpl:
    x, y = ventas_mes["Order Date"], ventas_mes["Sales"]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(x, y, color=PAL[0])
    ax.plot(x.iloc[-1], y.iloc[-1], "o", color=PAL[0], markersize=8, markeredgecolor=SURFACE, markeredgewidth=2)
    ax.annotate(f"{y.iloc[-1]/1000:.0f}k", (x.iloc[-1], y.iloc[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", color=TEXT)
    ax.set_ylim(0, y.max() * 1.1)
    ax.yaxis.set_major_formatter(miles)
    ygrid(ax)
    ax.set_ylabel("Ventas ($)")
    ax.set_title("Ventas mensuales · Matplotlib")
    mostrar(fig)

with tab_sns:
    fig, ax = plt.subplots(figsize=(9, 3.6))
    sns.lineplot(data=ventas_mes, x="Order Date", y="Sales", color=PAL[0], ax=ax)
    ult = ventas_mes.iloc[-1]
    ax.plot(ult["Order Date"], ult["Sales"], "o", color=PAL[0], markersize=8, markeredgecolor=SURFACE, markeredgewidth=2)
    ax.annotate(f"{ult['Sales']/1000:.0f}k", (ult["Order Date"], ult["Sales"]), xytext=(8, 0),
                textcoords="offset points", va="center", color=TEXT)
    ax.set_ylim(0, ventas_mes["Sales"].max() * 1.1)
    ax.yaxis.set_major_formatter(miles)
    ygrid(ax)
    ax.set(xlabel="", ylabel="Ventas ($)", title="Ventas mensuales · Seaborn")
    mostrar(fig)

# ===========================================================================
# 3 — Scatter Chart
# ===========================================================================
st.header("3 · Scatter Chart: ventas frente a beneficio por cliente")
st.caption("Relación. Cada punto es un cliente; los que quedan por debajo de 0 dejan pérdidas.")

clientes = datos.groupby("Customer ID", as_index=False)[["Sales", "Profit"]].sum()   # un punto por cliente
tab_st, tab_mpl, tab_sns = st.tabs(["Streamlit", "Matplotlib", "Seaborn"])

with tab_st:
    st.scatter_chart(clientes, x="Sales", y="Profit", color=PAL[0],
                     x_label="Ventas totales del cliente ($)", y_label="Beneficio total del cliente ($)")

with tab_mpl:
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.scatter(clientes["Sales"], clientes["Profit"], s=30, color=PAL[0], alpha=0.7, edgecolor=SURFACE, linewidth=1)
    ax.axhline(0, color=TEXT2, linewidth=1)
    ax.xaxis.set_major_formatter(miles)
    ax.yaxis.set_major_formatter(miles)
    ax.set_xlabel("Ventas totales del cliente ($)")
    ax.set_ylabel("Beneficio total del cliente ($)")
    ax.set_title("Ventas frente a beneficio por cliente · Matplotlib", loc="center")
    mostrar(fig)

with tab_sns:
    fig, ax = plt.subplots(figsize=(8, 4.4))
    sns.scatterplot(data=clientes, x="Sales", y="Profit", s=30, color=PAL[0], alpha=0.7,
                    edgecolor=SURFACE, linewidth=1, ax=ax)
    ax.axhline(0, color=TEXT2, linewidth=1)
    ax.xaxis.set_major_formatter(miles)
    ax.yaxis.set_major_formatter(miles)
    ax.set(xlabel="Ventas totales del cliente ($)", ylabel="Beneficio total del cliente ($)")
    ax.set_title("Ventas frente a beneficio por cliente · Seaborn", loc="center")
    mostrar(fig)

# ===========================================================================
# 4 — Column Histogram
# ===========================================================================
st.header("4 · Column Histogram: días de envío")
st.caption("Distribución. Cuántas líneas de pedido se envían en cada número de días.")

dias = datos["Días de envío"]
tab_st, tab_mpl, tab_sns = st.tabs(["Streamlit", "Matplotlib", "Seaborn"])

with tab_st:
    # Streamlit no tiene histograma propio: contamos cuántas hay en cada número de días
    # y lo pintamos con st.bar_chart (con números enteros es lo mismo que un histograma)
    conteo = dias.value_counts().sort_index()   # value_counts cuenta repeticiones; sort_index ordena por día
    st.bar_chart(conteo, color=PAL[0], x_label="Días entre el pedido y el envío", y_label="Líneas de pedido")

with tab_mpl:
    bordes = np.arange(dias.min() - 0.5, dias.max() + 1.5, 1)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.hist(dias, bins=bordes, color=PAL[0], edgecolor=SURFACE, linewidth=2)
    ax.set_xticks(range(dias.min(), dias.max() + 1))
    ax.set_xlabel("Días entre el pedido y el envío")
    ax.set_ylabel("Líneas de pedido")
    ygrid(ax)
    ax.set_title("Distribución de los días de envío · Matplotlib")
    mostrar(fig)

with tab_sns:
    fig, ax = plt.subplots(figsize=(8, 3.6))
    sns.histplot(data=datos, x="Días de envío", discrete=True, color=PAL[0],
                 edgecolor=SURFACE, linewidth=2, alpha=1, ax=ax)
    ax.set_xticks(range(dias.min(), dias.max() + 1))
    ax.set(xlabel="Días entre el pedido y el envío", ylabel="Líneas de pedido")
    ygrid(ax)
    ax.set_title("Distribución de los días de envío · Seaborn")
    mostrar(fig)

# ===========================================================================
# 5 — Stacked Column Chart
# ===========================================================================
st.header("5 · Stacked Column Chart: ventas por año y categoría")
st.caption("Composición, pocos periodos. Altura total = ventas del año; cada segmento = una categoría.")

tabla = datos.pivot_table(index="Año", columns="Categoría", values="Sales", aggfunc="sum")[ORDEN_CAT]
tab_st, tab_mpl, tab_sns = st.tabs(["Streamlit", "Matplotlib", "Seaborn"])

with tab_st:
    st.bar_chart(tabla,                                    # filas = años, columnas = categorías
                 stack=True,                               # apilar los segmentos
                 color=[COLOR_CAT[c] for c in ORDEN_CAT],  # un color por categoría, en el mismo orden
                 x_label="", y_label="Ventas ($)")

with tab_mpl:
    x = np.arange(len(tabla))
    bottom = np.zeros(len(tabla))
    fig, ax = plt.subplots(figsize=(8, 4))
    for cat in ORDEN_CAT:
        ax.bar(x, tabla[cat], bottom=bottom, width=0.55, color=COLOR_CAT[cat],
               edgecolor=SURFACE, linewidth=2, label=cat)
        bottom += tabla[cat].values
    ax.set_xticks(x, tabla.index)
    ax.yaxis.set_major_formatter(miles)
    ax.set_ylabel("Ventas ($)")
    ygrid(ax)
    ax.legend(ncols=3, loc="lower left", bbox_to_anchor=(0, 1.1))
    ax.set_title("Ventas por año y categoría · Matplotlib", loc="center")
    mostrar(fig)

with tab_sns:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(data=datos.sort_values("Año"), x="Año", hue="Categoría", hue_order=ORDEN_CAT[::-1],
                 palette=COLOR_CAT, weights="Sales", multiple="stack", shrink=0.55,
                 edgecolor=SURFACE, linewidth=2, alpha=1, ax=ax)
    ax.yaxis.set_major_formatter(miles)
    ax.set(xlabel="", ylabel="Ventas ($)")
    ygrid(ax)
    sns.move_legend(ax, "lower left", bbox_to_anchor=(0, 1.1), ncols=3, title=None)
    ax.set_title("Ventas por año y categoría · Seaborn", loc="center")
    mostrar(fig)

# ---------------------------------------------------------------------------
# Tabla de datos (desplegable)
# ---------------------------------------------------------------------------
st.divider()
with st.expander("Ver los datos filtrados"):
    st.dataframe(datos[["Order ID", "Order Date", "Región", "Segmento", "Categoría", "Subcategoría",
                        "Sales", "Quantity", "Discount", "Profit"]], width="stretch", hide_index=True)
