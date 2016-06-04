from django import forms

from apps.grader_core.models import Scenario


class ScenarioModelForm(forms.ModelForm):

    class Meta:
        model = Scenario
        exclude = []
