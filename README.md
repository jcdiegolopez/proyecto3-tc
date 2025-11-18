# Proyecto 3 · Cifrado César con Máquina de Turing

Guía rápida para preparar el entorno, generar las máquinas de Turing y ejecutar el programa tanto para cifrado como para descifrado.

## Requisitos
- Windows, macOS o Linux con Python 3.10+ instalado.
- (Opcional) `pip` actualizado para manejar dependencias.

## Preparar entorno virtual (recomendado)
```powershell
# Ubícate en la carpeta del proyecto
cd "C:\Users\dijol\OneDrive - UVG\Universidad\ciclo 6\teoria\proyecto3-tc"

# Crear entorno virtual
python -m venv venv

# Activar (PowerShell)
.\venv\Scripts\Activate.ps1

# Si usas CMD tradicional
venv\Scripts\activate.bat

# En macOS/Linux
source venv/bin/activate

# Instalar dependencias (actualmente el proyecto usa solo la librería estándar)
pip install --upgrade pip
```

## Generar los autómatas
Siempre que edites `generate_mt_json.py`, vuelve a generar los JSON:
```powershell
python generate_mt_json.py
```
Esto crea/actualiza `encrypt.json` y `decrypt.json` (están ignorados por Git, así que recuerda regenerarlos tras clonar).

## Ejecución rápida
### 1. Cifrar
```powershell
python main.py encrypt "3#HOLA"
```
- Formato: `LLAVE#MENSAJE`.
- La llave puede ser número o una letra (se normaliza mod 26).
- El resultado aparece en pantalla y también queda en la cinta 3 durante la simulación.

### 2. Descifrar
```powershell
python main.py decrypt "3#KROD"
```
- Formato: `LLAVE#TEXTO_CIFRADO`.
- Devuelve el texto plano original.

### 3. Ejecutar pruebas automatizadas
```powershell
python main.py test
```
- Lee `tests.txt` y ejecuta 68 casos que cubren desplazamientos grandes, wrap-around y reversibilidad.

## Modo interactivo
Si ejecutas `python main.py` sin argumentos aparecerá un menú con opciones para cifrar, descifrar o correr pruebas, todo paso a paso.

## Estructura principal
- `main.py`: CLI y orquestador de las cintas.
- `turing.py`: Intérprete genérico de MT multicinta.
- `generate_mt_json.py`: Genera las tablas de transición.
- `tests.txt`: Casos de prueba.

## Tips
- Si el entorno virtual ya estaba creado, basta con activarlo y correr los comandos de arriba.
- Después de clonar el repositorio, recuerda ejecutar `python generate_mt_json.py` antes de cifrar/descifrar para asegurarte de tener los JSON.
- Usa `python main.py encrypt "llave#mensaje"` o `python main.py decrypt "llave#texto"` directamente desde PowerShell con el venv activado.
