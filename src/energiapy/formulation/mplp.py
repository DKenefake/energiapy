"""Formulates a multiscale mixed integer linear programming (MILP) model from Scenario  
"""

__author__ = "Rahul Kakodkar"
__copyright__ = "Copyright 2022, Multi-parametric Optimization & Control Lab"
__credits__ = ["Rahul Kakodkar", "Efstratios N. Pistikopoulos"]
__license__ = "Open"
__version__ = "0.0.1"
__maintainer__ = "Rahul Kakodkar"
__email__ = "cacodcar@tamu.edu"
__status__ = "Production"

from ..components.scenario import Scenario
from ..model.sets import generate_sets
from ..model.variables import *
from ..model.constraints import *
from ..model.objectives import uncertainty_cost_objective
from pyomo.environ import ConcreteModel, Suffix

    
def formulate_mplp(scenario: Scenario, relax: dict = None, penalty = float) -> ConcreteModel:
    """formulates a multi-scale mixed integer linear programming formulation of the scenario
    
    Args:
        scenario (Scenario): scenario under consideration

    Returns:
        ConcreteModel: pyomo model instance with sets, variables, constraints, objectives generated
    """
    
    instance = ConcreteModel()
    
    generate_sets(instance= instance, location_set= scenario.location_set, transport_set= scenario.transport_set, scales= scenario.scales, \
        process_set= scenario.process_set, resource_set= scenario.resource_set, material_set= scenario.material_set, \
            source_set= scenario.source_locations, sink_set= scenario.sink_locations)

    generate_scheduling_vars(instance = instance, scale_level= scenario.scheduling_scale_level)
    generate_network_vars(instance = instance, scale_level= scenario.network_scale_level)
    generate_uncertainty_vars(instance= instance, scale_level= scenario.scheduling_scale_level)
    if len(instance.locations) > 1:
        generate_transport_vars(instance= instance, scale_level= scenario.scheduling_scale_level) 
    
    inventory_balance_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level,\
        conversion= scenario.conversion)
    uncertain_nameplate_production_constraint(instance= instance, network_scale_level= \
        scenario.network_scale_level, scheduling_scale_level= scenario.scheduling_scale_level)
    nameplate_inventory_constraint(instance= instance, loc_res_dict= scenario.loc_res_dict, network_scale_level= scenario.network_scale_level,\
        scheduling_scale_level= scenario.scheduling_scale_level)
    resource_consumption_constraint(instance= instance, loc_res_dict= scenario.loc_res_dict, cons_max= scenario.cons_max, scheduling_scale_level= scenario.scheduling_scale_level)
    uncertain_resource_purchase_constraint(instance= instance, price= scenario.price, \
        loc_res_dict= scenario.loc_res_dict, scheduling_scale_level= scenario.scheduling_scale_level, \
            expenditure_scale_level= scenario.expenditure_scale_level)
    # resource_discharge_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level)

    # production_facility_fix_constraint(instance= instance, production_binaries = relax['X_P'],prod_max= scenario.prod_max, loc_pro_dict= scenario.loc_pro_dict, network_scale_level= scenario.network_scale_level)
    # storage_facility_fix_constraint(instance= instance, storage_binaries = relax['X_S'], store_max= scenario.store_max, loc_res_dict= scenario.loc_res_dict, network_scale_level= scenario.network_scale_level)
    delta_cap_location_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    delta_cap_network_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
        
    
    location_production_constraint(instance= instance, network_scale_level= scenario.network_scale_level, cluster_wt = scenario.cluster_wt)
    location_discharge_constraint(instance= instance, network_scale_level= scenario.network_scale_level, cluster_wt = scenario.cluster_wt)
    location_consumption_constraint(instance= instance, network_scale_level= scenario.network_scale_level, cluster_wt = scenario.cluster_wt)
    location_purchase_constraint(instance= instance, network_scale_level= scenario.network_scale_level, cluster_wt = scenario.cluster_wt)

    network_production_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    network_discharge_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    network_consumption_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    network_purchase_constraint(instance= instance, network_scale_level= scenario.network_scale_level)


    process_capex_constraint(instance= instance, capex_dict= scenario.capex_dict, network_scale_level= scenario.network_scale_level)
    process_fopex_constraint(instance= instance, fopex_dict= scenario.fopex_dict, network_scale_level= scenario.network_scale_level)
    process_vopex_constraint(instance= instance, vopex_dict= scenario.vopex_dict, network_scale_level= scenario.network_scale_level)
    
    process_land_constraint(instance= instance, land_dict= scenario.land_dict, network_scale_level= scenario.network_scale_level)
    location_land_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    network_land_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    

    location_capex_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    location_fopex_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    location_vopex_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    
    network_capex_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    network_fopex_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    network_vopex_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
    
    demand_constraint(instance= instance, demand_scale_level= scenario.demand_scale_level, scheduling_scale_level= scenario.scheduling_scale_level, demand= scenario.demand)
    
    if len(scenario.location_set) > 1:
        transport_export_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level, transport_avail_dict= scenario.transport_avail_dict)
        transport_import_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level, transport_avail_dict= scenario.transport_avail_dict)
        transport_exp_UB_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level, trans_max= scenario.trans_max, transport_avail_dict= scenario.transport_avail_dict)  
        transport_imp_UB_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level, trans_max= scenario.trans_max, transport_avail_dict= scenario.transport_avail_dict)  
        transport_balance_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level)
        
        transport_exp_cost_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level, trans_cost= scenario.trans_cost, distance_dict= scenario.distance_dict)  
        transport_imp_cost_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level, trans_cost= scenario.trans_cost, distance_dict= scenario.distance_dict)  
        transport_cost_constraint(instance= instance, scheduling_scale_level= scenario.scheduling_scale_level)
        transport_cost_network_constraint(instance= instance, network_scale_level= scenario.network_scale_level)
        
        
    instance.dual = Suffix(direction=Suffix.IMPORT)

    uncertainty_cost_objective(instance= instance, penalty = penalty, network_scale_level= scenario.network_scale_level)
    
    return instance