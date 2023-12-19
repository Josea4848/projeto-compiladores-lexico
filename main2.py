import re

class Lexical:
    def __init__(self):
      self.patterns = [
      ('real', r'\b\d+\.\d*\b'), #REAIS
      ('integer', r'\b\d+\b'),  #KEYWORD: INTEIROS
      ('keyword',r'\b(var|program|real|integer|var|boolean|procedure|begin|end|if|then|else|while|do|not)\b'), #KEYWORD: VAR 
      ('multiplicative_operator', r'(\*|/|\band\b)'),
      ('additive_operators', r'(\+|-|\bor\b)'),  # OPERADORES ADITIVOS
      ('identifier', r'\b[a-zA-z]\w*\b'),
      ('WHITESPACE', r'\s+'), # Identificacao do espaco em branco
      ('assignment',r':='),
      ('relational_operator', r'<(=|>)?|>=?|='),
      ('delimiter',r'(;|\.|\(|\)|,|:)'),
      ('comment',r'{(.|\n)*}'),
      ('open_commentary',r'{'),
      ('close_commentary',r'}')]
      self.token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.patterns)
      self.lexer = re.compile(self.token_regex)
      self.table = {"Token":list(),"Classificação":list(),"Line":list()}
      self.open = False
      self.notOpen = False

    def tokenizador(self, program, line):
      for match in self.lexer.finditer(program):
          for name, pattern in self.patterns:
              token = match.group(name)
              if token:
                if name == "open_commentary":
                   self.open = True
                if name == "close_commentary":
                  if self.open:
                    self.open = False
                  else:
                     self.notOpen = True

                if not self.open and name not in 'WHITESPACEcommentclose_commentaryopen_commentary':
                    self.addTable(token, name, line)
                    break
    #Adiciona token a tabela
    def addTable(self, token, classificao, line):
       self.table["Token"].append(token)
       self.table["Classificação"].append(classificao)
       self.table["Line"].append(line)
    #Exibe tabela
    def showTable(self):
      arquivo = open("tabela2.csv", "w+")
      arquivo.write("Token;Classificação;Linha\n")

      for index in range(0, len(self.table["Token"])):
        arquivo.write(f""""{self.table['Token'][index]}";{self.table['Classificação'][index]}; {self.table['Line'][index]}\n""")

# Input program
arquivo = open("main.txt", "r")
program = arquivo.readlines()

#Instanciando um objeto
analisador = Lexical()

for index in range(0, len(program)):
  analisador.tokenizador(program[index], index+1)

if(analisador.open or analisador.notOpen):
   print("Comentário não fechado")

analisador.showTable()
