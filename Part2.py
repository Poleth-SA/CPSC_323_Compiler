#This code isn't finished a product, Had bug that weren't fixed.


from pTable import p_table
from part3 import Translator

# define reserved words and signs
reserved = {'program', 'var', 'begin', 'end.', 'write', 'integer'}
signs = {';', '=', '+', '*', '(', ')', ',', ':', '.'}

# intializes new token instance
# and an offical <str> rep of the instance
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"
    
class Lexer:
    def __init__(self, input):
        self.input = input
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        with open(self.input, 'r') as file:
            txt = file.read().split()

        for word in txt:
            if word in reserved:
                self.tokens.append(Token('STR', word))
            elif word in signs:
                self.tokens.append(Token('SIGN', word))
            elif word.isdigit():
                for digit in word:
                    self.tokens.append(Token('NUM', digit))
            elif word.startswith('"') and word.endswith('"'):
                self.tokens.append(Token('STR', word))
            else:
                self.split_non_reserved(word)

    def split_non_reserved(self, word):
        for char in word:
            if char.isdigit():
                self.tokens.append(Token('NUM', char))
            else:
                self.tokens.append(Token('IDENTIFIER', char))
        
    def next_token(self):
        try:
            return self.tokens.pop(0)
        except IndexError:
            return Token('EOF', None)
        
class Parser:
    def __init__(self, lexer, trans):
        self.lexer = lexer
        self.translator = trans
        self.stack = ['EOF', 'S']
        self.token_buffer = []
        self.in_var, self.in_main, self.in_write = False, False, False

    def parse(self):
        current_token = self.lexer.next_token()
        while self.stack:
            top = self.stack.pop()
            if self.match(top, current_token):
                if current_token.type == 'EOF':
                    break
                self.execute_actions(top, current_token)
                current_token = self.lexer.next_token()
            elif self.is_non_term(top):
                self.process_non_term(top, current_token)
            else:
                self.raise_syntax_error(top, current_token)

    def match(self, top, token):
        return top == token.value or top == token.type

    def execute_actions(self, top, token):
        if self.in_var and token.value == ':':
            self.in_var = False
            self.trans.add_code(f"{'='.join(''.join(self.token_buffer).split(','))} = 0")
            self.token_buffer = []
        elif token.type == "KEYWORD" and self.process_keyword(token):
            return
        elif self.in_main and token.value == ';':
            self.process_end_of_statement()
        elif self.in_main and token.value == 'write':
            self.in_write = True
            self.token_buffer.append("print")
        else:
            self.token_buffer.append(token.value)

    def process_keyword(self, token):
        if token.value in ('var', 'begin'):
            if token.value == 'var':
                self.in_var = True
            else:
                self.in_main = True
            return True
        return False

    def process_end_of_statement(self):
        self.in_write = False
        self.trans.add_code(''.join(self.token_buffer))
        self.token_buffer = []

    def process_non_terminal(self, non_term, token):
        key = (non_term, token.value)
        if key in p_table:
            for symbol in reversed(p_table[key]):
                self.stack.append(symbol)
        else:
            self.handle_missing_rule(non_term, token)

    def raise_syntax_error(self, expected, found):
        raise Exception(f"Syntax error: unexpected token {found.type} ({found.value}). Expected {expected}")

    def handle_missing_rule(self, non_term, token):
        expected_tokens = [k[1] for k in p_table if k[0] == non_term]
        expected_str = ', '.join(expected_tokens)
        if not expected_tokens:
            expected_str = 'No expected tokens found'
        raise Exception(f"Syntax error: No rule for {non_term} with lookahead {token.value}. Expected: {expected_str}")

    def is_non_terminal(self, symbol):
        return symbol in {key[0] for key in p_table.keys()}
    
if __name__ == "__main__":
    lexer = Lexer('final24.txt')
    trans = Translator()
    parser = Parser(lexer, trans)

    try:
        parser.parse()
        print("Parsing completed successfully!")
        trans.generate_code()
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
