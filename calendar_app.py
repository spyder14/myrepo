from exchangelib import Credentials, Account
from exchangelib.folders import Calendar

credentials = Credentials('spyder14@ufl.edu', 'Li@m1026!')
account = Account('spyder14@ufl.edu', credentials=credentials, autodiscover=True)

for item in account.calendar.all().order_by('-datetime_received')[:5]:
    print(item.subject)

#for f in account.folders[Calendar]:
#    print f