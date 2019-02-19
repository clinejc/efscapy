import random
import logging

from mesa.visualization.ModularVisualization import ModularServer
from .model import EfscapeAgent, EfscapePatch, EfscapeModel
from .SimpleContinuousModule import SimpleCanvas

logging.basicConfig(level=logging.INFO)

def agent_draw(agent):
    ''' Draws agents '''
    portrayal = None
    if agent is None:
        pass
    elif (isinstance(agent,EfscapeAgent)):
        print("Uid: {0}".format(agent.unique_id))
        portrayal = {"Shape": "circle",
                    "Color": "red",
                    "Filled": "true",
                    "Layer": 0,
                    "r": 3}
        return portrayal
    elif (isinstance(agent,EfscapePatch)):
        print("Uid: {0}".format(agent.unique_id))
        w = 1/agent.model.ncols
        h = 1/agent.model.nrows
        portrayal = {"Shape": "rect",
                    "Color": "black",
                    "Filled": False,
                    "Layer": 0,
                    "w": w,
                    "h": h}
        return portrayal

efscape_canvas = SimpleCanvas(agent_draw, 500, 500)

model_params = {
    "paramsFileName": "ef_relogo.zombie.json",
    "N": 100,
    "width": 100,
    "height": 100
}

def launch_efscape_model():
    logging.info("Running an efscape model...")

    server = ModularServer(EfscapeModel, [efscape_canvas], "Efscape Model",
                           model_params)
    server.max_steps = 0
    server.port = 8521
    server.launch()

    #model = EfscapeModel(num_agents)
    #for i in range(10): 
    #    model.step()

if __name__ == "__main__":
    random.seed(3)
    launch_efscape_model()
