from math import log
from java_random import Random

class RandomGenerator:
	def __init__(self, seed, arrival_rate_constant, service_rate_constant):
		self.arrival_rng = Random(seed)
		self.service_rng = Random(seed + 1)
		self.arrival_rate_constant = arrival_rate_constant
		self.service_rate_constant = service_rate_constant

	def generate_inter_arrival_time(self):
		return -log(self.arrival_rng.nextDouble()) / self.arrival_rate_constant

	def generate_service_time(self):
		return -log(self.service_rng.nextDouble()) / self.service_rate_constant
