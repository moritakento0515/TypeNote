from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
from django.urls import reverse


from .models import Score, ScoreType, TargetScore, Community, CommunityMember, UserProfile
from .forms import ScoreForm ,TargetScoreForm ,ProfileForm



#////////////////////////////////////////////////////////////////////////////////////////////////
#ユーザープロフィールを表示するビュー
@login_required
def profile_view(request):
    # ログインユーザーのプロフィールを取得
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    # 所属しているコミュニティ（CommunityMember経由）を取得
    communities = CommunityMember.objects.filter(user=request.user)
    
    context = {
        'profile': profile,
        'communities': communities,
    }
    return render(request, 'tracker/profile_view.html', context)

@login_required
def profile_edit(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('tracker:profile_view')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
    }
    return render(request, 'tracker/profile_edit.html', context)





#////////////////////////////////////////////////////////////////////////////////////////////////
#ユーザーのスコア一覧を表示するビュー
#ログインしていない状態でアクセスすると、ログインページにリダイレクトされる←すごい\
@login_required
def user_scores(request):
    # GETパラメータから score_type_id を取得
    score_type_id = request.GET.get("score_type_id")
    if score_type_id:
        score_type = get_object_or_404(ScoreType, id=score_type_id)
    else:
        score_type = ScoreType.objects.first()  # デフォルトのScoreType（例: 3000円のもの）
        
    # すべてのスコア種類を取得して、ドロップダウンに利用する
    # 対象のスコア種類でフィルタ
    all_score_types = ScoreType.objects.all()
    filtered_scores = Score.objects.filter(user=request.user, score_type=score_type)
    
    # ユーザーの全スコアから最高スコアを取得
    # ユーザーの直近20件のスコアを取得（降順）
    # ユーザーの最新スコアを取得（降順で1件）
    best_score = filtered_scores.aggregate(Max('score'))['score__max'] or 0
    recent_scores = filtered_scores.order_by('-timestamp')[:20]
    latest_score = filtered_scores.order_by('-timestamp').first()
    
    # TargetScore から、対象ユーザーとスコア種類の目標スコアを取得
    target_obj = TargetScore.objects.filter(user=request.user, score_type=score_type).first()
    target_score = target_obj.target_score if target_obj else 3000
    
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
          
    # 最新のスコアが目標スコアを超えているかどうかでメッセージを変更        
    message = '今日も頑張りましょう！'
    if latest_score and latest_score.score >= target_score:
        message = '次の目標を設定しよう！'

    context = {
        'message': message ,
        'scores': recent_scores,
        'best_score': best_score,
        'target_score': target_score,
        'score_type': score_type,
        'score_types': all_score_types,
    }
    return render(request, 'tracker/user_scores.html', context)

#ログインユーザーのスコア履歴データをJSONで返すビュー
@login_required
def score_history(request):
    # GETパラメータから score_type_id を取得
    score_type_id = request.GET.get("score_type_id")
    if score_type_id:
        score_type = get_object_or_404(ScoreType, id=score_type_id)
        # ユーザーのスコアを時系列（timestamp昇順）に取得
        scores = Score.objects.filter(user=request.user, score_type=score_type).order_by('timestamp')
    else:
        scores = Score.objects.filter(user=request.user).order_by('timestamp')
        score_type = None
    
    # 対象のスコア種類でフィルタ
    #scores = Score.objects.filter(user=request.user, score_type=score_type).order_by('timestamp')
    
    target_obj = TargetScore.objects.filter(user=request.user, score_type=score_type).first()
    target_score = target_obj.target_score if target_obj else 3000
    
    data = {
        #"2025-02-08 11:37:21" のような形の文字列に変換し、JSONで送信するためにリストに格納
        'timestamps': [score.timestamp.strftime('%Y-%m-%d %H:%M:%S') for score in scores],
        'scores': [score.score for score in scores],
        "target_score": target_score,
    }
    return JsonResponse(data)



