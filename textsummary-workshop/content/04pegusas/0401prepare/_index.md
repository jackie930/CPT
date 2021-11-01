+++
title = "pegasus模型实验"
weight = 0301
chapter = true
pre = "<b>3.1 </b>"
+++

##预训练任务

预训练任务模仿了PEGASUS的摘要式预训练。具体来说，假设一个文档有n个句子，我们从中挑出大约n/4个句子（可以不连续），使得这n/4个句子拼起来的文本，跟剩下的3n/4个句子拼起来的文本，最长公共子序列尽可能长，然后我们将3n/4个句子拼起来的文本视为原文，n/4个句子拼起来的文本视为摘要，通过这样的方式构成一个“(原文, 摘要)”的伪摘要数据对。

运行环境：tensorflow 1.15 + keras 2.3.1 + bert4keras 0.10.0

## 模型下载


# quick start

### train
将待训练的数据集放在`data`目录下

~~~shell script
git clone https://github.com/jackie930/t5-pegasus-textsummary.git
source activate tensorflow_p36
pip install tensorflow==1.15 keras==2.3.1 bert4keras==0.10.0 jieba tqdm rouge
python finetune.py
~~~

训练结束会产生一个keras结构的模型文件 - best_model.weights

### 预测
下载模型文件，目录结构为

chinese_t5_pegasus_base/ 
best_model.weights

~~~shell script
python test.py
~~~

### 评估

运行 `python evaluatiion.py`

得到结果 `{'rouge-1': 0.885041123153444, 'rouge-2': 0.8795828353099052, 'rouge-l': 0.9046418758557804, 'bleu': 0.8239310846742561}`

### 部署

~~~
#make sure you got trained models 
sh build_and_push.sh
~~~

run on endpoint

```shell script
#sin
endpoint_ecr_image="847380964353.dkr.ecr.ap-southeast-1.amazonaws.com/pegasus"
#ningxia
#endpoint_ecr_image="251885400447.dkr.ecr.cn-northwest-1.amazonaws.com.cn/pegasus"
python create_endpoint.py \
--endpoint_ecr_image_path ${endpoint_ecr_image} \
--endpoint_name 'pegasus' \
--instance_type "ml.g4dn.8xlarge"
```

在部署结束后，看到SageMaker控制台生成了对应的endpoint,可以使用如下客户端代码测试调用
```python
from boto3.session import Session
import json
txt = "来源|零壹财经作者|任俊东12月1日，国家互联网信息办公室发布关于《常见类型移动互联网应用程序（App）必要个人信息范围》公开征求意见的通知。此次《意见稿》规定了支付、借贷、银行等38类常见类型App必要个人信息范围，明确App必要个人信息界限，不得因非必要信息拒绝用户安装使用。零壹财经自今年3月起开展了手机App评测工作，通过对金融、购物、视频等10大类300多款App评测发现，9成以上APP都存在违规收集信息问题，其中违反必要原则，收集与其业务无关的个人信息、用户拒绝同意就无法安装使用等问题最为严重。上月，全国App个人信息保护监管会召开。会上阿里、腾讯、字节等互联网巨头遭监管点名批评：在App个人信息保护工作方面，存在思想漠视、侥幸心理、技术对抗三类问题。1.对38类App必要个人信息范围向社会征求意见针对此次《意见稿》，国家网信办表示，近年来App广泛应用在促进经济社会发展、服务民生等方面发挥了重要作用。同时，App超范围收集、强制收集用户个人信息普遍存在，用户拒绝同意就无法安装使用。为落实《中华人民共和国网络安全法》关于个人信息收集合法、正当、必要的原则，规范App个人信息收集行为，因而明确常见App收集必要个人信息范围。意见反馈时间截止到2020年12月16日。2.12类App无须个人信息，即可使用基本功能服务根据《意见稿》，国家网信办拟规定网络直播、在线影音、短视频、新闻资讯、运动健身、浏览器、输入法、安全管理、电子图书、拍摄美化、应用商店、实用工具类共12类App无须个人信息，即可使用基本功能服务。3.零壹App评测：9成以上App存在违规收集信息问题为规范收集APP信息收集和使用、加强个人信息保护，切实维护收集APP消费者合法权益，并依据相关监管政策法规，零壹财经App评测中心于2020年3月2日启动App评测专项工作。中心相关评测工作得到了App消费者、监管部门、相关企业、行业从业者等多方的广泛关注和支持。通过对金融、购物、视频等10大类300多款App评测发现，9成以上APP都存在违规收集信息问题，其中违反必要原则，收集与其业务无关的个人信息、用户拒绝同意就无法安装使用等问题最为严重。4.阿里、腾讯、字节等遭监管点名批评，App个人信息保护进入新的发展阶段11月27日，全国App个人信息保护监管会在北京召开，工信部召集国内互联网行业的头部企业，总结过去半年来App个人信息保护专项整治行动的成果，部署下一阶段整治行动。工信部信息通信管理局副局长鲁春从在会上表示，工信部针对大企业的App进行了全覆盖检测，对阿里巴巴的40余款、字节跳动30余款，腾讯30余款、百度20余款、网易10余款、小米10余款用户下载量大、使用率高的App进行了重点检测，发现存在思想漠视、侥幸心理、技术对抗三类问题。互联网个人信息数据野蛮生长时代已成过去，APP个人信息保护正在迎来新的发展阶段。切实维护用户合法权益，严厉惩处互联网企业违法违规行为是今后互联网监管的常态。企业只有从思想上重视、行动上遵守，把用户的利益作为企业的核心关切，才能持续发展。添加作者微信：daodao0312，可获取《常见类型移动互联网应用程序（App）必要个人信息范围（征求意见稿）》，或您有App评测需求请联系作者。"
data={"data": txt}
session = Session()
    
runtime = session.client("runtime.sagemaker")
response = runtime.invoke_endpoint(
    EndpointName='pegasus',
    ContentType="application/json",
    Body=json.dumps(data),
)

result = json.loads(response["Body"].read())
print (result)
```


