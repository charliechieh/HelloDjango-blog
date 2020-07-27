from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    # 设置 takes_context=True 表示渲染模板时也会传入父模板的上下文，即 context
    return {'recent_posts_list': Post.objects.all()[:num], }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {'date_list': Post.objects.dates('created_time', 'month', order='DESC'), }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    # 除了会返回数据库中全部 Category 的记录，还统计返回的 Category 记录的集合中每条记录下的文章数
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {'category_list': category_list, }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {'tag_list': tag_list, }
