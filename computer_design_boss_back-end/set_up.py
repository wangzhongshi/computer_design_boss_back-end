class config:
    def __init__(self):
        # 数据库
        self.set_db_host = 'localhost'
        self.set_db_user = 'root'
        self.set_db_password = '123456'
        self.set_db_prot = 3306
        self.set_db_name = 'boss_job'

        self.set_JWT_SECRET = 'your-secret-key'
        self.set_JWT_ALGORITHM = 'HS256'

        self.set_UPLOAD_FOLDER = 'static/audio'
        # 大模型和请求提示词
        self.set_LLM_appid = "af5d91f0"  # 填写控制台中获取的 APPID 信息
        self.set_LLM_api_secret = "OGRhOTVkMGY3ZTA2M2U2OWM2MTEyZmM4"  # 填写控制台中获取的 APISecret 信息
        self.set_LLM_api_key = "bbc640957c9754ce610385539be4dcdc"  # 填写控制台中获取的 APIKey 信息
        self.set_LLM_domain = "generalv3"  # 控制请求的模型版本
        self.set_LLM_Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"  # 查看接口文档  https://www.xfyun.cn/doc/spark/X1ws.html
        self.set_request_str_ask = '''\n我：以下是我的简历内容：{user_pdf_text}\n
                                        以下是我的目标岗位的招聘信息：{job_text}\n
                                        请帮我从简历和岗位的角度分析我这次求职经历。
                                        总字数<300字'''
        self.set_request_str_resume = '''\n我：以下是我的简历内容：{user_text}\n
                                          请为我评估我的简历，并为根据难易与匹配度为我推荐一些岗位。
                                          总字数<400字'''
        self.set_request_str_success = '''\n我：以下是我的简历内容：{user_pdf_text}\n
                                        以下是我的目标岗位的招聘信息：{job_text}\n
                                        请帮我从简历和岗位的角度给出我这次求职的成功率。
                                        优先回答成功率，然后再给出得出依据
                                        总字数<400字'''
        self.set_request_str_uni = '''\n我：以下是我的简历内容：{user_pdf_text}\n
                                        以下是我的目标岗位的招聘信息：{job_text}\n
                                        我现在是一名{user_grade}的学生,
                                        请为我的大学生活给出一个合理的规划，帮助成功获得目标岗位
                                        总字数<400字'''

        self.set_interview_start_str = """你现在是一名专业且真实的 AI 面试官。
                                        你将基于【候选人简历】和【目标岗位招聘信息】，对候选人进行一场完整的模拟面试。
                                        ====================
                                        【候选人简历】
                                        {resume_text}
                                            
                                        ====================
                                        【目标岗位招聘信息】
                                        {job_text}
                                            
                                        ====================
                                        【面试规则】
                                        1. 你必须主导面试流程
                                        2. 每次只问一个问题，问题要有针对性且自然
                                        3. 根据候选人的回答动态追问，深入挖掘细节
                                        4. 不要替候选人回答
                                        5. 不要输出分析过程或评价
                                        6. 只有在面试结束时才给出总结
                                        
                                        ====================
                                        【面试流程】
                                        第一阶段：自我介绍（1-2个问题）
                                        第二阶段：专业能力（结合岗位要求，2-3个问题）
                                        第三阶段：项目/实践经历（2-3个问题，深入追问）
                                        第四阶段：综合能力与思维（2个问题）
                                        第五阶段：反问环节（候选人提问）
                                        
                                        ====================
                                        【面试结束】
                                        当候选人说"面试结束"或"我没有问题了"时：
                                        - 给出综合评分（0-100，要有具体分项得分）
                                        - 给出是否通过（通过/待定/不通过）
                                        - 给出至少 3 条具体可执行的改进建议
                                        
                                        当前阶段：第一阶段（自我介绍）
                                        请开始面试，提出第一个问题。"""

        self.set_interview_end_str = """面试已结束，请严格按照以下JSON格式输出最终评价：
                                        {
                                            "overall_score": 85,
                                            "dimension_scores": {
                                                "专业匹配度": 90,
                                                "项目经验": 85,
                                                "表达能力": 80,
                                                "逻辑思维": 88,
                                                "综合素质": 82
                                            },
                                            "result": "通过",
                                            "strengths": ["优势1", "优势2", "优势3"],
                                            "weaknesses": ["不足1", "不足2"],
                                            "improvement_suggestions": ["建议1", "建议2", "建议3", "建议4"],
                                            "summary": "综合评价总结..."
                                        }
                                        确保输出合法的JSON格式。"""
        # 语音听写
        self.set_iat_appid = '2e81dc67'
        self.set_iat_api_key = 'fd79a4d97543e35b2881a64b81b8f124'
        self.set_iat_api_secret = 'NDcwM2M1OWY0NTQxOWZiZjg4YzZiNzY3'
        # 语音合成
        self.set_tts_appid = '2e81dc67'
        self.set_tts_api_key = 'fd79a4d97543e35b2881a64b81b8f124'
        self.set_tts_api_secret = 'NDcwM2M1OWY0NTQxOWZiZjg4YzZiNzY3'
        # 大模型的最大生成长度和灵活度
        self.set_LLM_max_tokens = 50  # 通过这个参数设置api的最大生成长度,具体值范围,依照官方文档
        self.set_LLM_temperature = 1

        self.max_str_len = 280

        self.want_thing_jd = '''招聘岗位：高级Web前端工程师（25-40K）
                                工作地点：海淀区，中关村软件园二期
                                学历要求：本科，经验要求：3-5年
                                岗位职责：负责抖音创作者平台前端架构设计与开发，优化首屏加载性能，建设前端工程化体系
                                任职要求：
                                 - 精通React/Vue
                                 - 熟悉Webpack/Vite
                                 - 有大型SPA开发经验
                                 - 了解Node.js
                                福利待遇：
                                 - 六险一金
                                 - 免费三餐
                                 - 租房补贴
                                 - 股票期权
                                岗位发布时间：，最近刷新：'''
        self.want_thing_form = '''我叫小菜鸟，男，2004-03-17出生，现居北京。
                                毕业于北京大学，人工智能专业，本科学历，2027年毕业，GPA 1.00。
                                联系方式：手机 15231231233，邮箱 233@qq.com，微信 。
                                自我介绍：各位好，我是[你的名字]，目前在北京大学攻读人工智能学士学位。在学习深度学习和各种算法的同时，我也一直在思考技术背后的人文关怀。除了掌握Python和Pytorch这些工具，我更希望能做一个有温度的AI研究者，让技术真正落地去解决一些社会问题。很高兴今天能在这里和大家相遇。
                                已获得的相关证书包括：Python编程证书（None，Python官方认证）。
                                共拥有 1 段实习经历，均与目标岗位高度相关。
                                曾在None担任None，主要工作内容：None。主要成果：None。
                                求职意向为None方向，优先行业为None，期望工作城市None，期望薪资15000–25000元/月，可协商，到岗时间：None。
                                工作偏好：0，0，None。'''