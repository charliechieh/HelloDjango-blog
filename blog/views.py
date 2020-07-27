from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag
import markdown, re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView

from pure_pagination.mixins import PaginationMixin


# Create your views here.
# user ListView
class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 分页功能，其值代表每一页包含多少文章
    paginate_by = 6


class PostDetailView(DetailView):
    """进入文章页"""
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是实现文章被访问一次，阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # self.object 的值就是被访问的文章 post

        self.object.increase_views()
        # 试图必须返回一个 Response 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
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
        return post


class ArchivesView(IndexView):
    """点击归档跳转"""
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)


class CategoryView(IndexView):
    """点击分类跳转"""
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    """点击分类跳转"""
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)
