from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.


class Category(models.Model):
    """分类类"""
    name = models.CharField(max_length=100, verbose_name='分类名')

    class Meta:
        verbose_name = '分类'
        # 负数显示，中文中没有专门的负数显示，直接使用verbose_name
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签类"""
    name = models.CharField(max_length=100, verbose_name='标签名')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    """文章类"""
    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    # timezone模块中的函数会自动帮我们处理时区，所以不使用Python提供的datetime模块来处理时间。
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # 文章和分类是一对一的关系，删除分类时下面所有文章全部删除
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    # 文章和标签是多对多的关系，一篇文章可以没有标签
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    views = models.PositiveIntegerField(default=0, editable=False, verbose_name='阅读量')

    # 重写 save 方法
    def save(self, *args, **kwargs):
        # 每次保存时更新 修改时间
        self.modified_time = timezone.now()

        # 未输入摘要时自动生成摘要
        if len(self.excerpt) == 0:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本，并去掉目录拓展
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    # 自定义 get_absolute_url 方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 文章阅读量自动增加
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time', 'title']

    def __str__(self):
        return self.title


