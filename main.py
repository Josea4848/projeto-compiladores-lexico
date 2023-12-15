import re

class finiteAutomation:
  def __init__(self):
    self.estado = 1
    self.alphaNum = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    self.tabela = list()

  def transition(self, char):
    match self.estado:
      case 1:
        if char == "p":
          self.estado = 2
      case 2:
        if char == "r":
          self.estado = 3
      case 3:
        if char == "o":
          self.estado = 4
      case 4: 
        if char == "g":
          self.estado = 5
      case 5:
        if char == "r":
          self.estado = 6
      case 6: 
        if char == "a":
          self.estado = 7
      case 7: 
        if char == "m":
          self.estado = 8
      case 8: 
        print(f"{char} não está em alpha: {char not in self.alphaNum}")
        if char not in self.alphaNum:
          self.tabela.append("program")
          self.estado = 1
        else:
          self.estado = 38

  def programInput(self, program):
    for char in program:
      self.transition(char)


#Lendo programa de um .txt
programFile = open("main.txt", "r")

#Criando string única com todo o programa
linhas = programFile.readlines()
linhas = [linha.replace("\n", " ") for linha in linhas]
linhaStr = "".join(linhas)

#Instanciando um objeto
lexical = finiteAutomation()
lexical.programInput(linhaStr)
print(lexical.tabela) 
