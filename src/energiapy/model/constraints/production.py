"""production constraints
"""

__author__ = "Rahul Kakodkar"
__copyright__ = "Copyright 2023, Multi-parametric Optimization & Control Lab"
__credits__ = ["Rahul Kakodkar", "Efstratios N. Pistikopoulos"]
__license__ = "MIT"
__version__ = "1.0.5"
__maintainer__ = "Rahul Kakodkar"
__email__ = "cacodcar@tamu.edu"
__status__ = "Production"

from pyomo.environ import ConcreteModel, Constraint

from ...utils.latex_utils import constraint_latex_render
from ...utils.scale_utils import scale_list


def constraint_production_facility_affix(instance: ConcreteModel, affix_production_cap: dict, location_process_dict: dict = None,
                                         network_scale_level: int = 0) -> Constraint:
    """affixes the capacity of production facilities

    Args:
        instance (ConcreteModel): pyomo instance
        prod_max (dict): maximum production of process at location
        location_process_dict (dict, optional): production facilities avaiable at location. Defaults to {}.
        network_scale_level (int, optional): scale of network decisions. Defaults to 0.

    Returns:
        Constraint: production_facility_affix
    """

    if location_process_dict is None:
        location_process_dict = dict()

    scales = scale_list(instance=instance,
                        scale_levels=network_scale_level + 1)

    def production_facility_affix_rule(instance, location, process, *scale_list):
        if process in location_process_dict[location]:
            if affix_production_cap[location, process, scale_list[:network_scale_level + 1][0]] > 0.0:
                return instance.Cap_P[location, process, scale_list[:network_scale_level + 1]] == affix_production_cap[location, process, scale_list[:network_scale_level + 1][0]]
            else:
                return instance.Cap_P[location, process, scale_list[:network_scale_level + 1]] >= 0.0
        else:
            return instance.Cap_P[location, process, scale_list[:network_scale_level + 1]] == 0

    instance.constraint_production_facility_affix = Constraint(
        instance.locations, instance.processes, *
        scales, rule=production_facility_affix_rule,
        doc='production facility sizing and location')
    constraint_latex_render(production_facility_affix_rule)
    return instance.constraint_production_facility_affix


def constraint_production_facility_fix(instance: ConcreteModel, prod_max: dict, production_binaries: dict,
                                       location_process_dict: dict = None, network_scale_level: int = 0) -> Constraint:
    """Determines where production facility of certain capacity is inserted at location in network

    Args:
        instance (ConcreteModel): pyomo instance
        prod_max (dict): maximum production of process at location
        location_process_dict (dict, optional): production facilities avaiable at location. Defaults to {}.
        network_scale_level (int, optional): scale of network decisions. Defaults to 0.

    Returns:
        Constraint: production_facility_fix
    """

    if location_process_dict is None:
        location_process_dict = dict()

    scales = scale_list(instance=instance,
                        scale_levels=network_scale_level + 1)

    def production_facility_fix_rule(instance, location, process, *scale_list):
        if process in location_process_dict[location]:
            return instance.Cap_P[location, process, scale_list[:network_scale_level + 1]] <= prod_max[location][
                process] * \
                production_binaries[(
                    location, process, *scale_list[:network_scale_level + 1])]
        else:
            return instance.Cap_P[location, process, scale_list[:network_scale_level + 1]] == 0

    instance.constraint_production_facility_fix = Constraint(
        instance.locations, instance.processes, *
        scales, rule=production_facility_fix_rule,
        doc='production facility sizing and location')
    constraint_latex_render(production_facility_fix_rule)
    return instance.constraint_production_facility_fix


def constraint_nameplate_production(instance: ConcreteModel, capacity_factor: dict = None, location_process_dict: dict = None,
                                    network_scale_level: int = 0, scheduling_scale_level: int = 0) -> Constraint:
    """Determines production capacity utilization of facilities at location in network and capacity of facilities

    Args:
        instance (ConcreteModel): pyomo instance
        capacity_factor (dict, optional): uncertain capacity availability training data. Defaults to {}.
        location_process_dict (dict, optional): production facilities avaiable at location. Defaults to {}.
        network_scale_level (int, optional): scale of network decisions. Defaults to 0.
        scheduling_scale_level (int, optional): scale of scheduling decisions. Defaults to 0.

    Returns:
        Constraint: nameplate_production
    """

    if capacity_factor is None:
        capacity_factor = dict()

    if location_process_dict is None:
        location_process_dict = dict()

    scales = scale_list(instance=instance,
                        scale_levels=len(instance.scales))

    def nameplate_production_rule(instance, location, process, *scale_list):

        if process not in location_process_dict[location]:
            return instance.P[location, process, scale_list[:scheduling_scale_level + 1]] == 0

        else:
            if process not in instance.processes_varying_capacity:
                return instance.P[location, process, scale_list[:scheduling_scale_level + 1]] <= instance.Cap_P[
                    location, process, scale_list[:network_scale_level + 1]]
            else:
                return instance.P[location, process, scale_list[:scheduling_scale_level + 1]] <= capacity_factor[location][process][scale_list[:scheduling_scale_level + 1]] * instance.Cap_P[location, process,
                                                                                                                                                                                              scale_list[:network_scale_level + 1]]

    instance.constraint_nameplate_production = Constraint(
        instance.locations, instance.processes, *
        scales, rule=nameplate_production_rule,
        doc='nameplate production capacity constraint')
    constraint_latex_render(nameplate_production_rule)
    return instance.constraint_nameplate_production


