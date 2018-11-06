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
    def __init__(self, N):
        self.num_agents = N
        self.width = 100
        self.height = 100
        self.grid = ContinuousSpace(self.width, self.height, torus=True)
        self.schedule = RandomActivation(self)
        self.timeCurrent = 0.

        # Create agents
        for i in range(self.num_agents):
            a = EfscapeAgent(i, self)
            self.schedule.add(a)
            x = random.randrange(3, self.grid.width - 3)
            y = random.randrange(3, self.grid.height - 3)
            pos = (x,y)
            self.grid.place_agent(a, pos)


    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.timeCurrent += 1.0
        print(self.timeCurrent)