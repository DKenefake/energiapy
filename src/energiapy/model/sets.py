"""pyomo sets
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
from pyomo.environ import ConcreteModel, Set


def generate_sets(instance: ConcreteModel, scenario: Scenario):
    """Generates pyomo sets based on declared lists.

    Creates the following sets:

    processes: Set of all processes

    processes_full: 'Set of all processes including dummy discharge'

    resources: Set of all resources

    resources_nosell: Set of non-dischargeable resources

    resources_sell: Set of dischargeable resources

    resources_store: Set of storeable resources

    resources_purch: Set of purchased resources  

    resources_varying: Set of resources with varying purchase price

    resources_demand: Set of resources with exact demand

    resources_transport: Set of resource which can be transported

    processes_varying: Set of processes with varying capacity

    processes_failure: Set of processes which can fail

    processes_materials: Set of processes with material requirements

    processes_storage: Set of storage process

    processes_multim: Set of processes with multiple modes

    processes_singlem: Set of processes with multiple modes

    locations: Set of locations

    sources: Set of locations which act as sources

    sinks: Set of locations which act as sinks

    materials: Set of materials

    transports: Set of transportation options



    scales: Set of scales


    Args:
        instance (ConcreteModel): pyomo instance
        scenario (Scenario): scenario

    """

    instance.scales = Set(scenario.scales.list,
                          initialize=scenario.scales.scale, doc='set of scales')

    # instance.source_sink_pairs = Set(list(scenario.transport_avail_dict.keys(
    # )), initialize={i: list(j) for i, j in scenario.transport_avail_dict.items()})

    sets = scenario.set_dict

    instance.processes = Set(
        initialize=sets['processes'], doc='Set of processes')
    instance.processes_full = Set(initialize=sets['processes_full'],
                                  doc='Set of all processes including dummy discharge')
    instance.resources = Set(
        initialize=sets['resources'], doc='Set of resources')
    instance.resources_nosell = Set(
        initialize=sets['resources_nosell'], doc='Set of non-dischargeable resources')
    instance.resources_sell = Set(
        initialize=sets['resources_sell'], doc='Set of dischargeable resources')
    instance.resources_store = Set(
        initialize=sets['resources_store'], doc='Set of storeable resources')
    instance.resources_purch = Set(
        initialize=sets['resources_purch'], doc='Set of purchased resources')

    instance.resources_varying_price = Set(initialize=sets['resources_varying_price'],
                                           doc='Set of resources with varying purchase price')

    instance.resources_certain_price = Set(initialize=sets['resources_certain_price'],
                                           doc='Set of resources with certain purchase price')

    instance.resources_varying_availability = Set(initialize=sets['resources_varying_availability'],
                                                  doc='Set of resources with varying purchase price')

    instance.resources_certain_availability = Set(initialize=sets['resources_certain_availability'],
                                                  doc='Set of resources with certain purchase price')

    instance.resources_varying_revenue = Set(initialize=sets['resources_varying_revenue'],
                                             doc='Set of resources with varying selling revenue')
    instance.resources_certain_revenue = Set(initialize=sets['resources_certain_revenue'],
                                             doc='Set of resources with certain selling revenue')
    instance.resources_varying_demand = Set(initialize=sets['resources_varying_demand'],
                                            doc='Set of resources with varying purchase price')
    instance.resources_certain_demand = Set(initialize=sets['resources_certain_demand'],
                                            doc='Set of resources with certain purchase price')
    instance.resources_demand = Set(
        initialize=sets['resources_demand'], doc='Set of resources with exact demand')
    instance.processes_varying_capacity = Set(
        initialize=sets['processes_varying_capacity'], doc='Set of processes with varying capacity')
    instance.processes_certain_capacity = Set(
        initialize=sets['processes_certain_capacity'], doc='Set of processes with certain capacity')
    instance.processes_varying_expenditure = Set(
        initialize=sets['processes_varying_expenditure'], doc='Set of processes with varying expenditure')
    instance.processes_failure = Set(
        initialize=sets['processes_failure'], doc='Set of processes which can fail')
    instance.processes_materials = Set(initialize=sets['processes_materials'],
                                       doc='Set of processes with material requirements')
    instance.processes_storage = Set(
        initialize=sets['processes_storage'], doc='Set of storage process')
    instance.processes_multim = Set(
        initialize=sets['processes_multim'], doc='Set of processes with multiple modes')
    instance.processes_singlem = Set(
        initialize=sets['processes_singlem'], doc='Set of processes with multiple modes')
    instance.locations = Set(
        initialize=sets['locations'], doc='Set of locations')

    instance.resources_uncertain_price = Set(initialize=sets['resources_uncertain_price'],
                                             doc='Set of resources with uncertain purchase price')
    instance.resources_uncertain_revenue = Set(initialize=sets['resources_uncertain_revenue'],
                                               doc='Set of resources with uncertain purchase revenue')
    instance.resources_uncertain_demand = Set(initialize=sets['resources_uncertain_demand'],
                                              doc='Set of resources with uncertain demand')
    instance.processes_uncertain_capacity = Set(initialize=sets['processes_uncertain_capacity'],
                                                doc='Set of processes with uncertain capacity')
    instance.processes_segments = Set(
        initialize=sets['processes_segments'], doc='Set of processes with PWL process segments')

    instance.process_material_modes = Set(initialize= sets['process_material_modes'], doc = 'Set of process and material combinations')
    
    instance.material_modes = Set(initialize= sets['material_modes'], doc = 'Set of material modes')
    
    if len(instance.locations) > 1:

        instance.transports_varying_capacity = Set(
            initialize=sets['transports_varying_capacity'], doc='Set of transports with varying capacity')
        instance.transports_varying_capex = Set(
            initialize=sets['transports_varying_capex'], doc='Set of transports with varying capex')
        instance.transports_varying_fopex = Set(
            initialize=sets['transports_varying_fopex'], doc='Set of transports with varying fopex')
        instance.transports_varying_vopex = Set(
            initialize=sets['transports_varying_vopex'], doc='Set of transports with varying vopex')

        instance.transports_certain_capacity = Set(
            initialize=sets['transports_certain_capacity'], doc='Set of transports with certain capacity')
        instance.transports_certain_capex = Set(
            initialize=sets['transports_certain_capex'], doc='Set of transports with certain capex')
        instance.transports_certain_fopex = Set(
            initialize=sets['transports_certain_fopex'], doc='Set of transports with certain fopex')
        instance.transports_certain_vopex = Set(
            initialize=sets['transports_certain_vopex'], doc='Set of transports with certain vopex')

        instance.transports_uncertain_capacity = Set(
            initialize=sets['transports_uncertain_capacity'], doc='Set of transports with uncertain capacity')
        instance.transports_uncertain_capex = Set(
            initialize=sets['transports_uncertain_capex'], doc='Set of transports with uncertain capex')
        instance.transports_uncertain_fopex = Set(
            initialize=sets['transports_uncertain_fopex'], doc='Set of transports with uncertain fopex')
        instance.transports_uncertain_vopex = Set(
            initialize=sets['transports_uncertain_vopex'], doc='Set of transports with uncertain vopex')

    mode_lens = []
    for j in scenario.location_set:
        for i in scenario.process_set:
            if i.name in scenario.location_process_dict[j.name]:
                mode_lens.append(len(scenario.prod_max[j.name][i.name].keys()))

    instance.modes = Set(initialize=list(
        range(max(mode_lens))), doc='Set of process modes')

    if scenario.source_locations is not None:
        instance.sources = Set(
            initialize=sets['sources'], doc='Set of sources')

    if scenario.sink_locations is not None:
        instance.sinks = Set(initialize=sets['sinks'], doc='Set of sinks')

    if len(scenario.material_set) > 0:
        instance.materials = Set(
            initialize=sets['materials'], doc='Set of materials')

    if scenario.transport_set is not None:
        instance.transports = Set(
            initialize=sets['transports'], doc='Set of transports')
        instance.resources_trans = Set(
            initialize=sets['resources_trans'], doc='Set of transportable resources')
    return
