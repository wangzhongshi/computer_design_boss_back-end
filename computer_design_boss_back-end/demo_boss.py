from X1_ws import main_answer
import pdfplumber
from sql_data_demo import ResumeManager, Job_prot, EndDemoDatabase
import json
from datetime import date, datetime
from tts_ws_python3_demo import tts_demo
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import json
from datetime import datetime
import threading
import time
from tts_ws_python3_demo import tts_demo
from iat_ws_python3 import demo_file_recognition
from X1_ws import main_answer
from set_up import config
config_data = config()


def extract_assistant_content(func):
    """
    装饰器：从对话列表中提取 assistant 角色的内容
    """

    def wrapper(*args, **kwargs):
        # 调用原始函数获取响应（预期是一个列表）
        response = func(*args, **kwargs)

        # 确保返回的是列表
        if isinstance(response, list):
            # 遍历列表找到 assistant 角色的内容
            for item in response:
                if isinstance(item, dict) and item.get("role") == "assistant":
                    return item.get("content", "")

            # 没找到 assistant，返回空字符串
            return ""

        # 如果不是列表，返回原始值（或根据需求处理）
        return response

    return wrapper


class Ai_job_demo:
    def __init__(self):
        self.db = EndDemoDatabase(host='localhost', user='root', password='123456')
        self.resume_manager = ResumeManager(self.db.connection)
        self.job_prot = Job_prot(self.db.connection)

        self.appid = config_data.set_LLM_appid  # 填写控制台中获取的 APPID 信息
        self.api_secret = config_data.set_LLM_api_secret  # 填写控制台中获取的 APISecret 信息
        self.api_key = config_data.set_LLM_api_key  # 填写控制台中获取的 APIKey 信息
        self.domain = config_data.set_LLM_domain  # 控制请求的模型版本
        # 服务地址
        self.Spark_url = config_data.set_LLM_Spark_url  # 查看接口文档  https://www.xfyun.cn/doc/spark/X1ws.html
        # 无用的辅助数据
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

    @extract_assistant_content
    def ask_by_pdf_and_job_id(self, pdf_path, job_id):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        print(f'user_pdf_text:{user_pdf_text}')
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = config_data.set_request_str_ask.format(user_pdf_text=user_pdf_text,
                                                                   job_text=job_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def ask_by_pdf_and_job_text(self, pdf_path, job_text):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        first_input_qus = config_data.set_request_str_ask.format(user_pdf_text=user_pdf_text,
                                                                   job_text=job_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def ask_by_user_id_and_job_text(self, user_id, job_text):
        user_text = self.get_user_app_text(user_id)
        first_input_qus = config_data.set_request_str_ask.format(user_pdf_text=user_text,
                                                                   job_text=job_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def ask_by_user_id_and_job_id(self, user_id, job_id):
        user_text = self.get_user_app_text(user_id)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = config_data.set_request_str_ask.format(user_pdf_text=user_text,
                                                                   job_text=job_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def chat(self, user_ask):
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, user_ask)

        return ai_answer

    @extract_assistant_content
    def resume_evalu_by_user_id(self, user_id):
        user_text = self.get_user_app_text(user_id)
        first_input_qus = config_data.set_request_str_resume.format(user_text=user_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def resume_evalu_by_user_pdf(self, pdf_path):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        first_input_qus = config_data.set_request_str_resume.format(user_text=user_pdf_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def success_rate_by_pdf_and_job_id(self, pdf_path, job_id):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = config_data.set_request_str_success.format(user_pdf_text=user_pdf_text,
                                                                    job_text=job_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def success_rate_by_pdf_and_job_text(self, pdf_path, job_text):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        first_input_qus = config_data.set_request_str_sucess.format(user_pdf_text=user_pdf_text,
                                                                    job_text=job_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def success_rate_by_user_id_and_job_text(self, user_id, job_text):
        user_text = self.get_user_app_text(user_id)
        first_input_qus = config_data.set_request_str_success.format(user_pdf_text=user_text,
                                                                    job_text=job_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def success_rate_by_user_id_and_job_id(self, user_id, job_id):
        user_text = self.get_user_app_text(user_id)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = config_data.set_request_str_success.format(user_pdf_text=user_text,
                                                                    job_text=job_text)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def uni_plan_by_pdf_and_job_id(self, pdf_path, job_id,user_grade):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus = config_data.set_request_str_uni.format(user_pdf_text=user_pdf_text,
                                                                 job_text=job_text,
                                                                 user_grade=user_grade)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def uni_plan_by_pdf_and_job_text(self, pdf_path, job_text,user_grade):
        user_pdf_text = self.extract_pdf_text(pdf_path)
        first_input_qus = config_data.set_request_str_uni.format(user_pdf_text=user_pdf_text,
                                                                 job_text=job_text,
                                                                 user_grade=user_grade)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def uni_plan_by_user_id_and_job_text(self, user_id, job_text, user_grade):
        user_text = self.get_user_app_text(user_id)
        first_input_qus = config_data.set_request_str_uni.format(user_pdf_text=user_text,
                                                                 job_text=job_text,
                                                                 user_grade=user_grade)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

    @extract_assistant_content
    def uni_plan_by_user_id_and_job_id(self, user_id, job_id,user_grade):
        user_text = self.get_user_app_text(user_id)
        job_text = self.get_job_text_in_db(job_id)
        first_input_qus =config_data.set_request_str_uni.format(user_pdf_text=user_text,
                                                                 job_text=job_text,
                                                                 user_grade=user_grade)
        ai_answer = main_answer(self.appid, self.api_key, self.api_secret, self.Spark_url, self.domain, first_input_qus)
        return ai_answer

class InterviewManager:
    """面试会话管理器"""

    def __init__(self):
        self.sessions = {}
        self.Ai_job = Ai_job_demo()

    def create_session(self, resume_text: str, job_text: str) -> str:
        """创建新面试会话"""
        session_id = str(uuid.uuid4())

        # 构建初始系统提示
        system_prompt = self._build_interview_prompt(resume_text, job_text)

        self.sessions[session_id] = {
            'messages': system_prompt,
            'history': [],  # 结构化聊天记录
            'stage': 'intro',  # intro, professional, project, comprehensive, qa, ended
            'start_time': datetime.now(),
            'resume_text': resume_text,
            'job_text': job_text,
            'question_count': 0
        }

        return session_id

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def _build_interview_prompt(self, resume_text: str, job_text: str) -> str:
        return config_data.set_interview_start_str.format(resume_text=resume_text,
                                                          job_text=job_text)

    def update_stage(self, session_id):
        """根据问题数量更新面试阶段"""
        session = self.sessions[session_id]
        count = session['question_count']

        if count <= 2:
            session['stage'] = 'intro'
        elif count <= 5:
            session['stage'] = 'professional'
        elif count <= 8:
            session['stage'] = 'project'
        elif count <= 10:
            session['stage'] = 'comprehensive'
        else:
            session['stage'] = 'qa'

        # 在提示词中更新当前阶段
        stage_names = {
            'intro': '第一阶段（自我介绍）',
            'professional': '第二阶段（专业能力）',
            'project': '第三阶段（项目/实践经历）',
            'comprehensive': '第四阶段（综合能力与思维）',
            'qa': '第五阶段（反问环节）'
        }

        return stage_names.get(session['stage'], '面试中')

    def add_to_history(self, session_id, role: str, content: str, audio_url: str = None):
        """添加聊天记录"""
        if session_id in self.sessions:
            self.sessions[session_id]['history'].append({
                'timestamp': datetime.now().isoformat(),
                'role': role,  # 'interviewer' 或 'candidate'
                'content': content,
                'audio_url': audio_url,
                'stage': self.sessions[session_id]['stage']
            })

    def append_message(self, session_id, content: str):
        """追加消息到上下文"""
        if session_id in self.sessions:
            self.sessions[session_id]['messages'] += f"\n{content}"

    def increment_question(self, session_id):
        """增加问题计数"""
        if session_id in self.sessions:
            self.sessions[session_id]['question_count'] += 1
            self.update_stage(session_id)

    def close_session(self, session_id):
        """结束会话"""
        if session_id in self.sessions:
            self.sessions[session_id]['stage'] = 'ended'
            self.sessions[session_id]['end_time'] = datetime.now()

    def end_interview_session(self,session_id, final_user_input):
        """结束面试并生成报告"""
        session = self.get_session(session_id)

        # 记录最后输入
        self.append_message(session_id, f"候选人：{final_user_input}")
        self.add_to_history(session_id, 'candidate', final_user_input)
        self.close_session(session_id)

        # 构建总结提示
        summary_prompt = session['messages'] + config_data.set_interview_end_str

        # 调用AI生成评价
        ai_result = main_answer(
            self.Ai_job.appid, self.Ai_job.api_key, self.Ai_job.api_secret,
            self.Ai_job.Spark_url, self.Ai_job.domain,
            summary_prompt
        )

        # 解析JSON（需要处理可能的格式问题）
        try:
            result_json = self.parse_json_safely(self.extract_ai_text(ai_result))
        except:
            result_json = {
                "overall_score": 75,
                "result": "待定",
                "summary": self.extract_ai_text(ai_result),
                "improvement_suggestions": ["请优化简历内容", "加强项目描述"]
            }

        # 构建详细报告
        report = {
            'session_id': session_id,
            'interview_info': {
                'start_time': session['start_time'].isoformat(),
                'end_time': datetime.now().isoformat(),
                'duration_minutes': int((datetime.now() - session['start_time']).total_seconds() / 60),
                'total_questions': session['question_count']
            },
            'evaluation': result_json,
            'transcript': session['history'],
            'resume_snapshot': session['resume_text'][:500] + '...',
            'job_snapshot': session['job_text'][:300] + '...'
        }

        # 保存报告（可选）
        report_path = os.path.join('reports', f'{session_id}.json')
        os.makedirs('reports', exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return jsonify({
            'is_ended': True,
            'report': report,
            'download_url': f'/api/interview/{session_id}/report'
        })

    # ============== 辅助函数 ==============

    def extract_ai_text(self, ai_response):
        """安全提取AI响应文本 - 只返回最新一轮的助手回复"""
        if isinstance(ai_response, str):
            return ai_response.strip()

        if isinstance(ai_response, list):
            # 过滤出所有助手消息，返回最后一条
            assistant_msgs = [
                msg.get("content", "").strip()
                for msg in ai_response
                if isinstance(msg, dict) and msg.get("role") == "assistant"
            ]
            if assistant_msgs:
                return assistant_msgs[-1]  # 只返回最后一条

        return str(ai_response)

    def speech_to_text(self, audio_path: str) -> str:
        """
        语音识别接口
        需要替换为实际的ASR调用，支持MP3/PCM，60秒以内
        """
        # 这里替换为你的语音识别实现
        # 可以是讯飞、百度、阿里等ASR服务
        try:
            # 示例：使用现有 demo_microphone_recognition 的逻辑改造
            # 或者调用第三方API
            result = self.demo_microphone_recognition_file(audio_path)
            return result
        except Exception as e:
            return f"[语音识别失败: {str(e)}]"

    def generate_tts(self, text: str, output_path: str):
        """
        语音合成并保存
        需要替换为实际的TTS调用
        """
        try:
            # 使用现有的 tts_demo 或改造为文件输出
            self.tts_to_file(text, output_path)
        except Exception as e:
            print(f"TTS生成失败: {e}")

    def parse_json_safely(self, text: str):
        """安全解析JSON，处理可能的Markdown代码块"""
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        return json.loads(text.strip())

    def demo_microphone_recognition_file(self, audio_path=None) -> str:
        """基于文件路径的语音识别（需你实现）"""
        result = str(demo_file_recognition(audio_path))
        return result

    def tts_to_file(self, text: str, output_path: str):
        """文本转语音并保存到文件（需你实现）"""
        tts_demo(text, output_path)

    # 全局配置（实际应从环境变量或配置文件读取）


    # 清理过期会话（可选，使用APScheduler）
    def cleanup_expired_sessions(self):
        """清理超过2小时的会话"""
        current_time = datetime.now()
        expired = []
        for sid, session in self.sessions.items():
            if (current_time - session['start_time']).total_seconds() > 7200:
                expired.append(sid)
        for sid in expired:
            del self.sessions[sid]

    def only_chat(self, text):
        ai_result = main_answer(
            self.Ai_job.appid, self.Ai_job.api_key, self.Ai_job.api_secret,
            self.Ai_job.Spark_url, self.Ai_job.domain,
            text
        )
        return ai_result



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
