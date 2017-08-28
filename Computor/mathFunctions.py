#!/usr/bin/python


def isInt(val):
	if val % 1 == 0:
		return True
	return False

def ftMCD(a,b):
    while b != 0:
        a, b = b, a % b
    return a


def simplifyFraction(upVal, downVal):
	mcd = ftMCD(upVal, downVal)
	if not mcd == 1:
		upVal /= mcd
		downVal /= mcd
	return upVal, downVal


def ftAbs(val):
	if val < 0:
		val *= -1
	return val


def ftPow(base, power):
	i = 0
	ret = 1
	if power <= 0:
		return 1
	while i < power:
		ret *= base
		i += 1
	return ret


def ftSquare(val):
	oldguess = 0
	guess = 1
	while ftAbs(guess - oldguess) > 0:
		oldguess = guess
		guess = (guess + val/guess) / 2.0

	return guess
