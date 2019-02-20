from mesa.visualization.ModularVisualization import VisualizationElement
from .model import EfscapeModel


class SimpleCanvas(VisualizationElement):
    local_includes = ["efscapy/simple_continuous_canvas.js"]
    portrayal_method = None
    canvas_height = 500
    canvas_width = 500

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        '''
        Instantiate a new SimpleCanvas
        '''
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Simple_Continuous_Module({}, {})".
                       format(self.canvas_width, self.canvas_height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []

        breedPortrayals = {}
        if 'visualization' in model.info:
            viz = model.info["visualization"]
            print(viz)
            for key, value in model.breeds.items():
                breedPortrayals[value] = viz[key]

        else:
            print("visualization not found")
            print(model.info)
            if 'description' not in model.info:
                print("Something is wrong")

        print(breedPortrayals)

        for obj in model.turtles:
            # portrayal = breedPortrayals[obj["type"]]
            portrayal = {#"Shape":"circle",
                    "Filled": "true",
                    "Layer": 0}

            portrayal["Shape"] = breedPortrayals[obj["type"]]["Shape"]
            portrayal["Color"] = breedPortrayals[obj["type"]]["Color"]
            portrayal["r"] = breedPortrayals[obj["type"]]["r"]

            # translate coordinates
            x = obj["xCor"] - model.min_x + 1
            y = model.max_y - obj["yCor"] - 1

            x = ((x - model.space.x_min) /
                 (model.space.x_max - model.space.x_min))
            y = ((y - model.space.y_min) /
                 (model.space.y_max - model.space.y_min))
            portrayal["x"] = x
            portrayal["y"] = y
            space_state.append(portrayal)
        
        print(model.breeds)

        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)
            x, y = obj.pos
            x = ((x - model.space.x_min) /
                 (model.space.x_max - model.space.x_min))
            y = ((y - model.space.y_min) /
                 (model.space.y_max - model.space.y_min))
            portrayal["x"] = x
            portrayal["y"] = y
            space_state.append(portrayal)

        return space_state
