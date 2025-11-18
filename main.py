"""
Programa principal para ejecutar las Máquinas de Turing de Cifrado César
"""

import sys
import io
from turing import load_turing_machine

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def prepare_tape_2_unary(key: str) -> str:
    """
    Convierte la llave a notación unaria con un marcador al inicio
    
    Args:
        key: Llave como número o letra
        
    Returns:
        String en notación unaria (ej: "_|||" con marcador al inicio)
    """
    # Si es un número
    if key.isdigit():
        shift = int(key)
    # Si es una letra
    elif key.isalpha() and len(key) == 1:
        shift = ord(key.upper()) - ord('A')
    else:
        raise ValueError(f"Llave inválida: {key}")
    
    # Normalizar a rango 0-25
    shift = shift % 26
    
    # Convertir a unario con marcador al inicio
    return '_' + ('|' * shift)


def prepare_tape_4_alphabet() -> str:
    """
    Genera el alfabeto base para wrap-around gestionado por transiciones
    
    Returns:
        String con alfabeto repetido
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet


def parse_input(input_str: str) -> tuple:
    """
    Parsea el input en formato: LLAVE#MENSAJE
    
    Args:
        input_str: String con formato LLAVE#MENSAJE
        
    Returns:
        Tupla (llave, mensaje)
    """
    if '#' not in input_str:
        raise ValueError("Formato incorrecto. Usar: LLAVE#MENSAJE")
    
    parts = input_str.split('#', 1)
    key = parts[0].strip()
    message = parts[1].strip().upper()  # Convertir a mayúsculas
    
    return key, message


def run_encryption(input_str: str, verbose: bool = False):
    """
    Ejecuta la MT de encriptación
    
    Args:
        input_str: Input en formato LLAVE#MENSAJE
        verbose: Si True, muestra información detallada
    """
    print("\n" + "="*60)
    print("🔒 CIFRADO CÉSAR - MÁQUINA DE TURING")
    print("="*60)
    
    try:
        # Parsear input
        key, message = parse_input(input_str)
        print(f"Llave: {key}")
        print(f"Mensaje: {message}")
        
        # Preparar cintas
        tape1 = input_str.upper()
        tape2 = prepare_tape_2_unary(key)
        tape3 = "_"  # Cinta de trabajo (vacía)
        tape4 = prepare_tape_4_alphabet()
        
        if verbose:
            print(f"\nCinta 1 (input): {tape1[:50]}...")
            print(f"Cinta 2 (llave unaria): {tape2}")
            print(f"Cinta 4 (alfabeto): {tape4[:52]}...")
        
        # Cargar MT
        tm = load_turing_machine('encrypt.json')
        
        # Configurar cintas
        tm.load_input(tape1, [tape1, tape2, tape3, tape4])
        
        # Ejecutar
        print("\n⚙️ Ejecutando máquina de Turing...")
        success = tm.run(max_steps=200000, debug=verbose)
        
        if success:
            # Obtener resultado de cinta 3
            result = tm.get_tape_content(2)
            print(f"\n✅ ENCRIPTACIÓN EXITOSA")
            print(f"Texto cifrado: {result}")
        else:
            print("\n ERROR: La máquina no aceptó el input")
            
    except Exception as e:
        print(f"\n ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


def run_decryption(input_str: str, verbose: bool = False):
    """
    Ejecuta la MT de desencriptación
    
    Args:
        input_str: Input en formato LLAVE#MENSAJE_CIFRADO
        verbose: Si True, muestra información detallada
    """
    print("\n" + "="*60)
    print("🔓 DESCIFRADO CÉSAR - MÁQUINA DE TURING")
    print("="*60)
    
    try:
        # Parsear input
        key, cipher = parse_input(input_str)
        print(f"Llave: {key}")
        print(f"Texto cifrado: {cipher}")
        
        # Preparar cintas
        tape1 = input_str.upper()
        tape2 = prepare_tape_2_unary(key)
        tape3 = "_"
        tape4 = prepare_tape_4_alphabet()
        
        if verbose:
            print(f"\nCinta 1 (input): {tape1[:50]}...")
            print(f"Cinta 2 (llave unaria): {tape2}")
            print(f"Cinta 4 (alfabeto): {tape4[:52]}...")
        
        # Cargar MT
        tm = load_turing_machine('decrypt.json')
        
        # Configurar cintas
        tm.load_input(tape1, [tape1, tape2, tape3, tape4])
        
        # Ejecutar
        print("\n⚙️ Ejecutando máquina de Turing...")
        success = tm.run(max_steps=200000, debug=verbose)
        
        if success:
            # Obtener resultado de cinta 3
            result = tm.get_tape_content(2)
            print(f"\n DESENCRIPTACIÓN EXITOSA")
            print(f"Texto descifrado: {result}")
        else:
            print("\n ERROR: La máquina no aceptó el input")
            
    except Exception as e:
        print(f"\n ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


def run_tests():
    """Ejecuta los casos de prueba del archivo tests.txt"""
    print("\n" + "="*60)
    print("🧪 EJECUTANDO PRUEBAS AUTOMÁTICAS")
    print("="*60)
    
    try:
        with open('tests.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        test_num = 0
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            test_num += 1
            parts = line.split('→')
            if len(parts) != 2:
                continue
            
            input_test = parts[0].strip()
            expected = parts[1].strip()
            
            print(f"\n{'─'*60}")
            print(f"Prueba {test_num}: {input_test}")
            print(f"Esperado: {expected}")
            
            # Determinar si es encriptación o desencriptación
            key, message = parse_input(input_test)
            
            # Ejecutar encriptación
            tm = load_turing_machine('encrypt.json')
            tape1 = input_test.upper()
            tape2 = prepare_tape_2_unary(key)
            tape3 = "_"
            tape4 = prepare_tape_4_alphabet()
            
            tm.load_input(tape1, [tape1, tape2, tape3, tape4])
            success = tm.run(max_steps=200000)
            
            if success:
                result = tm.get_tape_content(2)
                if result == expected:
                    print(f"PASÓ: {result}")
                else:
                    print(f" FALLÓ: Obtenido '{result}' != Esperado '{expected}'")
            else:
                print(" FALLÓ: La máquina no aceptó")
                
    except FileNotFoundError:
        print(" Archivo tests.txt no encontrado")
    except Exception as e:
        print(f" ERROR en pruebas: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Función principal con menú interactivo"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║   MÁQUINAS DE TURING - CIFRADO CÉSAR (4 CINTAS)          ║
║   Teoría de la Computación                                ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        # Modo línea de comandos
        command = sys.argv[1].lower()
        
        if command == 'test':
            run_tests()
        elif command == 'encrypt' and len(sys.argv) > 2:
            run_encryption(sys.argv[2], verbose=True)
        elif command == 'decrypt' and len(sys.argv) > 2:
            run_decryption(sys.argv[2], verbose=True)
        else:
            print("Uso:")
            print("  python main.py test")
            print("  python main.py encrypt 'LLAVE#MENSAJE'")
            print("  python main.py decrypt 'LLAVE#CIFRADO'")
    else:
        # Modo interactivo
        while True:
            print("\n" + "─"*60)
            print("Opciones:")
            print("  1. Encriptar")
            print("  2. Desencriptar")
            print("  3. Ejecutar pruebas automáticas")
            print("  4. Salir")
            print("─"*60)
            
            choice = input("\nSeleccione opción (1-4): ").strip()
            
            if choice == '1':
                input_str = input("\nIngrese LLAVE#MENSAJE: ").strip()
                run_encryption(input_str, verbose=True)
            elif choice == '2':
                input_str = input("\nIngrese LLAVE#CIFRADO: ").strip()
                run_decryption(input_str, verbose=True)
            elif choice == '3':
                run_tests()
            elif choice == '4':
                print("\n¡Hasta luego!\n")
                break
            else:
                print("\n Opción inválida")


if __name__ == "__main__":
    main()