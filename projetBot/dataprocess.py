"""Structure, save, load and process datas."""

import pickle
import os
from collections import defaultdict
from collections.abc import Collection


def dd_branch():
    """Module scope default_factory for branches in Module."""
    return Branch()


def dd_module():
    """Module scope default_factory for modules in User."""
    return Module()


class Grade:
    """Represents a grade, with a weight."""

    def __init__(self, value, weight=1):
        """Construct a grade with value and weight."""
        self.value = value
        self.weight = weight

    def __repr__(self):
        """Return userfriendly representation of the grade."""
        return f"{self.value} ({self.weight})"


class Branch:
    """Represents a branch with grades and module weight."""

    def __init__(self, weight=1):
        """Construct a branch with a weight."""
        self.weight = weight
        self.grades = []

    def __iadd__(self, values):
        """Add a grade to grades."""
        if not isinstance(values, Collection):
            values = [values]
        self.grades.append(Grade(*values))
        return self

    def add_grade(self, value, weight=1):
        """Add a grade with value and weight to grades."""
        self.grades.append(Grade(value, weight))

    def average(self):
        """Compute average of grades."""
        somme = 0
        diviseur = 0
        # print("grade:",self.grades)
        for grade in self.grades:
            somme += float(grade.value) * float(grade.weight)
            diviseur += float(grade.weight)
        assert(diviseur > 0)
        return round(somme/diviseur, 1)


class Module:
    """Represents the module with branches."""

    def __init__(self):
        """Construct a module."""
        self.branches = defaultdict(dd_branch)

    def __getattr__(self, name):
        """Return the branch in branches with the given name."""
        return self.branches[name]

    def __iadd__(self, values):
        """Add a branch to branches."""
        if not isinstance(values, Collection):
            values = [values]
        branch = Branch(*values)
        self.branches[branch.name] = branch
        return self

    def __getstate__(self):
        """Return the attribute to pickle."""
        return self.branches

    def __setstate__(self, state):
        """Update braches from pickeled state."""
        self.branches = state

    def get_branch(self, name):
        """Return the branch in branches with the given name."""
        return self.branches[name]

    def add_branch(self, name, weight=1):
        """Add a branch to branches at key name."""
        return self.branches[name]

    def average(self):
        """Compute average of branches for this module."""
        somme = 0
        diviseur = 0
        for branch in self.branches.values():
            somme += float(branch.weight) * branch.average()
            diviseur += float(branch.weight)
        if not diviseur:
            return 0
        return round(somme/diviseur, 1)


class User:
    """Represents the user with modules."""

    def __init__(self, discord_id):
        """Create user with the given discord_id."""
        self.discord_id = discord_id
        self.modules = defaultdict(dd_module)

    def __iadd__(self, values):
        """Add a module to modules."""
        if not isinstance(values, Collection):
            values = [values]
        self.modules.append(Module(*values))
        return self

    def __getattr__(self, name):
        """Return the mondule in modules with the givent name."""
        return self.modules[name]

    def get_module(self, name):
        """Return the mondule in modules with the givent name."""
        return self.modules[name]

    def save(self):
        """Save user datas in file named by discord_id."""
        if not os.path.exists("./user_datas"):
            os.makedirs("./user_datas")
        with open("./user_datas/"+self.discord_id + ".dat", "wb") as f:
            pickle.dump(self.modules, f)

    def load(self):
        """Load user datas from named like discord_id."""
        if not os.path.exists("./user_datas"):
            os.makedirs("./user_datas")
        try:
            with open("./user_datas/" + self.discord_id + ".dat", "rb") as f:
                self.modules = pickle.load(f)
        except FileNotFoundError:
            self.save()

    def __str__(self):
        """Return user readable datas of his modules, branches and grades."""
        string = str()
        for mod_name, module in self.modules.items():
            string += f"{mod_name} : \n"
            for branch_name, branch in module.branches.items():
                string += f"\t{branch_name} : {branch.grades}\n"
            string += "\n"
        return string


def load_user(name):
    """Return user with loaded datas by his name."""
    user = User(name)
    user.load()
    return user
