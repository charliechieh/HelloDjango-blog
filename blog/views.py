from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
import markdown, re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


# Create your views here.
def index(request):
    """主页"""
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    """进入文章页"""
    post = get_object_or_404(Post, pk=pk)
    # 将正文做markdown转html处理
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 美化标题的锚点
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    # re.S 将toc作为一整个字符串匹配，不逐行匹配
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    # group(1) 返回第一个()中匹配的字符串
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})


def archives(request, year, month):
    """点击归档跳转"""
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    """点击分类跳转"""
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    """点击分类跳转"""
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)
    return render(request, 'blog/index.html', context={'post_list': post_list})
