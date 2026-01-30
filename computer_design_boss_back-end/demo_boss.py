from X1_ws import main_answer
import pdfplumber
from sql_data_demo import ResumeManager, Job_prot, EndDemoDatabase
import json
from datetime import date, datetime

class Ai_job_demo:
    def __init__(self):
        self.db = EndDemoDatabase(host='localhost', user='root', password='123456')
        self.resume_manager = ResumeManager(self.db.connection)
        self.job_prot = Job_prot(self.db.connection)

        self.appid = "2e81dc67"  # 填写控制台中获取的 APPID 信息
        self.api_secret = "NDcwM2M1OWY0NTQxOWZiZjg4YzZiNzY3"  # 填写控制台中获取的 APISecret 信息
        self.api_key = "fd79a4d97543e35b2881a64b81b8f124"  # 填写控制台中获取的 APIKey 信息
        self.domain = "spark-x"  # 控制请求的模型版本
        # 服务地址
        self.Spark_url = "wss://spark-api.xf-yun.com/v1/x1"  # 查看接口文档  https://www.xfyun.cn/doc/spark/X1ws.html
        self.user_id = '1143526543212345678'
        self.job_id = '1'
        self.pdf_path = r'C:\Users\lenovo\Desktop\王柄屹简历.pdf'
        self.job_text = '''大模型应用实习生
        # 250-350元/天
        # 上海
        # 5天/周 3个月
        # 本科
        # 收藏立即沟通
        # 举报微信扫码分享
        # 职位描述
        # Python TensorFlow
        # 岗位职责
        # 1、使用相关工具和框架(如LangChain、LangGraph)构建LLM应用;2、基于强化学习方法对LLM进行微调与对齐;
        # 3、构建基于RAG技术的开发应用;
        # 4、协助开发和测试AIAgent项目;
        # 5、参与技术文档编写及项目报告整理。
        # 岗位要求
        # 1、熟练掌握Python，能够进行高效的代码开发和调试;
        # 2、本科及以上学历，计算机科学、人工智能、数据科学或相关专业优先;3、理解大语言模型原理及基础知识(如GPT、Transformer等架构)优先;4、了解或具备偏好优化相关实践经验，熟悉DPO、GRPO、GSPO等算法者优先;5、有基于RAG技术的项目经验或相关知识储备优先。
        # 大三、研二同学优先。
        # '''


    def format_dt(self, d):
        if isinstance(d, (date, datetime)):
            return d.strftime("%Y-%m-%d")
        return ""
    
    def generate_job_description(self, job_list: list) -> str:
        if not job_list:
            return ""
    
        job = job_list[0]
        lines = []
    
        # 基本信息
        lines.append(
            f"招聘岗位：{job.get('title')}（{job.get('salary_desc')}）"
        )
        lines.append(
            f"工作地点：{job.get('district')}，{job.get('address')}"
        )
        lines.append(
            f"学历要求：{job.get('edu_req')}，经验要求：{job.get('exp_req')}"
        )
    
        # 岗位描述
        lines.append(f"岗位职责：{job.get('description')}")
    
        # 任职要求
        require_list = json.loads(job.get("require_list", "[]"))
        if require_list:
            lines.append("任职要求：")
            for r in require_list:
                lines.append(f" - {r}")
    
        # 福利待遇
        welfare_list = json.loads(job.get("welfare_list", "[]"))
        if welfare_list:
            lines.append("福利待遇：")
            for w in welfare_list:
                lines.append(f" - {w}")
    
        # 时间信息
        lines.append(
            f"岗位发布时间：{self.format_dt(job.get('publish_time'))}，"
            f"最近刷新：{self.format_dt(job.get('refresh_time'))}"
        )
    
        return "\n".join(lines)
    
    
    def format_date(self,d):
        if isinstance(d, (date, datetime)):
            return d.strftime("%Y-%m-%d")
        return ""
    
    def generate_user_profile(self,data: dict) -> str:
        basic = data.get("basic_info", {})
        certs = data.get("certificates", [])
        campus = data.get("campus_experiences", {})
        internships = data.get("internships", [])
        intention = data.get("job_intention", {})
        preference = data.get("job_preference", {})
        stats = data.get("internship_stats", {})
    
        lines = []
    
        # 基本信息
        lines.append(f"我叫{basic.get('real_name')}，{basic.get('gender') and '男' or '女'}，"
                     f"{self.format_date(basic.get('birth_date'))}出生，现居{basic.get('city')}。")
        lines.append(
            f"毕业于{basic.get('school_name')}，{basic.get('major')}专业，本科学历，"
            f"{basic.get('graduation_year')}年毕业，GPA {basic.get('gpa')}。"
        )
        lines.append(
            f"联系方式：手机 {basic.get('phone')}，邮箱 {basic.get('email')}，微信 {basic.get('wechat')}。"
        )
    
        # 自我介绍
        if basic.get("self_introduction"):
            lines.append(f"自我介绍：{basic.get('self_introduction')}。")
    
        # 校园经历
        if campus.get("has_scholarship"):
            lines.append(f"在校期间获得奖项：{campus.get('scholarship_details')}。")
    
        # 证书
        if certs:
            cert_text = []
            for c in certs:
                cert_text.append(
                    f"{c['cert_name']}（{c['cert_level']}，{c['issuing_authority']}）"
                )
            lines.append("已获得的相关证书包括：" + "，".join(cert_text) + "。")
    
        # 实习经历
        lines.append(f"共拥有 {stats.get('total_count', 0)} 段实习经历，均与目标岗位高度相关。")
        for i in internships:
            lines.append(
                f"曾在{i['company_name']}担任{i['position']}，"
                f"主要工作内容：{i['work_content']}。"
                f"主要成果：{i['achievements']}。"
            )
    
        # 求职意向
        lines.append(
            f"求职意向为{intention.get('position_priority')}方向，"
            f"优先行业为{intention.get('industry_priority')}，"
            f"期望工作城市{intention.get('city_priority')}，"
            f"期望薪资{intention.get('salary_min')}–{intention.get('salary_max')}元/月，"
            f"{'可协商' if intention.get('salary_negotiable') else '不可协商'}，"
            f"到岗时间：{intention.get('availability')}。"
        )
    
        # 工作偏好
        lines.append(
            f"工作偏好：{preference.get('company_size_preference')}，"
            f"{preference.get('work_type_preference')}，"
            f"{preference.get('other_preferences')}。"
        )
    
        return "\n".join(lines)
    
    
    def extract_pdf_text(self,pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def get_user_app_text(self,user_id):
        user_app_text = self.resume_manager.get_complete_resume(user_id)
        user_app_text = self.generate_user_profile(user_app_text)
        return user_app_text
    
    def get_job_text_in_db(self,job_id):
        job_text = self.job_prot.fetch_one_job_all_data_posts(ones_id=job_id)
        job_text = self.generate_job_description(job_text)
        return job_text
    
    def ask_by_pdf_and_job_id(self, pdf_path, job_id):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_pdf_text}\n
                                以下是我的目标岗位的招聘信息：{job_text}\n
                                请帮我从简历和岗位的角度分析我这次求职经历。
                            '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def ask_by_pdf_and_job_text(self, pdf_path, job_text):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_pdf_text}\n
                                以下是我的目标岗位的招聘信息：{job_text}\n
                                请帮我从简历和岗位的角度分析我这次求职经历。
                            '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def ask_by_user_id_and_job_text(self, user_id, job_text):
        user_text = self.get_user_app_text(user_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_text}\n
                                以下是我的目标岗位的招聘信息：{job_text}\n
                                请帮我从简历和岗位的角度分析我这次求职经历。
                            '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def ask_by_user_id_and_job_id(self, user_id, job_id):
        user_text = self.get_user_app_text(user_id)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_text}\n
                            以下是我的目标岗位的招聘信息：{job_text}\n
                            请帮我从简历和岗位的角度分析我这次求职经历。
                            '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def chat(self, user_ask):
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, user_ask)
        return ai_answer
    
    def resume_evalu_by_user_id(self, user_id):
        user_text = self.get_user_app_text(user_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_text}\n
                                请为我评估我的简历，并为根据难易与匹配度为我推荐一些岗位。
                                '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def resume_evalu_by_user_pdf(self, pdf_path):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_pdf_text}\n
                                请为我评估我的简历，并为根据难易与匹配度为我推荐一些岗位。
                                '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def success_rate_by_pdf_and_job_id(self, pdf_path, job_id):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_pdf_text}\n
                                以下是我的目标岗位的招聘信息：{job_text}\n
                                请帮我从简历和岗位的角度给出我这次求职的成功率。
                                优先回答成功率，然后再给出得出依据
                            '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def success_rate_by_pdf_and_job_text(self, pdf_path, job_text):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_pdf_text}\n
                                    以下是我的目标岗位的招聘信息：{job_text}\n
                                    请帮我从简历和岗位的角度给出我这次求职的成功率。
                                    优先回答成功率，然后再给出得出依据
                                '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def success_rate_by_user_id_and_job_text(self, user_id, job_text):
        user_text = self.get_user_app_text(user_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_text}\n
                                    以下是我的目标岗位的招聘信息：{job_text}\n
                                    请帮我从简历和岗位的角度给出我这次求职的成功率。
                                    优先回答成功率，然后再给出得出依据
                                '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def success_rate_by_user_id_and_job_id(self, user_id, job_id):
        user_text = self.get_user_app_text(user_id)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_text}\n
                                    以下是我的目标岗位的招聘信息：{job_text}\n
                                    请帮我从简历和岗位的角度给出我这次求职的成功率。
                                    优先回答成功率，然后再给出得出依据
                                '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def uni_plan_by_pdf_and_job_id(self, pdf_path, job_id,user_grade):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_pdf_text}\n
                                    以下是我的目标岗位的招聘信息：{job_text}\n
                                    我现在是一名{user_grade}的学生,
                                    请为我的大学生活给出一个合理的规划，帮助成功获得目标岗位
                                '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def uni_plan_by_pdf_and_job_text(self, pdf_path, job_text,user_grade):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_pdf_text}\n
                                    以下是我的目标岗位的招聘信息：{job_text}\n
                                    我现在是一名{user_grade}的学生,
                                    请为我的大学生活给出一个合理的规划，帮助成功获得目标岗位
                                '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def uni_plan_by_user_id_and_job_text(self, user_id, job_text, user_grade):
        user_text = self.get_user_app_text(user_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_text}\n
                                    以下是我的目标岗位的招聘信息：{job_text}\n
                                    我现在是一名{user_grade}的学生,
                                    请为我的大学生活给出一个合理的规划，帮助成功获得目标岗位
                                '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer
    
    def uni_plan_by_user_id_and_job_id(self, user_id, job_id,user_grade):
        user_text = self.get_user_app_text(user_id)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = f'''\n我：以下是我的简历内容：{user_text}\n
                                    以下是我的目标岗位的招聘信息：{job_text}\n
                                    我现在是一名{user_grade}的学生,
                                    请为我的大学生活给出一个合理的规划，帮助成功获得目标岗位
                                '''
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

