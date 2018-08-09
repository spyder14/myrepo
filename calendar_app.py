from exchangelib import Credentials, Account

credentials = Credentials('spyder14@ufl.edu', 'Li@m1026!')
account = Account('spyder14@ufl.edu', credentials=credentials, autodiscover=True)

for f in account.root.walk():
    if f.name == 'Where_is_Mike':
        my_folder = f
        break
else:
    raise Exception('Folder not found')

for item in my_folder.all().order_by('-datetime_received')[:5]: print(item.subject)