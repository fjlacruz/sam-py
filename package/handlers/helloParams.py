import json

def handle(event, context):
    """Handler para la ruta /hello/{param}.

    Este handler extrae el parámetro de la ruta y lo retorna como parte de la respuesta.

    Parameters
    ----------
    event : dict
        El evento recibido por la función Lambda. Contiene detalles como el path y otros datos.

    context : object
        Información del contexto de ejecución de la Lambda.

    Returns
    -------
    dict
        Respuesta formateada para API Gateway con el parámetro extraído.
    """
    # Extraer el path desde el evento
    path = event.get("path", "")

    # Extraer el valor de {param} de la ruta
    try:
        param = path.split("/")[-1]  # Última parte del path
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Hello, {param}!",
                "param": param
            }),
        }
    except Exception as e:
        print(f"Error al procesar el parámetro: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error processing the parameter",
                "error": str(e),
            }),
        }
