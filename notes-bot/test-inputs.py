"""Test module for dataprocess. Message come from input() method."""

from dataprocess import load_user


def process(message, user):
    """Process message."""
    command, *args = message.split()

    if command == 'moyenne':
        module_ou_cours, *values = args
        if module_ou_cours in user.modules:
            print(user.get_module(module_ou_cours).average())
        else:
            # Ce n'est pas un module donc on cherche un cours
            for name, module in user.modules.items():
                if module_ou_cours in module.branches:
                    print(module.get_branch(module_ou_cours).average())

    if command == 'ajoute':
        cours_ou_note, nom_module, nom_du_cours, *values = args
        if cours_ou_note == 'cours':
            poids = values
            user.get_module(nom_module).add_branch(nom_du_cours, poids)
            print("cours ajouté :", nom_du_cours, "dans", nom_module)
            user.save()
        elif cours_ou_note == 'note':
            note, poids = values
            user.get_module(nom_module).get_branch(
                nom_du_cours).add_grade(note, poids)
            print("note ajoutée", note, poids, "dans", nom_du_cours)
            user.save()

    if command == 'affiche':
        print(user)

    if command == 'help':
        help_msg = """help message prototype"""
        print(help_msg)


user = load_user('Sylvain_Renaud')
# user = User('Sylvain_Renaud')
# user.load()

while True:
    message = input("message: ")
    process(message, user)
