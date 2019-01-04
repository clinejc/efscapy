import random
from mesa.space import ContinuousSpace
from mesa import Agent, Model
from mesa.time import RandomActivation

class EfscapeAgent(Agent):
    """ An agent that is represents an Efscape entity."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class EfscapeModel(Model):
    """A model with some number of agents from an Efscape simulation."""
    def __init__(self, N=1, width=200, height=100):
        self.num_agents = N
        self.width = width
        self.height = height
        self.space = ContinuousSpace(self.width, self.height, torus=True)
        self.schedule = RandomActivation(self)
        self.timeCurrent = 0.

        # Create agents
        for i in range(self.num_agents):
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
