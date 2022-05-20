from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework import serializers
from django.db.models import F
from app import models
import time as TM
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
from BAS_RES.BAS_RES_test import BASRESpredict
from app import Resnetpredict as Rp
from .serializers import *

predict = BASRESpredict()
# predict.setfilepath("https://wx-miniprogram-picture-1302593558.cos.ap-chengdu.myqcloud.com/146_1.png")
predict.loadmodel()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'AKIDqRmroiy1HBozve6pBJBDzVpysX0DQy0r'  # 替换为用户的secret_id
secret_key = 'rmS6oHThgWBZhusa03C8NuBLFsMjrqys'  # 替换为用户的secret_key
region = 'ap-chengdu'  # 替换为用户的region
token = None  # 使用临时密钥需要传入Token，默认为空,可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # 获取配置对象
client = CosS3Client(config)

# Create your views here.
'''
    获取物种图鉴
'''


class Getspeciesguide(APIView):
    # 返回动态信息
    def get(self, requst, *args, **kwargs):
        queryset = models.SpeciesGuide.objects.all().order_by('id')[0:10]
        ser = SpeciesguideSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    物种图鉴搜索
'''


class Setsearch(APIView):

    def post(self, requst, *args, **kwargs):
        # requst.query_params
        # requst.data
        search = requst.data.get('search')
        print(search)
        queryset = models.SpeciesGuide.objects.filter(speciesname__icontains=search)
        ser = SetsearchSerializer(instance=queryset, many=True)

        return Response(ser.data, status=200)


'''
    获取详情
'''


class Getspeciesdetail(RetrieveAPIView):
    queryset = models.SpeciesGuide.objects
    serializer_class = SpeciesdetailSerializer


'''
    我的化石
'''


class Getmyfossil(APIView):
    def get(self, requst, *args, **kwargs):
        username = requst.query_params.get('user')
        # 数据库访问
        userinfo = models.UserInfo.objects.get(nickname=username)
        userId = userinfo.id
        queryset = models.MyFossil.objects.filter(user_id=userId).order_by('-id')
        ser = MyfossilSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    修改描述信息
'''


class Setdocumentchange(APIView):
    def post(self, requst, *args, **kwargs):
        changecontent = requst.data.get('changecontent')
        changeid = requst.data.get('changeid')
        print(changeid, changecontent)
        models.FossilPicture.objects.filter(id=changeid).update(document=changecontent)
        return Response({"status": True})


'''
    上传检索图片
'''


class SetPhoto(APIView):
    def post(self, requst, *args, **kwargs):
        image = requst.data.get('image')
        return Response({"status": True})


'''
    保存检索结果
'''


class Setresult(APIView):
    def post(self, requst, *args, **kwargs):
        user = requst.data.get('user')
        context = requst.data.get('context')
        position = requst.data.get('pictureposition')
        print(position)
        picture = requst.data.get('picture')
        specieID = requst.data.get('specieID')
        tempuserinfo = models.UserInfo.objects.get(nickname=user)
        userid = tempuserinfo.id
        fossilid = models.FossilPicture.objects.create(
            picturepath=picture,
            picturelocation=position,
            species_id=specieID,
            document=context,
            reconstruction_id=models.ReconstrucationModel.objects.get(specie_id=specieID).id
        )
        models.MyFossil.objects.create(
            user_id=userid,
            fossil_id=fossilid.id,
        )
        models.FossilFamily.objects.create(
            user_id=userid,
            fossil_id=fossilid.id,
        )

        return Response({"status": True})


'''
    显示检索结果
'''


class Getresult(APIView):
    def get(self, requst, *args, **kwargs):
        picture = requst.query_params.get('picture')
        # 分类算法获得检索结果的化石id
        predict.setfilepath(picture)
        fossilname = predict.predict()
        # 显示化石卡片
        queryset = models.SpeciesGuide.objects.filter(speciesname=fossilname)
        ser = SortresultSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    显示重建结果
'''


class Getreconstruct(APIView):
    def get(self, requst, *args, **kwargs):
        # 获得需重建的化石
        fossilId = requst.query_params.get('fossilId')
        print(fossilId)
        queryset = models.ReconstrucationModel.objects.filter(specie_id=fossilId)
        ser = GetreconstructSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    显示主页信息
'''


class Getnews(APIView):
    def get(self, requst, *args, **kwargs):
        queryset = models.NewsList.objects.all().order_by('-id')[0:5]
        ser = NewsInfoSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    大家的虫
'''


class GetFossilFamily(APIView):
    def get(self, requst, *args, **kwargs):
        queryset = models.FossilFamily.objects.all().order_by('-id')[0:5]
        ser = FossilFamilySerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    加入收藏
'''


class SetCollection(APIView):
    def post(self, requst, *args, **kwargs):
        user = requst.data.get('nickname')
        collectionid = requst.data.get('collectionid')
        fossilid = models.FossilFamily.objects.get(id=collectionid).fossil_id
        userid = models.UserInfo.objects.get(nickname=user).id

        models.MyCollection.objects.create(
            user_id=userid,
            fossil_id=fossilid,
        )
        return Response({"status": True})


'''
    用户视图
'''


