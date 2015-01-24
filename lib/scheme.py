import math, operator as op

# basic data types
Symbol = str
List = list
Number = (int, float)

class Context():

    class __store(dict):
        pass

    __instance = None

    def __init__(self):
        if Context.__instance is None:
            Context.__instance = Context.__store()


        self.__dict__['_Context_instance'] = Context.__instance

        self.update(vars(math))
        self.update({
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.div,
            '>': op.gt,
            '<': op.lt,
            '>=': op.ge,
            '<=': op.le,
            '=': op.eq,
            'abs':     abs,
            'append':  op.add,  
            'apply':   apply,
            'begin':   lambda *x: x[-1],
            'car':     lambda x: x[0],
            'cdr':     lambda x: x[1:], 
            'cons':    lambda x,y: [x] + y,
            'eq?':     op.is_, 
            'equal?':  op.eq, 
            'length':  len, 
            'list':    lambda *x: list(x), 
            'list?':   lambda x: isinstance(x,list), 
            'map':     map,
            'max':     max,
            'min':     min,
            'not':     op.not_,
            'null?':   lambda x: x == [], 
            'number?': lambda x: isinstance(x, Number),
            'procedure?': callable,
            'round':   round,
            'symbol?': lambda x: isinstance(x, Symbol),
        })

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


class Scheme():

    def parse(self, input):
        return self.interpret(self.tokenize(input))

    def tokenize(self, input):
        return input.replace('(', ' ( ').replace(')', ' ) ').split()

    def interpret(self, tokens):
        if len(tokens) == 0:
            raise SyntaxError('unexpected EOF white reading')
        token = tokens.pop(0)

        if '(' == token:
            node = []
            while tokens[0] != ')':
                node.append(self.interpret(tokens))

            tokens.pop(0)
            return node
        elif ')' == token:
            raise SyntaxError('unexpected )')
        else:
            return self.atom(token)


    def atom(self, token):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return Symbol(token)

    def eval(self, node, context=False):

        if not context:
            context = Context()

        if isinstance(node, List) and len(node) == 1:
            node = node[0]

        if isinstance(node, Symbol):
            return context[node]
        elif not isinstance(node, List):
            return node
        elif node[0] == 'quote':
            (_, exp) = node
            return exp
        elif node[0] == 'if':
            (_, test, conseq, alt) = x
            exp = (conseq if self.eval(test, context) else alt)
            return self.eval(exp, context)
        elif node[0] == 'define':
            (_, var, exp) = node
            context[var] = self.eval(exp, context)
        else:
            proc = self.eval(node[0], context)
            args = [self.eval(arg, context) for arg in node[1:]]
            return proc(*args)

