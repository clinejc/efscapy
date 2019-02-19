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

        id2portrayal = {}
        if 'visualization' in model.info:
            viz = model.info["visualization"]
            print(viz)
            for key, value in model.breeds.items():
                id2portrayal[value] = viz[key]

        else:
            print("visualization not found")
            print(model.info)
            if 'description' not in model.info:
                print("Something is wrong")

        print(id2portrayal)

        for obj in model.turtles:
            portrayal = {"Shape": "circle",
                    "Color": "red",
                    "Filled": "true",
                    "Layer": 0,
                    "r": 3}
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
