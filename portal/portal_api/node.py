
from django.db import models
from django.forms import JSONField
from django.contrib.auth.models import User

class Question (models.Model):

    '''Create a model to represent each question node in the directed graph. This model should include fields such as:'''
    question_text = models.CharField
    options = JSONField
    is_multiple_choice = models.BooleanField #(indicating single or multiple-choice question.)

class Option(models.Model):

    '''If options for questions are complex and require additional information'''
    text = models.CharField
    is_correct = models.BooleanField
    score = models.IntegerField

class Batch (models.Model):

    '''Create a model to represent a batch of questions.'''
    nam = models.CharField()
    root_question = models.ForeignKey(Question)
    max_questions = models.IntegerField


class UserProgress(models.Model):

    '''Create a model to track a user's progress through the assessment.'''
    user = models.ForeignKey(User)
    current_batch = models.ForeignKey(Batch)
    last_answered_question = models.ForeignKey(Option)
    
    
class UserAnswer (models.Model):

    '''Create a model to store user answers.'''
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    selected_options = JSONField
