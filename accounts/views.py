from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

#サインアップはログインなどとは異なり自分でviewを作成する
#勤務地や会社名など使用者に合わせてフォームが変わるから
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # ログイン済みならuser_scoresへリダイレクト
            return redirect('tracker:user_scores')
        return super().dispatch(request, *args, **kwargs)