from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from .models import Score
from .forms import ScoreForm
from django.db.models import Max


#ユーザーのスコア一覧を表示するビュー
#ログインしていない状態でアクセスすると、ログインページにリダイレクトされる←すごい
@login_required
def user_scores(request):
    #user_scoreaには、ユーザーが登録したスコア一覧が入る
    user_scores = Score.objects.filter(user=request.user)
    best_score = Score.objects.filter(user=request.user).aggregate(Max('score'))['score__max'] or 0
    #テンプレートに渡すデータを作成
    context = {
        'message': '今日も頑張りましょう',
        'scores': user_scores,
        'best_score': best_score
    }
    #テンプレートを指定して、データを返す
    return render(request, 'tracker/user_scores.html', context)

    
#新規スコア登録ページを表示
@login_required
def new(request):
    #スコア登録フォームを作成
    scoreForm = ScoreForm()
    #テンプレートに渡すデータを作成
    context = {
        'message' : 'スコアを登録してください',
        'scoreForm': scoreForm
        }
    return render(request, 'tracker/new.html', context)


#登録内容をデータベースに保存
@login_required
def create(request):
    if request.method == 'POST':
        scoreForm = ScoreForm(request.POST)
        if scoreForm.is_valid():
            score = scoreForm.save(commit=False)
            score.user = request.user
            score.save()
            return redirect('tracker:user_scores')
    #POST 以外のリクエスト時に scoreForm 変数が定義されず、テンプレートでエラーが発生する可能性があるため、else 節で form 変数を定義しています。
    else:
        scoreForm = ScoreForm()
    return render(request, 'tracker/user_scores.html', {'scoreForm': scoreForm})

#ユーザーのスコアランキングを表示するビュー
