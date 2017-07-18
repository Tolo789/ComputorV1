#!/usr/bin/python

import sys, getopt

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
	print 'USAGE:\n $> python computor.py [options] "polinomial equation"\n'
	print "OPTIONS: (you need to include the '-')"
	print ' -h\tdisplay help and exit'
	print ' -p\tprints every step of the resolver'
	sys.exit(2)

def printError(error):
	if error == -1:
		message = 'No polinomial equation given !!\n'
	elif error == -2:
		message = 'Wrong parameters given !!\n'
	elif error == -3:
		message = 'Lexical error in the equation !!\n'
	elif error == -4:
		message = 'The equation is empty !!\n'
	elif error == -5:
		message = "The '=' symbol is missing !!\n"
	elif error == -6:
		message = 'Error with the pairing of parenthesis !!\n'
	else:
		message = 'Are you sure you know how to call this function ?'

	print bcolors.FAIL + 'ERROR - ' + message + bcolors.ENDC

	printUsage()

def printEquation(equation):
	output = ""
	for c in equation:
		if not output == "":
			output = output + " "
		output = output + str(c)
	output = output + " = 0"

	print 'Equation ==> ' + output


def parseOption(argv):
	debug_option = False
	equation = ""
	argc = len(argv)
	if argc == 1:
		printError(-1)
	elif sys.argv[1] == "-h":
		printUsage()
	elif sys.argv[1] == "-p":
	 	if argc == 2:
			printError(-1)
		elif argc > 3:
			printError(-2)
		debug_option = True
		equation = sys.argv[2]
	elif argc == 2:
		equation = sys.argv[1]
	else:
		printError(-2)

	return equation, debug_option

def lexicalCheck(equation):
	split_equation = []
	ok_chars = {'+', '-', '*', '/', 'X', '^', '(', ')', '='}
	tmp_number = 0
	is_tmp_number = False
	for c in equation:
		if not c in ok_chars:
			if not c.isdigit():
				printError(-3)
			else:
				if is_tmp_number:
					tmp_number = tmp_number * 10 + int(c)
				else:
					tmp_number = int(c)
					is_tmp_number = True
		else:
			if is_tmp_number:
				split_equation.append(str(tmp_number))
				is_tmp_number = False
			split_equation.append(c)

	if is_tmp_number:
		split_equation.append(tmp_number)

	if len(split_equation) == 0:
		printError(-4)
	elif not '=' in split_equation:
		printError(-5)


	return split_equation

def bringRightToLeft(equation):
	splitIndex = equation.index('=')
	leftSide = equation[:splitIndex]
	leftSide.insert(0, '(')
	rightSide = equation[splitIndex + 1:]
	rightSide.insert(0, '(')
	rightSide.insert(0, '-')
	rightSide.append(')')
	rightSide.append(')')

	leftSide.extend(rightSide)
	return leftSide


def reduceEquation(equation, debug_option):
	# TODO take out every parenthesis
	reduced = False
	while reduced == False:
		reduced = True
		start = 0
		end = 0

		if '(' in equation:
			index = 0
			while index < len(equation):
				if equation[index] == '(':
					start = index
				elif equation[index] == ')':
					end = index
					break
				index += 1
			if index == len(equation):
				printError(-6)
		elif ')' in equation:
			printError(-6)


def main(argv):
	equation, debug_option = parseOption(argv)
	equation = equation.replace(" ", "")

	equation = lexicalCheck(equation)
	equation = bringRightToLeft(equation)
	if debug_option:
		printEquation(equation)
	reduceEquation(equation, debug_option)


	print "\n\nSo far so good..!"

main(sys.argv)
