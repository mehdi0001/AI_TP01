from capteur import *
from Environement import *
from File import *
from math import sqrt
from Effecteur import *
import time

class aspirateur:
    def __init__ (self,Effecteur,environement,File):
        self.autonomie = 100
        self.score = 0
        self.Xasp = 3
        self.Yasp = 3
        self.energie = 100
        self.environement = environement
        self.File =File
        self.BDI = [] # liste du chemin a faire
        self.positionDirty = []
        self.positionBijoux = []
        self.ramasser = 0
        self.aspirer = 0

    def getPosition(self):
        position = []
        position = [self.Xasp,self.Yasp]
        return position

######## Partie non informe####################
    def nonInforme(self):
        self.File.file =[]
        tableau = self.environement.map   #tableau eq grid
        position = [self.Xasp,self.Yasp]
        # il faut remettre les parents des cases à leurs états initiaux ([-1,-1])
        for i in range(5):
            for j in range(5):
                self.environement.map[i][j][3] = [-1,-1]

        self.File.addFile(position)
        while (self.File.tailleFile()!= 0):
            x = self.File.file[0][0]
            y = self.File.file[0][1]
            if (tableau[x][y][1] == 1):
                return [x,y]
            if (tableau[x][y][2] == 1):
                return [x,y]
            if (x!=0 and tableau[x-1][y][3]==[-1,-1]):
                tableau[x-1][y][3] = [x,y]
                self.File.addFile([x-1,y])
            if (x!=4 and tableau[x+1][y][3]==[-1,-1]):
                tableau[x+1][y][3] = [x,y]
                self.File.addFile([x+1,y])
            if (y!=0 and tableau[x][y-1][3]==[-1,-1]):
                tableau[x][y-1][3] = [x,y]
                self.File.addFile([x,y-1])
            if (y!=4 and tableau[x][y+1][3]==[-1,-1]):
                tableau[x][y+1][3] = [x,y]
                self.File.addFile([x,y+1])
            self.File.removeFile([x,y])



    def moveNotInformed(self, captMap):
        self.BDI = []
        tableau = self.environement.map
        chemin = []
        position = [self.Xasp,self.Yasp]
        i=10
        while(captMap != position and i != 0):
            i -= 1
            chemin.append(captMap)
            captMap = tableau[captMap[0]][captMap[1]][3]
            #print(i, position, captMap)

        chemin.reverse()
        for j in chemin:
            self.BDI.append(j)
            #print(j)

    def nearestBDI(self,listCapteur):

        self.moveNotInformed(listCapteur[0])
        m = len(listCapteur)
        l = self.BDI
        n = len(l)
        for i in range(1,m):
            self.moveNotInformed(listCapteur[i])
            if(len(self.BDI)<n):
                l = self.BDI
                n = len(l)
        return l

    def executionNonInf(self,capteurMap,effecteur):
        tableau = self.environement.map
        self.nonInforme()
        self.environement.affichage()
        time.sleep(2)
        A = self.nearestBDI(capteurMap)

        for i in range(len(A)):

            L = self.getPosition()
            # print(L)
            effecteur.moveto(A[i][0],A[i][1],L)
            # print(L)
            L[0] = A[i][0]
            L[1] = A[i][1]
            #print(L)
            self.environement.affichage()
            time.sleep(2)
            # print(L)
        aspi = self.getPosition()
        if self.environement.map[aspi[0]][aspi[1]][1]== 1:
            effecteur.aspirer(aspi[0],aspi[1])
        else : effecteur.ramasser(aspi[0],aspi[1])
        print("\n\n\n\n")
        self.environement.affichage()
        time.sleep(2)
        print("nombre de bijoux ramasser",self.ramasser)
        print("nombre de pousierre aspirer",self.aspirer)
        print("Energie:",self.energie)

