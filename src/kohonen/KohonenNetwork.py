from random import random
from math import exp

class Neuron:
    
    def __init__(self, num_inputs, row, column, learning_rate, effective_width, tau):
        self.weights = [random() for i in range(num_inputs)]
        self.row = row
        self.column = column
        self._learning_rate = learning_rate
        self.effective_width = effective_width
        self.tau = tau
        self.recognized_pattern = 0
        
    def euclidean_distance(self, data):
        distance = 0
        
        for i in range(len(data)-1):
            distance += (data[i] - self.weights[i])**2
            
        return distance
    
    def adjust_weights(self, time, data, lateral_distance):
        for i in range(len(self.weights)):
            self.weights[i] += self.learning_rate(time) * self._topological_neighborhood(lateral_distance, self._effective_width(time)) * (data[i] - self.weights[i]) 
    
    def learning_rate(self, time):
        return self._learning_rate * exp(-time / self.tau)
    
    def _effective_width(self, time):
        return self.effective_width * exp(-time / self.tau)
    
    def _topological_neighborhood(self, l, sigma):
        return exp(- l / (2 * sigma**2))
    
    
    
class Kohonen:
    
    def __init__(self, num_inputs, rows=5, columns=5, learning_rate=0.5, effective_width=2, tau=1000):
        self.neurons = [[Neuron(num_inputs, i, j, learning_rate, effective_width, tau) for j in range(columns)] for i in range(rows)]
        
    def learn(self, times, data_set, define_patterns):
        now = 0
        
        print 'Aprendizado iniciado.'
        
        while now < times:
            print 'Aprendizado iteracao '+str(now)
            for data in data_set:
                self._adjust_weights(now, self.find_winner(data), data)
                
            now += 1

        print 'Aprendizado finalizado!\n'
        
        define_patterns(self, data_set)
                    
    def test(self, data):
        return self.find_winner(data).recognized_pattern
        
    def find_winner(self, data):
        winner = self.neurons[0][0]
        winner_distance = winner.euclidean_distance(data)
        
        for i in range(len(self.neurons)):
            for j in range(len(self.neurons[i])):
                distance = self.neurons[i][j].euclidean_distance(data)
                
                if winner_distance > distance and self.neurons[i][j].recognized_pattern != None:
                    winner_distance = distance
                    winner = self.neurons[i][j]
        
        return winner
    
    def _adjust_weights(self, time, winner, data):
        for i in range(len(self.neurons)):
            for j in range(len(self.neurons[i])):
                self.neurons[i][j].adjust_weights(time, data, self._lateral_distance(winner, self.neurons[i][j]))
                
    def _lateral_distance(self, winner, neuron):
        return (winner.row - neuron.row)**2 + (winner.column - neuron.column)**2
    
if __name__ == '__main__':
    import sys
    
    print >> sys.stderr, 'No main defined for this module.'
