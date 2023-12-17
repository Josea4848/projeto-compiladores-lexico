import re

patterns = [
    ('REAL', r'\b\d+\.\d+\b'), #REAIS
    ('INTEGER', r'\b\d+\b'),  #KEYWORD: INTEIROS
    ('KEYWORD',r'\b(var|program|real|integer|var|boolean|procedure|begin|end|if|then|else|while|do|not)\b'), #KEYWORD: VAR
    ('multiplicative_operator', r'\b(\*|/|and)\b'),
    ('ADDITIVE_OPERATORS', r'\b(\+|-|or)\b'),  # OPERADORES ADITIVOS
    ('IDENTIFICADOR', r'\b[a-zA-z|_]\w*\b'),
    ('WHITESPACE', r'\s+'), # Identificacao do espaco em branco
    ('relational_operator', r'<(=|>)?|>=?|=')
]

# Input program
arquivo = open("main.txt", "r")
program = arquivo.readlines()

# Compilacao dos padores regex
token_regex = '|'.join('(?P<%s>%s)' % pair for pair in patterns)
lexer = re.compile(token_regex)

# Tokenizacao (separacao dos tokens) do string de entrada
tokens = []
for line in program:
  for match in lexer.finditer(line):
      for name, pattern in patterns:
          token = match.group(name)
          if token:
              tokens.append((name, token))
              break

for token in tokens:
    print(token)