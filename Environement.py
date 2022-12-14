import random
from tkinter import *
class environement:
    def __init__(self,dessin):
        self.map = [[[0,0,0,[-1,-1]] for i in range(5)] for i in range(5)]
        self.dessin=dessin

    def generate_Dirty(self,img):
        x = random.randint(0,4)
        y= random.randint(0,4)
        self.map[x][y][1] = 1
        dirty = self.dessin.create_image(20+100*y,20+100*x,anchor=NW,image=img)
        return dirty

    def delete_Dirty(self,x,y,img):
        self.map[x][y][1]=0
        self.dessin.delete(self.dessin.create_image(20+100*y,20+100*x,anchor=NW,image=img))

    def generate_Bijoux(self,img):
        x = random.randint(0,4)
        y= random.randint(0,4)
        self.map[x][y][2]=1
        bijoux = self.dessin.create_image(20+100*y,20+100*x,anchor=NW,image=img)
        return bijoux
    def delete_Bijoux(self,x,y,img):
        self.map[x][y][2] = 0
        self.dessin.delete(self.dessin.create_image(20+100*y,20+100*x,anchor=NW,image=img))
    def affichage(self):
        print(" ###############################")
        for L in self.map:
            print(" # ", end = '')
            for l in L :
                if l[0] == 0:
                    print(" ",end = '')
                else :
                    print("A", end = '')
                if l[1] == 0:
                    print(" ",end = '')
                else :
                    print("D",end = '')
                if l[2] == 0:
                    print(" ",end = '')
                else :
                    print("B",end = '')
                print(" # ", end = '')
            print("")
        print(" ###############################")



