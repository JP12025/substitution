# Substitution

# What to Do

In a substitution cipher, we “encrypt” (i.e., conceal in a reversible way) a message by replacing every letter with another letter.
To do so, we use a key: in this case, a mapping of each of the letters of the alphabet to the letter it should correspond to when we encrypt it.
To “decrypt” the message, the receiver of the message would need to know the key, so that they can reverse the process:
translating the encrypted text (generally called `ciphertext`) back into the original message (generally called `plaintext`).

A key, for example, might be the string `NQXPOMAFTRHZLGECYJIUWSKDVB`.
This 26-character key means that A (the first letter of the alphabet) should be converted into N (the first character of the key),
B should be converted into Q (the second character of the key), and so forth.

|plain|A|B|C|D|E|F|G|H|I|J|K|L|M|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|cipher|N|Q|X|P|O|M|A|F|T|R|H|Z|L|
| | | | | | | | | | | | | | |
|plain|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|
|cipher|G|E|C|Y|J|I|U|W|S|K|D|V|B|

A message like `HELLO`, then, would be encrypted as `FOZZE`, replacing each of the letters according to the mapping determined by the key.

In a file called `substitution.py`, write a Python program that enables you to encrypt messages using a substitution cipher.
At the time the user executes the program, they should provide two command-line arguments:
- the first argument is the name of a file containing the message to encrypt;
- the second argument is the key used to encrypt the message.

The encrypted message is printed on the standard output.

```bash
$ python substitution.py examples/hello.txt NQXPOMAFTRHZLGECYJIUWSKDVB
FOZZE
```

Your program must encrypt the entire content of the file:
- only letters are replaced, and they keep their case: an uppercase letter stays uppercase, a lowercase letter stays lowercase;
- every other character (spaces, digits, punctuation, tabulations, newlines…) is copied unchanged;
- the output is exactly the encrypted content of the file: nothing more, nothing less (not even an extra empty line at the end).

```bash
$ python substitution.py examples/fish.txt AZERTYUIOPQSDFGHJKLMWXCVBN
Gft yoli. Mcg yoli! Ktr yoli? Zswt yoli.
```

![Demo of scrabble.py](scrabble.gif)

The key must contain each of the 26 letters of the alphabet exactly once.
It may be written in uppercase, in lowercase, or both: `NQXPOMAFTRHZLGECYJIUWSKDVB`, `nqxpomaftrhzlgecyjiuwskdvb`
and `NqXpOmAfTrHzLgEcYjIuWsKdVb` are the same key.

If there are not exactly two arguments, or if the key is not valid, the program prints `Usage: python substitution.py filename key` and stops,
without opening the file.
You don't have to check that the first argument is the name of an existing file.

```bash
$ python substitution.py
Usage: python substitution.py filename key
$ python substitution.py examples/hello.txt ABC
Usage: python substitution.py filename key
```

> [!TIP]
> The command-line arguments are stored in the list `sys.argv` (after `import sys`).
> `sys.argv[0]` is the name of the script, so for `python substitution.py examples/hello.txt NQXPOMAFTRHZLGECYJIUWSKDVB`,
> `sys.argv` is `['substitution.py', 'examples/hello.txt', 'NQXPOMAFTRHZLGECYJIUWSKDVB']`.
> To stop your program right away, you may use `sys.exit()`.

> [!TIP]
> To read the whole content of a file in a single `str`:
> ```python
> with open(filename) as file:
>     text = file.read()
> ```
> The text read ends with a newline character `"\n"`, which is part of the message:
> `print(text, end="")` prints a text without adding another newline.

> [!TIP]
> To find the position of a letter in the alphabet, you may use a string such as `"ABCDEFGHIJKLMNOPQRSTUVWXYZ"` and its method `index()`.
> The methods `isupper()`, `islower()`, `upper()` and `lower()` will help you keep the case of each letter.
> How can you check that the key contains every letter of the alphabet? Is checking its length enough?

## Bonus

Let your program accept an optional third argument `-r` at the end of the command line that lets you decrypt a message.

```bash
$ cat examples/secret.txt
Gft yoli. Mcg yoli! Ktr yoli? Zswt yoli.
$ python substitution.py examples/secret.txt AZERTYUIOPQSDFGHJKLMWXCVBN -r
One fish. Two fish! Red fish? Blue fish.
```

Any other third argument (e.g. `python substitution.py message.txt AZERTYUIOPQSDFGHJKLMWXCVBN -x`) prints the usage message.

# How to Test

Test your program from the exercise folder with:

```bash
python test_substitution.py
```

(use `python3` instead of `python` if that is how you run Python on your computer).

The script runs your program as a user would: it writes a message in a file, gives the file name and a key on the command line,
then checks what your program prints.
When a test fails, it explains what is wrong and shows the first letter that is not correctly encrypted.
The tests of the bonus are shown separately: if you did not do the bonus, you can ignore them.

Don't forget it's important to test your program yourself too.
The folder `examples` contains a few messages to start with.
What happens if:
* there is no argument at all? only one? three?
* the key is too short? too long?
* the key has 26 characters, but a letter appears twice?
* the key contains a digit?
* the key is written in lowercase?
* the key is given before the file name?
* the message contains spaces, digits, punctuation or several lines?

```bash
$ python substitution.py examples/hello.txt AZERTYUIOPQSDFGHJKLMWXCVBN
ITSSG
$ python substitution.py examples/harry.txt MLKJHGFDSQNBVCXWPOIUYTREZA
Dmooz Wxuuho rmi m dsfdbz ycyiymb lxz sc vmcz rmzi.
Gxo xch udscf, dh dmuhj udh iyvvho dxbsjmzi vxoh udmc mcz xudho usvh xg zhmo.
Gxo mcxudho, dh ohmbbz rmcuhj ux jx dsi dxvhrxon, lyu rmi gxokhj ux jx su sc ihkohu, sc udh jhmj xg udh csfdu.
Mcj dh mbix dmwwhchj ux lh m rsamoj.
$ python substitution.py examples/hello.txt GFDSQTREZABGCXWPOIUYMHKJHN
Usage: python substitution.py filename key
$ python substitution.py AZERTYUIOPQSDFGHJKLMWXCVBN examples/hello.txt
Usage: python substitution.py filename key
```

# How to Submit

Once you're done with all tasks, submit all your python files on Moodle.

# Licence

This course is freely inspired by [CS50’s Introduction to Computer Science](https://cs50.harvard.edu/x/2025/) Harvard. It is licensed under a [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.
