#!/usr/bin/python

from printFunctions import exitWithError, printMainStep, printMiniStep
from reduceEquationFunctions import resolveExtract
from mathFunctions import isInt, ftSquare, ftMCD


def getDelta(valA, valB, valC, debug_option):
	if debug_option > 1:
		printMiniStep("Getting delta (square of):", str(valB) + "^2 - 4 * " + str(valA) + " * " + str(valC))
	delta = valB * valB - 4 * valA * valC
	complexNumber = False
	if delta < 0:
		complexNumber = True
		delta *= -1
	if not delta == 0:
		delta = ftSquare(delta)
	return delta, complexNumber


def getSolution(realVal, imagVal, downVal):
	mcd = 1
	if not realVal == 0 and not downVal == 1 and isInt(realVal) and isInt(downVal):
		mcd = ftMCD (realVal, downVal)
	if not imagVal == 0 and isInt(imagVal) and isInt(mcd):
		mcd = ftMCD (imagVal, mcd)
	realVal /= mcd
	imagVal /= mcd
	downVal /= mcd

	realRes = realVal / downVal
	realStr = ""
	if isInt(realRes):
		realRes = int(realRes)
	if not realRes == 0:
		realStr = str(realRes)
		if not downVal == 1 and isInt(realVal) and isInt(downVal):
			realStr += " (" + str(int(realVal)) + "/" + str(int(downVal)) + ")"
	elif imagVal == 0:
		realStr = "0"

	imagRes = imagVal / downVal
	imagStr = ""
	if isInt(imagRes):
		imagRes = int(imagRes)
	if not imagRes == 0:
		if not realStr == "":
			imagStr = " + "
		imagStr += str(imagRes) + "i"
		if not downVal == 1 and isInt(imagVal) and isInt(downVal):
			imagStr += " (" + str(int(imagVal)) + "/" + str(int(downVal)) + ")"


	solutionStr = "\n\t" + realStr + imagStr

	return solutionStr


def getSolutions(valA, valB, delta, complexNumber):
	solutionsStr = ""
	valB *= -1
	valA *= 2
	if complexNumber:
		solutionsStr += getSolution(valB, delta, valA)
		solutionsStr += getSolution(valB, -delta, valA)
	else:
		solutionsStr += getSolution(valB + delta, 0, valA)
		if not delta == 0:
			solutionsStr += getSolution(valB - delta, 0, valA)
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
		delta, complexNumber = getDelta(valA, valB, valC, debug_option)
		if debug_option > 1:
			strEquation =  "(-" + str(valB) + " +- " + str(delta)
			if complexNumber:
				strEquation += "i"
			strEquation += ") / (2 * " + str(valA) + ")"
			printMiniStep("Solutions:", strEquation)

		if delta == 0:
			header = "Discriminant is equal to zero, the solution is:"
		elif complexNumber:
			header = "Discriminant is strictly negative, the two complex solutions are:"
		else:
			header = "Discriminant is strictly positive, the two solutions are:"
		message = getSolutions(valA, valB, delta, complexNumber)
	elif grade == 1:
		header = "The solution is: "
		message = getSolution(-valC, 0, valB)
	elif grade == 0:
		if valC == 0:
			header = "The equation is true for every value of X !"
		else:
			header = "The equation has no possible solutions..!"

	printMainStep(header, message)
	return 0
