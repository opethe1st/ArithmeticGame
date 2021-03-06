from __future__ import division
""" This is a game that tests skills with Arithmetic. The user is given an expression to evaluate
and given 10 seconds to answer.
"""
""" At this moment, I am violating the strict logic layer thing. Because I need to be able to test as I go.
I am going to provide generateExpression, evaluateExpression, Timeout and checkAnswer as public methods to the UI layer
"""

from random import randint
import time as t
import fractions

def generateNum(level):
    """ I am  noticing that I am having to use 10**level blah blah to generate a number often."""
    return randint(10*(level-1)+1,10*(level)-1)

def expression(level,nest,MaxNest):
    """numOrExpr = 1, indicates that a number is generated. if it is 0, an expression is generated. The nest is used
    limit the number of nests"""
    if nest<MaxNest: #Number of possible nestings of expressions
        numOrExpr = randint(0,1)
    else:
        numOrExpr = 1

    if numOrExpr:
        return str(generateNum(level))
    else:
        nest+=1
        return "".join(["(",generateExpression(level,nest,MaxNest),")"])

def generateExpression(level,nest,MaxNest):
    a = expression(level,nest,MaxNest)
    b = expression(level,nest,MaxNest)
    possibleOperators = ["*","-","+","/"] #I removed division, there are going to be problems with division by zero
    operator = possibleOperators[randint(0,len(possibleOperators)-1)]

    #randint, not pythonic, randint(0,3) includes 3. that's major crap
    return "%s %s %s"%(a,operator,b)
def evaluateExpression(st):
    #The thing to note though is that it uses integer division.And seems to follow BODMAS.
    #This is currently giving me problems. Sometimes I get zero division. Even no division is involved
    #Fixed. I have imported division from __future__ and I am using the fractions module.
    return str(eval(st))
def generateQuestion(level=1,MaxNest=1):
    """First draft. I think a better way to do this would make this easier to generalise would be to generate an
    expression string as the question and evaluate it and return the expression string and the answer. Make use of a
    generateExpression function and an evaluateExpression function"""
    while True:
        try:
            expr = generateExpression(level,0,MaxNest)
            result = fractions.Fraction(evaluateExpression(expr)).limit_denominator(1000)
            break
        except ZeroDivisionError:
            pass
    return expr,str(result)

def checkAnswer(CorrectAnswer,UserAnswer):
    """Checks if an answer is correct. Seems a little superfluous"""
    try:
        if fractions.Fraction(CorrectAnswer)==fractions.Fraction(UserAnswer):
            return True
        else:
            return False
    except:
        return False

def run(level,times):
    """Run the game a given number of times, at a certain level. The level indicates the number of digits of the numbers"""
    i = 0
    TotalTime = 0
    MaxNest = int(raw_input("How much nesting do you want in the expression?\n> "))
    while i<times:
        expr,result= generateQuestion(level,MaxNest)
        print "What is the %s"%expr
        start = t.time()
        #I want to use a better way of doing the timeout. I want it to stop requesting for input once it has timed out
        ans = raw_input('Answer Now!')
        elapsedTime = int(t.time()-start)
        if elapsedTime>10:
            TimeOut = True
        else:
            TimeOut = False
        if TimeOut:
            print "Time has run out. The answer is %s"%result
        elif ans==result and not TimeOut:
            print "That's correct! Your score is %d"%(10-elapsedTime)
            TotalTime+=(10-elapsedTime)
        if  ans!= result:
            print "That's wrong. The answer is %s"%result
        i+=1
    print "Nice Game. Your total score is %d"%TotalTime
#run(1,5)
