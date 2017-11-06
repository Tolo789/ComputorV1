# ComputorV1
42 project: ComputorV1

### Objective
Create a polynomial equation resolver (up to the 2nd grade). The resolver must at first reduce the equation to it's basic form, then it has to find the solution(s) and display them.

### Usage

$> python computor.py [option] "polinomial equation"
 
e.g: $>python computor.py -P -h "5 + 3X + 3 * X^2 = X^2 + 0 * X"

### Options: (you need to include the '-')
  - -h	display help and exit
  - -p	prints main steps of the resolver
  - -P	prints every single step of the resolver
 
### Notes
  - You can only give one option at the time
  - You cannot do operations in esponential value
  - Parenthesis are not fully supported: you can only do simple multiplications around them
