from django.contrib import admin
from .models import Question,Choice

class ChoiceInline(admin.StackedInline):
    """ Allows for answers to be  added when questions get created in the same screen"""
    model=Choice#What's the model you want to add? 
    extra=3 #how many answers/choice by defautl do you want to add?

class QuestionAdmin(admin.ModelAdmin):
    """modifies the order of the model as seen in admin"""
    fields=['pub_date', 'question_text']
    """with this change, the order of the fields in admin get changed so that pub_date appears first to the user"""
    #connecting both classes so that new answers are created for each question
    inlines=[ChoiceInline]#this attribute is a list with as many Classes I want to connect to this one class, 1 in this case
    list_display=("question_text","pub_date","was_published_recently")
    list_filter=['pub_date']
    search_fields=['question_text']
# Register your models here.
admin.site.register(Question,QuestionAdmin  )
admin.site.register(Choice)
