from math import log
from java_random import Random

class RandomGenerator:
	def __init__(self, seed, arrival_rate_constant, service_rate_constant, resting_rate_constant):
		self.arrival_rng = Random(seed)
		self.service_rng = Random(seed + 1)
		self.rest_rng = Random(seed + 2)
		self.rest_period_rng = Random(seed + 3)
		self.customer_type_rng = Random(seed + 4)

		self.arrival_rate_constant = arrival_rate_constant
		self.service_rate_constant = service_rate_constant
		self.resting_rate_constant = resting_rate_constant

	def generate_inter_arrival_time(self):
		return -log(self.arrival_rng.nextDouble()) / self.arrival_rate_constant

	def generate_service_time(self):
		return -log(self.service_rng.nextDouble()) / self.service_rate_constant

	def generate_resting_status(self):
		return self.rest_rng.nextDouble()

	def generate_resting_time(self):
		return -log(self.rest_period_rng.nextDouble()) / self.resting_rate_constant

	def generate_customer_type(self):
		return self.customer_type_rng.nextDouble()