######## Partie informe####################

    def heuristique(self, position_finale):
        l = [[0 for i in range(5)] for j in range(5)]
        for i in range(5):
            for j in range(5):
                l[i][j] = sqrt((i-position_finale[0])**2 + (j-position_finale[1])**2)
        return l

    def informe(self, heuristique, position_finale):
        tableau = self.environement.map   #tableau eq grid
        noeud_list = []   # eq list_nodes
        position = [self.Xasp,self.Yasp]
        # il faut remettre les parents des cases à leurs états initiaux ([-1,-1])
        for i in range(5):
            for j in range(5):
                tableau[i][j][3]= [-1,-1]
        noeud = [position, heuristique[position[0]][position[1]], 0]
        noeud_list.append(noeud)
        while (noeud[0]!= position_finale):
            x = noeud[0][0]
            y = noeud[0][1]
            if (x!=0 and tableau[x-1][y][3]==[-1,-1]):
                tableau[x-1][y][3] = [x,y]
                noeud_list.append([[x-1, y], heuristique[x-1][y], noeud[2]+1])
            if (x!=4 and tableau[x+1][y][3]==[-1,-1]):
                tableau[x+1][y][3] = [x,y]
                noeud_list.append([[x+1, y], heuristique[x+1][y], noeud[2]+1])
            if (y!=0 and tableau[x][y-1][3]==[-1,-1]):
                tableau[x][y-1][3] = [x,y]
                noeud_list.append([[x, y-1], heuristique[x][y-1], noeud[2]+1])
            if (y!=4 and tableau[x][y+1][3]==[-1,-1]):
                tableau[x][y+1][3] = [x,y]
                noeud_list.append([[x, y+1], heuristique[x][y+1], noeud[2]+1])
            #print(noeud_list)
            if len(noeud_list)>1:
                noeud_list.remove(noeud)
                noeud = noeud_list[0]
                for node in noeud_list:
                    if (node[1] + node[2] < noeud[1] + noeud[2]):
                        noeud = node
            if len(noeud_list)==1:
                #print(noeud_list)
                break
        #print(tableau)


    def chemin(self, position_final):
        self.BDI = []
        tableau = self.environement.map
        chemin = []
        position = [self.Xasp,self.Yasp]
        i=10
        while(position_final != position and i != 0):
            i -= 1
            chemin.append(position_final)
            position_final = tableau[position_final[0]][position_final[1]][3]

        chemin.reverse()
        for j in chemin:
            self.BDI.append(j)
        return self.BDI


    def position_finale(self):
        tableau = self.environement.map
        pos_cible =[]
        distance = 50
        for i in range(5):
            for j in range(5):
                if (tableau[i][j][1]== 1 or tableau[i][j][2] ==1):
                    if ((self.Yasp-i)**2+(self.Xasp-j)**2<distance):
                        distance = (self.Yasp-i)**2+(self.Xasp-j)**2
                        pos_cible.append([i,j])
        return pos_cible[len(pos_cible)-1]

    def executionInf(self,effecteur):
        tableau = self.environement.map
        position_final = self.position_finale()
        heuristique = self.heuristique(position_final)
        self.informe(heuristique, position_final)
        self.environement.affichage()
        time.sleep(2)
        A = self.chemin(position_final)
        print(A)
        for i in range(len(A)):
            L = self.getPosition()
            # print(L)
            effecteur.moveto(A[i][0],A[i][1],L)
            # print(L)
            L[0] = A[i][0]
            L[1] = A[i][1]
            #print(L)
            self.environement.affichage()
            time.sleep(2)
        aspi = self.getPosition()
        if tableau[aspi[0]][aspi[1]][1]== 1:
            effecteur.aspirer(aspi[0],aspi[1])
        else : effecteur.ramasser(aspi[0],aspi[1])
        print("\n\n\n\n")
        self.environement.affichage()
        print("nombre de bijoux ramasser",self.ramasser)
        print("nombre de pousierre aspirer",self.aspirer)
        print("Energie:",self.energie)
























