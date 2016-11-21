import plotly.plotly as py
import plotly.graph_objs as go
import math

n = 0
p = 100
all_x = []
a_y = []
b_y = []
c_y = []
d_y = []

while n < (p + 1):
    x_value = n * 2 * math.pi / p
    all_x.append(x_value)
    a_y.append(math.sin(x_value))
    b_y.append(math.cos(x_value))
    c_y.append(math.sin(x_value) + math.cos(x_value))
    d_y.append(math.sin(x_value) - math.cos(x_value))
    n += 1

trace0 = go.Scatter(name='Sine', mode='markers', x=all_x, y=a_y)
trace1 = go.Scatter(name='Cosine', mode='lines', x=all_x, y=b_y)
trace2 = go.Scatter(name='Sine+Cosine', mode='lines', x=all_x, y=c_y)
trace3 = go.Scatter(name='Sine-Cosine', mode='lines', x=all_x, y=d_y)
data = go.Data([trace0, trace1, trace2, trace3])
py.plot(data, filename='sine')