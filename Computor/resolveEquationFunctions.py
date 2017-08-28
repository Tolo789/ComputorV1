#!/usr/bin/python

from printFunctions import exitWithError, printMainStep, printMediumStep, printMiniStep
from reduceEquationFunctions import resolveExtract
from mathFunctions import isInt, ftSquare, simplifyFraction


def getDelta(valA, valB, valC):
	delta = valB * valB - 4 * valA * valC
	complexNumber = False
	if delta < 0:
		complexNumber = True
		delta *= -1
	if not delta == 0:
		delta = ftSquare(delta)
	return delta, complexNumber

def getRealSolution(upVal, downVal):
	if not upVal == 0 and not downVal == 1 and isInt(upVal) and isInt(downVal):
		upVal, downVal = simplifyFraction(upVal, downVal)
	solution = upVal / downVal
	if isInt(solution):
		solution = int(solution)
	solutionStr = "\n\t" + str(solution)
	if not upVal == 0 and not downVal == 1 and isInt(upVal) and isInt(downVal):
		solutionStr += " (Fraction equivalent: " + str(int(upVal)) + "/" + str(int(downVal)) + ")"
	return solutionStr


def getSolutions(valA, valB, delta, complexNumber):
	solutionsStr = ""
	valB *= -1
	valA *= 2
	if complexNumber:
		solutionsStr = ""
	else:
		solutionsStr += getRealSolution(valB + delta, valA)
		if not delta == 0:
			solutionsStr += getRealSolution(valB - delta, valA)
	return solutionsStr



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
	message = ""
	if grade > 2:
		header = "The polynomial degree is stricly greater than 2, I can't solve."
	elif grade == 2:
		delta, complexNumber = getDelta(valA, valB, valC)

		if delta == 0:
			header = "Discriminant is equal to zero, the solution is:"
		elif complexNumber:
			header = "Discriminant is strictly negative, the two complex solutions are:"
		else:
			header = "Discriminant is strictly positive, the two solutions are:"
		# TODO
		message = getSolutions(valA, valB, delta, complexNumber)
	elif grade == 1:
		header = "The solution is: "
		message = getRealSolution(-valC, valB)
	elif grade == 0:
		if valC == 0:
			header = "The equation is true for every value of X !"
		else:
			header = "The equation has no possible solutions..!"

	printMainStep(header, message)
	return 0
