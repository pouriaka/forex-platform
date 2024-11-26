from src import *  #It will import all the things in src folder

# Creating an instance of the class
obj = modul1_class(5, 3)


# Accessing instance variables in other methods
result_add = obj.add()
result_multiply = obj.multiply()


print("Addition:", result_add)          # Output: 8
print("Multiplication:", result_multiply)   # Output: 15

