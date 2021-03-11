"""
TEMA OPTIONALA PANA LA URMATORUL LABORATOR (PT. BONUS)
------------------------------------------------------

Presupunem ca avem costul de mutare al unui bloc egal cu indicele in alfabet, cu indicii incepand de la 1 (care se calculează prin 1+ diferenta dintre valoarea codului ascii al literei blocului de mutat si codul ascii al literei "a" ) .

Folosind algoritmul A* pentru determinarea solutiei minime (varianta cu listele OPEN si CLOSED) determinati cea mai buna solutie pentru problema blocurilor.

Implementati alte 2 euristici pe langa euristica banala.

Rulati codul pe exemple mai mari pentru a putea compara eficienta euristicilor.
"""
import copy

# informatii despre un nod din arborele de parcurgere (nu din graful initial)
import sys


class NodParcurgere:
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

    def afisDrum(
            self, afisCost=True, afisLung=False
    ):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
            print('Euristica:', nod.h)
        if afisCost:
            print("Cost: ", self.g)
        if afisCost:
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
        sir += str(self.info)
        return sir

    # euristica banală: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        sir = ""
        maxInalt = max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva) < inalt:
                    sir += "  "
                else:
                    sir += stiva[inalt - 1] + " "
            sir += "\n"
        sir += "-" * (2 * len(self.info) - 1)
        return sir


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        continut_fisier = f.read()

        siruriStari = continut_fisier.split("stari_finale")
        self.start = self.obtineStive(siruriStari[0])

        self.scopuri = []
        siruriStariFinale = siruriStari[1].strip().split("---")
        for scop in siruriStariFinale:
            self.scopuri.append(self.obtineStive(scop))

        print("Stare initiala: ", self.start)
        print("Stari finale: ", self.scopuri)
        input()

    def obtineStive(self, sir):
        """
        a x y z
        c b
        d
        ["a x y z","c b","d"]
        [["a","x","y","z"],["c","b"],["d"]]
        """
        stiveSiruri = sir.strip().split("\n")
        listaStive = [
            sirStiva.strip().split(" ") if sirStiva != "#" else []
            for sirStiva in stiveSiruri
        ]
        return listaStive

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    # va genera succesorii sub forma de noduri in arborele de parcurgere

    def genereazaSuccesori(self, nodCurent, tip_euristica):
        listaSuccesori = []
        stive_c = nodCurent.info  # stivele din nodul curent
        nr_stive = len(stive_c)
        for idx in range(nr_stive):
            if len(stive_c[idx]) == 0:
                continue
            copie_interm = copy.deepcopy(stive_c)
            bloc = copie_interm[idx].pop(-1)
            for j in range(nr_stive):
                if idx == j:
                    continue
                stive_n = copy.deepcopy(copie_interm)  # lista noua de stive
                stive_n[j].append(bloc)
                costMutareBloc = 1 + ord(bloc) - ord("a")
                nod_nou = NodParcurgere(
                    stive_n,
                    nodCurent,
                    cost=nodCurent.g + costMutareBloc,
                    h=self.calculeaza_h(stive_n, tip_euristica),
                )
                if not nodCurent.contineInDrum(stive_n):
                    listaSuccesori.append(nod_nou)

        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica):
        if tip_euristica == "euristica_banala":
            return self.euristica_banala(infoNod, tip_euristica)
        elif tip_euristica == "euristica_admisibila_1":
            return self.euristica_admisibila_1(infoNod, tip_euristica)
        elif tip_euristica == "euristica_admisibila_2":
            return self.euristica_admisibila_2(infoNod, tip_euristica)
        else:
            raise Exception("Aceasta euristica nu este definita")

    def euristica_banala(self, infoNod, tip_euristica):
        return 0 if infoNod in self.scopuri else 1

    def euristica_admisibila_1(self, infoNod, tip_euristica):
        """Comparam configuratia infoNod cu fiecare dintre starile finale,
        numarand cate blocuri din starea curenta nu se afla la locul lor din
        starea finala. Astfel numarul de blocuri care vor trebui mutate cel putin
        o data reprezinta estimarea costului de a ajunge in acea stare finala.

        Dintre toate estimarile calculate pentru fiecare stare finala, alegem
        drept euristica estimarea minima.
        """
        nrf = sys.maxsize
        for nodScop in self.scopuri:
            nr = 0
            # print(infoNod, nodScop)
            # print('-----')
            for stivaI, stivaF in zip(infoNod, nodScop):
                for nodI, nodF in zip(stivaI, stivaF):
                    if nodI != nodF:
                        nr += 1
                if len(stivaI) > len(stivaF):
                    #adaug restul nodurilor care nu se afla la locul lor
                    nr += len(stivaI) - len(stivaF)

            nrf = min(nrf, nr)

        # print('nr final')
        # print(nrf)
        return nrf

    def euristica_admisibila_2(self, infoNod, tip_euristica):
        """Asemanator cu 1. De aceasta data pentru fiecare bloc care nu se
        afla la locul lui, in loc sa adunam 1 la estimare, vom aduna costul
        de a muta blocul respectiv (stim ca blocul acela trebuie mutat cel putin
        o data, deci pentru a ajunge la starea finala vom face la un moment dat
        un pas de costul respectiv).
        """
        nrf = sys.maxsize
        for nodScop in self.scopuri:
            nr = 0
            # print(infoNod, nodScop)
            # print('-----')
            for stivaI, stivaF in zip(infoNod, nodScop):
                for nodI, nodF in zip(stivaI, stivaF):
                    if nodI != nodF:
                        nr += ord(nodI) - ord('a') + 1
                if len(stivaI) > len(stivaF):
                    # adaug costul pt restul nodurilor care nu se afla la locul lor
                    for i in range(len(stivaF), len(stivaI)):
                        nr += ord(stivaI[i]) - ord('a') + 1

            nrf = min(nrf, nr)


        # print('nr final')
        # print(nrf)
        return nrf

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def a_star(gr, tip_euristica):
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, "euristica_admisibila_2"))]
    closed = []

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()

        nodCurent = c.pop(0)
        closed.append(nodCurent)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="\n")
            nodCurent.afisDrum()
            print("\n--------------------\n")
            return

        lSuccesori = gr.genereazaSuccesori(nodCurent, "euristica_admisibila_2")
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
    pass


gr = Graph("input.txt")
print("\n\n##################\nSolutie obtinuta cu A*:")
a_star(gr, "euristica_admisibila_2")
