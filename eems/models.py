from django.db import models
from django.utils import timezone


# Create your models here.
class User_Master(models.Model):
    """
    description: 管理対象ユーザーのマスタ
    """
    # user_id
    user_id = models.CharField(max_length=4)
    # line_id
    # ex. U6bca9d80ca9e97f27cfb3077dee3748f
    line_id = models.CharField(max_length=33)
    # user name
    user_name = models.CharField(max_length=128)
    # line name
    line_name = models.CharField(max_length=128)
    # 会社名
    company = models.CharField(max_length=128)
    # 所属名
    department = models.CharField(max_length=128)
    # 入室回数
    num_entry = models.IntegerField(default=0)
    # ユーザーの写真のURL
    user_img = models.URLField(max_length=250, default='')


class Current_Entry(models.Model):
    """
    description: 現在入室しているユーザーのデータ
    """
    # user = models.ForeignKey(User_Master, on_delete=models.PROTECT)
    line_id = models.CharField(max_length=33, default='')
    line_name = models.CharField(max_length=128, default='')
    user_img = models.URLField(max_length=250, default='')
    entry_time = models.DateTimeField(default=timezone.now)
    leave_time = models.DateTimeField(default=timezone.now)


class Beacon_Log(models.Model):
    """
    description: ビーコンからきたログ
    """
    # replyToken
    reply_token = models.CharField(max_length=32)
    # line_id
    line_id = models.CharField(max_length=33)
    # timestamp
    timestamp = models.DateTimeField()
    # hwid
    hwid = models.CharField(max_length=10)
    # enter_or_leave
    enter_or_leave = models.CharField(max_length=5)
