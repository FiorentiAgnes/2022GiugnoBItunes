from model.model import Model

myModel = Model()
myModel.buildGraph(4500)
nodi, archi= myModel.getGraphDetails()
print(f"nodi: {nodi}, archi: {archi}")