class GetUserDetail(APIView):
    def get(self, requst, *args, **kwargs):
        username = requst.query_params.get('user')
        usericon = requst.query_params.get('icon')
        queryset = models.UserInfo.objects.filter(nickname=username)
        if queryset.count() == 0:
            models.UserInfo.objects.create(
                nickname=username,
                usericon=usericon,
                status='学生',
                institution='西北大学',
            )
            queryset = models.UserInfo.objects.filter(nickname=username)
            ser = UserDetailSerializer(instance=queryset, many=True)
            return Response(ser.data, status=200)
        else:
            ser = UserDetailSerializer(instance=queryset, many=True)
            return Response(ser.data, status=200)


class User(APIView):
    def get(self, requst, pk):
        response_msg = {'status': 200, 'msg': '成功'}
        try:
            queryset = models.UserInfo.objects.get(id=pk)
            ser = UserDetailSerializer(instance=queryset)
            response_msg['data'] = ser.data
        except Exception as e:
            response_msg['msg'] = "未找到"
        finally:
            return Response(response_msg)


'''
    我的收藏
'''


class GetMyCollection(APIView):
    def get(self, requst, *args, **kwargs):
        username = requst.query_params.get('nickname')
        tempuserinfo = models.UserInfo.objects.get(nickname=username)
        userid = tempuserinfo.id
        queryset = models.MyCollection.objects.filter(user_id=userid)
        ser = MyCollectionSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    删除
'''


class Deletepicture(APIView):
    def get(self, requst, *args, **kwargs):
        id = requst.query_params.get('pictureid')
        fossilid = models.MyFossil.objects.get(id=id).fossil_id
        models.MyFossil.objects.filter(id=id).delete()
        models.FossilPicture.objects.filter(id=fossilid).delete()
        models.FossilFamily.objects.filter(fossil_id=fossilid).delete()
        return Response({"status": True})


'''
    获取学习平台
'''


class GetstudyAdverstation(APIView):
    def get(self, requst, *args, **kwargs):
        queryset = models.StudyAdverstation.objects.all().order_by('-id')
        ser = StudyAdverstationSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    获取推广
'''


class GetAdverstation(APIView):
    def get(self, requst, *args, **kwargs):
        queryset = models.Adverstation.objects.all().order_by('-id')
        ser = AdverstationSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    获取新闻咨询
'''


class GetNewsReport(APIView):
    def get(self, requst, *args, **kwargs):
        queryset = models.NewsReport.objects.all()
        ser = NewsReportSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


'''
    获取大家的发布
'''


class EveryonePublish(APIView):
    def get(self, requst, *args, **kwargs):
        queryset = models.Publish.objects.all()
        ser = PublishSerialier(instance=queryset, many=True)
        return Response(ser.data, status=200)

    def post(self, request):
        response_msg = {'status': 200, 'msg': '成功'}
        content = request.data.get('content')
        picturepath = request.data.get('picturepath')
        user_id = request.data.get('user_id')
        if user_id and content:
            print(content, picturepath, user_id)
            Publish = models.Publish.objects.create(**request.data)
            ser = PublishSerialier(Publish)
            response_msg['data'] = ser.data
        else:
            response_msg['error'] = '有空值'
            response_msg['msg'] = '失败'
            response_msg['status'] = '500'
        return Response(response_msg)


'''
    获取某一个的发布
'''


class OnePublish(APIView):
    def get(self, request, pk):
        publish = models.Publish.objects.filter(id=pk)
        ser = PublishOneSerialier(instance=publish, many=True)
        return Response(ser.data, status=200)

    def delete(self, request, pk):
        print("删除")
        response_msg = {'status': 200, 'msg': '成功'}
        try:
            models.Publish.objects.filter(id=pk).update(isDelete=False)
            response_msg['msg'] = "删除成功"
        except Exception as e:
            response_msg['status'] = 500
            response_msg['msg'] = "删除失败"
        finally:
            return Response(response_msg)

    def put(self, request, pk):
        response_msg = {'status': 200, 'msg': '修改成功'}
        content = request.data.get('content')
        picturepath = request.data.get('picturepath')
        user_id = request.data.get('user_id')
        if pk and user_id:
            try:
                models.Publish.objects.filter(id=pk).update(content=content, picturepath=picturepath)
            except Exception as e:
                response_msg['status'] = 500
                response_msg['msg'] = "修改失败"
                response_msg['error'] = e
        else:
            response_msg['error'] = '有空值'
            response_msg['msg'] = '修改失败'
            response_msg['status'] = '500'
        return Response(response_msg)


'''
    获取用户的发布
'''


class UserPublish(APIView):
    def get(self, request, pk):
        publish = models.Publish.objects.filter(user_id=pk)
        ser = PublishSerialier(instance=publish, many=True)
        return Response(ser.data, status=200)


'''
    发布评论
'''


class Comment(APIView):
    def post(self, request):
        response_msg = {'status': 200, 'msg': '成功'}
        publish_id = request.data.get('publish_id')
        user_id = request.data.get('user_id')
        content = request.data.get('content')
        replyUser_id = request.data.get('replyUser_id')
        if publish_id and user_id and content and replyUser_id:
            Comment = models.Comment.objects.create(**request.data)
            ser = CommentSerializer(Comment)
            response_msg['data'] = ser.data
        else:
            response_msg['error'] = '有空值'
            response_msg['msg'] = '失败'
            response_msg['status'] = '500'
        return Response(response_msg)


'''
地图页面
'''


def MapView(request):  # 登陆
    obj = {
        "x": 112.4121,
        "y": 37.6611,
        "zoom":8
    }
    return render(request, "index.html", {
        'item': obj
    })  # 返回HTML模板
