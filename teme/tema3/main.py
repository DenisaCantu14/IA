"""TEMA OPTIONALA PANA LA URMATORUL LABORATOR (PT. BONUS)
------------------------------------------------------

Folosind algoritmul A* determinati 3 solutii pentru 8-puzzle.

Implementati o euristica nebanala admisibila.

Implementati verificarea daca jocul poate fi rezolvat.
"""

import math
import copy


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    gr = None  # trebuie setat sa contina instanta problemei

    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=True, afisLung=True):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisLung:
            print("Lungime: ", len(l))
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
        for linie in self.info:
            sir += " ".join(linie) + "\n"
        return sir

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += " ".join(linie) + "\n"
        return sir


def cautaPozElemMatr(matr, elemCautat):
    for i, linie in enumerate(matr):
        for j, elem in enumerate(linie):
            if elem == elemCautat:
                return i, j
    return -1


class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        f = open(nume_fisier, "r")
        textFisier = f.read()
        listaSiruriLinii = textFisier.strip().split("\n")  # ["1 2 3","4 5 6","7 0 8"]

        self.start = []
        for linie in listaSiruriLinii:
            self.start.append(linie.strip().split(" "))
        self.scopuri = [[["1", "2", "3"], ["4", "5", "6"], ["7", "8", "0"]]]
        print(self.start)

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    def verificaExistentaSolutie(self, infoNod):
        """Returneaza True sau False daca starea data de infoNod corespunde
        unui joc care poate fi rezolvat.

        1 2 3
        4 5 8
        0 6 7

        Ne formam permutarea celor 8 placute citite de sus in jos si de st la dr:
        1 2 3 4 5 8 6 7

        Existenta solutiei depinde de nr. de inversiuni ale permutarii.

        DE CE?
        """
        #transform in lista
        l = []
        for linie in infoNod:
            for elem in linie:
                l.append(elem)
        #calculez nr de inversiuni
        inv = 0
        for i in range(8):
            for j in range(i+1,9):
                if l[j] != 0 and l[i] > l[j]:
                   inv += 1
        #solutia finala are nr de inversiuni egal cu 0 si cum o mutare pe linie sau coloana nu schimba paritatea permutarii
        #paritatea starii initiale trebuie sa fie para, nu ai cum sa ajungi de la o permutare impara la una para
        if inv % 2 == 0:
            return True
        else:
            return False

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica nebanala"):
        listaSuccesori = []
        # lista de directii pentru sus, jos, stanga, dreapta
        directii = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        # caut gol
        linieGol, coloanaGol = cautaPozElemMatr(nodCurent.info, "0")
        for dl, dc in directii:
            linieVecin = linieGol + dl
            coloanaVecin = coloanaGol + dc
            try:
                if linieVecin < 0 or coloanaVecin < 0:
                    continue
                infoNodNou = copy.deepcopy(nodCurent.info)
                infoNodNou[linieGol][coloanaGol] = infoNodNou[linieVecin][coloanaVecin]
                infoNodNou[linieVecin][coloanaVecin] = "0"
                if not nodCurent.contineInDrum(infoNodNou):
                    listaSuccesori.append(
                        NodParcurgere(
                            infoNodNou,
                            nodCurent,
                            nodCurent.g + 1,
                            self.calculeaza_h(infoNodNou, tip_euristica),
                        )
                    )
            except IndexError:
                pass
        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if infoNod not in self.scopuri:
                return 1
            return 0
        else:
            count = 0
            for i, list in enumerate (infoNod):
                for j, elem in enumerate (list):
                    if elem != self.scopuri[0][i][j]:
                        if elem == '0':
                            pozI = 2
                            pozJ = 2
                        elif int(elem) % 3 == 0:
                            pozI = int(elem) // 3 -1
                            pozJ = 2
                        else:
                            pozI = int(elem) // 3
                            pozJ = int(elem) % 3 -1
                        count += abs(pozI - i) + abs(pozJ -j)
            return count


    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def a_star(gr, nrSolutiiCautate, tip_euristica):
    if not gr.verificaExistentaSolutie(gr.start):
        print("Nu avem solutii")
        return

    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="\n")
            nodCurent.afisDrum()
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            while i < len(c):
                if c[i].f >= s.f:
                    break
                i += 1
            c.insert(i, s)



gr = Graph("8puzzle.txt")
NodParcurgere.gr = gr

print("\n\n##################\nSolutii obtinute cu A*:")
nrSolutiiCautate = 3
a_star(gr, nrSolutiiCautate=nrSolutiiCautate, tip_euristica="euristica nebanala")
