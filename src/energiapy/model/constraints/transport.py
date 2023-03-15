"""pyomo transport constraints
"""

__author__ = "Rahul Kakodkar"
__copyright__ = "Copyright 2022, Multi-parametric Optimization & Control Lab"
__credits__ = ["Rahul Kakodkar", "Efstratios N. Pistikopoulos"]
__license__ = "Open"
__version__ = "0.0.1"
__maintainer__ = "Rahul Kakodkar"
__email__ = "cacodcar@tamu.edu"
__status__ = "Production"

from pyomo.environ import ConcreteModel, Constraint
from ...utils.latex_utils import constraint_latex_render
from ...utils.scale_utils import scale_list
from ...utils.scale_utils import scale_pyomo_set
from ...utils.scale_utils import scale_tuple
from ...components.location import Location
from itertools import product
from typing import Union
from enum import Enum, auto




# *-------------------------Transport constraints--------------------------
def constraint_transport_export(instance: ConcreteModel, scheduling_scale_level: int = 0, transport_avail_dict: dict = {}) -> Constraint:
    """Total resource exported equals amount transported through all modes

    Args:
        instance (ConcreteModel): pyomo model instance
        scheduling_scale_level (int, optional): scale of scheduling decisions. Defaults to 0.
        transport_avail_dict (dict, optional): Modes of transportation available between locations. Defaults to {}.

    Returns:
        Constraint: transport_export
    """
    scales = scale_list(instance=instance,
                        scale_levels=scheduling_scale_level+1)

    def transport_export_rule(instance, source, sink, resource, *scale_list):
        return instance.Exp[source, sink, resource, scale_list[:scheduling_scale_level+1]] == \
            sum(instance.Trans_exp[source, sink, resource, transport_, scale_list[:scheduling_scale_level+1]]
                for transport_ in instance.transports.intersection(transport_avail_dict[(source, sink)]))
    instance.constraint_transport_export = Constraint(instance.sources, instance.sinks,
                                                      instance.resources_trans, *scales, rule=transport_export_rule, doc='export of resource from source to sink')
    constraint_latex_render(transport_export_rule)
    return instance.constraint_transport_export


def constraint_transport_import(instance: ConcreteModel, scheduling_scale_level: int = 0, transport_avail_dict: dict = {}) -> Constraint:
    """Total amount of resource imported

    Args:
        instance (ConcreteModel): pyomo model instance
        scheduling_scale_level (int, optional): scale of scheduling decisions. Defaults to 0.
        transport_avail_dict (dict, optional): Modes of transportation available between locations. Defaults to {}.

    Returns:
        Constraint: transport_import
    """
    scales = scale_list(instance=instance,
                        scale_levels=scheduling_scale_level+1)

    def transport_import_rule(instance, sink, source, resource, *scale_list):
        return instance.Imp[sink, source, resource, scale_list[:scheduling_scale_level+1]] == \
            sum(instance.Trans_imp[sink, source, resource, transport_, scale_list[:scheduling_scale_level+1]]
                for transport_ in instance.transports.intersection(transport_avail_dict[(source, sink)]))
    instance.constraint_transport_import = Constraint(instance.sinks, instance.sources,
                                                      instance.resources_trans, *scales, rule=transport_import_rule, doc='import of resource from sink to source')
    constraint_latex_render(transport_import_rule)
    return instance.constraint_transport_import


def constraint_transport_balance(instance: ConcreteModel, scheduling_scale_level: int = 0) -> Constraint:
    """Imported resources from sink to source equals exported resources from sink to source

    Args:
        instance (ConcreteModel): pyomo model instance
        scheduling_scale_level (int, optional): scale of scheduling decisions. Defaults to 0.

    Returns:
        Constraint: transport_balance
    """
    scales = scale_list(instance=instance,
                        scale_levels=scheduling_scale_level+1)

    def transport_balance_rule(instance, sink, source, resource, *scale_list):
        return instance.Imp[sink, source, resource, scale_list[:scheduling_scale_level+1]] == instance.Exp[source, sink, resource, scale_list[:scheduling_scale_level+1]]
    instance.constraint_transport_balance = Constraint(instance.sinks, instance.sources,
                                                       instance.resources_trans, *scales, rule=transport_balance_rule, doc='balances import and export from source to sinks')
    constraint_latex_render(transport_balance_rule)
    return instance.constraint_transport_balance


def constraint_transport_exp_UB(instance: ConcreteModel, scheduling_scale_level: int = 0, trans_max: dict = {}, transport_avail_dict: dict = {}) -> Constraint:
    """Maximum resource that can be transported

    Args:
        instance (ConcreteModel): pyomo model instance
        scheduling_scale_level (int, optional): scale of scheduling decisions. Defaults to 0.
        trans_max (dict, optional): Maximum allowed transportation. Defaults to {}.
        transport_avail_dict (dict, optional): Modes of transportation available between locations. Defaults to {}.

    Returns:
        Constraint: transport_exp_UB
    """
    scales = scale_list(instance=instance,
                        scale_levels=scheduling_scale_level+1)

    def transport_exp_UB_rule(instance, source, sink, resource, transport, *scale_list):
        if transport in transport_avail_dict[(source, sink)]:
            return instance.Trans_exp[source, sink, resource, transport, scale_list[:scheduling_scale_level+1]] <= trans_max[transport]
        else:
            return instance.Trans_exp[source, sink, resource, transport, scale_list[:scheduling_scale_level+1]] <= 0
    instance.constraint_transport_exp_UB = Constraint(instance.sources, instance.sinks, instance.resources_trans,
                                                      instance.transports, *scales, rule=transport_exp_UB_rule, doc='import of resource from sink to source')
    constraint_latex_render(transport_exp_UB_rule)
    return instance.constraint_transport_exp_UB


def constraint_transport_imp_UB(instance: ConcreteModel, scheduling_scale_level: int = 0, trans_max: dict = {}, transport_avail_dict: dict = {}) -> Constraint:
    """Maximum amount of resource that can be imported

    Args:
        instance (ConcreteModel): pyomo model instance
        scheduling_scale_level (int, optional): scale of scheduling decisions. Defaults to 0.
        trans_max (dict, optional): Maximum allowed transportation. Defaults to {}.
        transport_avail_dict (dict, optional): Modes of transportation available between locations. Defaults to {}.

    Returns:
        Constraint: transport_imp_UB
    """
    scales = scale_list(instance=instance,
                        scale_levels=scheduling_scale_level+1)

    def transport_imp_UB_rule(instance, sink, source, resource, transport, *scale_list):
        if transport in transport_avail_dict[(source, sink)]:
            return instance.Trans_imp[sink, source, resource, transport, scale_list[:scheduling_scale_level+1]] <= trans_max[transport]
        else:
            return instance.Trans_imp[sink, source, resource, transport, scale_list[:scheduling_scale_level+1]] <= 0
    instance.constraint_transport_imp_UB = Constraint(instance.sinks, instance.sources, instance.resources_trans,
                                                      instance.transports, *scales, rule=transport_imp_UB_rule, doc='import of resource from sink to source')
    constraint_latex_render(transport_imp_UB_rule)
    return instance.constraint_transport_imp_UB
