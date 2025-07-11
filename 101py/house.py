import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import spacy

# Load spaCy model
nlp = spacy.load("es_core_news_sm")

# Load data
df = pd.read_excel("datos_casas_mexico.xlsx")

# -------------------------------
# ESTADÍSTICA DESCRIPTIVA

def resumen_estadistico(df):
    cols = ['precio', 'terreno_m2']
    stats = pd.DataFrame({
        'Media': df[cols].mean(),
        'Mediana': df[cols].median(),
        'Moda': df[cols].mode().iloc[0],
        'Desviación estándar': df[cols].std()
    })
    print("\nResumen de precios y terreno (m2):")
    print(stats.to_string())

    avg_ciudad = df.groupby('ciudad')['precio'].mean().sort_values(ascending=False)
    print("\nPrecio promedio por ciudad:")
    print(avg_ciudad.to_string())

    corr_cols = ['precio', 'habitaciones', 'baños', 'terreno_m2', 'antiguedad']
    corr = df[corr_cols].corr()
    print("\nMatriz de correlación:")
    print(corr.to_string())
    return corr

# -------------------------------
# VISUALIZACIONES

def visualizar(df, corr):
    sns.set_style("whitegrid")
    
    plt.figure(figsize=(8, 5))
    sns.histplot(df['precio'], kde=True, bins=30, color='skyblue')
    plt.title("Distribución de precios")
    plt.xlabel("Precio (MXN)")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(7, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Mapa de calor de correlaciones")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.boxplot(x='ciudad', y='precio', data=df)
    plt.xticks(rotation=45)
    plt.title("Precio por ciudad")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))
    sns.boxplot(x='habitaciones', y='precio', data=df)
    plt.title("Precio por número de habitaciones")
    plt.tight_layout()
    plt.show()

# -------------------------------
# INTENT DETECTION SETUP

INTENT_PRECIO = nlp("precio casa habitaciones zona")
INTENT_SEGURA = nlp("zona mas segura ciudad precio bajo")

# -------------------------------
# EXTRAER INFORMACIÓN DE LA PREGUNTA

def extraer_info(pregunta):
    doc = nlp(pregunta)
    num = None
    zona = None

    for tok in doc:
        if tok.like_num and num is None:
            try:
                num = int(tok.text)
            except ValueError:
                continue
    for ent in doc.ents:
        if ent.label_ in ("LOC", "GPE", "PROPN"):
            zona = ent.text.capitalize()
            break

    return num, zona

# -------------------------------
# LÓGICA DE RESPUESTA

def responder_pregunta(pregunta):
    doc = nlp(pregunta)
    sim_precio = doc.similarity(INTENT_PRECIO)
    sim_segura = doc.similarity(INTENT_SEGURA)

    if sim_precio > 0.6:
        num, zona = extraer_info(pregunta)
        if num and zona:
            matches = df[(df['habitaciones'] == num) & df['ciudad'].str.contains(zona, case=False)]
            if not matches.empty:
                promedio = matches['precio'].mean()
                return f"Una casa de {num} habitaciones en {zona} cuesta en promedio ${promedio:,.0f} MXN."
            return "No se encontraron casas con esas características."
        return "Por favor especifica cuántas habitaciones y la ciudad o zona."

    elif sim_segura > 0.6:
        seguras = df[df['zona_segura'] == True]
        if not seguras.empty:
            agrupado = seguras.groupby('ciudad')['precio'].mean().sort_values()
            ciudad_segura = agrupado.index[0]
            precio = agrupado.iloc[0]
            return f"La ciudad más segura con precios bajos es {ciudad_segura}, con un precio promedio de ${precio:,.0f} MXN."
        return "No hay datos suficientes sobre zonas seguras."

    return "No entendí tu pregunta. Intenta usar una de las opciones del menú."

# -------------------------------
# CHATBOT INTERACTIVO

def chatbot():
    print("\nChatBot activado - Bienvenido")
    while True:
        print("\nOpciones disponibles:")
        print("1. Consultar el precio promedio de una casa con X habitaciones en Y ciudad")
        print("2. Saber cuál es la ciudad más segura con precios accesibles")
        print("3. Salir")

        opcion = input("\nEscribe el número de opción o tu pregunta directamente: ").strip()

        if opcion == "3" or opcion.lower() == "salir":
            print("Gracias por usar el chatbot. Hasta luego.")
            break
        elif opcion == "1":
            ejemplo = input("Ejemplo: ¿Cuánto cuesta una casa de 3 habitaciones en Puebla?\n> ")
            print(responder_pregunta(ejemplo))
        elif opcion == "2":
            print(responder_pregunta("zona más segura con precio bajo"))
        elif len(opcion) > 10:
            print(responder_pregunta(opcion))
        else:
            print("Opción no válida. Intenta de nuevo.")

# -------------------------------
# MAIN

if __name__ == "__main__":
    corr = resumen_estadistico(df)
    visualizar(df, corr)
    chatbot()
