from django.forms import ModelForm
from .models import Requirements_list, Members, Grades, Requirements, Allowances



class MembersForm(ModelForm):
    class Meta:
        model = Members
        fields = '__all__'

class GradesForm(ModelForm):
    class Meta:
        model = Grades
        fields = '__all__'  

class ReqsForm(ModelForm):
    class Meta:
        model = Requirements
        fields = '__all__' 

class ReqsListForm(ModelForm):
    class Meta:
        model = Requirements_list
        fields = '__all__'

class AllowanceForm(ModelForm):
    class Meta:
        model = Allowances
        fields = '__all__'
