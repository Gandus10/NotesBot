import pickle

class User:
	"""docstring for User"""
	list_module = []
	def __init__(self, username):
		self.username = username

	def add_module(self, name_module):
		if self.get_module(name_module) == None:
			module = Module(name_module)
			self.list_module.append(module)
			return module
		else:
			print("Module déjà existant")

	def save(self):
		with open(self.username + ".dat", "wb") as f:
			pickle.dump(self.list_module, f)

	def load(self):
		with open(self.username + ".dat", "rb") as f:
			list_module = pickle.load(f)

	def get_module(self, module_name):
		for module in self.list_module:
			if(module.name == module_name):
				return module
		return None
		
class Module:
	"""docstring for Module"""
	list_cours = []
	def __init__(self, name):
		self.name = name

	def add_cours(self, name_cours, poids_cours):
		if self.get_cours(name_cours) == None:
			cours = Cours(name_cours, poids_cours)
			self.list_cours.append(cours)
			return cours
		else:
			print("Cours déjà existant")

	def average(self):
		somme = 0
		diviseur = 0
		for cours in self.list_cours:
			somme += cours.average() * cours.poids
			diviseur += cours.poids
		assert(diviseur>0)
		return round(somme/diviseur,1)

	def get_cours(self, cours_name):
		for cours in self.list_cours:
			if(cours.name == cours_name):
				return cours
		return None

class Cours:
	"""docstring for Course"""
	list_notes = []
	def __init__(self, name, poids):
		self.name = name
		self.poids = poids

	def add_note(self, value, poids):
		self.list_notes.append(Note(value, poids))
		return self.list_notes

	def average(self):
		somme = 0
		diviseur = 0
		for note in self.list_notes:
			somme += note.value * note.poids
			diviseur += note.poids
		assert(diviseur>0)
		return round(somme/diviseur, 1)


class Note:
	"""docstring for Notes"""
	def __init__(self, value, poids):
		self.value = value
		self.poids = poids


jean = User("jean")

jean.add_module("sciences").add_cours("math", 1).add_note(5, 1)

jean.save()
jean.load()

print("Moyenne du cours:", jean.get_module("sciences").get_cours("math").average())
print("Moyenne du module:", jean.get_module("sciences").average())

jean.get_module("sciences").get_cours("math").add_note(6,0.5)
print("Moyenne du cours après ajout d'un 6 de poids 0.5:", jean.get_module("sciences").get_cours("math").average())