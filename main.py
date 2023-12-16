import re

class finiteAutomation:
  def __init__(self):
    self.estado = 0
    self.alphaNum = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    self.nums = "0123456789"
    self.keyWords = ("program", "var", "integer", "real", "boolean", "procedure", "begin",
    "end", "if", "then", "else", "while", "do", "not")
    self.delimiters = ";.,:()"
    self.addOperator = "+-"
    self.multOperator = "*/"
    self.tabela = list()
    self.substring = ""
    self.error = False
    self.index = 0
    self.relacionalOpe = ("=", "<", ">", "<=", ">=", "<>")
    
  def transition(self, char):

    self.substring += char

    match self.estado:      
      #Estado inicial
      case 0:
        #Consigo ter parte de uma keyword?
        if(self.isKeyWord(self.substring)):
          self.estado = 1
        elif char == "{":
          self.estado = 3
        elif char in self.delimiters:
          if(char != ":"):
            self.tabela.append(char)
          else:
            self.estado = 4
        elif char == " ": #Para não comprometer a substring, ela é nula quando tem espaço em branco
          self.substring = ""
        elif char in self.alphaNum[0:52]:
          self.estado = 2
        elif char in self.alphaNum[52:]: #Estado que recebe número
          self.estado = 5
        elif char in self.addOperator or char in self.multOperator or char in self.relacionalOpe:
          if(char in "<>"):
            self.estado = 6
          else:
            self.tabela.append(char)

      case 1:
        if not self.isKeyWord(self.substring):
          if(char in self.alphaNum or char == "_"):
            self.estado = 2
          else:
            self.estado = 0
            self.tabela.append(self.substring[0:len(self.substring)-1])
            self.index -= 1 #Faz com que o caractere permaneça para a próxima análise
            self.substring = ""
        
      case 2:
        if char not in self.alphaNum and char != "_":
          self.estado = 0
          self.tabela.append(self.substring[0:len(self.substring)-1])
          self.substring = ""
          self.index -= 1
          self.substring = ""
      #Estado em que foi aberto um comentário
      case 3:
        self.error = True #Até que se fechem os comentários será retornado erro    
        if char == "}":
          self.estado = 0
          self.error = False 
          self.substring = ""
          self.tabela.append("{")
          self.tabela.append("}")
      
      case 4:
        if char == "=":
          self.tabela.append(":=")
          self.estado = 0
          self.substring = ""
        else:
          self.error = True
          self.estado = 0
          self.substring = ""
      case 5:
        #Erro
        if char in self.alphaNum[0:52] or char == "_":
          self.error = True
          self.estado = 0
        elif char != "." and char in self.delimiters or char in self.addOperator or char in self.multOperator or char in self.relacionalOpe:
          self.estado = 0
          self.tabela.append(self.substring[0:len(self.substring)-1])
          self.index -= 1
      case 6:
        if(self.substring in self.relacionalOpe):
          self.tabela.append(self.substring)
          self.estado = 0
        else:
          self.error = True

  def programInput(self, program):
    for self.index in range(0, len(program)):
      self.transition(program[self.index])

  def isKeyWord(self, word):
    for kw in self.keyWords:
      if(kw.startswith(word)):
        return True
    return False

#Lendo programa de um .txt
programFile = open("main.txt", "r")

#Criando string única com todo o programa
linhas = programFile.readlines()
linhas = [linha.replace("\n", " ") for linha in linhas]
linhaStr = "".join(linhas)

print(linhaStr)

#Instanciando um objeto
lexical = finiteAutomation()
lexical.programInput(linhaStr)
print(lexical.tabela) 

