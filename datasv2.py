import pickle
import os
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

	def add_grade(self, value, weight):
		self.grades.append(Grade(value, weight))

	def average(self):
		somme = 0
		diviseur = 0
		#print("grade:",self.grades)
		for grade in self.grades:
			somme += float(grade.value) * float(grade.weight)
			diviseur += float(grade.weight)
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

	def get_branch(self, name):
		return self.branches[name]

	def add_branch(self, name, weight=1):
		return self.branches[name]

	def average(self):
		somme = 0
		diviseur = 0
		for branch in self.branches.values():
			somme += float(branch.weight) * branch.average()
			diviseur += float(branch.weight)
		if not diviseur:
			return 0
		return round(somme/diviseur,1)


class User:
	"""Represents the user, has a list of modules."""

	def __init__(self, discord_id):
		self.discord_id = discord_id
		self.modules = defaultdict(dd_module)

	def __iadd__(self, values):
		if not isinstance(values, Collection):
			values = [values]
		self.modules.append(Module(*values))
		return self

	def __getattr__(self, name):
		return self.modules[name]

	def get_module(self, name):
		return self.modules[name]

	def save(self):
		if not os.path.exists("./user_datas"):
			os.makedirs("./user_datas")
		with open("./user_datas/"+self.discord_id + ".dat", "wb") as f:
			pickle.dump(self.modules, f)

	def load(self):
		if not os.path.exists("./user_datas"):
			os.makedirs("./user_datas")
		try:
			with open("./user_datas/" + self.discord_id + ".dat", "rb") as f:
				self.modules = pickle.load(f)

		except FileNotFoundError:
			self.save()

	def __str__(self):
		string = str()
		for mod_name, module in self.modules.items():
			string += f"{mod_name} : \n"
			for branch_name, branch in module.branches.items():
				string += f"\t{branch_name} : {branch.grades}\n"
			string += "\n"
		return string


def load_user(name):
	user = User(name);
	user.load()
	return user
