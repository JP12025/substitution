"""Acceptance tests for the Substitution exercise.

Each test runs your program as a whole, exactly as a user would: it writes
a message in a file, gives the file name and a key on the command line,
then checks what your program prints and tries to explain what is wrong.

Run the tests from the exercise folder with:

    python test_substitution.py
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

EXERCISE_DIR = Path(__file__).resolve().parent
SCRIPT = "substitution.py"
USAGE = "Usage: python substitution.py filename key"
FILENAME = "message.txt"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TIMEOUT = 5  # seconds

HARRY = (
    "Harry Potter was a highly unusual boy in many ways.\n"
    "For one thing, he hated the summer holidays more than any other "
    "time of year. \n"
    "For another, he really wanted to do his homework, but was forced to "
    "do it in secret, in the dead of the night. \n"
    "And he also happened to be a wizard.\n"
)

# Encryption: (what is checked, key, content of the message file).
CASES = [
    ("HELLO (example of the instructions)",
     "NQXPOMAFTRHZLGECYJIUWSKDVB", "HELLO\n"),
    ("uppercase and lowercase letters, punctuation",
     "AZERTYUIOPQSDFGHJKLMWXCVBN",
     "One fish. Two fish! Red fish? Blue fish.\n"),
    ("HELLO with another key",
     "AZERTYUIOPQSDFGHJKLMWXCVBN", "HELLO\n"),
    ("apostrophes and exclamation marks",
     "MLKJHGFDSQNBVCXWPOIUYTREZA",
     "Congratulations! Today is your day. You're off to Great Places! "
     "You're off and away!\n"),
    ("several lines, spaces at the end of some lines",
     "MLKJHGFDSQNBVCXWPOIUYTREZA", HARRY),
    ("commas and apostrophes",
     "GFDSQTREZABVCXWPOIUYMLKJHN",
     "It's a dangerous business, Frodo, going out your door.\n"),
    ("digits and symbols are kept",
     "ZYXWVUTSRQPONMLKJIHGFEDCBA", "DNA: ATG-GCC x 42 (codon #1)\n"),
    ("empty lines, indentation and tabulations are kept",
     "QWERTYUIOPASDFGHJKLZXCVBNM",
     "Gene list:\n\n"
     "    BRCA1\tbreast cancer\n"
     "    TP53\ttumor protein\n\n"
     "End\n"),
    ("a key written in lowercase",
     "nqxpomaftrhzlgecyjiuwskdvb", "Hello, World!\n"),
    ("a key mixing uppercase and lowercase",
     "NqXpOmAfTrHzLgEcYjIuWsKdVb", "Hello, World!\n"),
]

# Invalid command lines: (what is checked, arguments).
# The program must print the usage message and stop.
# A message file named FILENAME always exists.
USAGE_CASES = [
    ("no argument at all", []),
    ("a file name but no key", [FILENAME]),
    ("a key that is too short", [FILENAME, "SQNBUYTR"]),
    ("a key that is too long (27 letters)",
     [FILENAME, "AZERTYUIOPQSDFGHJKLMWXCVBNA"]),
    ("a key with repeated letters (26 characters)",
     [FILENAME, "GFDSQTREZABGCXWPOIUYMHKJHN"]),
    ("a key with a digit instead of a letter (26 characters)",
     [FILENAME, "AZERTYUIOPQSDFGHJKLMWXCVB1"]),
    ("a key with the same letter in uppercase and lowercase",
     [FILENAME, "ABCDEFGHIJKLMNOPQRSTUVWXYa"]),
    ("the key given before the file name",
     ["AZERTYUIOPQSDFGHJKLMWXCVBN", FILENAME]),
    ("a third argument that is not -r",
     [FILENAME, "AZERTYUIOPQSDFGHJKLMWXCVBN", "-x"]),
]

# Bonus, decryption: (what is checked, key, content of the message file).
BONUS_CASES = [
    ("-r (example of the instructions)",
     "AZERTYUIOPQSDFGHJKLMWXCVBN",
     "Gft yoli. Mcg yoli! Ktr yoli? Zswt yoli.\n"),
    ("-r with apostrophes and exclamation marks",
     "MLKJHGFDSQNBVCXWPOIUYTREZA",
     "Kxcfomuybmusxci! Uxjmz si zxyo jmz. Zxy'oh xgg ux Fohmu Wbmkhi! "
     "Zxy'oh xgg mcj mrmz!\n"),
    ("-r with commas and apostrophes",
     "GFDSQTREZABVCXWPOIUYMLKJHN",
     "Zy'u g sgxrqiwmu fmuzxquu, Tiwsw, rwzxr wmy hwmi swwi.\n"),
    ("-r on several lines",
     "QWERTYUIOPASDFGHJKLZXCVBNM", "Rgft.\n\nLtt ngx ftbz zodt!\n"),
    ("-r with a key written in lowercase",
     "nqxpomaftrhzlgecyjiuwskdvb", "Fozze, Kejzp!\n"),
]

# Bonus, invalid command lines.
BONUS_USAGE_CASES = [
    ("-r given before the key",
     [FILENAME, "-r", "AZERTYUIOPQSDFGHJKLMWXCVBN"]),
    ("-r given twice",
     [FILENAME, "AZERTYUIOPQSDFGHJKLMWXCVBN", "-r", "-r"]),
    ("-r with an invalid key", [FILENAME, "SQNBUYTR", "-r"]),
]

# Content of the message file for the invalid command lines.
USAGE_MESSAGE = "Hello\n"


# ---------------------------------------------------------------------------
# Expected answer
# ---------------------------------------------------------------------------

def substitute(text, key, decrypt=False):
    """Encrypt text with key (or decrypt it if decrypt is True)."""
    source = ALPHABET
    target = key.upper()
    if decrypt:
        source, target = target, source
    result = ""
    for char in text:
        if char in source:
            result += target[source.index(char)]
        elif char.upper() in source:
            result += target[source.index(char.upper())].lower()
        else:
            result += char
    return result


# ---------------------------------------------------------------------------
# Running the student's program
# ---------------------------------------------------------------------------

def run_program(arguments, content):
    """Write content in FILENAME, then run the program with the arguments.

    The program runs in a temporary folder that contains only FILENAME.
    Return (stdout, stderr, return code), or None if the program
    did not stop in time.
    """
    with tempfile.TemporaryDirectory() as folder:
        message_file = Path(folder) / FILENAME
        message_file.write_text(content, encoding="utf-8", newline="\n")
        try:
            # sys.executable is the Python running the tests,
            # so "python" vs "python3" does not matter.
            # PYTHONUTF8 makes open() read the file as UTF-8 everywhere.
            result = subprocess.run(
                [sys.executable, str(EXERCISE_DIR / SCRIPT)] + arguments,
                input="",
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=folder,
                env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"),
                timeout=TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return None
    stdout = result.stdout.replace("\r\n", "\n")
    stderr = result.stderr.replace("\r\n", "\n").strip()
    return stdout, stderr, result.returncode


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def show(text):
    """Indent the lines of text, make spaces and tabulations visible.

    Spaces are shown as '·', tabulations as '→' and empty lines
    as '(empty line)'.
    """
    if text == "":
        return "    (nothing)"
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    shown = []
    for line in lines:
        if line == "":
            shown.append("    (empty line)")
        else:
            shown.append("    " + line.replace(" ", "·").replace("\t", "→"))
    return "\n".join(shown)


def last_lines(text, nb_lines=4):
    """Return the last lines of a text, indented."""
    lines = text.split("\n")[-nb_lines:]
    return "\n".join("    " + line for line in lines)


def command(arguments):
    """Return the command line typed by the user."""
    return " ".join(["python", SCRIPT] + arguments)


def ordinal(number):
    """Return '1st', '2nd', '3rd', '4th'... for number."""
    if number % 100 in (11, 12, 13):
        return f"{number}th"
    suffixes = {1: "st", 2: "nd", 3: "rd"}
    return f"{number}{suffixes.get(number % 10, 'th')}"


def explain_crash(stderr, usage_expected):
    """Explain the most common errors that make the program crash."""
    message = f"Your program crashed:\n{last_lines(stderr)}"
    if "IndexError" in stderr and "argv" in stderr:
        message += ("\nsys.argv does not have as many elements as you think: "
                    "check len(sys.argv) before using sys.argv[1] or "
                    "sys.argv[2].")
    elif "FileNotFoundError" in stderr and usage_expected:
        message += ("\nYour program tried to open a file before checking the "
                    "command line: check the number of arguments and the key "
                    "first, then open the file.")
    elif "FileNotFoundError" in stderr:
        message += (f"\nOpen the file whose name is given on the command "
                    f"line (sys.argv[1], here {FILENAME!r}), not a fixed "
                    f"file name.")
    elif "EOFError" in stderr:
        message += ("\nYour program reads the keyboard with input(): the "
                    "message must be read from the file given on the command "
                    "line, and the key from sys.argv.")
    elif "ValueError" in stderr and ("substring not found" in stderr
                                     or "not in list" in stderr):
        message += ("\nindex() fails when the character is not found: check "
                    "first that the character is a letter of the alphabet "
                    "(e.g. with the operator in), and remember that the key "
                    "may be written in lowercase.")
    elif "KeyError" in stderr:
        message += ("\nThis key is not in your dictionary: check first with "
                    "the operator in, and remember that only letters are "
                    "replaced (in uppercase or lowercase).")
    elif "IndexError" in stderr:
        message += ("\nAn index is too large: the alphabet and the key have "
                    "26 letters, so the indices go from 0 to 25.")
    return message


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_usage(arguments):
    """Check that an invalid command line prints the usage message only.

    Return None if the test passes, else an error message.
    """
    result = run_program(arguments, USAGE_MESSAGE)
    if result is None:
        return "Your program did not stop (infinite loop?)."
    stdout, stderr, return_code = result
    if stdout == USAGE + "\n" and stderr == "":
        return None
    # sys.exit("Usage: ...") writes the message on stderr: it is accepted too.
    if stdout == "" and stderr == USAGE:
        return None

    lines = stdout.splitlines()
    printed = "Your program printed:\n" + show(stdout)
    if "Traceback" in stderr and USAGE in stdout:
        return (f"Your program printed the usage message, but then it went "
                f"on and crashed. It should stop right after the usage "
                f"message (e.g. with sys.exit()).\n{printed}\n"
                f"{explain_crash(stderr, True)}")
    if "Traceback" in stderr:
        return explain_crash(stderr, True)
    if USAGE in lines and len(lines) > 1:
        return (f"Your program printed the usage message, but then it went "
                f"on. It should print only {USAGE!r} and stop right away "
                f"(e.g. with sys.exit()).\n{printed}")
    if any(line.strip() == USAGE for line in lines):
        return (f"Your program should print only {USAGE!r}, nothing else "
                f"(not even spaces).\n{printed}")
    if any(line.strip().lower() == USAGE.lower() for line in lines):
        return (f"Check the case and the spelling: the message must be "
                f"exactly {USAGE!r}.\n{printed}")
    if any(line.startswith("Usage") for line in lines):
        return f"The usage message must be exactly {USAGE!r}.\n{printed}"
    if stdout != "":
        return (f"The command line is invalid: your program should print "
                f"{USAGE!r} instead of encrypting the message.\n{printed}")
    return f"Your program should print {USAGE!r}.\n{printed}"


def explain_letter(char, key, decrypt):
    """Explain how one letter is encrypted (or decrypted) with key."""
    letter = char.upper()
    key = key.upper()
    if decrypt:
        position = key.index(letter)
        result = ALPHABET[position]
        explanation = (f"{letter!r} is the {ordinal(position + 1)} letter of "
                       f"the key, so it becomes the {ordinal(position + 1)} "
                       f"letter of the alphabet: {result!r}")
    else:
        position = ALPHABET.index(letter)
        result = key[position]
        explanation = (f"{letter!r} is the {ordinal(position + 1)} letter of "
                       f"the alphabet, so it becomes the "
                       f"{ordinal(position + 1)} letter of the key: "
                       f"{result!r}")
    if char.islower():
        explanation += f", written in lowercase: {result.lower()!r}"
    return explanation + "."


def explain_wrong_text(given, content, expected, key, decrypt):
    """Explain why the encrypted (or decrypted) text is wrong."""
    if given == content:
        return "Your program printed the message unchanged."
    if given == substitute(content, key, not decrypt):
        if decrypt:
            return ("Your program encrypted the message instead of "
                    "decrypting it: with -r, each letter of the key "
                    "becomes the letter of the alphabet at the same place.")
        return ("Your program decrypted the message instead of encrypting "
                "it: each letter of the alphabet becomes the letter of the "
                "key at the same place, not the other way round.")
    if given == expected + "\n":
        return ("There is an extra empty line at the end: the file already "
                "ends with a newline character, which is part of the "
                "message, and print() adds another one. Use "
                "print(text, end=\"\") to print the text as it is.")
    if given.lower() == expected.lower():
        message = ("The letters are right but not their case: an uppercase "
                   "letter must stay uppercase, a lowercase one lowercase.")
        if key.isupper() and given.upper() == given:
            message += (" Here the key is in uppercase: convert the letter "
                        "of the key with lower() when the original letter is "
                        "in lowercase.")
        elif key.islower() and given.lower() == given:
            message += (" Here the key is in lowercase: convert the letter "
                        "of the key with upper() when the original letter is "
                        "in uppercase.")
        return message

    if expected in given:
        return ("The right text is there, but your program printed "
                "something else too: remove the other print() (for instance "
                "prints used to debug).")

    given_lines = given.split("\n")
    expected_lines = expected.split("\n")
    stripped_given = [line.strip() for line in given_lines if line.strip()]
    stripped_expected = [line.strip() for line in expected_lines
                         if line.strip()]
    if given_lines != expected_lines and stripped_given == stripped_expected:
        return ("Each line contains the right text, but some spaces, "
                "tabulations or empty lines are lost (or added): the message "
                "must be kept exactly as it is in the file. Do not use "
                "strip(), and print the text with print(text, end=\"\").")
    if len(given_lines) != len(expected_lines):
        message = (f"Your program printed {len(given_lines) - 1} line(s) "
                   f"instead of {len(expected_lines) - 1}: every newline "
                   f"character of the file must be kept.")
        if "\n" in content.rstrip("\n") and given.count("\n") <= 1:
            message += (" Your program seems to read (or print) only one "
                        "line: read the whole file with read().")
        return message

    # First character that is wrong.
    content_lines = content.split("\n")
    for line_number, (original, good, bad) in enumerate(
            zip(content_lines, expected_lines, given_lines), start=1):
        if good == bad:
            continue
        if len(good) != len(bad):
            return (f"Line {line_number} has {len(bad)} characters instead "
                    f"of {len(good)}: every character of the message must "
                    f"give exactly one character.")
        for position, (char, good_char, bad_char) in enumerate(
                zip(original, good, bad), start=1):
            if good_char != bad_char:
                message = (f"Line {line_number}, character {position} "
                           f"({char!r}) should become {good_char!r}, but your "
                           f"program printed {bad_char!r}.")
                if char.upper() in ALPHABET:
                    message += " " + explain_letter(char, key, decrypt)
                else:
                    message += (" Only letters are replaced: copy the other "
                                "characters unchanged.")
                return message
    return ""


def check_text(arguments, content, expected, decrypt):
    """Run one encryption or decryption test.

    Return None if it passes, else an error message.
    """
    result = run_program(arguments, content)
    if result is None:
        return "Your program did not stop (infinite loop?)."
    stdout, stderr, return_code = result
    if stdout == expected and stderr == "":
        return None
    if "Traceback" in stderr:
        message = explain_crash(stderr, False)
        if stdout:
            message = f"Your program printed:\n{show(stdout)}\n" + message
        return message
    if stdout == expected:
        return f"Your program wrote on the error output:\n{last_lines(stderr)}"
    if stdout.startswith(USAGE):
        return (f"Your program printed the usage message, but the command "
                f"line is valid.\nYour program printed:\n{show(stdout)}")

    message = explain_wrong_text(stdout, content, expected, arguments[1],
                                 decrypt)
    return (f"{message}\n"
            f"Expected output:\n{show(expected)}\n"
            f"Your program printed:\n{show(stdout)}")


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def run_test(arguments, content):
    """Run one test. Return None if it passes, else an error message.

    content is None for an invalid command line (the usage message is
    expected).
    """
    if content is None:
        return check_usage(arguments)
    key = arguments[1]
    decrypt = "-r" in arguments
    expected = substitute(content, key, decrypt)
    return check_text(arguments, content, expected, decrypt)


def run_tests(title, tests, colors):
    """Run a list of tests (description, arguments, content of the file).

    Print the results and return the number of tests that pass.
    """
    green, red, reset = colors
    print(title)
    nb_ok = 0
    for description, arguments, content in tests:
        message = run_test(arguments, content)
        if message is None:
            nb_ok += 1
            print(f"{green}✔{reset} {description}")
        else:
            print(f"{red}✗{reset} {description}")
            print(f"    Command: {command(arguments)}")
            file_content = USAGE_MESSAGE if content is None else content
            print(f"    Content of {FILENAME} (spaces shown as '·', "
                  f"tabulations as '→'):")
            print("    " + show(file_content).replace("\n", "\n    "))
            print("    " + message.replace("\n", "\n    ") + "\n")
    color = green if nb_ok == len(tests) else red
    print(f"Validated: {color}{nb_ok}/{len(tests)}{reset}\n")
    return nb_ok


def main():
    sys.stdout.reconfigure(errors="replace")
    use_colors = sys.stdout.isatty() and (
        os.name != "nt" or "WT_SESSION" in os.environ)
    green = "\033[32m" if use_colors else ""
    red = "\033[31m" if use_colors else ""
    reset = "\033[0m" if use_colors else ""
    colors = (green, red, reset)

    if not (EXERCISE_DIR / SCRIPT).is_file():
        print(f"No {SCRIPT} found in {EXERCISE_DIR}")
        return 1

    tests = [(description, [FILENAME, key], content)
             for description, key, content in CASES]
    tests += [(description, arguments, None)
              for description, arguments in USAGE_CASES]
    nb_ok = run_tests("Substitution", tests, colors)

    bonus = [(description, [FILENAME, key, "-r"], content)
             for description, key, content in BONUS_CASES]
    bonus += [(description, arguments, None)
              for description, arguments in BONUS_USAGE_CASES]
    run_tests("Bonus: -r (optional, ignore it if you did not do the bonus)",
              bonus, colors)

    return 0 if nb_ok == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
