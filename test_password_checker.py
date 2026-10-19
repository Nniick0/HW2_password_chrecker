import io
import unittest
from unittest import mock

import password_checker as pc

LEN = pc.RULES[0][0]
UPPER = pc.RULES[1][0]
LOWER = pc.RULES[2][0]
DIGIT = pc.RULES[3][0]
SPECIAL = pc.RULES[4][0]
REPEAT = pc.RULES[5][0]


def run_main(inputs):
    """Run main() with scripted input; return everything it printed."""
    out = io.StringIO()
    with mock.patch("builtins.input", side_effect=inputs), \
            mock.patch("sys.stdout", out):
        pc.main()
    return out.getvalue()


class CheckPasswordTests(unittest.TestCase):
    def test_all_pass(self):
        self.assertEqual(pc.check_password("Abcdef1!"), [])

    def test_each_rule_fails_alone(self):
        cases = [
            ("Ab1!xyz", [LEN]),            # 7 chars
            ("abcdef1!", [UPPER]),
            ("ABCDEF1!", [LOWER]),
            ("Abcdefg!", [DIGIT]),
            ("Abcdefg1", [SPECIAL]),
            ("Abbb1xy!", [REPEAT]),
        ]
        for pw, expected in cases:
            with self.subTest(pw=pw):
                self.assertEqual(pc.check_password(pw), expected)

    def test_multiple_failures_all_listed(self):
        self.assertEqual(pc.check_password("abc"),
                         [LEN, UPPER, DIGIT, SPECIAL])

    def test_exactly_8_chars_passes_length(self):
        self.assertNotIn(LEN, pc.check_password("Abcdef1!"))
        self.assertIn(LEN, pc.check_password("Abcde1!"))

    def test_two_repeats_ok_three_fail(self):
        self.assertEqual(pc.check_password("Aabb1cd!"), [])
        self.assertEqual(pc.check_password("Abbb1cd!"), [REPEAT])
        self.assertEqual(pc.check_password("Aaaab1c!"), [REPEAT])

    def test_repeat_is_case_sensitive(self):
        self.assertEqual(pc.check_password("aAab1cD!"), [])
        self.assertEqual(pc.check_password("aaab1cD!"), [REPEAT])

    def test_repeated_special_chars_count(self):
        self.assertIn(REPEAT, pc.check_password("Abcd1!!!"))

    def test_symbols_outside_list_are_not_special(self):
        for ch in "-_ ":
            with self.subTest(ch=repr(ch)):
                self.assertEqual(pc.check_password("Abcde1" + ch + "x"),
                                 [SPECIAL])

    def test_empty_and_whitespace_only_return_failures(self):
        self.assertEqual(len(pc.check_password("")), 5)  # all but repeat
        self.assertIn(LEN, pc.check_password("   "))

    def test_non_ascii_digit_not_accepted(self):
        self.assertIn(DIGIT, pc.check_password("Abcdef²!"))


class QuitCommandTests(unittest.TestCase):
    def test_quit_variants(self):
        for text in ["q", "Q", "quit", "QUIT", "Quit", "  q  ", "\tquit\n"]:
            with self.subTest(text=text):
                self.assertTrue(pc.is_quit_command(text))

    def test_not_quit(self):
        for text in ["", "qq", "quit now", "quitt", "Abcdef1!"]:
            with self.subTest(text=text):
                self.assertFalse(pc.is_quit_command(text))


class MainLoopTests(unittest.TestCase):
    def test_success_ends_loop(self):
        out = run_main(["Abcdef1!"])
        self.assertIn("Password meets strength requirements.", out)

    def test_quit_exits_immediately(self):
        out = run_main(["QUIT"])
        self.assertIn("Goodbye.", out)
        self.assertNotIn("meets", out)

    def test_failure_lists_all_then_reprompts(self):
        out = run_main(["abc", "Abcdef1!"])
        for msg in (LEN, UPPER, DIGIT, SPECIAL):
            self.assertIn(msg, out)
        self.assertNotIn(LOWER, out)
        self.assertIn("Password meets strength requirements.", out)

    def test_empty_gets_dedicated_message(self):
        for text in ["", "   "]:
            with self.subTest(text=repr(text)):
                out = run_main([text, "q"])
                self.assertIn("Password cannot be empty.", out)
                self.assertNotIn(LEN, out)

    def test_ctrl_d_and_ctrl_c_exit_cleanly(self):
        for exc in (EOFError, KeyboardInterrupt):
            with self.subTest(exc=exc.__name__):
                out = run_main(exc())
                self.assertIn("Goodbye.", out)


if __name__ == "__main__":
    unittest.main()
