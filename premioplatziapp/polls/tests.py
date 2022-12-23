import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question




# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently returns False for questions whose pub_date is in the future"""
        time=timezone.now()+datetime.timedelta(days=30)
        future_question=Question(question_text='Quién es el mejor Course Director de Platzi',pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)
    
    def test_was_published_recently_with_present_questions(self):
        time=timezone.now()
        present_question=Question(question_text='Quién es el mejor Course Director de Platzi',pub_date=time)
        self.assertIs(present_question.was_published_recently(),True)
        
    def test_was_published_recently_with_past_questions(self):
        time=time=timezone.now()-datetime.timedelta(days=30)
        past_question=Question(question_text='Quién es el mejor Course Director de Platzi',pub_date=time)
        self.assertIs(past_question.was_published_recently(),False)
        
def create_question(question_text, days):
    """
    Create a question with the given question_text and published the number of 
    days offset to now (negative for questions published in the past, positive  for questions
    that have yet to be published)
    
    """    
    time = timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)


        
class QuestionIndexViewTests(TestCase):
    
    
    def test_no_questions(self):
        """if no questions exists, an appropiate message is displayed."""
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains('No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])    
    
    def test_future_questions(self):
        """"pass"""
        create_question('future question',days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertContains(response,'No polls are available')
        self.assertQuerysetEqual(response.content['latest_question_list'],[])
    
    def test_past_questions(self):
        question= create_question('past question',days=-10)
        response=self.client.get(reverse('polls:index'))        
        self.assertQuerysetEqual(response.content['latest_question_list'],[question])
        
    def test_future_question_and_past_question(self):
        """even if both past and future questions exist, only past questions are displayed."""
        past_question=create_question(question_text='past question', days=-30)
        future_question=create_question(question_text='future question', days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
            [past_question]
        )
        
        def test_two_past_questions(self):
            """
        the questions index page may display multiple questions
        """
        past_question1=create_question(question_text='past question1', days=-30)
        past_question2=create_question(question_text='past question2', days=-40)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question1,past_question2]
            )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """the detail view of a question with a pub_date in the future returns a 404 error , not found"""
        future_question=create_question('future question',days=30)
        url=reverse('polls:detail',args=(future_question.id,))
        response=self.self.client.get(url)
        self.assertEqual(response.status_code,404)
    
    def test_past_question(self): 
        """the detail view of a question with a pub_date in the past , returns the text"""
        past_question=create_question('future question',days=-30)
        url=reverse('polls:detail',args=(past_question.id,))
        response=self.self.client.get(url)
        self.assertContains(response,past_question.question_text)
        
        
        
        
        
