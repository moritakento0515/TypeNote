from django import forms
from .models import Score, TargetScore, UserProfile

#検索フォーム
#class SearchForm(forms.Form):
    #search = forms.CharField(label='Search', max_length=100)

#プロフィール編集フォーム   
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'bio']
        
#スコア登録フォーム
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('score','score_type',)

#目標スコア設定フォーム
class TargetScoreForm(forms.ModelForm):
   class Meta:
        model = TargetScore
        fields = ('target_score', 'score_type', )
   
