import plotly.plotly as py
import plotly.graph_objs as go
import math

n = 0
p = 100  # number of points
all_x = []
square_y = []

while n < (p + 1):
    x_value = n * 2 * math.pi / p
    all_x.append(x_value)
    square_y.append(math.sin(math.pi*x_value)+
                    (1 / 3.0 * math.sin(3.0 * math.pi * x_value)) +
                    (1 / 5.0 * math.sin(5.0 * math.pi * x_value)) +
                    (1 / 7.0 * math.sin(7.0 * math.pi * x_value)) +
                    (1 / 9.0 * math.sin(9.0 * math.pi * x_value)) +
                    (1 / 11.0 * math.sin(11.0 * math.pi * x_value)) +
                    (1 / 13.0 * math.sin(13.0 * math.pi * x_value)) +
                    (1 / 15.0 * math.sin(15.0 * math.pi * x_value))
                    )
    n += 1

trace0 = go.Scatter(name='Square', mode='line', x=all_x, y=square_y)
data = go.Data([trace0])
py.plot(data, filename='square')
