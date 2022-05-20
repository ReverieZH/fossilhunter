from rest_framework import serializers
from app import models

'''
    获取物种图鉴
'''


class SpeciesguideSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpeciesGuide  # 指定生成字段的模型类
        fields = ['id', 'speciescover', 'speciesname']  # 指定模型类中的字段


'''
    物种图鉴搜索
'''


class SetsearchSerializer(serializers.ModelSerializer):
    # 增加修改字段
    # 显示指明字段 可以指定模型没有的字段，但要在fields只声明
    # speciesname=serializers.CharField(max_length=20)
    class Meta:
        model = models.SpeciesGuide
        fields = ['id', 'speciesname']
        # 可以增加修改字段选项参数
        # extra_kwargs = {
        #     "speciesname": {
        #         'max_length': 20
        #     }
        # }
        # read_only_fields=('speciesname')


'''
    获取详情
'''


class SpeciesdetailSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    class Meta:
        model = models.SpeciesGuide
        fields = ['speciesname', 'speciescover', 'specieslocation', 'epoch', 'describe', 'picture']

    def get_picture(self, obj):
        cos_qureyset = obj.picture.lstrip('[').rstrip(']').replace(' ', '').replace("'", '').split(',')
        return cos_qureyset


'''
    我的化石
'''


class MyfossilSerializer(serializers.ModelSerializer):
    fossil = serializers.SerializerMethodField()

    class Meta:
        model = models.MyFossil
        fields = ['id', 'fossil']

    def get_fossil(self, obj):
        return {'fossilid': obj.fossil.id,
                'speciesname': obj.fossil.species.speciesname,
                'specieslocation': obj.fossil.species.specieslocation,
                'epoch': obj.fossil.species.epoch,
                'picturepath': obj.fossil.picturepath,
                'document': obj.fossil.document,
                'speciesId': obj.fossil.species_id,
                }


'''
    显示检索结果
'''


class SortresultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpeciesGuide
        fields = ['id', 'speciesname', 'specieslocation', 'epoch', 'describe']


'''
    显示重建结果
'''


class GetreconstructSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReconstrucationModel
        fields = ['id', 'modelpath']


'''
    显示主页信息
'''


class NewsInfoSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    class Meta:
        model = models.NewsList
        fields = ['id', 'title', 'content', 'time']

    def get_time(self, obj):
        return {
            'time': str(obj.time)[:16],
        }


'''
    大家的虫
'''


class FossilFamilySerializer(serializers.ModelSerializer):
    fossil = serializers.SerializerMethodField()

    class Meta:
        model = models.FossilFamily
        fields = ['id', 'fossil', 'user_id']

    def get_fossil(self, obj):
        return {'fossilid': obj.fossil.id,
                'speciesname': obj.fossil.species.speciesname,
                'usericon': obj.user.usericon,
                'picturetime': str(obj.fossil.picturetime)[:16],
                'picturepath': obj.fossil.picturepath,
                }


'''
    用户表
'''


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ['id', 'nickname', 'usericon', 'status', 'institution']


'''
    我的收藏
'''


class MyCollectionSerializer(serializers.ModelSerializer):
    fossil = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = models.MyCollection
        fields = ['id', 'fossil', 'time']

    def get_time(self, obj):
        return {
            'time': str(obj.time)[:16],
        }

    def get_fossil(self, obj):
        return {
            'fossilid': obj.fossil.id,
            'speciesname': obj.fossil.species.speciesname,
            'picturepath': obj.fossil.picturepath,
        }


'''
    获取学习平台
'''


class StudyAdverstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudyAdverstation
        fields = ['picture', 'path']


'''
    获取推广
'''


class AdverstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Adverstation
        fields = ['picture', 'path']


'''
    新闻咨询
'''


class NewsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewsReport
        fields = ['id', 'title', 'imagecover', 'url', 'source']


'''
评论序列化器
'''


class CommentSerializer(serializers.ModelSerializer):
    replyUser = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = '__all__'
        write_only = ['id', 'replyUser', 'content', 'time', 'user']

    def get_time(self, obj):
        return str(obj.time)[:16]

    def get_user(self, obj):
        return {
            'userid': obj.user.id,
            'username': obj.user.nickname,
            'usericon': obj.user.usericon,
        }

    def get_replyUser(self, obj):
        return {
            'replyUserId': obj.replyUser.id,
            'replyUserName': obj.replyUser.nickname,
        }

'''
    发布鉴别
'''


class PublishSerialier(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    commentlength = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = models.Publish
        fields = ['id', 'content', 'time', 'picture', 'user', 'commentlength', 'isDelete']

    def get_picture(self, obj):
        # print(str(obj.picturepath).split(","))
        return str(obj.picturepath).split(",")

    def get_user(self, obj):
        return {
            'userid': obj.user.id,
            'username': obj.user.nickname,
            'usericon': obj.user.usericon,
        }

    def get_commentlength(self, obj):
        comment = obj.comment_set.all()
        return len(comment)

    def get_time(self, obj):
        return str(obj.time)[:16]


'''
    发布鉴别
'''


class PublishOneSerialier(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = models.Publish
        fields = ['id', 'content', 'time', 'picture', 'user', 'comment']

    def get_picture(self, obj):
        return str(obj.picturepath).split(",")

    def get_user(self, obj):
        return {
            'userid': obj.user.id,
            'username': obj.user.nickname,
            'usericon': obj.user.usericon,
        }

    def get_time(self, obj):
        return str(obj.time)[:16]

    def get_comment(self, obj):
        comment = obj.comment_set.all()
        res = CommentSerializer(comment, many=True)
        return res.data
