import random
from mesa.space import ContinuousSpace, MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation

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
