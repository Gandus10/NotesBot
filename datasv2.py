import pickle
from collections import defaultdict
from collections.abc import Collection

class User:
	"""Represents the user, has a list of modules."""

	def __init__(self, username):
		self.username = username
		self.modules = defaultdict(Module)

	def __iadd__(self, values):
		if not isinstance(values, Collection):
			values = [values]
		self.modules.append(Module(*values))
		return self

	def __getattr__(self, name):
		return self.modules[name]

	def save(self):
		with open(self.username + ".dat", "wb") as f:
			pickle.dump(self.modules, f)

	def load(self):
		with open(self.username + ".dat", "rb") as f:
			modules = pickle.load(f)

#	def get_module(self, module_name):
#		for module in self.modules:
#			if(module.name == module_name):
#				return module
#		return None
#
#	def add_module(self, name_module):
#		if self.modules[name_module] == None:
#			self.modules[name_module] = Module(name_module)
#			return self.modules[name_module]
#		else:
#			print("Module déjà existant")
		
class Module:
	"""Represents the module, contains list of branches."""
	def __init__(self):
		self.branches = defaultdict(Branch)

	def __getattr__(self, name):
		return self.branches[name]

	def __iadd__(self, values):
		if not isinstance(values, Collection):
			values = [values]
		branch = Branch(*values)
		self.branches[branch.name] = branch
		return self

	def average(self):
		somme = 0
		diviseur = 0
		for branch in self.branches.values():
			somme += branch.weight * branch.average()
			diviseur += branch.weight
		assert(diviseur > 0)
		return round(somme/diviseur,1)

#	def get_Branch(self, branch_name):
#		for branch in self.branches:
#			if(branch.name == branch_name):
#				return branch
#		return None
#
#	def add_Branch(self, name_Branch, weight_branch):
#		if self.get_branch(name_Branch) == None:
#			self.branches.append(Branch(name_Branch, weight_branch))
#			return self.branches[-1]
#		else:
#			print("Cours déjà existant")


class Branch:
	"""Represents a branch, contains a list of grades."""
	def __init__(self, weight=1):
		self.weight = weight
		self.grades = []

	def average(self):
		somme = 0
		diviseur = 0
		for grade in self.grades:
			somme += grade.value * grade.weight
			diviseur += grade.weight
		assert(diviseur > 0)
		return round(somme/diviseur, 1)

	def __iadd__(self, values):
		if not isinstance(values, Collection):
			values = [values]
		self.grades.append(Grade(*values))
		return self

#	def add_grade(self, value, weight):
#		self.grades.append(Grade(value, weight))
#		return self.grades


class Grade:
	"""docstring for Grade"""
	def __init__(self, value, weight=1):
		self.value = value
		self.weight = weight

	def __repr__(self):
		return "{self.grade} ({self.weight})".format(self=self)

def load_user(name):
	user = User(name);
	user.load()
	return user

jean = User("jean")

jean.sciences.math += 4
jean.sciences.analyse += 5
print(jean.sciences.average(),"/", jean.sciences.math.average(),"/", jean.sciences.analyse.average())

jean.save();

jean2 = load_user("jean2")
print(jean2.sciences.math.average())

#jean.add_module("sciences").add_Branch("math", 1).add_Grade(5, 1)
#
#jean.save()
#jean.load()
#
#print("Moyenne du cours:", jean.get_module("sciences").get_Branch("math").average())
#print("Moyenne du module:", jean.get_module("sciences").average())
#
#jean.get_module("sciences").get_Branch("math").add_Grade(6, 0.5)
#print("Moyenne du cours après ajout d'un 6 de weight 0.5:", 
#		jean.get_module("sciences").get_Branch("math").average())
