from lxml import etree
import os

def createFile(name):
    """Crée un fichier xml avec le nom de l'utilisateur et y ajoute la déclaration XML au début du fichier."""
    name = name + ".xml"
    fichier = open(name, "w")
    fichier.write("""<?xml version="1.0" encoding="UTF-8"?>\n<modules>\n\t\n</modules>""")
    fichier.close()


def insertNotes(nameCour, note, poids):
    """Insert une nouvelle note dans le cour donnée."""
    cour = etree.Element(nameCour)
    etree.SubElement(cour, "note", nom=nameCour, poids=poids).text = note
    print(etree.tostring(cour, pretty_print=True))
    #return "Aucun cours de ce nom"


def insertModule(root, name):
    """Insert un nouveau module."""
    etree.SubElement(root, "module", nom=name)


def insertCour(nameModule, nameCours, poids):
    """Insert un nouveau cours dans un module donné."""
    module = etree.Element(nameModule)
    etree.SubElement(module, "cours", nom = nameCours, poids = poids)


#créer le fichier laurent_gander.xml
#ajoute le module programmation
#ajoute le cour java
#ajoute la note 5 avec le poids 1
if (os.path.isfile("laurent_gander.xml")!=1):
    createFile("laurent_gander")

tree = etree.parse("laurent_gander.xml")
root = tree.getroot()
insertModule(root,"programmation")
insertCour("programmation","java","1")
insertNotes("java","5","1")
