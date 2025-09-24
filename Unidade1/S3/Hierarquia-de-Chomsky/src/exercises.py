"""Exercícios sobre Hierarquia de Chomsky, AFD, AP e Máquina de Turing.

Este módulo contém:
- respostas objetivas das questões (funções que retornam a letra correta);
- implementações demonstrativas:
  - DFA que aceita cadeias com número par de 'a' (alfabeto {a,b});
  - PDA simples que reconhece a^n b^n (n>=0);
  - Simulador minimal de Máquina de Turing para incrementar número binário na fita.

As implementações são educacionais e não otimizadas.
"""

from typing import List, Tuple

## Respostas objetivas (funções que retornam a letra correta)
def q1() -> str:
    return 'C'  # Linguagens orientadas a objetos não fazem parte da Hierarquia de Chomsky

def q2() -> str:
    return 'C'  # AFD reconhece linguagens regulares

def q3() -> str:
    return 'B'  # Máquina de Turing é modelo de computação universal

def q4() -> str:
    return 'B'  # {a^n b^n} não é regular

def q5() -> str:
    return 'C'  # Máquina de Turing é mais poderosa

def q6() -> str:
    return 'B'  # Autômato com Pilha reconhece linguagens livres de contexto

def q7() -> str:
    return 'C'  # Autômato com Pilha usa uma pilha

def q8() -> str:
    return 'B'  # Classifica pela complexidade sintática (tipo de regras)

def q9() -> str:
    return 'B'  # Autômato finito não reconhece palíndromos em geral

def q10() -> str:
    return 'B'  # Objetivo: compreender limites da computação


## Exemplos algorítmicos

def dfa_even_a(s: str) -> bool:
    """DFA que aceita cadeias sobre {a,b} onde o número de 'a' é par.

    Estados: q0 (par), q1 (impar)
    q0 é inicial e final.
    Transitions: ao ler 'a' alterna q0<->q1; ao ler 'b' fica no mesmo estado.
    """
    state = 'q0'
    for ch in s:
        if ch == 'a':
            state = 'q1' if state == 'q0' else 'q0'
        elif ch == 'b':
            pass
        else:
            # símbolo fora do alfabeto -> rejeitar
            return False
    return state == 'q0'


def pda_an_bn(s: str) -> bool:
    """PDA não-determinístico simulado que reconhece a^n b^n.

    Implementação determinística: empilha 'A' para cada 'a' lido, depois desempilha para cada 'b'.
    Rejeita se houver símbolos diferentes de a/b ou se ordem for inválida.
    Aceita a cadeia vazia.
    """
    stack: List[str] = []
    stage = 'push'  # duas fases: push para 'a', then pop para 'b'
    for ch in s:
        if stage == 'push':
            if ch == 'a':
                stack.append('A')
            elif ch == 'b':
                stage = 'pop'
                if not stack:
                    return False
                stack.pop()
            else:
                return False
        else:  # pop stage
            if ch == 'b':
                if not stack:
                    return False
                stack.pop()
            else:
                return False
    return len(stack) == 0


class SimpleTMSimulator:
    """Simulador simples de Máquina de Turing que incrementa um número binário.

    Convenções:
    - Fita é representada por lista de chars '0'/'1' e '_' (branco) nas laterais.
    - Cabeçote começa na posição 0 (início da lista passada).
    - A máquina realiza incremento binário (como somar 1).
    - Retorna a fita resultante como string e a posição final do cabeçote.
    """

    def __init__(self, tape: List[str]):
        self.tape = tape
        self.head = 0
        self.state = 's0'

    def step(self) -> bool:
        """Executa um passo. Retorna False se atingir estado de aceitação ou parada."""
        if self.state == 's0':
            # mover para o fim do número (encontrar primeiro '_')
            if self.head >= len(self.tape):
                self.tape.append('_')
            if self.tape[self.head] in ('0', '1'):
                self.head += 1
                return True
            else:
                # encontrado branco; volte uma célula e mude para carry
                self.head -= 1
                self.state = 'carry'
                return True
        elif self.state == 'carry':
            if self.head < 0:
                # precisamos inserir um '1' à esquerda
                self.tape.insert(0, '1')
                self.head = 0
                self.state = 'halt'
                return False
            sym = self.tape[self.head]
            if sym == '0':
                self.tape[self.head] = '1'
                self.state = 'halt'
                return False
            elif sym == '1':
                self.tape[self.head] = '0'
                self.head -= 1
                return True
            elif sym == '_':
                self.tape[self.head] = '1'
                self.state = 'halt'
                return False
            else:
                self.state = 'halt'
                return False
        else:
            return False

    def run(self, max_steps: int = 1000) -> Tuple[str, int]:
        steps = 0
        while steps < max_steps:
            cont = self.step()
            steps += 1
            if not cont:
                break
        return (''.join(self.tape), self.head)


def tm_increment_binary(bin_str: str) -> str:
    """Convenience wrapper: cria fita e executa o incremento binário.

    Exemplo: '1011' -> '1100'
    """
    # fita: os bits seguidos por '_' para o fim
    tape = list(bin_str) + ['_']
    tm = SimpleTMSimulator(tape)
    tape_out, _ = tm.run()
    # retirar brancos da direita
    return tape_out.rstrip('_')


def get_description() -> str:
    """Retorna a docstring de alto nível deste módulo para exibição em UIs.

    Útil para mostrar uma descrição do exercício sem abrir o arquivo fonte.
    """
    return __doc__ or ''


if __name__ == '__main__':
    # pequenas demos quando executado diretamente
    print('Respostas:')
    print('1.', q1())
    print('2.', q2())
    print('3.', q3())
    print('4.', q4())
    print('\nDFA par de a:')
    for s in ['', 'a', 'aa', 'aba', 'aab']:
        print(f"{s!r}: {dfa_even_a(s)}")

    print('\nPDA a^n b^n:')
    for s in ['', 'ab', 'aabb', 'aaabbb', 'aba']:
        print(f"{s!r}: {pda_an_bn(s)}")

    print('\nTM incremento binário:')
    for s in ['0', '1', '1011', '111']:
        print(f"{s} -> {tm_increment_binary(s)}")
