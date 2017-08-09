#!/usr/bin/python

import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def printUsage():
	print 'USAGE:\n $> python computor.py [option] "polinomial equation"\n'
	print "OPTIONS: (you need to include the '-')"
	print ' -h\tdisplay help and exit'
	print ' -p\tprints main steps of the resolver'
	print ' -P\tprints every single step of the resolver'
	sys.exit(2)


def exitWithError(error):
	printHelp = False
	if error == -1:
		message = 'No polinomial equation given !!\n'
		printHelp = True
	elif error == -2:
		message = 'Wrong parameters given !!\n'
		printHelp = True
	elif error == -3:
		message = 'Lexical error in the equation !!\n'
	elif error == -4:
		message = 'The equation is empty !!\n'
	elif error == -5:
		message = "The '=' symbol is missing !!\n"
	elif error == -6:
		message = 'Pairing of parenthesis is wrong !!\n'
	elif error == -7:
		message = 'Syntax error, left-side of the equation is empty !!\n'
	elif error == -8:
		message = 'Syntax error, right-side of the equation is empty !!\n'
	elif error == -9:
		message = "Syntax error, the '=' should appear only once !!\n"
	elif error == -10:
		message = 'Syntax error, missing values !!\n'
	elif error == -11:
		message = 'Syntax error, operator at the start/end of expression !!\n'
	elif error == -12:
		message = "Syntax error, you have a '0' char that is not needed !!\n"
	elif error == -13:
		message = "Syntax error, wrong usage of '.' char !!\n"
	elif error == -14:
		message = "Syntax error, you can't put an operator after another (except for '+' followed by '-') !!\n"
	elif error == -15:
		message = "Syntax error, wrong usage around a 'X' char !!\n"
	elif error == -16:
		message = "Syntax error, wrong usage of '^' operator !!\n"
	elif error == -17:
		message = "Zero division detected !!\n"
	elif error == -18:
		message = "Syntax error, grade of a 'X' must be an integer equal or greather than 0 (no operation allowed) !!\n"
	elif error == -19:
		message = "Grades of 'X' must be integers !!\n"
	else:
		message = bcolors.WARNING + 'Are you sure to know how to call this function ? (Error code: ' + str(error) + ')'

	print bcolors.FAIL + 'ERROR - ' + message + bcolors.ENDC

	if printHelp:
		printUsage()
	sys.exit(2)


def printEquation(equation):
	output = ""
	for c in equation:
		if not output == "":
			output = output + " "
		output = output + str(c)
	output = output + " = 0"

	print bcolors.OKBLUE + 'Equation ==> ' + bcolors.ENDC + output

def humanizeArray(extract):
	output = ""
	for c in extract:
		if not output == "":
			output = output + " "
		output = output + str(c)

	return output


def ft_pow(base, power):
	i = 0
	ret = 1
	if power <= 0:
		return 1
	while i < power:
		ret *= base
		i += 1
	return ret


def parseArgv(argv):
	debug_option = 0
	equation = ""
	argc = len(argv)
	if argc == 1:
		exitWithError(-1)
	elif sys.argv[1] == "-h":
		printUsage()
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
					c = int(c) / float(ft_pow(10, decimalCount))
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


def syntaxCheck(extract):
	length = len(extract)
	if length == 0:
		exitWithError(-10)
	index = 0
	prevVal = None
	isGrade = False
	allSimbols = {'+', '-', '*', '/', '^'}
	while index < length:
		currentVal = str(extract[index])
		if currentVal in allSimbols:
			if prevVal == None and not currentVal == '-':
				exitWithError(-11)
			if currentVal == '^':
				if not prevVal == 'X':
					exitWithError(-16)
				isGrade = True
			elif prevVal == 'X' and (currentVal == '/' or currentVal == '*'):
				exitWithError(-15)
			elif prevVal and prevVal in allSimbols:
				exitWithError(-14)
			elif isGrade and (currentVal == '*' or currentVal == '/'):
				exitWithError(-18)
			elif currentVal == '+' or currentVal == '-':
				isGrade = False
		elif prevVal == 'X':
			exitWithError(-15)
		elif currentVal == 'X' and prevVal == '/':
			exitWithError(-15)
		elif not currentVal == 'X' and float(currentVal) == 0 and prevVal == '/':
			exitWithError(-17)
		elif not currentVal == 'X' and not currentVal == '.':
			if prevVal == '^' and not float(currentVal) % 1 == 0:
				print currentVal
				exitWithError(-19)
		prevVal = currentVal
		index += 1
	if currentVal in allSimbols:
		exitWithError(-11)

	return


