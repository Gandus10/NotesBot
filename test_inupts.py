
from datasv2 import User
from datasv2 import load_user

def traitement(message, user):
	commande, *args = message.split()

	if commande == 'moyenne':
		module_ou_cours, *values = args
		if module_ou_cours in user.modules:
			print(user.get_module(module_ou_cours).average())
		else:
			# Ce n'est pas un module donc on cherche un cours
			for name, module in user.modules.items():
				if module_ou_cours in module.branches:
					print(module.get_branch(module_ou_cours).average())

	if commande == 'ajoute':
		cours_ou_note, nom_module, nom_du_cours, *values = args
		if  cours_ou_note == 'cours':
			poids = values
			user.get_module(nom_module).add_branch(nom_du_cours, poids)
			print("cours ajouté :", nom_du_cours,"dans",nom_module)
			user.save()
		elif cours_ou_note == 'note':
			note, poids = values
			user.get_module(nom_module).get_branch(nom_du_cours).add_grade(note, poids)
			print("note ajoutée", note, poids,"dans",nom_du_cours)
			user.save()

	if commande == 'affiche':
		print(user)

	if commande == 'help':
		print("Ajouter un cours avec :\n\tajoute nom_du_module nom_du_cours poids_du_cours_dans_le_module\n",
			  "Ajouter une note avec : \n\tajoute nom_du_module nom_du_cours note poids_de_la_note\n",
			  "Calcul la moyenne d'un cours avec : \n\t moyenne nom_du_cours\n",
			  "Calcul la moyenne d'un module avec : \n\t moyenne nom_du_module\n",
			  "Affichage d'un résumé : affiche"
			  )

user = load_user('Sylvain_Renaud')
#user = User('Sylvain_Renaud')
#user.load()

while True:
	message = input("message: ")
	traitement(message, user)
