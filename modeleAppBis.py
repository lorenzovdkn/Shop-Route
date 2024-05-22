from grid import Grille
from grid import Case
class Modele():
    def __init__(self) -> None:
        pass
   
    
if __name__ == '__main__':
    laby = Grille(8, 8)
    print('Grille de dimensions 8 x 8 avec bordure (par défaut) :')
    laby.setLockGrid((2,2),True)
    liste = laby.parcours_min((0,0),(7,7))
    for i in liste:
        laby.setContenu(i,"X")
    print(laby.afficheGrille())