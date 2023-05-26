from _class.Game import *
from _class.Kills import *

#Lib pour la création d'heatmap
import numpy as np
import time,os
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image

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

def extract_position(game,):
    position_x = []
    position_y = []
    for i in range(0,len(game.kills)):
        x,y = game.kills[i].getPosition()
        position_x.append(x)
        position_y.append(y)


def create_heatmap(game:Game,output:str="heatmap",map_file:str="database/img/map.png",debug:bool=False):
    #Valeurs correspondantes au dimension de la map
    x_min = -120 
    x_max = 14870
    y_min = -120
    y_max = 14980

    #Nombre de colone pour les histogrames
    bins=1000 #normalement il est optimisé mais sinon il faut le toucher
    #Variable d'ecart type
    sigma=15
    #Variable de localisation de la heatmap
    location_heatmap = 'tmp/heatmap.png'

    if debug:
        print(f"[+] Init HeatMap creation with the param :\nx_min:{x_min} | x_max:{x_max}\ny_min:{y_min} | y_max:{y_max}\nsigma:{sigma} | bins:{bins}\nlocation_heatmap:{location_heatmap} | map_file:{map_file}")

    position_x = []
    position_y = []
    for i in range(0,len(game.kills)):
        x,y = game.kills[i].getPosition()
        position_x.append(x)
        position_y.append(y)

    if debug:
        print(f"[+] End attribution variable position\nposition_x:{position_x}\nposition_y:{position_y}")
        print("[+] Caculate the heatmap filter")

    #Calcul de la carte de chaleurs
    heatmap, xedges, yedges = np.histogram2d(position_x, position_y, bins=bins, range=[[x_min,x_max],[y_min,y_max]])
    heatmap = gaussian_filter(heatmap, sigma=sigma)
    
    if debug:
        print("[+] HeatMap Caculated")

    #Création de l'image de la heatmap sans modification
    if debug:
        print("[+] Heatmap filter image creation")
    img = heatmap.T

    fig, ax1 = plt.subplots()
    ax1.imshow(img, extent=[x_min,x_max,y_min,y_max], origin='lower', cmap=cm.jet,alpha=0.8)

    plt.axis('off')
    
    plt.savefig(location_heatmap, bbox_inches='tight', pad_inches=0,dpi=1000)

    if debug:
        print(f"[+] Image saved at : {location_heatmap}")
    
    #Petit moment pour que le fichier du filtre gaussien soit bien crée
    time.sleep(1)

    #Supprésion du fond
    if debug:
        print(f'[+] Background Suppression')
    
    #Ouverture du filtre gaussien enregistré plus tot
    im = Image.open(location_heatmap)
    
    if debug:
        print('[+] Conversion to RGBA')
    #Convertissement de l'image en tableau contentant le code RGB de l'image
    im = im.convert('RGBA')

    data = np.array(im)
    
    if debug:
        print("[+] Loop delete blue")
    # Boucle pour enlever les nuances de bleu
    for i in range (150,230):
        rgb = data[:,:,:3]
        color = [51, 51, i]
        white = [255,255,255,255]
        mask = np.all(rgb == color, axis = -1)
        # On change les pixels correspondants en blanc
        data[mask] = white
    
    if debug:
        print("[+] Loop end\n[+] New Image Creation")

    #Création de la nouvelle image
    img = Image.fromarray(data)
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    if debug:
        print('[+] Creation finished')
        img.save("tmp/heatmap_transparent.png", "PNG")
        print('[+] Saving the heatmap with transparent background')

    #Ouverture de l'image de fond
    if debug:
        print('[+] Oppening the background map')    
    base_image = Image.open(map_file)
    #Récupération des dimmensions de l'image
    width, height = base_image.size

    # Attribution de l'image de mask
    mask_image = img
    # Resize the mask image to 512x512
    mask_image = mask_image.resize((width, height))

    # Ajout de l'image du mask au dessus de l'image de la map
    base_image.paste(mask_image, (0,0), mask = mask_image)
    if debug:
        print("[+] Saving the output file")
    if debug == False:
        os.remove("heatmap.png")
    base_image.save(str(output)+'.png')
