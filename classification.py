import numpy as np
import math
from random import uniform
from pearson import pearson
sigma=0.3

def PNN(input_layer, output_layer):
    input_layer, output_layer = np.array(input_layer), np.array(output_layer)
    letters = list(set(output_layer))
    pattern_layer = np.zeros(len(x))
    w1 = input_layer
    w2 = np.zeros((len(input_layer), len(letters)))
    for i, yi in enumerate(letters):
        index = np.where(output_layer == yi)
        w2[index, i] = 1 / len(output_layer[index])
    def result(input_data):
        for i, learn_data in enumerate(w1):
            pattern_layer[i] = np.sum(np.exp(-(learn_data - input_data) ** 2 / sigma ** 2))
        summation_layer = np.dot(pattern_layer, w2)
        output_layer = letters[np.argmax(summation_layer)]
        return output_layer

    return result
x = ([[]]*10000)
y = []
for i in range(len(x)):
        x[i] = [(uniform(18, 100)), (uniform(0, 10)),]
length = len(x)
for i in range(length):
    y.append((uniform(300, 2000)))

output = PNN(x, y)

a = [25, 5 ]
print(output(a))
pearson_res= math.fabs(pearson(x[0],y)*100)