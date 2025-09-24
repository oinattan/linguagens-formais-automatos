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
    """
    DFA que aceita cadeias sobre {a,b} onde o número de 'a' é par.
    Retorna True se aceita, False caso contrário (inclui símbolo inválido).
    """
    state = 0  # 0 = par, 1 = impar
    for ch in s:
        if ch == 'a':
            state ^= 1
        elif ch == 'b':
            pass
        else:
            # símbolo inválido para o alfabeto {a,b}
            return False
    return state == 0


def pda_an_bn(s: str) -> bool:
    """
    PDA determinístico simples que aceita a^n b^n (n >= 0).
    Aceita somente cadeias na forma a...ab...b com mesmo número de a's e b's.
    """
    # contar 'a's no prefixo, depois consumir com 'b's
    i = 0
    n = len(s)
    count_a = 0
    # contar prefixo de 'a'
    while i < n and s[i] == 'a':
        count_a += 1
        i += 1
    # agora devem vir exatamente count_a símbolos 'b'
    count_b = 0
    while i < n and s[i] == 'b':
        count_b += 1
        i += 1
    # aceito se consumi toda a string e counts iguais
    return i == n and count_a == count_b


class SimpleTMSimulator:
    """
    Simulador minimal e específico de Máquina de Turing para operação de
    incremento de número binário (com fita infinita à direita conceitual).
    Implementação educativa: cabeça inicia no último bit (direita) e faz
    a operação de somar 1 binário.
    """

    def __init__(self, tape: str):
        # Representar fita como lista mutável; assumir entrada sem separadores
        self.tape = list(tape) if tape else ['0']
        # posicionar cabeça no último símbolo
        self.head = len(self.tape) - 1 if self.tape else 0

    def increment(self) -> str:
        i = self.head
        carry = 1
        # percorre da direita para a esquerda aplicando o carry
        while i >= 0 and carry:
            if self.tape[i] == '0':
                self.tape[i] = '1'
                carry = 0
            elif self.tape[i] == '1':
                self.tape[i] = '0'
                carry = 1
            else:
                # símbolo inválido, tratar como erro simples: abortar
                raise ValueError(f"Símbolo inválido na fita: {self.tape[i]}")
            i -= 1
        if carry:
            # se ainda há carry, inserir '1' à esquerda (expande a fita)
            self.tape.insert(0, '1')
        # remover possíveis zeros à esquerda não significativos exceto único '0'
        # (mantemos representação simples: não removemos zeros a não ser necessidade)
        return ''.join(self.tape)


def tm_increment_binary(bin_str: str) -> str:
    """
    Interface simples para incrementar uma string binária usando o simulador.
    Aceita apenas '0'/'1' na entrada.
    """
    if any(c not in '01' for c in bin_str):
        raise ValueError("Entrada deve conter apenas '0' e '1'")
    sim = SimpleTMSimulator(bin_str if bin_str != '' else '0')
    return sim.increment()


def get_description() -> str:
    """Retorna a docstring do módulo para exibição na GUI."""
    return __doc__ or ""


if __name__ == '__main__':
    # Demonstração rápida das respostas e exemplos
    print("Respostas:")
    for i, fn in enumerate((q1, q2, q3, q4, q5, q6, q7, q8, q9, q10), start=1):
        try:
            print(f"{i}.", fn())
        except Exception as e:
            print(f"{i}.", f"Erro ao obter resposta: {e}")
    print()

    print("DFA (número par de 'a'):")
    for s in ['', 'a', 'aa', 'aba', 'aab']:
        print(f"'{s}':", dfa_even_a(s))
    print()

    print("PDA a^n b^n:")
    for s in ['', 'ab', 'aabb', 'aaabbb', 'aba']:
        print(f"'{s}':", pda_an_bn(s))
    print()

    print("TM incremento binário:")
    for s in ['0', '1', '1011', '111']:
        print(f"{s} ->", tm_increment_binary(s))
