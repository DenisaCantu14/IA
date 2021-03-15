
import math


class NodParcurgere:

    def __init__(self, info, x, y, greutateM, greutateC, parinte, insecte, cost=0, h=0 ):
        # info = (x, y, greutate)
        self.info = info
        self.x = x
        self.y = y
        self.gCurent = greutateC
        self.gMaxima = greutateM
        self.cost = cost
        self.parinte = parinte
        self.h = h
        self.insecte = insecte
        self.insecteMancate = insecte
        self.f = self.cost + self.h

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
                print(i, ") Broscuta a sarit de la ", str(nod.parinte), " la ", str(nod) )
                print("Broscuta a mancat ", nod.parinte.insecteMancate, " insecte. Greutate broscuta: ", nod.parinte.gCurent)

        if afisCost:
            print("Cost: ", self.cost)
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
        return (str(self.info) + "(" + str(self.x) + "," + str(self.y) + ")")


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
        self.scopuri = []
        mini = 99999999
        for i in range (4, len(infoFisier)):
            nod = infoFisier[i].split()
            self.noduri.append((nod[0], int(nod[1]), int(nod[2]), int(nod[3]), int(nod[4])))
            dist = int(nod[1])* int(nod[1]) + int(nod[2])*int(nod[2])
            if mini > math.sqrt(dist):
                mini = math.sqrt(dist)
                self.scopuri.append(nod[0])


    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir

    def genereazaSuccesori(self, nodCurent, tip_euristica):
        listaSuccesori = []
        for idx in range (len(self.noduri)):
            dist = math.sqrt((nodCurent.x - self.noduri[idx][1]) ** 2 + (nodCurent.y - self.noduri[idx][2]) ** 2)
            if nodCurent.gCurent / 3 < dist:
                continue
            else:
                nodNou = NodParcurgere(self.noduri[idx][0],  #info
                                       self.noduri[idx][1],  #x
                                       self.noduri[idx][2],  #y
                                       self.noduri[idx][4],  #g
                                       self.noduri[idx][3] + nodCurent.gCurent, #greuatte curenta
                                       nodCurent,
                                       0,
                                       nodCurent.cost + 1,
                                       self.euristica_banala(self.noduri[idx][0], tip_euristica))
                if not nodCurent.contineInDrum(nodNou):
                    listaSuccesori.append(nodNou)
        return listaSuccesori


    def euristica_banala(self, infoNod, tip_euristica):
        return 0 if infoNod in self.scopuri else 1


def a_star(gr, tip_euristica):
    c = [NodParcurgere(gr.start[0], gr.start[1], gr.start[2], gr.start[4], gr.start[4], None, gr.start[3], 0, gr.euristica_banala(gr.start[0], tip_euristica))]
    closed = []

    while len(c) > 0:
        nodCurent = c.pop(0)
        closed.append(nodCurent)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisLung=True, afisCost=True)
            print("\n--------------------\n")
            return

        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        lSuccesoriCopy = lSuccesori.copy()
        for s in lSuccesoriCopy:
            gasitOpen = False
            for elem in c:
                if s.info == elem.info:
                    gasitOpen = True
                    if s.f < elem.f:
                        c.remove(elem)
                    else:
                        lSuccesori.remove(s)
                    break
            if not gasitOpen:
                for elem in closed:
                    if s.info == elem.info:
                        if s.f < elem.f:
                            closed.remove(elem)
                        else:
                            lSuccesori.remove(s)
                        break

        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i, s)


gr = Graph("input.txt")
print("\n\n##################\nSolutie obtinuta cu A*:")
a_star(gr, "euristica_admisibila_2")

