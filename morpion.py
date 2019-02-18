#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

import threading
import time
import random


##############################################################################
# Mise en place de la grille du jeu
imax = 3
jmax = 3
grille=[]
for i in range(0,imax):
    grille.append([])
    for j in range(0,jmax):
        grille[i].append(' ')

###############################################################################
def initcoef():
    """créer un tableau  de coefficients: 1.0 pour les cases vides, 0.0 sinon"""
    global grille,imax,jmax
    coef=[]
    for i in range(0,imax):
        coef.append([])
        for j in range(0,jmax):
            if grille[i][j]==' ':
                coef[i].append(1.0)
            else:
                coef[i].append(0.0)
    return coef

###############################################################################
def pondcoef(coef):
    """pondère les cases vides en fonction de leurs positions"""
    coef[1][1]*=3.0
    coef[0][0]*=2.0
    coef[2][2]*=2.0
    coef[0][2]*=2.0
    coef[2][0]*=2.0
    return coef

###############################################################################
def coupscoef(coef):
    global grille, imax, jmax

    # obtenir la liste des coups possibles par ordre décroissant des coef
    L=[]
    for i in range(0,imax):
        for j in range(0,jmax):
            if coef[i][j]>0:
                L.append([coef[i][j], i, j])
    L.sort()
    L.reverse()

    # si plusieurs cases avec coef le + fort, sélectionner le 1er au hasard
    if len(L)!=0:
        c=L[0][0]
        im=0
        for i in range(1,len(L)):
            if L[i][0]!=c:
                im=i-1
                break
        k=random.randint(0,im)
        x=L.pop(k)
        L.insert(0,x)

    # renvoyer une liste ordonnee (coef décroissants) sans les coef
    R=[]
    for i,j,k in L:
        R.append([j,k])
    return R

###############################################################################
def coupsgagnants(pion):
    global grille
    L=[]
    p1=pion + pion + " "
    p2=pion + " " + pion
    p3=" " + pion + pion
    # 1ère ligne
    x = "".join(grille[0])
    if x==p1: L.append([0,2])
    if x==p2: L.append([0,1])
    if x==p3: L.append([0,0])

    # 2ème ligne
    x = "".join(grille[1])
    if x==p1: L.append([1,2])
    if x==p2: L.append([1,1])
    if x==p3: L.append([1,0])

    # 3ère ligne
    x = "".join(grille[2])
    if x==p1: L.append([2,2])
    if x==p2: L.append([2,1])
    if x==p3: L.append([2,0])

    z=list(zip(grille[0],grille[1],grille[2]))
    # 1ère colonne
    x = "".join(z[0])
    if x==p1: L.append([2,0])
    if x==p2: L.append([1,0])
    if x==p3: L.append([0,0])

    # 2ème colonne
    x = "".join(z[1])
    if x==p1: L.append([2,1])
    if x==p2: L.append([1,1])
    if x==p3: L.append([0,1])

    # 3ème colonne
    x = "".join(z[2])
    if x==p1: L.append([2,2])
    if x==p2: L.append([1,2])
    if x==p3: L.append([0,2])

     # 1ère diagonale
    x = grille[0][0] + grille[1][1] + grille[2][2]
    if x==p1: L.append([2,2])
    if x==p2: L.append([1,1])
    if x==p3: L.append([0,0])

     # 2ème diagonale
    x = grille[0][2] + grille[1][1] + grille[2][0]
    if x==p1: L.append([2,0])
    if x==p2: L.append([1,1])
    if x==p3: L.append([0,2])

    return L