# if __name__ == '__main__':

    # print("========== 求职分析（user_id + job_id） ==========")
    # print(ask_by_user_id_and_job_id(user_id=user_id, job_id=job_id))
    #
    # print("\n========== 求职分析（user_id + job_text） ==========")
    # print(ask_by_user_id_and_job_text(user_id=user_id, job_text=job_text))
    #
    # print("\n========== 求职分析（pdf + job_id） ==========")
    # print(ask_by_pdf_and_job_id(pdf_path=pdf_path, job_id=job_id))
    #
    # print("\n========== 求职分析（pdf + job_text） ==========")
    # print(ask_by_pdf_and_job_text(pdf_path=pdf_path, job_text=job_text))
    #
    # print("\n========== 简历评估（user_id） ==========")
    # print(resume_evalu_by_user_id(user_id=user_id))
    #
    # print("\n========== 简历评估（纯文本） ==========")
    # user_text = get_user_app_text(user_id)
    # print(resume_evalu_by_user_text(user_text))
    #
    # print("\n========== 求职成功率（pdf + job_id） ==========")
    # print(success_rate_by_pdf_and_job_id(pdf_path=pdf_path, job_id=job_id))
    #
    # print("\n========== 求职成功率（pdf + job_text） ==========")
    # print(success_rate_by_pdf_and_job_text(pdf_path=pdf_path, job_text=job_text))
    #
    # print("\n========== 求职成功率（user_id + job_text） ==========")
    # print(success_rate_by_user_id_and_job_text(user_id=user_id, job_text=job_text))
    #
    # print("\n========== 求职成功率（user_id + job_id） ==========")
    # print(success_rate_by_user_id_and_job_id(user_id=user_id, job_id=job_id))
    #
    # print("\n========== 大学规划（pdf + job_id） ==========")
    # print(uni_plan_by_pdf_and_job_id(
    #         pdf_path=pdf_path,
    #         job_id=job_id,
    #         user_grade="大二"
    # ))
    #
    # print("\n========== 大学规划（pdf + job_text） ==========")
    # print(uni_plan_by_pdf_and_job_text(
    #         pdf_path=pdf_path,
    #         job_text=job_text,
    #         user_grade="大二"
    # ))
    #
    # print("\n========== 大学规划（user_id + job_text） ==========")
    # print(uni_plan_by_user_id_and_job_text(
    #         user_id=user_id,
    #         job_text=job_text,
    #         user_grade="大二"
    # ))
    #
    # print("\n========== 大学规划（user_id + job_id） ==========")
    # print(uni_plan_by_user_id_and_job_id(
    #         user_id=user_id,
    #         job_id=job_id,
    #         user_grade="大二"
    # ))
    #
    # print("\n========== 普通对话测试 ==========")
    # print(chat("请用一句话评价我的简历整体竞争力"))
    #
