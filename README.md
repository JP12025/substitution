# Substitution

<img src="https://images.saymedia-content.com/.image/c_limit%2Ccs_srgb%2Cq_auto:eco%2Cw_672/MTc0NDYwNzg4ODA2MTk4OTE4/top-insane-magic-the-gathering-cards.webp" alt="abc" width="300">

# What to Do

In a substitution cipher, we “encrypt” (i.e., conceal in a reversible way) a message by replacing every letter with another letter. To do so, we use a key: in this case, a mapping of each of the letters of the alphabet to the letter it should correspond to when we encrypt it. To “decrypt” the message, the receiver of the message would need to know the key, so that they can reverse the process: translating the encrypt text (generally called ciphertext) back into the original message (generally called plaintext).

A key, for example, might be the string `NQXPOMAFTRHZLGECYJIUWSKDVB`. This 26-character key means that A (the first letter of the alphabet) should be converted into N (the first character of the key), B (the second letter of the alphabet) should be converted into Q (the second character of the key), and so forth.

|plain|A|B|C|D|E|F|G|H|I|J|K|L|M|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|cipher|N|Q|X|P|O|M|A|F|T|R|H|Z|L|
| | | | | | | | | | | | | | |
|plain|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|
|cipher|G|E|C|Y|J|I|U|W|S|K|D|V|B|

A message like HELLO, then, would be encrypted as FOZZE, replacing each of the letters according to the mapping determined by the key.

In a file called `substitution.py`, create a program that enables you to encrypt messages using a substitution cipher. At the time the user executes the program, they should provide two command-line arguments. 
- The first argument must be the name of a file containing the message to encrypt. 
- The second argument must be the key to encrypt the message.
- The encrypted message must be printed on the standard output.

You don't have to verify that the first argument is a filename, but you must check that the second
argument contains all 26 alphabet characters. Obviously, you must verify that two arguments are provided.
If an error occurs at this step, your program should print the folloing `Usage` and quit.

```bash
$ python substitution.py
Usage: python substitution.py filename key
```

Your program must encrypt the entire contents of the file. Of course, it must only encrypt letters, but it must be case-sensitive. The encrypted message should keep punctuation, spaces, newlines and other hidden characters.

## Bonus

Add an optional third parameter at the of end the command line `-r` that let you decrypt a message.

```bash
$ cat message.txt
Gft yoli. Mcg yoli! Ktr yoli? Zswt yoli.
$ python substitution.py message.txt AZERTYUIOPQSDFGHJKLMWXCVBN
One fish. Two fish! Red fish? Blue fish.
```

# When to Do it

By Sunday, january 26, 2025 at 11:59 PM

# How to Test

Test your script with command `./check substitution.py`

The following examples should help you to develop your program.

```bash
$ python substitution.py .test/01.in AZERTYUIOPQSDFGHJKLMWXCVBN
Gft yoli. Mcg yoli! Ktr yoli? Zswt yoli.
```

```bash
$ python substitution.py .test/02.in AZERTYUIOPQSDFGHJKLMWXCVBN
ITSSG
```

```bash
$ python substitution.py .test/03.in MLKJHGFDSQNBVCXWPOIUYTREZA
Kxcfomuybmusxci! Uxjmz si zxyo jmz. Zxy'oh xgg ux Fohmu Wbmkhi! Zxy'oh xgg mcj mrmz!
```

```bash
$ python substitution.py .test/04.in MLKJHGFDSQNBVCXWPOIUYTREZA
Dmooz Wxuuho rmi m dsfdbz ycyiymb lxz sc vmcz rmzi.
Gxo xch udscf, dh dmuhj udh iyvvho dxbsjmzi vxoh udmc mcz xudho usvh xg zhmo. 
Gxo mcxudho, dh ohmbbz rmcuhj ux jx dsi dxvhrxon, lyu rmi gxokhj ux jx su sc ihkohu, sc udh jhmj xg udh csfdu. 
Mcj dh mbix dmwwhchj ux lh m rsamoj.
```

# How to Submit

Once you're done with all tasks, submit all your python files for the week on Moodle.

# Licence

This course is freely inspired from [CS50’s Introduction to Computer Science](https://cs50.harvard.edu/x/2025/) Harvard. It is licensed under a [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license. 