###############################################################################
def correction(LC,pionautre):
    """parmi les coups de la liste LC, mettre en avant un coup plus efficace s'il y en a un"""
    if len(LC)<=1:
        return LC
    kc=0
    for k in range(0,len(LC)):
        ic=LC[k][0]
        jc=LC[k][1]

        # vérif ligne ic
        ch=grille[ic][0] + grille[ic][1] + grille[ic][2]
        if ch.find(pionautre)<0:
            # => la ligne ic n'a pas le pion de l'adversaire
            kc=k
            break

        # vérif colonne jc
        ch=grille[0][jc] + grille[1][jc] + grille[2][jc]
        if ch.find(pionautre)<0:
            # => la colonne jc n'a pas le pion de l'adversaire
            kc=k
            break

        # vérif 1ère diagonale si la case ic,jc en fait partie
        if ic==jc:
            ch=grille[0][0] + grille[1][1] + grille[2][2]
            if ch.find(pionautre)<0:
                # => la 1ère diagonale n'a pas le pion de l'adversaire
                kc=k
                break

        # vérif 2ème diagonale si la case ic,jc en fait partie
        if ic==(2-jc):
            ch=grille[0][2] + grille[1][1] + grille[2][0]
            if ch.find(pionautre)<0:
                # => la 2ème diagonale n'a pas le pion de l'adversaire
                kc=k
                break

    if kc>0:
        # on a trouvé un meilleur coup que le 1er: le mettre en 1ère position
        L=LC.pop(kc)
        LC.insert(0,L)

    return LC

###############################################################################
def ajouer(pion):
    global aide  # dit si l'affichage de l'aide à chaque coup est demandé

    # recherche de qui est en train de jouer
    if pion=='X':
        pionautre='O'
    else:
        pionautre='X'

    # recherche des positions gagnantes s'il y en a
    LG = coupsgagnants(pion)
    if aide:
        print(u"coups gagnants: ", LG)

    # recherche des positions perdantes (=gagnantes pour l'autre!) s'il y en a
    LP = coupsgagnants(pionautre)
    if aide:
        print(u"coups perdants: ", LP)

    # recherche des positions recommandees avec les coefficients
    # initialise le tableau des coefficients
    c=initcoef()
    # ajoute les pondérations des cases
    c=pondcoef(c)
    # sélectionne tous les coups possibles dans l'ordre décroissant des coefficients
    LC=coupscoef(c)
    if aide:
        print(u"coups recommandés avant correction: ", LC)

    # met au début de cette liste, si possible, un coup efficace
    LC=correction(LC,pionautre)
    if aide:
        print(u"coups recommandées: ", LC)

    # restituer le meilleur coup
    if len(LG)!=0:
        return LG[0]

    if len(LP)!=0:
        return LP[0]

    return LC[0]

###############################################################################
def grillepleine():
    global grille,imax,jmax
    for i in range(0,imax):
        for j in range(0,jmax):
            if grille[i][j]==' ':
                return False
    return True

###############################################################################
def jeugagne():

    def _jeugagne(pion):
        global grille
        x = pion + pion + pion
        if \
        "".join(grille[0])==x or \
        "".join(grille[1])==x or \
        "".join(grille[2])==x or \
        grille[0][0]+grille[1][0]+grille[2][0]==x or \
        grille[0][1]+grille[1][1]+grille[2][1]==x or \
        grille[0][2]+grille[1][2]+grille[2][2]==x or \
        grille[0][0]+grille[1][1]+grille[2][2]==x or \
        grille[0][2]+grille[1][1]+grille[2][0]==x:
            return True
        else:
            return False

    if _jeugagne('X'):
        return 'X'
    if _jeugagne('O'):
        return 'O'
    return ''

