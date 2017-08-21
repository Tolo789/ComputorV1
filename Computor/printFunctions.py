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
	elif error == -20:
		message = "Syntax error around parenthesis !!\n"
	else:
		message = bcolors.WARNING + 'Are you sure to know how to call this function ? (Error code: ' + str(error) + ')'

	print bcolors.FAIL + 'ERROR - ' + message + bcolors.ENDC

	if printHelp:
		printUsage()
	sys.exit(2)


def stringifyEquation(equation):
	output = ""
	skipSpace = False
	for c in equation:
		if skipSpace:
			skipSpace = False
		elif str(c) == "^":
			skipSpace = True
		elif not output == "":
			output = output + " "
		output = output + str(c)
	output = output + " = 0"
	return output


def humanizeArray(extract):
	output = ""
	for c in extract:
		if not output == "":
			output = output + " "
		output = output + str(c)
	return output


def printMainStep(header, message):
	print bcolors.HEADER + header + bcolors.ENDC + message


def printMediumStep(equation):
	print bcolors.OKBLUE + 'Equation ==> ' + bcolors.ENDC + stringifyEquation(equation)


def printMiniStep(header, message):
	print bcolors.OKGREEN + header + bcolors.ENDC
	print "\t" + message
