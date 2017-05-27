from lxml import etree

def calculMoyenneModule(module, module_name):
	"""Calcul la moyenne d'un module. Moyenne des moyennes des cours de ce module."""
	somme = 0
	diviseur = 0

	for cours in module.iter("cours"):
		poids = float(cours.get("poids"))
		somme += poids * round(calculMoyenneCours(cours, cours.get("nom")), 1)
		diviseur += poids

	return round(somme/diviseur, 1)

def calculMoyenneCours(cours, cours_name):
	"""Calcul de la moyenne pour un cours."""	
	somme = 0
	diviseur = 0

	for note in cours.iter("note"):
		poids = float(note.get("poids"))
		somme += poids * round(float(note.text), 1)
		diviseur += poids

	return round(somme/diviseur, 1)

def getMoyenne(root, cours_ou_module):
	"""Affiche la moyenne du cours ou du module demandée."""
	for element in root.iter() :
		if element.get("nom") == cours_ou_module :
			if element.tag == "module" : 
				return calculMoyenneModule(element, cours_ou_module)
			elif element.tag == "cours" :
				return calculMoyenneCours(element, cours_ou_module)
			break
	return "Aucun cours ou module de ce nom"

def getNotes(root, cours_ou_module):
	"""Affiche les notes et leurs pondérations d'un cours."""
	for element in root.iter():
		if element.get("nom") == cours_ou_module:
			if element.tag == "cours":
				listNote = []
				for note in element.iter("note"):
					listNote.append(note.text + "*" + note.get("poids"))
				return listNote
	return "Aucun cours ce nom"

# ex : moyenne qt / moyenne programmation / notes analyse
inputs = input("Message : ")

inputs = inputs.split()

tree = etree.parse("sylvain_renaud.xml")
root = tree.getroot()

if inputs[0] == "moyenne" :
	print("Moyenne de", inputs[1],": ", getMoyenne(root, inputs[1]))
elif inputs[0] == "notes" :
	print("Notes de", inputs[1],": ", getNotes(root, inputs[1]))
else :
	print("Commande inconnue")
