# 人脸识别系统接口说明文档

	1.人员扫码浏览web接口
		输入：二维码
		输出：注册界面
		接口地址：
	2.人脸识别接口
		输入：注册界面人脸图片
		输出：是否检测到人脸
		接口地址：
	3.人员注册接口
		输入：注册信息（所属公司、所属部门、人员名称、邮箱、备注、人脸识别图片）
		输出：注册是否成功，响应注册结果界面
		接口地址：
	4.大屏展示接口：
		输出：筛选公司或全部公司
		输出：筛选公司（各个部门注册统计和部门注册滚动），全部公司（各个公司注册统计和所有公司注册滚动）
		
		
# 需求描述：
	1.生成注册界面URL二维码展示到大屏右下角
	2.注册界面包含所属公司、所属部门、人员名称、邮箱、备注、人脸识别图片信息
	3.人脸识别调用摄像头拍照，拍照完成自动后台校验是否检测到人脸，未检测到不能注册
	4.存储注册信息到数据库，关联注册图片存储地址，并调用人脸大头贴接口响应结果
	5.注册完成等待5秒提示自动跳转大头贴展示
	6.大头贴可以调用打印机打印或存储到手机或返回
	7.大屏展示内容包含筛选公司或全部公司、筛选展示统计结果和实时注册信息滚动及注册二维码，全屏展示功能（全屏隐藏筛选框）
	8.针对重复注册用户提示已注册并响应注册人脸大头贴响应界面
	123