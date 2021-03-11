import copy

# informatii despre un nod din arborele de parcurgere
class NodParcurgere:
    def __init__(self, info, cost, parinte):
        self.info = info
        self.parinte = parinte
        self.g = cost

    def obtineDrum(self):
        l = [self];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self):
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        print("Lungime: ", len(l) - 1, " pasi")
        print("Costul: ", self.g)
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
        return (sir)

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
        stiveSiruri = sir.strip().split("\n")
        listaStive = [sirStiva.strip().split(" ") if sirStiva != "#" else [] for sirStiva in stiveSiruri]
        return listaStive

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        stive_c = nodCurent.info
        for idx in range(len(stive_c)):
            if len(stive_c[idx]) == 0:
                continue
            copie_interm = copy.deepcopy(stive_c)
            bloc = copie_interm[idx].pop()
            cost = ord(bloc) - ord('a') + 1
            for j in range(len(stive_c)):
                if j == idx:
                    continue
                stive_nou = copy.deepcopy(copie_interm)
                stive_nou[j].append(bloc)
                if not nodCurent.contineInDrum(stive_nou):
                    nod_nou = NodParcurgere(stive_nou, nodCurent.g + cost, nodCurent)
                    listaSuccesori.append(nod_nou)

        return listaSuccesori



def uniform_cost(gr, nrSolutiiCautate=1):

    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, 0, None)]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: \n", end="")
            nodCurent.afisDrum()
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)



gr = Graph("input.txt")


uniform_cost(gr, nrSolutiiCautate=6)