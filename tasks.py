import shutil
import zipfile
from invoke import task
import os

@task
def activate_env(c):
    """=====> Activate the virtual environment."""
    venv_path = ".\\env\\Scripts\\activate"

    if not os.path.exists(venv_path):
        print("Virtual environment not found. Please create it first (e.g., 'python -m venv env').")
        return

    c.run(f"cmd /k {venv_path}")

@task
def build(c):
    """=====> Build the project """
    c.run("sam build --use-container")

@task
def start(c):
    """=====> Start the project (default port: 3000)."""
    c.run("sam local start-api")

@task
def startPort(c, port=3000):
    """=====> Start the project on a specific port (e.g., invoke start_port --port=3001)."""
    c.run(f"sam local start-api --port {port}")

@task
def install(c):
    """=====> Install dependencies from requirements.txt."""
    c.run("pip install -r requirements.txt")

@task
def test(c):
    """=====> Run tests using pytest."""
    c.run("pytest --cov=app --cov-branch --cov-fail-under=90")
    
@task
def test_coverage(c):
    """=====> Run tests using pytest with html coverag report."""
    c.run("pytest --cov=app --cov-report=html")
    


@task
def package(ctx):
    """
    Copia el contenido del directorio src al directorio package, incluyendo el archivo requirements.txt.

    :param ctx: Contexto de Invoke
    """
    source_dir = "src"
    target_dir = "package"
    requirements_file = "requirements.txt"

    if not os.path.exists(source_dir):
        print(f"Error: El directorio {source_dir} no existe.")
        return

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(target_dir, item)
        if os.path.isdir(s):
            if item == "__pycache__":
                continue
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    # Copia el archivo requirements.txt si existe
    if os.path.exists(requirements_file):
        shutil.copy2(requirements_file, target_dir)
        print(f"Archivo {requirements_file} copiado a {target_dir}.")

    # Elimina el directorio __pycache__ en el destino si existe
    pycache_path = os.path.join(target_dir, "__pycache__")
    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path)
        print(f"Directorio {pycache_path} eliminado del destino.")

    print(f"Contenido de {source_dir} copiado a {target_dir}.")
    
    package_dir = "package"
    output_file = os.path.join(package_dir, "package.zip")

    if not os.path.exists(package_dir):
        print(f"Error: El directorio {package_dir} no existe.")
        return

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, package_dir))

    print(f"Contenido de {package_dir} empaquetado en {output_file}.")




@task
def options(c):
    """=====> List all available tasks."""
    c.run("invoke --list")
