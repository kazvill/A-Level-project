def checkNum(x):
    numbers = str([0,1,2,3,4,5,6,7,8,9])
    isNum = None
    if x in numbers:
        print(x + " is a number")
        isNum = True
    else:
        print(x + " is not a number")
        isNum = False
    return isNum


def isEmpty(x):
	if len(x) == 0:
		empty = True
	else:
		empty = False
	return empty
	

def findA(u,v,t):
    a = round(((v-u)/t),1)
    return a


def findS(a,b,h,fromR):
    if fromR == False:
        s = round(((1/2)*(a+b)*(h)),1)
    else:
        s = round(((1/2)*(a+b)*(h)),1)
    return s