def replaceMinus(extract):
	while '-' in extract:
		index = extract.index('-')
		nextVal = extract[index + 1]
		if nextVal == 'X':
			extract.insert(index + 1, str(-1.0))
		else:
			extract[index + 1] = str(float(nextVal) * -1.0)
		if index == 0 or extract[index - 1] == '+':
			del extract[index]
		else:
			extract[index] = '+'

	return extract

def addPolynom(coefficient, grade, data):
	if grade == None:
		grade = 0
	prevVal = 0
	if grade in data:
		prevVal = data[grade]
	data[int(grade)] = float(coefficient) + prevVal

	return data

def convertDataToExpression(data):
	extract = []
	first = True
	for grade, coefficient in data.viewitems():
		if not coefficient == 0:
			if not first:
				extract.append('+')
			else:
				first = False
			extract.append(str(coefficient))
			extract.append(str('X'))
			extract.append(str('^'))
			extract.append(str(grade))

	return extract

def resolveExtract(extract, debug_option):
	extract = replaceMinus(extract)
	if debug_option > 1:
		print bcolors.OKGREEN + "Minus replaced: " + bcolors.ENDC
		print "\t" + humanizeArray(extract)

	data = {}
	coefficient = None
	grade = None
	index = 0
	while index < len(extract):
		currentVal = extract[index]
		if currentVal == '*' or currentVal == '/':
			if index + 1 == len(extract):
				exitWithError(-11)
			if not extract[index + 1] == 'X':
				index += 1
				nextVal = float(extract[index])
				if currentVal == '*':
					coefficient = coefficient * nextVal
				else:
					if nextVal == 0:
						exitWithError(-17)
					coefficient = coefficient / nextVal
		elif currentVal == 'X':
			if coefficient == None:
				coefficient = 1;
			if index + 1 == len(extract):
				grade = 1
			elif extract[index + 1] == '^':
				if index + 2 == len(extract):
					exitWithError(-11)
				index += 2
				grade = float(extract[index])
			else:
				grade = 1
		elif currentVal == '+':
			if index + 1 == len(extract):
				exitWithError(-11)
			data = addPolynom(coefficient, grade, data)
		else :
			coefficient = float(currentVal)

		index += 1

	data = addPolynom(coefficient, grade, data)
	return data

def resolveParenthesis(equation, rawData, start, end):

	#print extract
	equation[start + 1 : end] = convertDataToExpression(rawData)

	printEquation(equation)
	return equation

def reduceEquation(equation, debug_option):
	# TODO take out every parenthesis
	reduced = False
	while '(' in equation:
		index = equation.index('(')
		while index < len(equation):
			if equation[index] == '(':
				start = index
			elif equation[index] == ')':
				end = index
				break
			index += 1
		if index == len(equation):
			exitWithError(-6)
		else:
			extract = equation[start + 1:end]

			if debug_option > 1:
				print bcolors.OKGREEN + "Parenthesis extracted: " + bcolors.ENDC
				print "\t" + humanizeArray(extract)

			syntaxCheck(extract)
			# Simplify parenthesis
			rawData = resolveExtract(extract, debug_option)
			if debug_option > 1:
				print bcolors.OKGREEN + "Extract simplified: " + bcolors.ENDC
				print "\t" + humanizeArray(convertDataToExpression(rawData))
			# TODO: take out parenthesis
			equation = resolveParenthesis(equation, rawData, start, end)
			# TODO: parenthesis checks
			if debug_option > 0:
				printEquation(equation)
			break
	if ')' in equation:
		exitWithError(-66)


def main(argv):
	equation, debug_option = parseArgv(argv)
	equation = equation.replace(" ", "")

	equation = lexicalCheck(equation)
	equation = bringRightToLeft(equation)
	if debug_option > 0:
		printEquation(equation)
	reduceEquation(equation, debug_option)


	print "\n\nSo far so good..!"

main(sys.argv)
