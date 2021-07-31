from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

# テンプレート内のhtmlファイルでpostsを記述すると上記post_list()で指定したクエリセットを呼び出せる


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    # ブログページの右上にある+マークをクリックすると記事を新しく作るためpost_edit.htmlへ遷移する
    # post_edit.thmlはviews.pyのpost_newを参照する
    # 遷移するとまず、投稿フォームには何も書かれていないのでif分岐は必ずelseを選択する
    # Saveボタンを押すとrequest.POSTにデータが送信されるのでform = PostForm(request.POST)がそれを受けてコードが進む
    # if分岐はif form.is_valid():へ進む
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # commit=False とすることでこの時点ではまだ保存しない
            post.author = request.user
            post.published_date = timezone.now()
            # post へ author と published_date を save するために追加する
            post.save()
            # ここですべてを保存する
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    # 1.get_object_...はpkを参照して既存の記事を取得する
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        # 3.編集終わった記事をrequest.POSTで取得してヴァリデーションへ進む
        if form.is_valid():
            # 4.記事を書き替えたらヴァリデーションを受けて同じpkの記事へ上書き保存
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 2.既存の記事をPostFormに引数として渡してページに表示する
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

    