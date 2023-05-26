account = []
f = open("src/Projet_Traiton/account.csv")
for lines in f.readlines():
    data = {}
    data["player"] = lines.split("	")[0]
    data["account"] = lines.split("	")[1].replace("\n","")
    account.append(data)
print(account)