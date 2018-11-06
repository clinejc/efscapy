import random
import logging

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from .model import EfscapeModel

logging.basicConfig(level=logging.INFO)

def launch_efscape_model():
    logging.info("Running an efscape model...")
    model = EfscapeModel(10)
    for i in range(10): 
        model.step()

if __name__ == "__main__":
    random.seed(3)
    launch_efscape_model()