#////////////////////////////////////////////////////////////////////////////////////////////////
#新規スコア追加フォームを表示
@login_required
def new_score(request):
    #スコア登録フォームを作成
    scoreForm = ScoreForm()
    #テンプレートに渡すデータを作成
    context = {
        'message' : 'スコアを登録してください',
        'scoreForm': scoreForm
        }
    return render(request, 'tracker/new_score.html', context)

#新規スコア追加フォームの入力内容を受け取り、データベースに保存するビュー
@login_required
def new_score_create(request):
    if request.method == 'POST':
        scoreForm = ScoreForm(request.POST)
        if scoreForm.is_valid():
            score = scoreForm.save(commit=False)
            score.user = request.user
            score.save()
            # スコアのスコアタイプIDをGETパラメータとして付与してリダイレクト
            return redirect(f'{reverse("tracker:user_scores")}?score_type_id={score.score_type.id}')
        else:
            return render(request, 'tracker/new_score.html', {'scoreForm': scoreForm,})

#////////////////////////////////////////////////////////////////////////////////////////////////
#目標スコア登録フォームを表示
@login_required
def new_target_score(request):
    #スコア登録フォームを作成
    targetScoreForm = TargetScoreForm()
    #テンプレートに渡すデータを作成S
    context = {
        'message' : '目標スコアを設定してください',
        'targetScoreForm': targetScoreForm
        }
    
    return render(request, 'tracker/new_target_score.html', context)


#目標スコア登録フォームの入力内容を受け取り、データベースに保存するビュー
@login_required
def new_target_score_create(request):
    if request.method == 'POST':
        targetScoreForm = TargetScoreForm(request.POST)
        if targetScoreForm.is_valid():
            # score_type をフォームから取得
            score_type = targetScoreForm.cleaned_data['score_type']
            target_score_value = targetScoreForm.cleaned_data['target_score']
            # 既存のレコードがあれば取得、なければ作成
            targetScore, created = TargetScore.objects.get_or_create(
                user=request.user,
                score_type=score_type,
                defaults={'target_score': target_score_value}
            )
            if not created:
                # 既に存在している場合は更新
                targetScore.target_score = target_score_value
                targetScore.save()
            return redirect(f'{reverse("tracker:user_scores")}?score_type_id={score_type.id}')
        else:
            return render(request, 'tracker/new_target_score.html', {'targetScoreForm': targetScoreForm,})


#////////////////////////////////////////////////////////////////////////////////////////////////
#スコアランキングを表示するビュー
@login_required
def community_score_ranking(request):
    communities = Community.objects.all()
    score_types = ScoreType.objects.all()

    community_id = request.GET.get("community")
    score_type_id = request.GET.get("score_type")

    ranking = []
    community = None
    score_type = None

    if community_id and score_type_id:
        community = get_object_or_404(Community, id=community_id)
        score_type = get_object_or_404(ScoreType, id=score_type_id)

        community_members = CommunityMember.objects.filter(community=community).values_list("user", flat=True)

        ranking = (
            Score.objects.filter(user__in=community_members, score_type=score_type)
            .values("user__id", "user__username", "user__userprofile__nickname")
            .annotate(best_score=Max("score"))
            .order_by("-best_score")
        )

        ranked_list = []
        last_score = None
        rank = 0
        for index, entry in enumerate(ranking, start=1):
            if last_score != entry["best_score"]:
                rank = index
            last_score = entry["best_score"]
            ranked_list.append({
                "rank": rank,
                "user_id": entry["user__id"],
                "nickname": entry["user__userprofile__nickname"] or entry["user__username"],
                "best_score": entry["best_score"],
            })

        ranking = ranked_list

    context = {
        'communities': communities,
        'score_types': score_types,
        'selected_community_id': int(community_id) if community_id else None,
        'selected_score_type_id': int(score_type_id) if score_type_id else None,
        'community': community,
        'score_type': score_type,
        'ranking': ranking,
    }
    return render(request, 'tracker/community_score_ranking.html', context)