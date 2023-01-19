from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        """这个内置类告诉django根据哪个模型创建表单以及在表单中包含那些字段"""
        model = Topic
        fields = ['text']
        labels = {'text':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':''}
        widgets = {'text':forms.Textarea(attrs={'cols': 80})}


