import spacy

def extraer_nombres_cliente(texto):
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(texto)

    nombres_cliente = []

    # Identificar entidades que podrían ser nombres de clientes
    for entidad in doc.ents:
        if entidad.label_ == "PER":  # "PER" se refiere a personas
            nombres_cliente.append(entidad.text)

    return nombres_cliente

# Ejemplo de uso
texto = "GYC 0998-0457 Casa Dr Martin Villa"
nombres_cliente = extraer_nombres_cliente(texto)

print("Nombres de clientes:", nombres_cliente)