###############################################################################
class Joueur(threading.Thread):

    def __init__(self, nom, num, pion, typejoueur):
        threading.Thread.__init__(self)
        self.setName(nom)  # nom du joueur. Ex: "joueur1", "joueur2", ...
        self.num = num  # numéro du joueur. Ex: 0 pour joueur1, 1 pour joueur2, etc...
        self.pion = pion  # forme de pion affecté
        self.typejoueur = typejoueur  # type de joueur: 0 = ordinateur, 1 = humain
        self.stop = False  # drapeau pour stopper le thread à la demande du programme principal

    def run(self):
        # accès aux variables globales
        global verrou # verrou d'accès aux variables globales
        global okjoue  # drapeau donnée par le programme principal qui permet au joueur de jouer
        global cdcoups  # compteur de coups
        global premier  # désigne le numéro du joueur qui a joué en premier
        global nbjoueurs  # nombre de joueurs du jeu
        global aide  # dit si l'affichage d'une aide est demandé

        while not self.stop:  # tant que le jeu n'est pas terminé

            ##### => chaque joueur attend son tour pour jouer
            while True:
                # on prend le verrou d'accès aux variables globales
                verrou.acquire()
                if self.stop:
                    # jeu terminé. on sort de la boucle, mais en conservant le blocage du verrou
                    break
                if okjoue and (cdcoups+premier)%nbjoueurs==self.num:
                    # = ça y est, on peut jouer, mais on conserve le verrou jusqu'à la fin du coup
                    break
                # on libère le verrou pour que les autres joueurs accédent aussi aux variables globales
                verrou.release()

            ##### => le joueur en cours joue

            if not self.stop:
                if self.typejoueur==0:
                    # c'est un joueur "ordinateur" qui joue
                    if self.pion=='X':
                        pionautre='O'
                    else:
                        pionautre='X'
                    print()
                    print(self.getName() + " joue ('" + self.pion + "' contre '" + pionautre + "')")
                    self.chx = ajouer(self.pion)
                    print(self.getName() + " joue case: ",self.chx)
                    grille[self.chx[0]][self.chx[1]]=self.pion
                    time.sleep(0.1)
                else:
                    # c'est un joueur "humain" qui joue
                    if self.pion=='X':
                        pionautre='O'
                    else:
                        pionautre='X'
                    print()
                    print(self.getName() + " joue ('" + self.pion + "' contre '" + pionautre + "')")
                    self.chx = ajouer(self.pion)
                    ch=self.getName() + " joue case: "
                    if aide:
                        ch = self.getName() + " joue case " + str(self.chx) + ": "
                    else:
                        ch = self.getName() + " joue case (ligne,colonne):"
                    while True:
                        self.coup = input(ch)
                        if aide and self.coup=="":
                            # ici, le jour a choisi le coup proposé
                            grille[self.chx[0]][self.chx[1]]=self.pion
                            break
                        try:
                            # ici, le joueur a entré un choix ligne,colonne
                            x = eval(self.coup)
                            if ((type(x)==list or type(x)==tuple) and len(x)==2) \
                                    and (x[0] in [0,1,2]) and (x[1] in [0,1,2]) \
                                        and grille[x[0]][x[1]]==' ':
                                grille[x[0]][x[1]]=self.pion
                                break
                        except:
                            # ici, le choix entré n'est pas correct
                            pass

            ##### => fin du coup du joueur en cours

            # le joueur repasse la main au programme principal après chaque coup
            okjoue = False

            # on libère le verrou d'accès aux variables globales
            verrou.release()

            # et fin du thread si c'est demandé (sinon, attente du prochain coup)
            if self.stop:
                break

    def stopper(self):
        self.stop = True

###############################################################################

print("Bonjour! En route pour le jeu de morpion!")

############################## => initialisation du jeu et des conditions de son démarrage

# nombre de joueurs
nbjoueurs = 2

# type de joueurs: 0=ordinateur, 1=humain; on doit avoir: len(typejoueurs)==nbjoueurs
while True:
    print()
    print(u"Type de joueurs:")
    print(u"[1]: 2 joueurs humains jouent ensemble")
    print(u"[2]: l'ordinateur contre 1 joueur humain")
    print(u"[3]: l'ordinateur joue contre lui-même")
    x = input("Quel choix voulez-vous? [2 par defaut]: ")
    if x=='1':
        typejoueurs=[1,1]
        break
    if x=='2' or x=='':
        typejoueurs=[0,1]
        break
    if x=='3':
        typejoueurs=[0,0]
        break

