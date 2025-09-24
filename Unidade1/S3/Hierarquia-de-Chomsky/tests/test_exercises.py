import sys
from pathlib import Path

# Garantir que o diretório raiz do projeto esteja no sys.path para que
# `from src import exercises` funcione quando pytest executar os testes.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from src import exercises


def test_objective_answers():
    assert exercises.q1() == 'C'
    assert exercises.q2() == 'C'
    assert exercises.q3() == 'B'
    assert exercises.q4() == 'B'
    assert exercises.q5() == 'C'
    assert exercises.q6() == 'B'
    assert exercises.q7() == 'C'
    assert exercises.q8() == 'B'
    assert exercises.q9() == 'B'
    assert exercises.q10() == 'B'


def test_dfa_even_a():
    assert exercises.dfa_even_a('') is True
    assert exercises.dfa_even_a('a') is False
    assert exercises.dfa_even_a('aa') is True
    assert exercises.dfa_even_a('aba') is True
    assert exercises.dfa_even_a('babab') is True


def test_pda_an_bn():
    assert exercises.pda_an_bn('') is True
    assert exercises.pda_an_bn('ab') is True
    assert exercises.pda_an_bn('aabb') is True
    assert exercises.pda_an_bn('aaabbb') is True
    assert exercises.pda_an_bn('aba') is False
    assert exercises.pda_an_bn('aab') is False


def test_tm_increment_binary():
    assert exercises.tm_increment_binary('0') == '1'
    assert exercises.tm_increment_binary('1') == '10'
    assert exercises.tm_increment_binary('1011') == '1100'
    assert exercises.tm_increment_binary('111') == '1000'
