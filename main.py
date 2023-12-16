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
    self.tabela =  {"Token": list(), "Classificação": list(), "Line": list()}
    self.substring = ""
    self.line = 1
    self.error = False
    self.index = 0
    self.relacionalOpe = ("=", "<", ">", "<=", ">=", "<>")
    
  def transition(self, char):

    self.substring += char
    #Contador de linhas

    match self.estado:      
      #Estado inicial
      case 0:
        #Consigo ter parte de uma keyword?
        if(self.isKeyWord(self.substring)):
          self.estado = 1
        elif(self.isOperator(self.substring)):
          self.estado = 7
        elif char == "{":
          self.estado = 3
        elif char in self.delimiters:
          if(char != ":"):
            self.addTable(char, "Delimiter", self.line)
            self.substring = ""
          else:
            self.estado = 4
        elif char == " " or char == "\n": #Para não comprometer a substring, ela é nula quando tem espaço em branco
          self.substring = ""
        elif char in self.alphaNum[0:52]: #Recebe letra
          self.estado = 2
        elif char in self.alphaNum[52:]: #Estado que recebe número
          self.estado = 5
        elif char in "+-":
          self.estado = 6
          self.keepIndex()
      
      case 1:
        if not self.isKeyWord(self.substring):
          if(char in self.alphaNum or char == "_"):
            self.estado = 2
          else:
            self.estado = 0
            self.addTable(self.substring[0:len(self.substring)-1], "Palavra reservada", self.line)
            if(char != "\n"):
              self.keepIndex() #Faz com que o caractere permaneça para a próxima análise
            self.substring = ""
        
      case 2:
        if char not in self.alphaNum and char != "_":
          self.estado = 0
          self.addTable(self.substring[0:len(self.substring)-1], "identificador", self.line)
          self.substring = ""
          if(char != "\n"):
            self.keepIndex()
      #Estado em que foi aberto um comentário
      case 3:
        self.error = True #Até que se fechem os comentários será retornado erro    
        if char == "}":
          self.estado = 0
          self.error = False 
          self.substring = ""
      
      case 4:
        if char == "=":
          self.addTable(":=", "Atribuição", self.line)
        else:
          self.addTable(":", "Delimitador", self.line)
          if(char != "\n"):
            self.keepIndex()
        self.estado = 0
        self.substring = ""
          
      case 5:
        #Erro
        if char != "." and char not in self.alphaNum[52:]:
          self.estado = 0
          if("." in self.substring):
            self.addTable(self.substring[0:len(self.substring)-1], "real", self.line)
          else: 
            self.addTable(self.substring[0:len(self.substring)-1], "int", self.line)
          if(char != "\n"):
            self.keepIndex()
      
      case 6:
        self.addTable(char, "Additive operator", self.line)
        self.estado = 0
        self.substring = ""
      
      case 7:
        if not self.isOperator(self.substring):
          if(char in self.alphaNum):
            self.estado = 2
          else:
            self.estado = 0
            if("or" in self.substring):
              self.addTable(self.substring[0:len(self.substring)-1], "Additive operator", self.line)
            else:
              self.addTable(self.substring[0:len(self.substring)-1], "multiplicative operator", self.line)
            self.substring = ""

    if(char == "\n"):
      self.line += 1

  def programInput(self, program):    
    while(self.index < len(program)):
      self.transition(program[self.index])
      self.index += 1

  def isKeyWord(self, word):
    for kw in self.keyWords:
      if(kw.startswith(word)):
        return True
    return False
  
  def isOperator(self, word):
    return "or".startswith(word) or "and".startswith(word)

  def keepIndex(self):
    self.index -= 1

  def addTable(self, token, classification, line):
    self.tabela["Token"].append(token)
    self.tabela["Classificação"].append(classification)
    self.tabela["Line"].append(line)

  def showTable(self):
    arquivo = open("tabela.csv", "w+")
    arquivo.write("Token;Classificação;Linha\n")

    for index in range(0, len(self.tabela["Token"])):
      arquivo.write(f""""{self.tabela['Token'][index]}";{self.tabela['Classificação'][index]}; {self.tabela['Line'][index]}\n""")
      

#Lendo programa de um .txt
programFile = open("main.txt", "r")

#Criando string única com todo o programa
linhas = programFile.readlines()
linhaStr = "".join(linhas)

print(linhaStr)

#Instanciando um objeto
lexical = finiteAutomation()
lexical.programInput(linhaStr)
lexical.showTable()