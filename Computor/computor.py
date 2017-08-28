#!/usr/bin/python

import sys
from printFunctions import printUsage, exitWithError
from reduceEquationFunctions import reduceEquation
from resolveEquationFunctions import resolveEquation
from mathFunctions import ftPow

def parseArgv(argv):
	debug_option = 0
	equation = ""
	argc = len(argv)
	if argc == 1:
		exitWithError(-1)
	elif sys.argv[1] == "-h":
		printUsage()
		sys.exit(2)
	elif sys.argv[1] == "-p" or sys.argv[1] == "-P":
	 	if argc == 2:
			exitWithError(-1)
		elif argc > 3:
			exitWithError(-2)
		if sys.argv[1] == "-p":
			debug_option = 1
		else:
			debug_option = 2
		equation = sys.argv[2]
	elif argc == 2:
		equation = sys.argv[1]
	else:
		exitWithError(-2)

	return equation, debug_option


def lexicalCheck(equation):
	splitEquation = []
	okChars = {'+', '-', '*', '/', 'X', '^', '(', ')', '=', '.'}
	tmpNumber = 0
	decimalCount = 0
	isTmpNumber = False
	isDecimal = False
	leftSide = True
	count = 0
	for c in equation:
		if not c in okChars:
			if not c.isdigit():
				exitWithError(-3)
			else:
				if isDecimal:
					decimalCount += 1
					c = int(c) / float(ftPow(10, decimalCount))
					tmpNumber += c
				elif isTmpNumber:
					if tmpNumber == 0:
						exitWithError(-12)
					tmpNumber = tmpNumber * 10 + float(c)
				else:
					tmpNumber = float(c)
					isTmpNumber = True
		else:
			if c == '(':
				count += 1
			elif c == ')':
				if count == 0:
					exitWithError(-6)
				count -= 1
			elif c == '=':
				if not leftSide:
					exitWithError(-9)
				elif not count == 0:
					exitWithError(-6)
				leftSide = False

			if c == '.':
				if not isTmpNumber or isDecimal:
					exitWithError(-13)
				isDecimal = True
				decimalCount = 0
			elif isDecimal and decimalCount == 0:
				exitWithError(-13)
			elif isTmpNumber:
				splitEquation.append(str(tmpNumber))
				isTmpNumber = False
				isDecimal = False
				splitEquation.append(c)
			else:
				splitEquation.append(c)

	if isTmpNumber:
		splitEquation.append(str(tmpNumber))

	if len(splitEquation) == 0:
		exitWithError(-4)
	elif not '=' in splitEquation:
		exitWithError(-5)
	elif not count  == 0:
		exitWithError(-6)

	return splitEquation


def bringRightToLeft(equation):
	splitIndex = equation.index('=')

	leftSide = equation[:splitIndex]
	if len(leftSide) == 0:
		exitWithError(-7)
	leftSide.insert(0, '(')

	rightSide = equation[splitIndex + 1:]
	if len(rightSide) == 0:
		exitWithError(-8)
	rightSide.insert(0, '(')
	rightSide.insert(0, '-')
	rightSide.append(')')
	rightSide.append(')')

	leftSide.extend(rightSide)
	if '=' in leftSide:
		exitWithError(-9)
	return leftSide


def main(argv):
	equation, debug_option = parseArgv(argv)
	equation = equation.replace(" ", "")

	equation = lexicalCheck(equation)
	equation = bringRightToLeft(equation)
	equation = reduceEquation(equation, debug_option)
	resolveEquation(equation, debug_option)

	return 0

main(sys.argv)
