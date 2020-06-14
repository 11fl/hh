import pytest
import hhparce

def test_reg():
    string = '200 000-200 000 руб.'
    assert hhparce.reg(string) == 200000