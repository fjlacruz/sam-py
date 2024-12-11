import sys
import os
import json
import pytest
from unittest import mock

# Agregar el directorio src al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Importamos la función lambda_handler que vamos a probar
from app import lambda_handler, ROUTE_MAPPING

# Mock de las funciones manejadoras
def mock_hello_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps("Hello, world!")
    }

def mock_goodbye_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps("Goodbye, world!")
    }

# Test para el caso en que la ruta sea "/hello"
@mock.patch("importlib.import_module")
def test_lambda_handler_hello(mock_import_module):
    # Simulamos que la función hello está siendo importada correctamente
    mock_import_module.return_value = mock.Mock(handle=mock_hello_handler)

    # Creamos un evento simulado para "/hello"
    event = {
        'path': '/hello'
    }
    context = {}

    # Ejecutamos la función lambda_handler
    response = lambda_handler(event, context)

    # Comprobamos que el código de estado es 200
    assert response['statusCode'] == 200
    # Comprobamos que el cuerpo contiene el mensaje esperado
    assert json.loads(response['body']) == "Hello, world!"

# Test para el caso en que la ruta sea "/goodbye"
@mock.patch("importlib.import_module")
def test_lambda_handler_goodbye(mock_import_module):
    # Simulamos que la función goodbye está siendo importada correctamente
    mock_import_module.return_value = mock.Mock(handle=mock_goodbye_handler)

    # Creamos un evento simulado para "/goodbye"
    event = {
        'path': '/goodbye'
    }
    context = {}

    # Ejecutamos la función lambda_handler
    response = lambda_handler(event, context)

    # Comprobamos que el código de estado es 200
    assert response['statusCode'] == 200
    # Comprobamos que el cuerpo contiene el mensaje esperado
    assert json.loads(response['body']) == "Goodbye, world!"

# Test para el caso en que la ruta no esté mapeada
@mock.patch("importlib.import_module")
def test_lambda_handler_path_not_found(mock_import_module):
    # Simulamos que no hay ninguna función de manejador
    mock_import_module.return_value = mock.Mock()

    # Creamos un evento simulado para una ruta no definida
    event = {
        'path': '/unknown'
    }
    context = {}

    # Ejecutamos la función lambda_handler
    response = lambda_handler(event, context)

    # Comprobamos que el código de estado es 404
    assert response['statusCode'] == 404
    # Comprobamos que el cuerpo contiene el mensaje esperado
    assert "Path unknown not found" in json.loads(response['body'])['message']

# Test para el caso de "favicon.ico" (se debe ignorar la solicitud)
def test_lambda_handler_favicon():
    # Creamos un evento simulado para la ruta "favicon.ico"
    event = {
        'path': '/favicon.ico'
    }
    context = {}

    # Ejecutamos la función lambda_handler
    response = lambda_handler(event, context)

    # Comprobamos que el código de estado es 204 (No Content)
    assert response['statusCode'] == 204
    # Comprobamos que el cuerpo sea None
    assert response['body'] is None

# Test para manejar errores de importación de módulos
@mock.patch("importlib.import_module")
def test_lambda_handler_import_error(mock_import_module):
    # Simulamos que hay un error al importar el módulo
    mock_import_module.side_effect = ImportError("Module not found")

    # Creamos un evento simulado para "/hello"
    event = {
        'path': '/hello'
    }
    context = {}

    # Ejecutamos la función lambda_handler
    response = lambda_handler(event, context)

    # Comprobamos que el código de estado es 500
    assert response['statusCode'] == 500
    # Comprobamos que el cuerpo contiene el mensaje de error
    assert "Error executing handler for path hello" in json.loads(response['body'])['message']
