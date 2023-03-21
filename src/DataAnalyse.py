

def AnalyseDraft(bans):
    resultat = {}
    compteur = 0
    for ban in bans:
        if len(ban) != 0:
            for i in range (0,len(ban)):
                if ban[i] in resultat:
                    resultat[ban[i]] = resultat[ban[i]]+1
                else:
                    resultat[ban[i]] = 1
            compteur = compteur +1

    for champ in resultat :
        resultat[champ] = format(resultat[champ]*100/compteur,'.1f')
    return resultat
