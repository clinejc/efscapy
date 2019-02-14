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
    """A model with some number of agents from an Efscape simulation."""
    def __init__(self, N=1, width=500, height=500):
        self.num_agents = N
        self.width = width
        self.height = height
        self.nrows = 10
        self.ncols = 10
        self.space = ContinuousSpace(self.width, self.height, torus=True)
        self.schedule = RandomActivation(self)
        self.timeCurrent = 0.

        # Connect to efscape proxy
        efscape_config_path = Path(os.environ['EFSCAPE_PATH']) / 'src/server/config.client'
        self.communicator = Ice.initialize(sys.argv, str(efscape_config_path))

        # connect to modelHome
        modelHome = efscape.ModelHomePrx.checkedCast(
        self.communicator.propertyToProxy('ModelHome.Proxy').ice_twoway().ice_secure(False))
        if not modelHome:
            print("invalid proxy")
            sys.exit(1)

        print("ModelHome accessed successfully!")

        parmName = 'ef_relogo.zombie.json'
        f = open(str(Path(os.environ['EFSCAPE_HOME']) / parmName), 'r')
        parmString = f.read()

        model = modelHome.createFromParameters(parmString)

        if not model:
            print('Invalid mode proxy!')
            sys.exit(1)

        print('model successfully created!')

        simulator = modelHome.createSim(model)

        if not simulator:
            print('Invalid simulator proxy!')
            sys.exit(1)

        print('simulator created!')

        if simulator.start():
            print('simulator started!')
        else:
            print('simulator failed to start!')

        # Create agents
        cnt = 0
        pwidth = self.width/self.ncols
        pheight = self.height/self.nrows
        for i in range(self.ncols):
            for j in range(self.nrows):
                p = EfscapePatch(cnt, self)
                x = pwidth * (0.5 + i)
                y = pheight * (0.5 + j)
                pos = (x,y)
                self.space.place_agent(p, pos)
                self.schedule.add(p)
                cnt = cnt + 1

        for i in range(cnt, self.num_agents + cnt):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = (x,y)
            a = EfscapeAgent(i, self)
            self.space.place_agent(a, pos)
            self.schedule.add(a)


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.timeCurrent += 1.0
        print(self.timeCurrent)
