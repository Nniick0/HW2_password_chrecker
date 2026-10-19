HW2 - Password Strength Checker
================================

Files
-----
password_checker.py       Main program (standard library only, Python 3.8+)
test_password_checker.py  unittest suite
README.txt                This file

How to run
----------
  python password_checker.py          (start the interactive checker)
  python -m unittest -v               (run all tests)

Rules (a password must satisfy ALL of them)
-------------------------------------------
1. Length >= 8
2. At least one uppercase letter (A-Z)
3. At least one lowercase letter (a-z)
4. At least one digit (0-9)
5. At least one special character from this list only: ! @ # $ % ^ & *
6. No character repeated 3 or more times in a row
   ("aa" is fine, "aaa" is not; "aAa" is fine because case differs)

Interaction
-----------
- The program prompts in a loop.
- If the password fails, ALL failed rules are listed, then it prompts again.
- If everything passes it prints "Password meets strength requirements." and exits.
- "q" or "quit" (any case, surrounding spaces ignored) exits immediately.

Design decisions
----------------
- The quit command is checked BEFORE validation, so "q" is never treated as a password.
- An empty or whitespace-only input gets its own message
  ("Password cannot be empty.") instead of a list of every failed rule.
- Symbols outside the list (e.g. - _ and space) are allowed in a password
  but do NOT count as special characters.
- Ctrl+C (KeyboardInterrupt) and Ctrl+D (EOFError) end the program with
  "Goodbye." instead of a traceback.
- input() is used (not getpass) so the typed password is visible in screenshots.
- Validation uses the raw input (not stripped), so leading/trailing spaces
  count as characters. Only the quit check and the empty check use strip().
- Letters and digits are matched by ASCII range, so characters such as the
  superscript "2" or full-width digits are not accepted as digits.
- Logic and I/O are separated: check_password(str) -> list of failure
  messages (empty list = strong); main() only handles the prompt loop.
- Rules live in one table (RULES) of (message, predicate); adding a rule
  means adding one line.

Test cases (input -> expected output)
-------------------------------------
Input            Expected output
---------------  ---------------------------------------------------------
Abcdef1!         Password meets strength requirements.   (exactly 8 chars)
Ab1!xyz          Fails: length (7 chars)
abcdef1!         Fails: uppercase
ABCDEF1!         Fails: lowercase
Abcdefg!         Fails: digit
Abcdefg1         Fails: special character
Abcdef1-         Fails: special character ("-" is not in the list)
Aabb1cd!         Meets requirements (two repeats are allowed)
Abbb1cd!         Fails: repeated 3+ times in a row
aAab1cD!         Meets requirements (a, A, a differ by case)
abc              Fails: length, uppercase, digit, special character
aaa              Fails: length, uppercase, digit, special, repeated
(empty line)     Password cannot be empty.
(spaces only)    Password cannot be empty.
q / Q            Goodbye.  (exit)
quit / QUIT      Goodbye.  (exit)
  quit           Goodbye.  (surrounding spaces ignored)
quit now / qq    Treated as a password and validated
Ctrl+C / Ctrl+D  Goodbye.  (exit, no traceback)

Sample console session
----------------------
Enter a password (q or quit to exit): abc
Password does not meet the following requirements:
  - At least 8 characters long
  - At least one uppercase letter (A-Z)
  - At least one digit (0-9)
  - At least one special character (!@#$%^&*)
Enter a password (q or quit to exit): Abbb1cd!
Password does not meet the following requirements:
  - No character repeated 3 or more times in a row
Enter a password (q or quit to exit): Aabb1cd!
Password meets strength requirements.