# savoir si une aide est demandée:
while True:
    print
    x = input(u"L'affichage d'une aide est-il demandé? O/N [O par défaut]: ")
    if x=='O' or x=='o' or x=='':
        aide=True
        break
    elif x=='N' or x=='n':
        aide=False
        break
    else:
        pass

# type de pion affecté à chaque joueur.
pions = ['O','X']  #
print()
print(u"=====> le joueur1 a le pion 'O', et l'autre le pion 'X'")

# définir celui qui commence, ou définir au hasard
while True:
    print()
    print(u"Définir qui va commencer")
    print(u"[1] le joueur 1 commence")
    print(u"[2] le joueur 2 commence")
    print(u"[3] le joueur qui commence est défini au hasard")
    x = input(u"Quel choix voulez-vous? [3 par defaut]: ")
    if x=='1':
        premier = 0
        break
    elif x=='2':
        premier = 1
        break
    elif x=='3' or x=='':
        premier = random.randint(0,nbjoueurs-1)
        break

print()
print("=====> c'est joueur"+str(premier+1)+" qui commence")

############################## => initialisation du programme

# création du verrou qui permettra le monopole d'accès aux variables globales (lecture-écriture)
verrou = threading.Lock()

# création du "compteur de coups" initialisé à -1 parce que c'est le programme principal qui commence
cdcoups = -1

# drapeau initialisé à True pour que le programme principal reprenne la main après chaque coup
#   (initialisé à -1 parce que c'est le programme principal qui commence)
okjoue = False

# creation de la liste des joueurs (NB: le joueur numéro 0 est appelé "joueur1")
joueurs = []
for i in range(0,nbjoueurs):
    j = Joueur("joueur%d" % (i+1), i, pions[i], typejoueurs[i])
    j.setDaemon(True)
    joueurs.append(j)

# lancement de tous les threads des joueurs
for i in range(0,nbjoueurs):
    joueurs[i].start()

##############################
# surveillance du jeu et attente condition de fin de partie

tps=time.time()
while True:
    # attente qu'un joueur ait joué
    while True:
        verrou.acquire()
        if not okjoue:
            cdcoups+=1 #  on incrémente le compteur de coups du coup qui vient d'être joué
            # on sort de la boucle, mais le verrou reste bloqué pendant la surveillance
            break
        verrou.release()

    # affichage de la grille après le dernier coup
    print
    for i in range(0,imax):
        print(grille[i])


    # voir si un gagnant
    x = jeugagne()
    if x!="":
        if x==pions[0]:
            gagnant = "joueur1 ('" + pions[0] + "')"
        else:
            gagnant = "joueur2 ('" + pions[1] + "')"
        print()
        print("le gagnant est: " + gagnant)
        verrou.release()
        break

    # condition de fin de jeu
    if grillepleine():
        print()
        print("pas de gagnant!")
        verrou.release()
        break

    # détection du départ d'un nouveau tour numéro ((cdcoups//nbjoueurs)+1) par (cdcoups%nbjoueurs==0)
    ch=""
    if cdcoups%nbjoueurs==0:
        print()
        print(u"=====> début du tour " + str((cdcoups//nbjoueurs)+1))

    # permet au joueur suivant de jouer
    okjoue = True
    verrou.release()
    # et on boucle pour attendre jusqu'à ce que le joueur suivant ait joué

#############################
# fin du jeu
print()
print("fin du jeu")

# arrêt de tous les threads
for i in range(0,nbjoueurs):
    joueurs[i].stopper()

# attente jusqu'à ce que tous les threads soient terminés
for i in range(0,nbjoueurs):
    joueurs[i].join()
    verrou.acquire()
    print("fin du thread " + joueurs[i].getName())
    verrou.release()

print()
print(u"A bientôt pour un prochain jeu!")
