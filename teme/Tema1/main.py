
import math


class NodParcurgere:

    def __init__(self, info, x, y, greutate, parinte, insecte, cost=0, h=0 ):
        # info = (x, y, greutate)
        self.info = info
        self.x = x
        self.y = y
        self.g = greutate
        self.cost = cost
        self.parinte = parinte
        self.h = h
        self.insecte = insecte
        self.insecteMancate = insecte
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):
        l = self.obtineDrum()
        i = 2
        for nod in l:
            if nod.parinte is not None:
                print(i, ") Broscuta a sarit de la ", str(nod), " la ", str(nod.parinte) )
                print("Broscuta a mancat ", nod.parinte.insecteMancate, " insecte. Greutate broscuta: ", nod.parinte.greutate)

        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
            print("Nr noduri: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        return (self.info, "(", self.x, ",", self.y, ")")


class Graph:
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        continutFisier = f.read()
        infoFisier = continutFisier.split('\n')

        self.raza = int(infoFisier[0])
        self.g = int(infoFisier[1])
        self.infoStart = infoFisier[2]
        nod = infoFisier[3].split()
        self.start = (nod[0], int(nod[1]), int(nod[2]), int(nod[3]), int(nod[4]) )
        self.noduri = []
        mini = 99999999
        for i in range (4, len(infoFisier)):
            nod = infoFisier[i].split()
            self.noduri.append((nod[0], int(nod[1]), int(nod[2]), int(nod[3]), int(nod[4])))
            dist = int(nod[1])* int(nod[1]) + int(nod[2])*int(nod[2])
            if mini > math.sqrt(dist):
                mini = math.sqrt(dist)
                self.scopuri = nod[0]


    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir



gr = Graph("input.txt")

gr.__repr__();
