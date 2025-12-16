from dataclasses import dataclass

@dataclass
class Connessione:
    id: int
    id_rifugio1: int
    id_rifugio2: int
    distanza: float
    difficolta: str
    durata:str
    anno: int

    def __eq__(self, other):
        return isinstance(other, Connessione) and self.id == other.id

    def __str__(self):
        return f"{self.id}{self.id_rifugio1}{self.id_rifugio2}{self.distanza}{self.difficolta}"

    def __hash__(self):
        return hash(self.id)