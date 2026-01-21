"""Test substitution.py"""

import subprocess
import pytest


def test_substitution_empty():
    """Test substitution.py"""
    result = subprocess.run(
        ["python", "substitution.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "Usage: python substitution.py filename key\n"


def test_substitution_smallkey():
    """Test substitution.py"""
    result = subprocess.run(
        ["python", "substitution.py", "./test/01.in", "SQNBUYTR"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "Usage: python substitution.py filename key\n"


def test_substitution_repeatkey():
    """Test substitution.py"""
    result = subprocess.run(
        ["python", "substitution.py", "./test/01.in", "GFDSQTREZABGCXWPOIUYMHKJHN"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "Usage: python substitution.py filename key\n"


def test_substitution_keyfirst():
    """Test substitution.py"""
    result = subprocess.run(
        ["python", "substitution.py", "AZERTYUIOPQSDFGHJKLMWXCVBN", "./test/01.in"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "Usage: python substitution.py filename key\n"


DATA_IN = [
    (".test/01.in", "AZERTYUIOPQSDFGHJKLMWXCVBN"),
    (".test/02.in", "AZERTYUIOPQSDFGHJKLMWXCVBN"),
    (".test/03.in", "MLKJHGFDSQNBVCXWPOIUYTREZA"),
    (".test/04.in", "MLKJHGFDSQNBVCXWPOIUYTREZA"),
    (".test/05.in", "GFDSQTREZABVCXWPOIUYMLKJHN"),
]
DATA_OUT = [
    "Gft yoli. Mcg yoli! Ktr yoli? Zswt yoli.",
    "ITSSG",
    "Kxcfomuybmusxci! Uxjmz si zxyo jmz. Zxy'oh xgg ux Fohmu Wbmkhi! Zxy'oh xgg mcj mrmz!",
    """Dmooz Wxuuho rmi m dsfdbz ycyiymb lxz sc vmcz rmzi.
Gxo xch udscf, dh dmuhj udh iyvvho dxbsjmzi vxoh udmc mcz xudho usvh xg zhmo. 
Gxo mcxudho, dh ohmbbz rmcuhj ux jx dsi dxvhrxon, lyu rmi gxokhj ux jx su sc ihkohu, sc udh jhmj xg udh csfdu. 
Mcj dh mbix dmwwhchj ux lh m rsamoj.""",
    "Zy'u g sgxrqiwmu fmuzxquu, Tiwsw, rwzxr wmy hwmi swwi.",
]


@pytest.mark.parametrize(
    "input_data, expected_output",
    zip(DATA_IN, DATA_OUT),
)
def test_substitution_single(input_data, expected_output):
    """Test substitution.py"""
    result = subprocess.run(
        ["python", "substitution.py", input_data[0], input_data[1]],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == f"{expected_output}\n"


def test_substitution_reverse_01():
    """Test substitution.py"""
    result = subprocess.run(
        [
            "python",
            "substitution.py",
            ".test/11.in",
            "MLKJHGFDSQNBVCXWPOIUYTREZA",
            "-r",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert (
        result.stdout
        == "Congratulations! Today is your day. You're off to Great Places! You're off and away!\n"
    )


def test_substitution_reverse_02():
    """Test substitution.py"""
    result = subprocess.run(
        [
            "python",
            "substitution.py",
            ".test/12.in",
            "GFDSQTREZABVCXWPOIUYMLKJHN",
            "-r",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout == "It's a dangerous business, Frodo, going out your door.\n"
