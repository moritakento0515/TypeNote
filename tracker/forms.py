from django import forms
from .models import Score,UserProfile

#検索フォーム
#class SearchForm(forms.Form):
    #search = forms.CharField(label='Search', max_length=100)
    
#スコア登録フォーム
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('score',)

#目標スコア設定フォーム
class TargetScoreForm(forms.ModelForm):
   class Meta:
        model = UserProfile
        fields = ('target_score',)
      