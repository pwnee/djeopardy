from django import forms
from djeo.models import FinalJeopardy


class FinalJeopardyWager(forms.Form):
	"""User enters wager and answer
	"""
	wager = forms.CharField(max_length = 100, required=True)
	correct_answer = forms.CharField(required=True)
	answer = forms.CharField(required=True)
	user = forms.CharField(required=True)

	def is_valid(self):
		return True

	def is_answer_correct(self):
		if self.answer == self.correct_answer:
			return True		
		else:
			return False

	def check_wager(self):
		try:
			wager = int(self.wager)
		except ValueError:
			return False
		return wager
