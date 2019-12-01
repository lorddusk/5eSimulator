def calcPercentage(x, y):
    if not x and not y:
       return None
    elif x < 0 or y < 0:
       return None
    else:
       return 100 * float(x)/float(y)