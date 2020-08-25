from typing import List

class Cluster:
    """ Will be used to store information about extracted cluster"""
    def __init__(self, ids: List[int], central_features: List[str]):
        self.ids = ids
        self.central_features = central_features
