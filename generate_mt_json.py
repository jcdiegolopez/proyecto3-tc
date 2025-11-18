"""
Generador automático de Máquinas de Turing para Cifrado César
Genera encrypt.json y decrypt.json
"""

import json


def generate_encrypt_mt():
    """Genera la MT de encriptación"""
    
    mt = {
        "description": "Máquina de Turing de 4 cintas para Cifrado César - Encriptación",
        "Q": [
            "q0", "q_skip_key", "q_process_char", "q_find_in_alphabet",
            "q_count_shift", "q_read_shifted", 
            "q_rewind_tape2", "q_rewind_tape4", "q_accept"
        ],
        "Sigma": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789# "),
        "Gamma": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789# |_"),
        "num_tapes": 4,
        "q0": "q0",
        "F": ["q_accept"],
        "delta": {}
    }
    
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Estado q0: inicio - mover cabezal de cinta 2 al primer |
    mt["delta"]["q0"] = {
        "*,_,*,*": {"write": ["*", "*", "*", "*"], "move": ["R", "R", "S", "S"], "next_state": "q_skip_key"}
    }
    
    # Estado q_skip_key: saltar la llave hasta encontrar #
    mt["delta"]["q_skip_key"] = {
        "#,*,*,*": {"write": ["#", "*", "*", "*"], "move": ["R", "S", "S", "S"], "next_state": "q_process_char"}
    }
    for c in letters + "0123456789":
        mt["delta"]["q_skip_key"][f"{c},*,*,*"] = {
            "write": [c, "*", "*", "*"], "move": ["R", "S", "S", "S"], "next_state": "q_skip_key"
        }
    
    # Estado q_process_char: procesar siguiente carácter
    mt["delta"]["q_process_char"] = {
        "_,*,*,*": {"write": ["_", "*", "*", "*"], "move": ["S", "S", "S", "S"], "next_state": "q_accept"},
        " ,*,*,*": {"write": [" ", "*", " ", "*"], "move": ["R", "S", "R", "S"], "next_state": "q_process_char"}
    }
    for letter in letters:
        mt["delta"]["q_process_char"][f"{letter},*,*,*"] = {
            "write": [letter, "*", "*", "*"], "move": ["S", "S", "S", "S"], "next_state": "q_find_in_alphabet"
        }
    
    # Estado q_find_in_alphabet: encontrar letra actual en alfabeto de cinta 4
    mt["delta"]["q_find_in_alphabet"] = {}
    for letter in letters:
        mt["delta"]["q_find_in_alphabet"][f"{letter},*,*,{letter}"] = {
            "write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "S"], "next_state": "q_count_shift"
        }
        mt["delta"]["q_find_in_alphabet"][f"{letter},*,*,*"] = {
            "write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "R"], "next_state": "q_find_in_alphabet"
        }
    
    # Estado q_count_shift: contar | y avanzar en alfabeto SIN consumir los |
    mt["delta"]["q_count_shift"] = {
        "*,|,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "R", "S", "R"], "next_state": "q_count_shift"},
        "*,_,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "L", "S", "S"], "next_state": "q_read_shifted"}
    }
    
    # Estado q_read_shifted: leer letra desplazada
    mt["delta"]["q_read_shifted"] = {}
    for letter in letters:
        mt["delta"]["q_read_shifted"][f"*,*,*,{letter}"] = {
            "write": ["*", "*", letter, "*"], "move": ["R", "S", "R", "S"], "next_state": "q_rewind_tape2"
        }
    
    # Estado q_rewind_tape2: rebobinar cinta 2 al inicio (antes del primer |)
    # El cabezal de cinta 2 está justo después del último |, entonces retrocedemos
    # hasta llegar a un _ (que significa que estamos antes del primer |)
    mt["delta"]["q_rewind_tape2"] = {
        "*,|,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "L", "S", "S"], "next_state": "q_rewind_tape2"},
        "*,_,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "R", "S", "S"], "next_state": "q_rewind_tape4"}
    }
    
    # Estado q_rewind_tape4: rebobinar cinta 4 al inicio del alfabeto
    mt["delta"]["q_rewind_tape4"] = {
        "*,*,*,A": {"write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "S"], "next_state": "q_process_char"}
    }
    for letter in letters[1:]:  # Saltar 'A' que ya está manejada arriba
        mt["delta"]["q_rewind_tape4"][f"*,*,*,{letter}"] = {
            "write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "L"], "next_state": "q_rewind_tape4"
        }
    mt["delta"]["q_rewind_tape4"]["*,*,*,_"] = {
        "write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "R"], "next_state": "q_process_char"
    }
    
    return mt


def generate_decrypt_mt():
    """Genera la MT de desencriptación"""
    
    mt = {
        "description": "Máquina de Turing de 4 cintas para Cifrado César - Desencriptación",
        "Q": [
            "q0", "q_skip_key", "q_process_char", "q_prepare_counter",
            "q_find_in_alphabet", "q_check_counter",
            "q_read_shifted", "q_rewind_tape2", "q_find_marker_or_pipe", "q_rewind_tape4", "q_accept"
        ],
        "Sigma": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789# "),
        "Gamma": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789# |_"),
        "num_tapes": 4,
        "q0": "q0",
        "F": ["q_accept"],
        "delta": {}
    }
    
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Estado q0: inicio - mover cabezal de cinta 2 al primer |
    mt["delta"]["q0"] = {
        "*,_,*,*": {"write": ["*", "*", "*", "*"], "move": ["R", "R", "S", "S"], "next_state": "q_skip_key"}
    }
    
    # Estado q_skip_key: saltar la llave hasta encontrar #
    mt["delta"]["q_skip_key"] = {
        "#,*,*,*": {"write": ["#", "*", "*", "*"], "move": ["R", "S", "S", "S"], "next_state": "q_process_char"}
    }
    for c in letters + "0123456789":
        mt["delta"]["q_skip_key"][f"{c},*,*,*"] = {
            "write": [c, "*", "*", "*"], "move": ["R", "S", "S", "S"], "next_state": "q_skip_key"
        }
    
    # Estado q_process_char: procesar siguiente carácter
    mt["delta"]["q_process_char"] = {
        "_,*,*,*": {"write": ["_", "*", "*", "*"], "move": ["S", "S", "S", "S"], "next_state": "q_accept"},
        " ,*,*,*": {"write": [" ", "*", " ", "*"], "move": ["R", "S", "R", "S"], "next_state": "q_process_char"}
    }
    for letter in letters:
        mt["delta"]["q_process_char"][f"{letter},*,*,*"] = {
            "write": [letter, "*", "*", "*"], "move": ["S", "L", "S", "R"], "next_state": "q_prepare_counter"
        }
    
    # Estado q_prepare_counter: ir al marcador _ inicial de cinta 2
    mt["delta"]["q_prepare_counter"] = {
        "*,|,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "L", "S", "S"], "next_state": "q_prepare_counter"},
        "*,_,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "R", "S", "S"], "next_state": "q_find_in_alphabet"}
    }
    
    # Estado q_find_in_alphabet: encontrar letra en alfabeto
    # Cuando la encontramos, contamos hacia atrás SIN modificar cinta 2 (igual que encrypt)
    mt["delta"]["q_find_in_alphabet"] = {}
    for letter in letters:
        # Cuando encontramos la letra Y hay un | en cinta 2, contar (sin consumir) y retroceder alfabeto
        mt["delta"]["q_find_in_alphabet"][f"{letter},|,*,{letter}"] = {
            "write": ["*", "*", "*", "*"], "move": ["S", "R", "S", "L"], "next_state": "q_check_counter"
        }
        # Cuando encontramos la letra Y llegamos al marcador _, leer la letra actual
        mt["delta"]["q_find_in_alphabet"][f"{letter},_,*,{letter}"] = {
            "write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "S"], "next_state": "q_read_shifted"
        }
        # Si no es la letra correcta, avanzar en el alfabeto
        mt["delta"]["q_find_in_alphabet"][f"{letter},*,*,*"] = {
            "write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "R"], "next_state": "q_find_in_alphabet"
        }
    
    # Estado q_check_counter: verificar si quedan más | para contar (SIN consumir)
    mt["delta"]["q_check_counter"] = {
        # Si hay otro |, continuar contando y retrocediendo en alfabeto
        "*,|,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "R", "S", "L"], "next_state": "q_check_counter"},
        # Si llegamos al marcador _, leer la letra actual del alfabeto
        "*,_,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "S"], "next_state": "q_read_shifted"}
    }
    
    # Estado q_read_shifted: leer letra desplazada y escribir en cinta 3
    # NO necesitamos mover cabezal de cinta 2 - ya no se modifica
    mt["delta"]["q_read_shifted"] = {}
    for letter in letters:
        mt["delta"]["q_read_shifted"][f"*,*,*,{letter}"] = {
            "write": ["*", "*", letter, "*"], "move": ["R", "S", "R", "S"], "next_state": "q_rewind_tape2"
        }
    
    # Estado q_rewind_tape2: rebobinar cinta 2 al primer |
    # Después de contar, el cabezal puede estar en posición más allá del último |
    # Debemos retroceder hasta encontrar un |, y luego seguir hasta encontrar el marcador _
    mt["delta"]["q_rewind_tape2"] = {
        # Si hay |, retroceder
        "*,|,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "L", "S", "S"], "next_state": "q_rewind_tape2"},
        # Si encontramos _ (puede ser el marcador o espacio vacío), retroceder para buscar el marcador
        "*,_,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "L", "S", "S"], "next_state": "q_find_marker_or_pipe"}
    }
    
    # Estado q_find_marker_or_pipe: después de encontrar _, verificar si hay | o _ atrás
    mt["delta"]["q_find_marker_or_pipe"] = {
        # Si hay | atrás, seguir retrocediendo
        "*,|,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "L", "S", "S"], "next_state": "q_rewind_tape2"},
        # Si hay _ atrás, ese es el marcador - avanzar al primer |
        "*,_,*,*": {"write": ["*", "*", "*", "*"], "move": ["S", "R", "S", "S"], "next_state": "q_rewind_tape4"}
    }
    
    # Estado q_rewind_tape4: rebobinar alfabeto
    mt["delta"]["q_rewind_tape4"] = {
        "*,*,*,A": {"write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "S"], "next_state": "q_process_char"}
    }
    for letter in letters[1:]:  # Saltar 'A' que ya está manejada arriba
        mt["delta"]["q_rewind_tape4"][f"*,*,*,{letter}"] = {
            "write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "L"], "next_state": "q_rewind_tape4"
        }
    mt["delta"]["q_rewind_tape4"]["*,*,*,_"] = {
        "write": ["*", "*", "*", "*"], "move": ["S", "S", "S", "R"], "next_state": "q_process_char"
    }
    
    return mt


def main():
    """Genera ambos archivos JSON"""
    
    print("Generando Máquinas de Turing...")
    
    # Generar MT de encriptación
    print("\n Generando encrypt.json...")
    encrypt_mt = generate_encrypt_mt()
    with open('encrypt.json', 'w', encoding='utf-8') as f:
        json.dump(encrypt_mt, f, indent=2, ensure_ascii=False)
    print(f" encrypt.json generado ({len(encrypt_mt['delta'])} estados con transiciones)")
    
    # Generar MT de desencriptación
    print("\n📝 Generando decrypt.json...")
    decrypt_mt = generate_decrypt_mt()
    with open('decrypt.json', 'w', encoding='utf-8') as f:
        json.dump(decrypt_mt, f, indent=2, ensure_ascii=False)
    print(f" decrypt.json generado ({len(decrypt_mt['delta'])} estados con transiciones)")
    
    print("\n🎉 ¡Archivos JSON generados exitosamente!")
    print("\nPuedes ejecutar:")
    print("  python main.py")


if __name__ == "__main__":
    main()