import policy_explorer
import predictor
import utils
import random
import numpy as np


class explorer(object):
	def __init__(self,state_dim,action_dim,max_action,min_action,discount=0.99,tau=1e-4,rnd=False):

		self.min_action = min_action
		self.max_action = max_action
		self.ddpg = policy_explorer.DDPG_EXPLORER(state_dim, action_dim, max_action, min_action)
		self.rnd = rnd
		if self.rnd:
			# RND
			self.rnd_predictor = predictor.RND_Predictor(state_dim)
			self.rnd_target = predictor.RND_Target(state_dim)
		else:
			# CE
			self.predictor = predictor.Predictor(state_dim,action_dim)
		self.counter = 0

	# TODO: どうやってrnd_targetのoutputをreplay_bufferのbatchを利用して渡す？
	def train(self, replay_buffer, batch_size=64):
		if self.rnd:
			# RND
			return (self.ddpg.train(replay_buffer, batch_size),
					self.rnd_predictor.train(replay_buffer, self.rnd_target, batch_size))
		else:
			# CE
			return (self.ddpg.train(replay_buffer, batch_size),  self.predictor.train(replay_buffer, batch_size))

	def select_action(self, state):
		self.counter += 1
		eps= random.random()
		dec = min(max(0.1,1.0 - float(self.counter)*0.00003),1)
		if eps < dec:
			action = np.random.uniform(self.min_action, self.max_action)
		else:
			action = self.ddpg.select_action(state)
		return action, dec

	def predict(self, state, action):
		if self.rnd:
			# RND
			return self.rnd_predictor.predict(state), self.rnd_target.predict(state)
		else:
			# CE
			return self.predictor.predict(state, action)
