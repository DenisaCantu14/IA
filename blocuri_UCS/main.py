"""
Implementati cautarea solutiilor folosind algoritmul UCS. Pentru aceasta trebuie sa adaugati in plus la clasa `NodParcurgere` un parametru pentru costul drumului de la radacina pana la nodul respectiv din arborele de parcurgere si sa actualizati implementarea din `genereazaSuccesori` corespunzator.

Asociem unei mutari urmatorul cost: indicele din alfabet al literei corespunzatoare blocului mutat. De exemplu: daca la un pas mutam blocul cu litera "b", costul acestei mutari va fi 2.

Folosind UCS determinati `nrSolutiiCautate` solutii cu cost minim.

Dati enter dupa fiecare solutie afisata.
"""
import copy


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, cost, parinte):
        self.info = info
        self.g = cost
        self.parinte = parinte  # parintele din arborele de parcurgere

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(
        self, afisLung=False, afisCost=False
    ):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisLung:
            print("Lungime: ", len(l) - 1, " pasi")
        if afisCost:
            print("Cost: ", self.g)
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
        sir = ""
        if self.parinte:
            print("Cost mutare: ", self.g - self.parinte.g)
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
        listaStive = [
            sirStiva.strip().split(" ") if sirStiva != "#" else []
            for sirStiva in stiveSiruri
        ]
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
            for j in range(len(stive_c)):
                if j == idx:
                    continue
                stive_nou = copy.deepcopy(copie_interm)
                stive_nou[j].append(bloc)
                costMutareBloc = 1 + ord(bloc) - ord("a")
                if not nodCurent.contineInDrum(stive_nou):
                    nod_nou = NodParcurgere(
                        stive_nou,
                        nodCurent.g + costMutareBloc,
                        nodCurent,
                    )
                    listaSuccesori.append(nod_nou)

        return listaSuccesori


def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, 0, None)]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisLung=True, afisCost=True)
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            while i < len(c):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g > s.g:
                    break
                i += 1
            c.insert(i, s)


gr = Graph("input.txt")

print("\n\n##################\nSolutii obtinute cu UCS:")
uniform_cost(gr, nrSolutiiCautate=4)
