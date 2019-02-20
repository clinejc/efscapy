import random
from mesa.space import ContinuousSpace, MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation

import sys
import os
import Ice
from pathlib import Path
import json

# 1. set the path of the 'efscape' slice defitions
efscape_slice_dir = Path(os.environ['EFSCAPE_PATH']) / 'src/slice'

# 2. generate the python stubs for 'efscape'
Ice.loadSlice('-I' + str(efscape_slice_dir) + ' --all ' + str(efscape_slice_dir / 'efscape/ModelHome.ice'))

# 3. import efscape python API
import efscape

class EfscapeAgent(Agent):
    """ An agent that represents an Efscape entity."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class EfscapePatch(Agent):
    """ An agent that represents a patch. """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class EfscapeModel(Model):
    """A model with some number of agents from an Efscape simulation.
    """
    def __init__(self, paramsFileName, N=1, width=500, height=500):
        # set the default model parameter file name
        self.paramsFileName = paramsFileName

        # Connect to efscape zeroc-ice proxy
        efscape_config_path = Path(os.environ['EFSCAPE_PATH']) / 'src/server/config.client'
        self.communicator = Ice.initialize(sys.argv, str(efscape_config_path))

        # connect to modelHome
        modelHome = efscape.ModelHomePrx.checkedCast(
        self.communicator.propertyToProxy('ModelHome.Proxy').ice_twoway().ice_secure(False))
        if not modelHome:
            print("invalid proxy")
            sys.exit(1)

        print("ModelHome accessed successfully!")

        # open the model parameter file
        f = open(str(Path(os.environ['EFSCAPE_HOME']) / paramsFileName), 'r')
        paramsString = f.read()

        # create a model instance from the parameters
        self.model = modelHome.createFromParameters(paramsString)

        if not self.model:
            print('Invalid mode proxy!')
            sys.exit(1)

        print('model successfully created!')

        # now retrieve model meta data
        parameters = json.loads(paramsString)
        self.info = parameters
        if 'properties' not in parameters:
            print('Missing <properties>!')
            sys.exit(1)
        
        # get dimensions
        self.max_x = parameters['properties']['max.x']
        self.min_x = parameters['properties']['min.x']
        self.max_y = parameters['properties']['max.y']
        self.min_y = parameters['properties']['min.y']

        self.num_agents = N
        self.width = self.max_x - self.min_x + 1 #width
        self.height = self.max_y - self.min_y + 1 #height
        print('width=' + str(self.width))
        print('height=' + str(self.height))
        self.nrows = 10
        self.ncols = 10
        self.space = ContinuousSpace(self.width, self.height, torus=True)
        self.schedule = RandomActivation(self)
        self.currentTick = 0.

        self.simulator = modelHome.createSim(self.model)

        if not self.simulator:
            print('Invalid simulator proxy!')
            sys.exit(1)

        print('simulator created!')

        if self.simulator.start():
            print('simulator started!')
        else:
            print('simulator failed to start!')

        # attempt to load messages
        self.loadMessages()

        t = 0
        if len(self.turtles) == 0:
            t = self.simulator.nextEventTime()
            self.simulator.execNextEvent()
            self.loadMessages()
            print('start time = ' + str(t))
            print('Model currentTick = ' + str(self.currentTick))

        self.running = not self.simulator.halt()
        print('number of agents = ' + str(len(self.turtles)))

        # Create agents
        cnt = 0
        pwidth = self.width/self.ncols
        pheight = self.height/self.nrows
        # for i in range(self.ncols):
        #     for j in range(self.nrows):
        #         p = EfscapePatch(cnt, self)
        #         x = pwidth * (0.5 + i)
        #         y = pheight * (0.5 + j)
        #         pos = (x,y)
        #         self.space.place_agent(p, pos)
        #         self.schedule.add(p)
        #         cnt = cnt + 1

        # for i in range(cnt, self.num_agents + cnt):
        #     x = self.random.random() * self.space.x_max
        #     y = self.random.random() * self.space.y_max
        #     pos = (x,y)
        #     a = EfscapeAgent(i, self)
        #     self.space.place_agent(a, pos)
        #     self.schedule.add(a)

    def __del__(self):
        print('Model died')
        self.communicator.destroy()

    def loadMessages(self):
        '''
        Retrieves turtles from the following output ports:

        * turtles: list of all turtles
        * breeds: map of all breeds to type ids
        * currentTick: current simulation time
        '''
        message = self.model.outputFunction()
        print('message size = ' + str(len(message)))
        self.breeds = {} # (re-)initialize breed list
        self.turtles = [] # (re-)initialize turtle set
        for x in message:
            if x.port == 'turtles':
                self.turtles = json.loads(x.valueToJson)
            elif x.port == 'breeds':
                self.breeds = json.loads(x.valueToJson)
            elif x.port == 'currentTick':
                self.currentTick = json.loads(x.valueToJson)

    def step(self):
        '''Advance the model by one step.'''
        self.running = not self.simulator.halt()
        if self.running:
            self.schedule.step()
            t = self.simulator.nextEventTime()
            self.simulator.execNextEvent()
            self.loadMessages()
            print('Client event time = ' + str(t))
            print('Model currentTick = ' + str(self.currentTick))
