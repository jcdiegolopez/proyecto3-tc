"""
Intérprete de Máquinas de Turing Multicinta
Soporta hasta N cintas con transiciones basadas en JSON
"""

import json
from typing import List, Tuple, Optional, Dict, Any


class TuringMachine:
    """Simulador de Máquina de Turing Multicinta"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa la MT desde un diccionario de configuración
        
        Args:
            config: Diccionario con la definición formal de la MT
        """
        self.states = config['Q']
        self.input_alphabet = config['Sigma']
        self.tape_alphabet = config['Gamma']
        self.num_tapes = config['num_tapes']
        self.initial_state = config['q0']
        self.accept_states = config['F']
        self.transitions = config['delta']
        
        # Inicializar cintas
        self.tapes: List[List[str]] = []
        self.heads: List[int] = []
        self.current_state = self.initial_state
        
    def load_input(self, input_string: str, tape_configs: Optional[List[str]] = None):
        """
        Carga el input en las cintas según la configuración
        
        Args:
            input_string: Cadena de entrada principal
            tape_configs: Lista opcional con contenido inicial de cada cinta
        """
        self.tapes = []
        self.heads = []
        
        for i in range(self.num_tapes):
            if i == 0 and tape_configs is None:
                # Cinta 1: input principal
                self.tapes.append(list(input_string) + ['_'] * 1000)
            elif tape_configs and i < len(tape_configs):
                # Cintas configuradas manualmente
                self.tapes.append(list(tape_configs[i]) + ['_'] * 1000)
            else:
                # Cintas vacías
                self.tapes.append(['_'] * 1000)
            
            self.heads.append(0)
    
    def read_symbols(self) -> Tuple[str, ...]:
        """Lee los símbolos actuales bajo cada cabezal"""
        return tuple(self.tapes[i][self.heads[i]] for i in range(self.num_tapes))
    
    def match_transition(self, read_symbols: Tuple[str, ...]) -> Optional[Dict]:
        """
        Busca una transición válida para los símbolos leídos
        
        Args:
            read_symbols: Tupla con los símbolos leídos de cada cinta
            
        Returns:
            Diccionario con la transición o None si no existe
        """
        state_key = self.current_state
        
        if state_key not in self.transitions:
            return None
        
        # Convertir tupla a string para búsqueda
        read_key = ','.join(read_symbols)
        
        # Buscar transición exacta
        if read_key in self.transitions[state_key]:
            return self.transitions[state_key][read_key]
        
        # Buscar con comodines
        for pattern, transition in self.transitions[state_key].items():
            pattern_symbols = pattern.split(',')
            
            if len(pattern_symbols) != len(read_symbols):
                continue
            
            match = True
            for ps, rs in zip(pattern_symbols, read_symbols):
                if ps not in ['*', 'x', rs]:
                    match = False
                    break
            
            if match:
                return transition
        
        return None
    
    def apply_transition(self, transition: Dict):
        """
        Aplica una transición a las cintas
        
        Args:
            transition: Diccionario con write, move y next_state
        """
        write_symbols = transition['write']
        moves = transition['move']
        next_state = transition['next_state']
        
        # Escribir símbolos
        for i, symbol in enumerate(write_symbols):
            if symbol not in ['*', 'x']:
                self.tapes[i][self.heads[i]] = symbol
        
        # Mover cabezales
        for i, move in enumerate(moves):
            if move == 'R':
                self.heads[i] += 1
            elif move == 'L':
                self.heads[i] = max(0, self.heads[i] - 1)
            # 'S' no mueve
            
            # Expandir cinta si es necesario
            if self.heads[i] >= len(self.tapes[i]):
                self.tapes[i].extend(['_'] * 1000)
        
        # Cambiar estado
        self.current_state = next_state
    
    def run(self, max_steps: int = 100000, debug: bool = False) -> bool:
        """
        Ejecuta la MT hasta llegar a un estado de aceptación o rechazo
        
        Args:
            max_steps: Número máximo de pasos para evitar loops infinitos
            debug: Si True, muestra información de depuración
            
        Returns:
            True si acepta, False si rechaza o excede max_steps
        """
        steps = 0
        last_states = []
        
        while steps < max_steps:
            # Verificar si llegamos a estado de aceptación
            if self.current_state in self.accept_states:
                return True
            
            # Leer símbolos actuales
            read_symbols = self.read_symbols()
            
            # Debug: mostrar estado cada 1000 pasos o primeros 100
            if debug and (steps < 100 or steps % 1000 == 0):
                print(f"\n[Paso {steps}] Estado: {self.current_state}")
                print(f"Símbolos: {read_symbols}")
                print(f"Cabezales: {self.heads}")
            
            # Guardar últimos estados para detectar loops
            if len(last_states) >= 10:
                last_states.pop(0)
            last_states.append((self.current_state, read_symbols, tuple(self.heads)))
            
            # Buscar transición
            transition = self.match_transition(read_symbols)
            
            if transition is None:
                # No hay transición: rechazar
                print(f"\n❌ No hay transición para estado '{self.current_state}' con símbolos {read_symbols}")
                return False
            
            # Aplicar transición
            self.apply_transition(transition)
            
            steps += 1
        
        # Excedió el límite de pasos
        print(f"⚠️ Advertencia: Se excedió el límite de {max_steps} pasos")
        print(f"Estado final: {self.current_state}")
        print(f"Símbolos: {self.read_symbols()}")
        print(f"Cabezales: {self.heads}")
        return False
    
    def get_tape_content(self, tape_index: int, strip_blanks: bool = True) -> str:
        """
        Obtiene el contenido de una cinta
        
        Args:
            tape_index: Índice de la cinta (0-based)
            strip_blanks: Si True, elimina blancos al final
            
        Returns:
            Contenido de la cinta como string
        """
        content = ''.join(self.tapes[tape_index])
        if strip_blanks:
            content = content.rstrip('_')
        return content
    
    def print_state(self, max_chars: int = 80):
        """Imprime el estado actual de la MT (para debugging)"""
        print(f"\n{'='*60}")
        print(f"Estado actual: {self.current_state}")
        
        for i in range(self.num_tapes):
            tape_str = ''.join(self.tapes[i][:max_chars])
            head_pos = min(self.heads[i], max_chars - 1)
            
            print(f"\nCinta {i+1}: {tape_str}")
            print(f"         {' ' * head_pos}^")
            print(f"         {' ' * head_pos}(posición {self.heads[i]})")


def load_turing_machine(json_file: str) -> TuringMachine:
    """
    Carga una MT desde un archivo JSON
    
    Args:
        json_file: Ruta al archivo JSON
        
    Returns:
        Instancia de TuringMachine
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return TuringMachine(config)


if __name__ == "__main__":
    print("Intérprete de Máquinas de Turing Multicinta")
    print("Usar main.py para ejecutar las MT de cifrado César")