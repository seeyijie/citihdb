from datetime import datetime, date, time

def today():
    lastupdated = datetime.now()
    return(str(lastupdated.day) +'/' + str(lastupdated.month) + '/'+ str(lastupdated.year) + '\n' +str(lastupdated.time()))
