import re

class finiteAutomation:
  def __init__(self):
    word = ""
  
  def transition(self, char):
    key_words = ("program", "var", "integer", "real", "boolean", "procedure", "begin",
    "end", "if", "then", "else", "while", "do", "not")
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"
    

  def programInput(self, program):
    for char in program:
      self.transition(char)