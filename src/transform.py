import json

def transform_data(input_data):
    transformed_data = []

    for product in input_data:
        transformed_product = {
            "fecha": product["fecha"],
            "imagen": product["imagen"],
            "nombre": product["nombre"],
            "ASIN": product["ASIN"],
            "EAN": product["EAN"],
            "historicos": {}
        }

        for vendedor, precio in zip(product["vendedores"], product["precios"]):
            if vendedor not in transformed_product["historicos"]:
                transformed_product["historicos"][vendedor] = []

            transformed_product["historicos"][vendedor].append({
                "fecha": product["fecha"],
                "precio": precio
            })

        transformed_data.append(transformed_product)

    return transformed_data

def main():
    with open('test7.json', 'r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)

    transformed_data = transform_data(input_data)

    with open('data.json', 'w', encoding='utf-8') as output_file:
        json.dump(transformed_data, output_file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()