#!/usr/bin/python

from printFunctions import exitWithError, printMainStep, printMediumStep, printMiniStep
from reduceEquationFunctions import resolveExtract


def ftSquare(val):
	#TODO
	result = 0

	return result


def getDelta(valA, valB, valC):
	#TODO
	delta = valB * valB - 4 * valA * valC
	complexNumber = False
	if delta > 0:
		complexNumber = True
		delta *= -1
	return delta, complexNumber


def resolveEquation(equation, debug_option):
	equation = resolveExtract(equation, 0)
	valA = 0
	valB = 0
	valC = 0
	other = 0

	for grade, coefficient in equation.viewitems():
		if grade == 0:
			valC = coefficient
		elif grade == 1:
			valB = coefficient
		elif grade == 2:
			valA = coefficient
		else:
			other = grade

	if not other == 0:
		grade = other
	elif not valA == 0:
		grade = 2
	elif not valB == 0:
		grade = 1
	else:
		grade = 0

	printMainStep("Polynomial degree: ", str(grade))
	if grade > 2:
		printMainStep("The polynomial degree is stricly greater than 2, I can't solve.", "")
	elif grade == 2:
		delta, complexNumber = getDelta(valA, valB, valC)

		if delta == 0:
			header = "Discriminant is equal to zero, the solution is:"
		elif not complexNumber:
			header = "Discriminant is strictly positive, the two solutions are:"
		else:
			header = "Discriminant is strictly negative, the two complex solutions are:"
			# TODO
		message = ""
		printMainStep(header, message)
	elif grade == 1:
		printMainStep("The only solution is: ", str(-valC / valB))
	elif grade == 0:
		if valC == 0:
			printMainStep("The equation is true for every value of X !", "")
		else:
			printMainStep("The equation has no possible solutions..!", "")
