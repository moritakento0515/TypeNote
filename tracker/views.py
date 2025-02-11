from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from .models import Score ,UserProfile
from .forms import ScoreForm ,TargetScoreForm
from django.db.models import Max
import json
from django.http import JsonResponse


#ユーザーのスコア一覧を表示するビュー
#ログインしていない状態でアクセスすると、ログインページにリダイレクトされる←すごい
@login_required
def user_scores(request):
    # ユーザーの全スコアから最高スコアを取得
    best_score = Score.objects.filter(user=request.user).aggregate(Max('score'))['score__max'] or 0

    # ユーザーの直近20件のスコアを取得（降順）
    recent_scores = Score.objects.filter(user=request.user).order_by('-timestamp')[:20]

    # ユーザーの目標スコアを取得
    target_score = UserProfile.objects.get(user=request.user).target_score

    # 各スコアに対して、目標スコアとの差分と符号を計算して追加
    for score in recent_scores:
        diff = score.score - target_score 
        score.diff = diff  # 数値としての差分
        # 符号の判定
        if diff > 0:
            score.diff_sign = "positive"
        elif diff < 0:
            score.diff_sign = "negative"
            score.diff = abs(diff)
        else:
            score.diff_sign = "zero"
            
        message = '今日も頑張りましょう！'
        if best_score >= target_score:
            message = '次の目標を設定しよう！'

    context = {
        'message': message ,
        'scores': recent_scores,
        'best_score': best_score,
        'target_score': target_score,
    }
    return render(request, 'tracker/user_scores.html', context)



#新規スコア追加フォームを表示
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

#フォームの入力内容を受け取り、データベースに保存するビュー
@login_required
def create(request):
    if request.method == 'POST':
        scoreForm = ScoreForm(request.POST)
        if scoreForm.is_valid():
            score = scoreForm.save(commit=False)
            score.user = request.user
            score.save()
            return redirect('tracker:user_scores')
        else:
            return render(request, 'tracker/new.html', {'scoreForm': scoreForm,})


#目標スコア登録フォームを表示
@login_required
def register(request):
    #スコア登録フォームを作成
    targetForm = TargetScoreForm()
    #テンプレートに渡すデータを作成
    context = {
        'message' : '目標スコアを設定してください',
        'targetForm': targetForm
        }
    return render(request, 'tracker/target_score.html', context)


#ターゲットスコアのフォームの表示とデータの保存を処理するビュー
@login_required
def target_score(request):

    if request.method == 'POST':
        #フォームを生成するときに、既存のプロフィールインスタンスを渡す
        targetForm = TargetScoreForm(request.POST)
        if targetForm.is_valid():
            # ユーザーのプロフィールを取得、存在しなければ新たに作成
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            # フォームから送信されたtarget_scoreで更新
            user_profile.target_score = targetForm.cleaned_data['target_score']
            user_profile.save()
            return redirect('tracker:user_scores')
        else:
            targetForm = TargetScoreForm()

            return render(request, 'tracker/target_score.html', {'targetForm': targetForm})



#ログインユーザーのスコア履歴データをJSONで返すビュー
@login_required
def score_history(request):
    # ユーザーのスコアを時系列（timestamp昇順）に取得
    scores = Score.objects.filter(user=request.user).order_by('timestamp')
    
    data = {
        #"2025-02-08 11:37:21" のような形の文字列に変換し、JSONで送信するためにリストに格納
        'timestamps': [score.timestamp.strftime('%Y-%m-%d %H:%M:%S') for score in scores],
        'scores': [score.score for score in scores],
    }
    return JsonResponse(data)


#チャートを表示するビュー
@login_required
def score_history_page(request):
    return render(request, 'tracker/score_history.html')