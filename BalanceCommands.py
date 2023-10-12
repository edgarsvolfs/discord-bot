import json


def addUserToDict(member):
    with open('UserBalance.txt') as f:
        data = f.read()
    js = json.loads(data)
    js[str(member)] = 0
    f.close()
    with open('UserBalance.txt', 'w') as file:
        file.write(
            json.dumps(js))  # json dumps - replaces single quotes with double quotes
        file.close()
    return


def checkDict(member):
    with open(r'UserBalance.txt', 'r+') as file:
        data = file.read()
        res = data.find(str(member))
        file.close()
        return res


def getUserBalance(member):
    with open('UserBalance.txt') as f:
        data = f.read()
        js = json.loads(data)  # nolasa informaciju to parversot dictionarya
        balance = js[str(member)]
    return balance


def updateUserBalance(member, balanceChange):
    with open('UserBalance.txt') as f:
        data = f.read()
    js = json.loads(data)  # nolasa informaciju to parversot dictionarya
    with open('UserBalance.txt', 'r') as file:
        data = file.read()
        stringToReplace = f'"{member}": {str(js[str(member)])}'
        newBalance = int(js[str(member)]) + balanceChange
        updatedString = f'"{member}": {str(newBalance)}'
        # data = data.replace(str(js[str(member)]),
        #                     str(int(js[str(member)]) + balanceChange))  # js[member] - user vecais balance
        data = data.replace(stringToReplace,
                            updatedString)  # js[member] - user vecais balance
    with open('UserBalance.txt', 'w') as file:
        file.write(str(data))


def checkUserInDictionary(user):
    if checkDict(user) == -1:
        addUserToDict(user)  # ads the message author on the user balance.txt filed
