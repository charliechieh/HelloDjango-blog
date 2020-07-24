from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentFrom


# Create your views here.
@require_POST
def comment(request, post_pk):
    """发表评论"""
    # 先获取被评论的文章，若文章不存在，返回404
    post = get_object_or_404(Post, pk=post_pk)
    # 生成一个绑定了用户提交数据的表单
    form = CommentFrom(request.POST)
    # 检查表单是否合法
    if form.is_valid():
        # commit=False 的作用是仅仅利用表单的数据生成一个 Comment 实例，不提交到数据库
        comment = form.save(commit=False)
        # 将评论和文章关联起来
        comment.post = post
        # 现在才执行到保存
        comment.save()

        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        # 重定向到 post 的详情页，实际上当redirect接受一个模型的实例时，它会调用 get_absolute_url 方法
        return redirect(post)
    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
    context = {
        'post': post,
        'form': form
    }
    messages.add_message(request, messages.ERROR, '评论发表失败，请修改表单中的错误后再提交！', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