def constraint_nameplate_production_material_mode(instance: ConcreteModel, capacity_factor: dict = None, location_process_dict: dict = None,
                                                  network_scale_level: int = 0, scheduling_scale_level: int = 0) -> Constraint:
    """Determines production capacity utilization of facilities at location in network and capacity of facilities

    Args:
        instance (ConcreteModel): pyomo instance
        capacity_factor (dict, optional): uncertain capacity availability training data. Defaults to {}.
        location_process_dict (dict, optional): production facilities avaiable at location. Defaults to {}.
        network_scale_level (int, optional): scale of network decisions. Defaults to 0.
        scheduling_scale_level (int, optional): scale of scheduling decisions. Defaults to 0.

    Returns:
        Constraint: nameplate_production_material_mode
    """

    if capacity_factor is None:
        capacity_factor = dict()

    if location_process_dict is None:
        location_process_dict = dict()

    scales = scale_list(instance=instance,
                        scale_levels=len(instance.scales))

    def nameplate_production_material_mode_rule(instance, location, process, material_mode, *scale_list):

        if process not in location_process_dict[location]:
            return instance.P_material_m[location, process, material_mode, scale_list[:scheduling_scale_level + 1]] == 0

        else:
            if process not in instance.processes_varying_capacity:
                return instance.P_material_m[location, process, material_mode, scale_list[:scheduling_scale_level + 1]] <= instance.Cap_P_M[
                    location, process, material_mode, scale_list[:network_scale_level + 1]]
            else:
                return instance.P_material_m[location, process, material_mode, scale_list[:scheduling_scale_level + 1]] <= capacity_factor[location][process][scale_list[:scheduling_scale_level + 1]] * instance.Cap_P_M[location, process, material_mode,
                                                                                                                                                                                                                          scale_list[:network_scale_level + 1]]

    instance.constraint_nameplate_production_material_mode = Constraint(
        instance.locations, instance.processes, instance.material_modes, *
        scales, rule=nameplate_production_material_mode_rule,
        doc='nameplate production capacity constraint for material mode')
    constraint_latex_render(nameplate_production_material_mode_rule)
    return instance.constraint_nameplate_production_material_mode


def constraint_production_max(instance: ConcreteModel, prod_max: dict, location_process_dict: dict = None,
                              network_scale_level: int = 0) -> Constraint:
    """Restricts maximum capacity realized to cap_max, binary network constraints can override

    Args:
        instance (ConcreteModel): pyomo instance
        prod_max (dict): maximum production of process at location
        location_process_dict (dict, optional): production facilities avaiable at location. Defaults to {}.
        network_scale_level (int, optional): scale of network decisions. Defaults to 0.

    Returns:
        Constraint: production_max
    """
    scales = scale_list(instance=instance,
                        scale_levels=network_scale_level + 1)

    def production_max_rule(instance, location, process, *scale_list):
        if location_process_dict is not None:
            if process in location_process_dict[location]:
                return instance.Cap_P[location, process, scale_list[:network_scale_level + 1]] <= prod_max[location][process][list(prod_max[location][process].keys())[-1:][0]]
            else:
                return instance.Cap_P[location, process, scale_list[:network_scale_level + 1]] == 0
        else:
            return Constraint.Skip

    instance.constraint_production_max = Constraint(
        instance.locations, instance.processes, *scales, rule=production_max_rule,
        doc='production facility sizing')
    constraint_latex_render(production_max_rule)
    return instance.constraint_production_max


def constraint_production_min(instance: ConcreteModel, prod_min: dict, location_process_dict: dict = None,
                              network_scale_level: int = 0) -> Constraint:
    """Restricts minimum capacity of production facility to prod_min

    Args:
        instance (ConcreteModel): pyomo instance
        prod_max (dict): maximum production of process at location
        location_process_dict (dict, optional): production facilities avaiable at location. Defaults to {}.
        network_scale_level (int, optional): scale of network decisions. Defaults to 0.

    Returns:
        Constraint: production_min
    """

    if location_process_dict is None:
        location_process_dict = dict()

    scales = scale_list(instance=instance,
                        scale_levels=network_scale_level + 1)

    def production_min_rule(instance, location, process, *scale_list):

        if location_process_dict is not None:
            if process in location_process_dict[location]:
                return instance.Cap_P[location, process, scale_list[:network_scale_level + 1]] >= prod_min[location][process][list(prod_min[location][process].keys())[-1:][0]]
            else:
                return instance.Cap_P[location, process, scale_list[:network_scale_level + 1]] == 0
        else:
            return Constraint.Skip

    instance.constraint_production_min = Constraint(
        instance.locations, instance.processes, *
        scales, rule=production_min_rule,
        doc='production facility sizing and location')
    constraint_latex_render(production_min_rule)
    return instance.constraint_production_min
