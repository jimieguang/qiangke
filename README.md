# qiangke
暨南大学抢课脚本（适用于第二第三阶段）

# 使用方法
部署好selenium环境（用于获取cookie）
输入账号密码
修改需要筛选课程的编号（需要同步修改querySetting中的queryContent参数）
运行并等待
输出课程名及监测次数则标明部署成功

# 基本原理
每隔一定时间获取一次选课记录，筛选出给定课程，如果课程有余量则选课，反之继续等待

# 注意事项
1. cookie更新时需要过滑块验证，这部分耗时较长，第一次使用可以开启selenium的可视化观察是否成功
2. token获取时偶现失败现象，时间有限并未深究原因，一般重启即可
3. 获取课程信息频率不能太高，默认为10s一次，频率过高可能被风控
4. 本脚本用于帮助选不到课就难以毕业的同学，请勿用于其他不良用途
5. 点名批评垃圾学校的学分制度以及容量极其小的高英部分课程
