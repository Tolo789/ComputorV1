#!/usr/bin/python

from printFunctions import exitWithError, printMainStep, printMediumStep, printMiniStep, stringifyEquation

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
				if not currentVal == '-' or not prevVal == '+':
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
				exitWithError(-19)
		prevVal = currentVal
		index += 1
	if currentVal in allSimbols:
		exitWithError(-11)


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
			if float(coefficient) < 0:
				coefficient *= -1
				extract.append('-')
				first = False
			elif not first:
				extract.append('+')
			else:
				first = False
			if not float(coefficient) == 1:
				extract.append(str(coefficient))
			#extract.append(str('*'))
			if not float(grade) == 0:
				extract.append(str('X'))
				if not float(grade) == 1:
					extract.append(str('^'))
					extract.append(str(grade))

	return extract

def resolveExtract(extract, debug_option):
	extract = replaceMinus(extract)
	if debug_option > 1:
		printMiniStep("Minus replaced: ", extract)

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
			coefficient = None
			grade = None
		else :
			coefficient = float(currentVal)

		index += 1

	data = addPolynom(coefficient, grade, data)
	return data


def resolveParenthesis(equation, rawData, start, end, debug_option):
	minIndex = start
	maxIndex = end + 1
	notSupportedOperators = {'/', '^'}
	if not start == 0:
		multiplier = 1
		gradeIncrease = 0
		if equation[start - 1] == '+':
			minIndex -= 1
		elif equation[start - 1] == '-':
			minIndex -= 1
			multiplier = -1
		#TODO
		elif equation[start - 1] == '*':
			minIndex -= 2
			endChars = {'+', '-', '('}
			errorChars = {'/', 'X', '^', ')'}
			while not equation[minIndex] in endChars:
				if equation[minIndex] in errorChars:
					exitWithError(-20)
				if not equation[minIndex] == '*':
					multiplier = multiplier * float(equation[minIndex])
				minIndex -= 1
			if equation[minIndex] == '-':
				multiplier *= -1
		else:
			exitWithError(-20)

		rawData = {grade + gradeIncrease: coefficient * multiplier for grade, coefficient in rawData.items()}

	newExtract = convertDataToExpression(rawData)
	if not minIndex == 0:
		if equation[minIndex] == '(':
			minIndex += 1
		elif minIndex > 1 and not equation[minIndex - 1] == '(' and not newExtract[0] == '-':
			newExtract.insert(0, '+')
	if debug_option > 1:
		printMiniStep("Parenthesis solved: ", newExtract)
	equation[minIndex: maxIndex] = newExtract

	return equation


def reduceEquation(equation, debug_option):
	reduced = False
	while '(' in equation:
		if debug_option > 0:
			printMediumStep(equation)
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
				printMiniStep("Parenthesis extracted: ", extract)

			syntaxCheck(extract)
			rawData = resolveExtract(extract, debug_option)
			if debug_option > 1:
				printMiniStep("Extract simplified: ", convertDataToExpression(rawData))
			# TODO: take out parenthesis
			equation = resolveParenthesis(equation, rawData, start, end, debug_option)
	if ')' in equation:
		exitWithError(-6)

	printMainStep("Reduced form: ", stringifyEquation(equation))
	return equation
