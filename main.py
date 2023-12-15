import re

class finiteAutomation:
  def __init__(self):
    self.estado = 0
    self.alphaNum = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    self.keyWords = ("program", "var", "integer", "real", "boolean", "procedure", "begin",
    "end", "if", "then", "else", "while", "do", "not")
    self.delimiters = ";.,:"
    self.tabela = list()
    self.substring = ""
    self.error = False
    self.index = 0
    
  def transition(self, char):

    self.substring += char

    match self.estado:      
      #Estado inicial
      case 0:
        self.substring = ""

        #Consigo ter parte de uma keyword?
        if(self.isKeyWord(self.substring)):
          self.estado = 1
        elif char == "{":
          self.estado = 3
        elif char in delimiters:
          if(char != ":"):
            self.tabela.append(char)
          else:
            self.estado = 4
      case 1:
        if not self.isKeyWord(self.substring):
          if(char in self.alphaNum):
            self.estado = 2
          else:
            self.estado = 0
            self.tabela.append(self.substring[0:len(self.substring)-1])
            self.index -= 1 #Faz com que o caractere permaneça para a próxima análise
            
      case 2:
        if char not in self.alphaNum:
          self.estado = 0
          self.tabela.append(self.substring[0:len(self.substring)-1])
          self.substring = ""
          self.index -= 1
      #Estado em que foi aberto um comentário
      case 3:
        self.error = True #Até que se fechem os comentários será retornado erro    
        if char == "}":
          self.estado = 0
          self.error = False 
          self.substring = ""
          self.tabela.append("{")
          self.tabela.append("}")
      #Leu :
      case 4:
        if char == "=":
          self.tabela.append(":=")
          self.estado = 0
        else:
          self.error = True
          self.estado = 0

  def programInput(self, program):
    for self.index in range(0, len(program)):
      self.transition(program[self.index])

  def isKeyWord(self, word):
    for kw in self.keyWords:
      if(word in kw):
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

