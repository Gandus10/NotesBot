import pickle
from collections import defaultdict
from collections.abc import Collection

def dd_branch():
	return Branch()

def dd_module():
	return Module()


class Grade:
	"""Represents a grade, with a weight."""

	def __init__(self, value, weight=1):
		self.value = value
		self.weight = weight

	def __repr__(self):
		return f"{self.value} ({self.weight})"


class Branch:
	"""Represents a branch, contains a list of grades. Also has a weight in the module."""

	def __init__(self, weight=1):
		self.weight = weight
		self.grades = []

	def __iadd__(self, values):
		if not isinstance(values, Collection):
			values = [values]
		self.grades.append(Grade(*values))
		return self

	def average(self):
		somme = 0
		diviseur = 0
		#print("grade:",self.grades)
		for grade in self.grades:
			somme += grade.value * grade.weight
			diviseur += grade.weight
		assert(diviseur > 0)
		return round(somme/diviseur, 1)


class Module:
	"""Represents the module, contains list of branches."""

	def __init__(self):
		self.branches = defaultdict(dd_branch)

	def __getattr__(self, name):
		return self.branches[name]

	def __iadd__(self, values):
		"""Error, branch has no attribute name."""
		if not isinstance(values, Collection):
			values = [values]
		branch = Branch(*values)
		self.branches[branch.name] = branch
		return self

	def __getstate__(self):
		return self.branches

	def __setstate__(self, state):
		self.branches = state

	def average(self):
		somme = 0
		diviseur = 0
		for branch in self.branches.values():
			somme += branch.weight * branch.average()
			diviseur += branch.weight
		assert(diviseur > 0)
		return round(somme/diviseur,1)


class User:
	"""Represents the user, has a list of modules."""

	def __init__(self, username):
		self.username = username
		self.modules = defaultdict(dd_module)

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


def load_user(name):
	user = User(name);
	user.load()
	return user

#jean = load_user("jean")
jean = User('jean')
#mod = input("modules : ")
#cours = input("cours : ")

entree = input("entree : ")

#eval(entree)

jean.sciences.math += 4
jean.sciences.analyse += 4
jean.mod.cours += 6
print(jean.mod.cours.average())
print(jean.sciences.average(),"/", jean.sciences.math.average(),"/", jean.sciences.analyse.average())

jean.save();
