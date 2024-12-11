import json
import importlib
import re

# Define un mapeo de rutas a módulos y funciones.
ROUTE_MAPPING = {
    "/hello": "handlers.hello.handle",
    "/goodbye": "handlers.goodbye.handle",
    "/hello/{param}": "handlers.helloParams.handle"
}

def lambda_handler(event, context):
    """Lambda function to handle API Gateway requests.

    This function processes incoming requests from API Gateway, dynamically imports the 
    appropriate handler based on the request path, and returns a response. It supports 
    error handling in case of issues with the handler import or function execution.

    Parameters
    ----------
    event : dict
        The event parameter contains the request data, including the path, which is used 
        to route the request to the appropriate handler.

    context : object
        The context parameter contains runtime information for the Lambda function, such as 
        request and response details.

    Returns
    -------
    dict
        A dictionary formatted in the API Gateway Lambda Proxy Output format. This dictionary 
        includes a status code and a body, which could contain the response message or an error.

    Notes
    -----
    The function dynamically imports and calls handler functions based on the mapped route. 
    If the handler cannot be imported or executed, a 500 error is returned. If no handler is 
    found for the requested path, a 404 error is returned.
    """
    # Extraer el path completo
    full_path = event.get('path', '').rstrip('/')  # Quitar cualquier '/' final

    # Buscar una ruta base que coincida con el mapeo
    matching_route = None
    for route in ROUTE_MAPPING:
        if re.match(f"^{route.replace('{param}', '[^/]+')}$", full_path):
            matching_route = route
            break

    # Ignorar solicitudes a favicon.ico
    if matching_route == '/favicon.ico':
        return {
            "statusCode": 204,  # No Content
            "body": None
        }

    # Log de la ruta que se está procesando
    print(f"Processing request path: {full_path}")

    # Verificar si la ruta coincidente está mapeada a un manejador
    handler_path = ROUTE_MAPPING.get(matching_route)
    if handler_path:
        try:
            # Importar y ejecutar el handler dinámicamente
            module_name, func_name = handler_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            handler_function = getattr(module, func_name)
            return handler_function(event, context)
        except (ImportError, AttributeError) as e:
            print(f"Error importing handler for path {matching_route}: {e}")
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": f"Error executing handler for path {matching_route}: {str(e)}"
                }),
            }
    else:
        # Retornar 404 si la ruta no está mapeada
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": f"Path {full_path} not found"
            }),
        }
