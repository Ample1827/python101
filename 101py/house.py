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
# Helper to format prices
def format_mxn(valor):
    if valor >= 1e6:
        return f"${valor / 1e6:.2f} millones"
    elif valor >= 1e3:
        return f"${valor / 1e3:.1f} mil"
    return f"${valor:.0f}"

# -------------------------------
# Estadística descriptiva

def resumen_estadistico(df):
    print("\n=== Estadísticas descriptivas de precios y terreno (m²) ===")
    cols = ['precio', 'terreno_m2']
    stats = pd.DataFrame({
        'Media': df[cols].mean(),
        'Mediana': df[cols].median(),
        'Moda': df[cols].mode().iloc[0],
        'Desviación estándar': df[cols].std()
    })
    print(stats.round(2).to_string())

    print("\n=== Precio promedio por ciudad ===")
    avg_ciudad = df.groupby('ciudad')['precio'].mean().sort_values(ascending=False)
    for ciudad, precio in avg_ciudad.items():
        print(f"{ciudad}: {format_mxn(precio)} MXN")

    print("\n=== Matriz de correlación ===")
    corr = df[['precio', 'habitaciones', 'baños', 'terreno_m2', 'antiguedad']].corr()
    print(corr.round(2).to_string())
    return corr

# -------------------------------
# Visualizaciones

def visualizar(df, corr):
    sns.set_style("whitegrid")

    plt.figure(figsize=(10, 6))
    sns.histplot(df['precio'] / 1e6, kde=True, bins=40, color='cornflowerblue')
    plt.title("Distribución de precios de casas")
    plt.xlabel("Precio en millones de MXN")
    plt.ylabel("Cantidad de casas")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Mapa de calor de correlaciones entre variables")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='ciudad', y=df['precio'] / 1e6)
    plt.xticks(rotation=45)
    plt.ylabel("Precio (millones de MXN)")
    plt.title("Distribución de precios por ciudad")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x='habitaciones', y=df['precio'] / 1e6)
    plt.ylabel("Precio (millones de MXN)")
    plt.title("Precios por número de habitaciones")
    plt.tight_layout()
    plt.show()

# -------------------------------
# Extraer datos de la pregunta

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
# Lógica de respuesta

def responder_pregunta(pregunta):
    doc = nlp(pregunta.lower())
    if "precio" in pregunta or "cuánto" in pregunta:
        num, zona = extraer_info(pregunta)
        if num and zona:
            matches = df[(df['habitaciones'] == num) & df['ciudad'].str.contains(zona, case=False)]
            if not matches.empty:
                promedio = matches['precio'].mean()
                return f"Una casa de {num} habitaciones en {zona} cuesta en promedio {format_mxn(promedio)} MXN."
            return "No se encontraron casas con esas características."
        return "Por favor indica el número de habitaciones y la ciudad."

    elif "segura" in pregunta or "zona más segura" in pregunta:
        seguras = df[df['zona_segura'] == True]
        if not seguras.empty:
            ciudad_segura = seguras.groupby('ciudad')['precio'].mean().sort_values().index[0]
            precio = seguras.groupby('ciudad')['precio'].mean().sort_values().iloc[0]
            return f"La ciudad más segura con precios bajos es {ciudad_segura}, con un precio promedio de {format_mxn(precio)} MXN."
        return "No hay datos suficientes sobre zonas seguras."

    return "No entendí tu pregunta. Intenta con: ¿Cuánto cuesta una casa de 3 habitaciones en Puebla?"

# -------------------------------
# Chatbot interactivo

def chatbot():
    print("\n=== ChatBot de Bienes Raíces en México ===")
    print("Puedes hacer preguntas como:")
    print("- ¿Cuánto cuesta una casa de 3 habitaciones en Puebla?")
    print("- ¿Cuál es la ciudad más segura con precios bajos?")
    print("\nCiudades disponibles:")
    print(", ".join(sorted(df['ciudad'].unique())))

    while True:
        print("\n--- Menú ---")
        print("1. Consultar precio promedio de una casa")
        print("2. Consultar ciudad más segura con precios bajos")
        print("3. Escribir mi propia pregunta")
        print("4. Salir")
        opcion = input("Selecciona una opción (1-4): ").strip()

        if opcion == "4":
            print("Gracias por usar el chatbot. ¡Hasta luego!")
            break
        elif opcion == "1":
            pregunta = input("Ejemplo: ¿Cuánto cuesta una casa de 3 habitaciones en Guadalajara?\n> ")
            print(responder_pregunta(pregunta))
        elif opcion == "2":
            print(responder_pregunta("zona más segura con precio bajo"))
        elif opcion == "3":
            pregunta = input("Escribe tu pregunta:\n> ")
            print(responder_pregunta(pregunta))
        else:
            print("Opción no válida. Intenta de nuevo.")

# -------------------------------
# MAIN

if __name__ == "__main__":
    corr = resumen_estadistico(df)
    visualizar(df, corr)
    chatbot()
