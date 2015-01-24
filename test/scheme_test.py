import unittest

import os, sys
lib = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(lib))
from lib.scheme import Scheme

class SchemeTest(unittest.TestCase):

    def test_parse_a_given_str(self):
        result = Scheme().parse("(begin (define r 10) (* pi (* r r)))")
        output = ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]
        self.assertEqual(result, output)

    def test_tokenize(self):
        input = Scheme().tokenize("(first (a))")
        output = ["(", "first", "(", "a", ")", ")"]
        self.assertEqual(input, output)

    def test_interpret(self):
        input = Scheme().interpret(["(", "first", "(", "a", ")", ")"])
        output = ['first', ['a']]
        self.assertEqual(input, output)

    def test_atom(self):
        input = Scheme().atom("1")
        output = 1
        input2 = Scheme().atom("1.2")
        output2 = 1.2
        input3 = Scheme().atom("hello")
        output3 = "hello"
        self.assertEqual(input, output)
        self.assertEqual(input2, output2)
        self.assertEqual(input3, output3)

    def test_global_scope(self):
        global_context = Scheme().globals()
        self.assertTrue('-' in global_context)

    def test_eval(self):
        scheme = Scheme()
        input = scheme.eval(scheme.parse("(* 5 2)"))
        output = 10
        self.assertEqual(input, output)




if __name__ == "__main__":
    unittest.main()
