from rest_framework.response import Response
from django.conf import settings
from sts.sts import Sts

def get_credential():
    config = {
        # 'url': 'https://sts.tencentcloudapi.com/',
        # 'domain': 'sts.tencentcloudapi.com',
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        'secret_id': settings.TENCENT_SECRET_ID,
        # 固定密钥
        'secret_key': settings.TENCENT_SECRET_KEY,
        # 设置网络代理
        # 'proxy': {
        #     'http': 'xx',
        #     'https': 'xx'
        # },
        # 换成你的 bucket
        'bucket': 'htyper-1255622648',
        # 换成 bucket 所在地区
        'region': 'ap-nanjing',
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': 'UploadPictures/*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # 简单上传
            # 'name/cos:PutObject',
            'name/cos:PostObject',
            'name/cos:DeleteObject',
            # 分片上传
            # 'name/cos:InitiateMultipartUpload',
            # 'name/cos:ListMultipartUploads',
            # 'name/cos:ListParts',
            # 'name/cos:UploadPart',
            # 'name/cos:CompleteMultipartUpload'
        ],
    }
    try:
        sts = Sts(config)
        response = sts.get_credential()  # 密钥
        # print('get data : ' + json.dumps(dict(response), indent=4))
        return response
    except Exception as e:
        print(e)


if __name__ == '__main__':
    get_credential()
