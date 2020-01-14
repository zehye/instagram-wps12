from django.db import models
from members.models import User
import re


class Post(models.Model):
    """
    인스타그램의 포스트
    """
    TAG_PATTERN = re.compile(r'#(\w+)')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    like_user = models.ManyToManyField(
        # PostLike 를 통한 Many to Many 구현
        User,
        through='PostLike',
        related_name='like_post_set',
    )
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', verbose_name='해시태그 목록', related_query_name='posts', blank=True)

    def __str__(self):
        return f'{self.author}가 {self.content}를 {self.created}에 작성했어요.'

    def _save_html(self):
        """
        content속성의 값을 사용해서 해시태그에 해당하는 문자열을 #태그로 바꾸어줌
        :return: 해시태그가 a태그로 변환된 html
        """
        self.content_html = re.sub(
            self.TAG_PATTERN,
            r'<a href="/explore/tags/\g<1>/"#\g<1></a>',
            self.content,
        )

    def _save_tags(self):
        """
        content에 포함된 해시태그 문자열(ex: #Python)의 tag들을 만들고
        자신의 tags Many-to-Many field에 추가한다.
        """
        tag_name_list = re.findall(self.TAG_PATTERN, self.content)
        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_name_list]
        self.tags.set(tags)

    def save(self, *args, **kwargs):
        self._save_html()
        super().save(*args, **kwargs)
        self._save_tags()
        # for tag_name in tag_name_list:
        #     tag = Tag.objects.get_or_create(name=tag_name)[0]
        '''
        post객체가 저장될 떄, content값을 분석해서 자신의 tags항목을 적절히 채워줌
        ex) #Django #Python 이 온 경우, post.tags.all()시 name이 Django, Python 인 tag 2개 QuerySet이 리턴되어야 
        
        instance, created = Tag.objects.get_or_create(속성)
        manyToManyField.set <- 쓰면 편합니다. 
        '''


class PostImage(models.Model):
    """
    포스트의 사진들
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images')


class PostComment(models.Model):
    """
    각 포스트의 댓글 (Many to one)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class PostLike(models.Model):
    """
    사용자가 좋아요 뉴른 Post정보를 저장
    Many to Many 필드를 참조모델(Intermediate Model)을 거쳐 사용
        언제 생성되었는지를 Extra fields로 저장!(created)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

