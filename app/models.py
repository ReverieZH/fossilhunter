from django.db import models
import django.utils.timezone as timezone

# Create your models here.
'''
    用户表（用户ID，微信名，用户头像，身份，单位）
    化石图片（图片ID，图片云链接，拍摄时间，拍摄地点，物种ID，描述信息，重建结果链接）
    我的化石（用户ID，图片ID，保存时间）
    我的收藏（用户ID，图片ID，收藏时间）
    物种图鉴（物种ID，物种名，谱系位置，生存时期，详细描述，物种图片[]）
    大家的虫（用户ID，图片ID）
'''

'''
    用户表
'''
class UserInfo(models.Model):
    nickname = models.CharField(verbose_name='用户名', max_length=11)
    usericon = models.CharField(verbose_name='用户头像', max_length=128)
    status = models.CharField(verbose_name='身份', max_length=20)
    institution = models.CharField(verbose_name='单位', max_length=20)

'''
    化石图片
'''
class FossilPicture(models.Model):
    picturepath = models.CharField(verbose_name='图片链接', max_length=128)
    picturetime = models.DateTimeField(verbose_name='拍摄时间', default=timezone.now)
    picturelocation = models.CharField(verbose_name='拍摄地点', max_length=128)
    species = models.ForeignKey(verbose_name="物种名称", to='SpeciesGuide', on_delete=models.CASCADE)
    document = models.CharField(verbose_name='描述信息', max_length=140)
    reconstruction = models.ForeignKey(verbose_name="模型连接", to='ReconstrucationModel', on_delete=models.CASCADE)

'''
    物种图鉴
'''
class SpeciesGuide(models.Model):
    speciesname = models.CharField(verbose_name='物种名', max_length=20)
    speciescover = models.CharField(verbose_name='封面图片', max_length=200)
    specieslocation = models.CharField(verbose_name='谱系位置', max_length=20)
    epoch = models.CharField(verbose_name='生存时期', max_length=20)
    describe = models.CharField(verbose_name='详细描述', max_length=140)
    picture = models.CharField(verbose_name='图片', max_length=128*5)

'''
    我的化石
'''
class MyFossil(models.Model):
    user = models.ForeignKey(verbose_name="用户ID", to='UserInfo', on_delete=models.CASCADE)
    fossil = models.ForeignKey(verbose_name="化石ID", to='FossilPicture', on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='保存时间', default=timezone.now)

'''
    我的收藏
'''
class MyCollection(models.Model):
    user = models.ForeignKey(verbose_name="用户ID", to='UserInfo', on_delete=models.CASCADE)
    fossil = models.ForeignKey(verbose_name="化石ID", to='FossilPicture', on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='收藏时间', default=timezone.now)

'''
    大家的虫
'''
class FossilFamily(models.Model):
    user = models.ForeignKey(verbose_name="用户ID", to='UserInfo', on_delete=models.CASCADE)
    fossil = models.ForeignKey(verbose_name="化石ID", to='FossilPicture', on_delete=models.CASCADE)

'''
    通知
'''
class NewsList(models.Model):
    title = models.CharField(verbose_name='标题', max_length=20)
    content = models.CharField(verbose_name='内容', max_length=20)
    time = models.DateTimeField(verbose_name='发布时间', default=timezone.now)

'''
    模型库
'''
class ReconstrucationModel(models.Model):
    specie = models.ForeignKey(verbose_name="物种ID", to='SpeciesGuide', on_delete=models.CASCADE)
    modelpath = models.CharField(verbose_name='模型链接', max_length=128)

'''
    学习平台
'''
class StudyAdverstation(models.Model):
    picture = models.CharField(verbose_name='图片链接', max_length=128)
    path = models.CharField(verbose_name='链接', max_length=128)

'''
    推广软件
'''
class Adverstation(models.Model):
    picture = models.CharField(verbose_name='图片链接', max_length=128)
    path = models.CharField(verbose_name='链接', max_length=128)


'''
    新闻咨询列表
'''
class NewsReport(models.Model):
    title = models.CharField(verbose_name='标题', max_length=128)
    imagecover = models.CharField(verbose_name='封面图片', max_length=200)
    url = models.CharField(verbose_name='新闻链接', max_length=200)
    source = models.CharField(verbose_name='新闻来源', max_length=20)

'''
    发布鉴别
'''
class Publish(models.Model):
    content = models.CharField(verbose_name='标题', max_length=128)
    user = models.ForeignKey(verbose_name="用户ID", to='UserInfo', on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='发布时间', default=timezone.now)
    picturepath = models.TextField(verbose_name='图片路径')
    isDelete = models.BooleanField(verbose_name='是否删除',default=True)
    # comment = models.ForeignKey(verbose_name="评论", to='Comment', on_delete=models.CASCADE)
'''
    发布鉴别的评论
'''
class Comment(models.Model):
    replyUser = models.ForeignKey(verbose_name='回复人id',  related_name='replyUser',to='UserInfo', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户ID", related_name='commentUser', to='UserInfo', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='回复内容', max_length=128)
    time = models.DateTimeField(verbose_name='发布时间', default=timezone.now)
    publish = models.ForeignKey(verbose_name="所属文章", to='Publish', on_delete=models.CASCADE)

    def __str__(self):
        return "%s_%s" % (self.replyName, self.content)
