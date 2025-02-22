# %%.
"""mode-based production variables
"""

__author__ = "Rahul Kakodkar"
__copyright__ = "Copyright 2022, Multi-parametric Optimization & Control Lab"
__credits__ = ["Rahul Kakodkar", "Efstratios N. Pistikopoulos"]
__license__ = "MIT"
__version__ = "1.0.5"
__maintainer__ = "Rahul Kakodkar"
__email__ = "cacodcar@tamu.edu"
__status__ = "Production"

from itertools import product
from pyomo.environ import Binary, ConcreteModel, NonNegativeReals, Var


def generate_mode_vars(instance: ConcreteModel, scale_level: int = 0, mode_dict: dict = None):
    """declares pyomo variables for mode based production at the chosen scale:

    P_m: Production within a mode

    X_P_m: Production mode binary variable, 1 if process is in mode

    X_P_mm: 1, if there is a mode transition from m to m' in a time period


    Args:
        instance (ConcreteModel): pyomo instance
        scale_level (int, optional):  scale for scheduling variables. Defaults to 0.
    """

    if mode_dict is None:
        mode_dict = dict()
    instance.X_P_m = Var(instance.locations, [(i, j) for i in mode_dict.keys(
    ) for j in mode_dict[i]], instance.scales_scheduling, within=Binary, doc='Production mode binaries')
    instance.Cap_P_m = Var(instance.locations, [(i, j) for i in mode_dict.keys(
    ) for j in mode_dict[i]], instance.scales_scheduling, within=NonNegativeReals, doc='Production mode capacity')
    instance.X_P_mm = Var(instance.locations, [(i, j) for i in mode_dict.keys() for j in product(
        mode_dict[i], mode_dict[i])], instance.scales_scheduling, within=Binary, doc="Production mode transition binaries")

    return
