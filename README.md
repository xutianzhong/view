# 系统接口文档
## 1.大屏展示-获取公司及其相应人数
```
	Get  /screen_display/company
	返回数据：
	{
	    "state":"Success", # Success或者Fail代表请求执行成功或失败
	"info":"Success",#当state为Fail时，info包含请求失败原因，companies为空（“”）
	    "Companies":[#公司列表
		{
		    "company_name":20 #公司名称
		},
		{
		    "company_name":30
		}
	    ]
	}
```
## 2.大屏展示-获取注册时间最近的10名用户
```
	Get  /screen_display/user
	返回数据：
	{
	    "state":"Success",# Success或者Fail代表请求执行成功或失败
	"info":"Success",#当state为Fail时，info包含请求失败原因，users为空（“”）
	    "Users":[
		{
		    "user_name":"",#用户名
		    "company_name":"",#公司名
		    "time":""#时间
		}
	    ]
	}
```
## 3.注册页面-根据公司关键字，返回含有关键字的公司名称
```
	Get  /register/company?keywords=#公司名称
	返回数据：
	{
	    "state":"Success",# Success或者Fail代表请求执行成功或失败
	"info":"Success",#当state为Fail时，info包含请求失败原因，companies为空（“”）
	    "Companies":[
		"company_name",公司名
		"company_name"
	    ]
	}
```
## 4.注册页面-上传头像，检测图片是否含有人脸
```
	Post  /register/picture
	返回数据：
	{
	    "state":"Success",# Success或者Fail代表请求执行成功或失败
	"info":"Success",#当state为Fail时，info包含请求失败原因，result为空（“”）
	    "result":{
		"verify":"pass",#pass或no 代表验证成功或失败
		"msg":""#当verify为no时，msg包含原因,
	    "pid":""#头像唯一标示，每一个用户对应唯一的头像标示
	    }
	}
```
## 5.注册页面-上传注册信息，注册
```
	Post  /register/register
	请求数据：
	{
	    "company":"",#公司
	    "department":"",#部门
	    "user":"",#用户
	    "mail":"",#邮箱
	    "comment":"",#备注
	    "pid":""#头像唯一标示，每一个用户对应唯一的头像标示
	}
	返回数据：
	{
	    "state":"Success",# Success或者Fail代表请求执行成功或失败
	"info":"Success",#当state为Fail时，info包含请求失败原因，result为空（“”）
	   "result":{
		"verify":"pass",#pass或no 代表注册成功或失败
		"msg":"",#当verify为no时，msg包含原因
		"pid":""#当用户已存在和第一次注册成功时，pid含有值，其他情况为空
	    }
	}
```
## 6.注册页面 获取用户大头贴
```
	Get  /register/photo_sticker?pid= #头像唯一标示，每一个用户对应唯一的头像标示
```

# 人脸识别系统接口说明文档
## 1.人员扫码浏览web接口
	输入：二维码
	输出：注册界面
	接口地址：
## 2.人脸识别接口
	输入：注册界面人脸图片
	输出：是否检测到人脸
	接口地址：
## 3.人员注册接口
	输入：注册信息（所属公司、所属部门、人员名称、邮箱、备注、人脸识别图片）
	输出：注册是否成功，响应注册结果界面
	接口地址：
## 4.大屏展示接口：
	输出：筛选公司或全部公司
	输出：筛选公司（各个部门注册统计和部门注册滚动），全部公司（各个公司注册统计和所有公司注册滚动）

# 需求描述：
	1.生成注册界面URL二维码展示到大屏右下角
	2.注册界面包含所属公司、所属部门、人员名称、邮箱、性别（照片大头贴关键）、备注、人脸识别图片信息
	3.人脸识别调用摄像头拍照，拍照完成自动后台校验是否检测到人脸，未检测到不能注册
	4.存储注册信息到数据库，关联注册图片存储地址，并调用人脸大头贴接口响应结果
	5.注册完成等待5秒提示自动跳转大头贴展示
	6.大头贴可以调用打印机打印或存储到手机或返回
	7.大屏展示内容包含筛选公司或全部公司、筛选展示统计结果和实时注册信息滚动及注册二维码，全屏展示功能（全屏隐藏筛选框）
	8.针对重复注册用户提示已注册并响应注册人脸大头贴响应界面

# 技术参考
  [人脸合成技术参考](https://blog.csdn.net/chengxuyuan997/article/details/80809843)
  [人脸性别识别参考]()
  [人脸检测参考]()
