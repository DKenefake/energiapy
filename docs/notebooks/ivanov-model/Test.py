import sys

sys.path.append('../../src')
import energiapy
import pandas
from energiapy.components.temporal_scale import TemporalScale
from energiapy.components.resource import Resource, VaryingResource
from energiapy.components.process import Process, ProcessMode, VaryingProcess
from energiapy.components.location import Location
from energiapy.components.transport import Transport
from energiapy.components.network import Network
from energiapy.components.scenario import Scenario
from energiapy.components.result import Result
from energiapy.model.formulate import formulate, Constraints, Objective
from energiapy.model.solve import solve

# ======================================================================================================================
# Initialize Case Study
# ======================================================================================================================
_time_intervals = 10  # Number of time intervals in a planning horizon    (L_chi)
_commodities = 1  # Number of commodities                             (rho)
_exec_scenarios = 2  # Number of execution scenarios                     (chi)

M = 1e7  # Big M

# Define temporal scales
scales = TemporalScale(discretization_list=[_exec_scenarios, _time_intervals])

# ======================================================================================================================
# Declare resources/commodities
# ======================================================================================================================

com1 = Resource(name='com1', cons_max=M, demand=True, sell=True, revenue= 100.00, price= 7.50,
                block={'imp': 1, 'urg': 1}, label='Commodity 1', store_max=M)

# ======================================================================================================================
# Declare processes/storage capacities
# ======================================================================================================================
store20 = Process(name='store20', storage=com1, store_max=20, prod_max=M, conversion={com1: -1, com1: 1}, capex=2000,
                  label="Storage capacity of 20 units")
store50 = Process(name='store50', storage=com1, store_max=50, prod_max=M, conversion={com1: -1, com1: 1}, capex=5000,
                  label="Storage capacity of 50 units")

# ======================================================================================================================
# Declare locations/warehouses
# ======================================================================================================================
loc1 = Location(name='loc1', processes={store50}, label="Location 1", scales=scales, demand_scale_level=1,
                capacity_scale_level=1, availability_scale_level=1)
loc2 = Location(name='loc2', processes={store20}, label="Location 2", scales=scales, demand_scale_level=1,
                capacity_scale_level=1, availability_scale_level=1)

# ======================================================================================================================
# Declare transport/trucks
# ======================================================================================================================
truck100 = Transport(name='truck100', resources=[com1], trans_max=100, label='Truck with maximum capacity of 100 units',
                     trans_cost=0.1)

transport_matrix = [
    [[], [truck100]],  # sink: location 1
    [[truck100], []],  # sink: location 2
]

distance_matrix = [
    [0, 10],
    [10, 0],
]

# ======================================================================================================================
# Declare network
# ======================================================================================================================
locset = {loc1, loc2}

sources = list(locset)
sinks = list(locset)

network = Network(name='Network', source_locations=sources, sink_locations=sinks, transport_matrix=transport_matrix,
                  distance_matrix=distance_matrix)


# ======================================================================================================================
# Declare scenario
# ======================================================================================================================
demand_dict = {i: {com1: 100} for i in locset if i == loc2}
scenario = Scenario(name='scenario', scales=scales, scheduling_scale_level=1, network_scale_level=0, expenditure_scale_level=0, purchase_scale_level=1,
                    demand_scale_level=1, network=network, demand=demand_dict, label='scenario')


problem = formulate(scenario=scenario, constraints={Constraints.COST, Constraints.TRANSPORT,
                                                    Constraints.RESOURCE_BALANCE, Constraints.PRODUCTION,
                                                    Constraints.INVENTORY, Constraints.RESOURCE_BALANCE},
                    objective=Objective.COST)

results = solve(scenario=scenario, instance=problem, solver='gurobi', name='LP')