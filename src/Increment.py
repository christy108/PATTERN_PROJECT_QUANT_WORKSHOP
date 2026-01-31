class Increment:
    def __init__(self, direction, returns, weights):
        self.direction = direction
        self.returns = returns
        self.weights = weights

    def get_direction(self):
        return self.direction
    
    def get_returns(self):
        return self.returns
    
    def get_weights(self):
        return self.weights
