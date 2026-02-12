from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError, JWTDecodeError
from flask_sqlalchemy import SQLAlchemy
from datetime import  timedelta
from dotenv import load_dotenv
from sqlalchemy import text, func
from X1_ws import think_speaker
from demo_boss import Ai_job_demo, InterviewManager
import logging
from pathlib import Path
from sql_data_demo import EndDemoDatabase, Job_prot, Job_category_simple, Forum_comments, Sys_user, ResumeManager, ComplaintTypeManager,UserFeedbackManager,UserDeliverJobs,UserFavoriteJobs
from sqlalchemy import text
import hashlib
import re
from datetime import datetime
from flask import request, jsonify, g
from functools import wraps
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import time
import base64
import tempfile
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from  set_up import config

config_data = config()

db = EndDemoDatabase(host=config_data.set_db_host, user=config_data.set_db_user, password=config_data.set_db_password)
job_prot = Job_prot(db.connection)
job_category_simple = Job_category_simple(db.connection)
forum_comments = Forum_comments(db.connection)
sys_user = Sys_user(db.connection)
resume_manager = ResumeManager(db.connection)
type_manager = ComplaintTypeManager(db.connection)
feedback_manager = UserFeedbackManager(db.connection)
deliver_jobs = UserDeliverJobs(db.connection)
favorite_jobs = UserFavoriteJobs(db.connection)

ai_job_demo = Ai_job_demo()
manager = InterviewManager()


think_speaker = think_speaker()

# 假设的JWT密钥和配置
JWT_SECRET = config_data.set_JWT_SECRET
JWT_ALGORITHM = config_data.set_JWT_ALGORITHM

app = Flask(__name__)
CORS(app)  # 允许跨域
UPLOAD_FOLDER = config_data.set_UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 存储聊天记录
chat_history = []
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
CORS(app)  # 允许跨域

# 配置
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / 'uploads' / 'images'
HISTORY_FILE = BASE_DIR / 'data' / 'chat_history.json'

# 确保目录存在
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

# 配置
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB最大上传
# 配置上传文件夹和允许的扩展名
UPLOAD_FOLDER = r'D:\class_demo\uniapp_end_demo\currency_python3_demo\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 初始化历史记录
if not HISTORY_FILE.exists():
    HISTORY_FILE.write_text('[]')



# 加载环境变量
load_dotenv()


# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'mysql+pymysql://root:123456@localhost:3306/boss_job')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 300,
    'pool_pre_ping': True,
}

# 初始化扩展
CORS(app, supports_credentials=True)
jwt = JWTManager(app)
db = SQLAlchemy(app)

# 配置文件上传设置
UPLOAD_FOLDER = tempfile.gettempdir()  # 使用临时目录存储上传的PDF文件
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 辅助函数：验证手机号格式
def validate_mobile(mobile):
    """验证手机号格式"""
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, mobile))


# 辅助函数：验证邮箱格式
def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


# 装饰器：需要登录
def login_required(func):
    """登录验证装饰器 - flask_jwt_extended 版本"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # 验证 token 并获取 payload
            verify_jwt_in_request()
            jwt_data = get_jwt()
            g.user_id = jwt_data.get('user_id') or get_jwt_identity()
            g.user_info = jwt_data

            # 验证用户状态
            user = sys_user.get_user_by_field('user_id', g.user_id)
            if not user:
                return jsonify({
                    'code': 401,
                    'message': '用户不存在',
                    'data': None
                }), 401

            if user['status'] == 0:
                return jsonify({
                    'code': 403,
                    'message': '账号已被禁用',
                    'data': None
                }), 403

            if user['status'] == 3:
                return jsonify({
                    'code': 403,
                    'message': '账号已被锁定',
                    'data': None
                }), 403

        except NoAuthorizationError:
            return jsonify({
                'code': 401,
                'message': '未提供认证令牌',
                'data': None
            }), 401
        except (InvalidHeaderError, JWTDecodeError):
            return jsonify({
                'code': 401,
                'message': '无效的认证令牌',
                'data': None
            }), 401
        except Exception as e:
            return jsonify({
                'code': 500,
                'message': f'认证失败: {str(e)}',
                'data': None
            }), 500

        return func(*args, **kwargs)

    return wrapper

# 错误处理
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'code': 400, 'message': '请求参数错误'}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'code': 401, 'message': '未授权访问'}), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({'code': 404, 'message': '资源不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


# JWT回调函数
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'code': 401, 'message': '令牌已过期'}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'code': 401, 'message': '无效的令牌'}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'code': 401, 'message': '缺少访问令牌'}), 401


# API路由

@app.route('/api/job/Job_List_all',methods=['GET'])
def update_all_job_list():
    '''
    :input:none
    :return: [{id:1, title:......}] # 用于列表中的岗位数据展示的部分数据
    实现默认的列表数据查找，返回全部的岗位数据
    '''
    try:
        list_data = job_prot.fetch_some_job_posts_all()
        return jsonify(list_data),200

    except Exception as e:
        app.logger.error(f'获取全部列表信息失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/job/job_lis_one_type',methods=['POST'])
def update_one_type_job_list():
    '''
    input: category_id: 1001 # 岗位类别，前端需要实现从编码到岗位名的对应，后端返回的岗位类别也是岗位编码。
    :return: [{id:1, title:......}] # 用于列表中的岗位数据展示的部分数据
    实现基于岗位类别的岗位列表数据查找，返回这一类别的岗位的数据
    '''
    try:
        data = request.get_json()
        if not data:
            app.logger.error('未获取到工作分类')
            return jsonify({
                'code':500,
                'message':'服务器内部错误'
            }),500

        category_id = data.get('category_id', '').strip()
        print(type(category_id))
        print(category_id)
        if category_id == '100':
            list_data = job_prot.fetch_one_big_type_job_posts(category_id)
        else:
            list_data = job_prot.fetch_some_job_posts_some(category_id=category_id)
        return jsonify(list_data), 200
    except Exception as e:
        app.logger.error(f'获取一类列表信息失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/job/job_list_two_given',methods=['POST'])
def update_job_list_by_two_given():
    '''
    input: category_id: 1001, emp_type: 1 #emp_type-》1=全职 2=兼职 3=实习
    :return: [{id:1, title:......}] # 用于列表中的岗位数据展示的部分数据
    实现基于大类+小类的数据查找，返回这一入全职——开发工程师类的岗位数据
    '''
    try:
        data = request.get_json()
        if not data:
            app.logger.error('未获取到两个工作分类')
            return jsonify({
                'code':500,
                'message':'服务器内部错误'
            }),500
        category_id = data.get('category_id', '').strip()
        emp_type = data.get('emp_type', '').strip()
        list_data = job_prot.fetch_job_list_by_two_given(category_id=category_id, emp_type=emp_type)
        return jsonify(list_data), 200
    except Exception as e:
        app.logger.error(f'获取全职-综合列表信息失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/job/job_search',methods=['POST'])
def job_search():
    '''
    input: user_input :'开发工程师' #用户在搜索框中的输入内容
    :return: [{id:1, title:......}]# 用于列表中的岗位数据展示的部分数据
    实现搜索功能
    '''
    try:
        data = request.get_json()
        if not data:
            app.logger.error('用户输入为空')
            return jsonify({
                'code': 400,
                'message': '用户输入为空'
            }), 400
        user_input = data.get('user_input', '').strip()
        list_data = job_prot.search_job_by_user_input(user_input=user_input)
        print(list_data)
        return jsonify(list_data),200
    except Exception as e:
        app.logger.error(f'搜索列表信息失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/job/job_details',methods=['POST'])
def job_details():
    '''
    input: id:1 #岗位的唯一id
    :return: [{id:1, title:......}]# 用于岗位详情页中的岗位数据展示的全部数据
    返回数据库中该岗位的全部数据，用于详情页的数据在展示
    '''
    try:
        data = request.get_json()
        if not data:
            app.logger.error('前端岗位id信息为空')
            return jsonify({
                'code': 400,
                'message': '前端岗位id信息为空'
            }), 400
        id = data.get('id', '').strip()
        job_data = job_prot.fetch_one_job_all_data_posts(ones_id=id)
        return jsonify(job_data),200
    except Exception as e:
        app.logger.error(f'岗位详情信息失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500


@app.route('/api/job/job_add', methods=['POST'])
def job_add():
    '''
    发布新的职位信息，提示该函数执行完后应立刻向后端获取新的职位列表来更新前端的信息
    input: boss_job_id Boss平台ID,
           title 岗位名称,
           company_id 公司ID,
           city_id 城市ID,
           category_id 职位分类ID,
           emp_type 雇佣类型(1=全职 2=兼职 3=实习),
           salary_min 最低薪资,
           salary_max 最高薪资,
           salary_desc 薪资描述,
           edu_req 学历要求,
           exp_req 经验要求,
           district 区域,
           address 地址,
           recruiter_id 招聘者ID,
           description 职位描述,
           require_list 要求列表(JSON数组),
           welfare_list 福利列表(JSON数组),
           publish_time 发布时间,
           refresh_time 刷新时间,
           status 职位状态
    return：返回插入的职位ID
    '''
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据为空'
            }), 400

        # 检查必要字段
        required_fields = ['boss_job_id', 'title', 'company_id', 'city_id', 'category_id']
        for field in required_fields:
            value = data.get(field)
            if value is None or value == '':
                print(f'后端接受到的{field}信息为空')
                return jsonify({
                    'code': 300,
                    'message': f'后端接受到的{field}信息为空'
                }), 300

        # 获取参数并处理空值
        boss_job_id = str(data.get('boss_job_id', '')).strip()
        title = str(data.get('title', '')).strip()
        company_id = int(data.get('company_id', 0))
        city_id = int(data.get('city_id', 0))
        category_id = int(data.get('category_id', 0))

        # 处理整数参数
        emp_type = int(data.get('emp_type', 1)) if data.get('emp_type') not in [None, ''] else 1
        recruiter_id = int(data.get('recruiter_id')) if data.get('recruiter_id') not in [None, ''] else None
        status = int(data.get('status', 1)) if data.get('status') not in [None, ''] else 1

        # 处理小数参数
        salary_min = float(data.get('salary_min')) if data.get('salary_min') not in [None, ''] else None
        salary_max = float(data.get('salary_max')) if data.get('salary_max') not in [None, ''] else None

        # 处理字符串参数
        district = str(data.get('district', '')).strip() if data.get('district') not in [None, ''] else None
        address = str(data.get('address', '')).strip() if data.get('address') not in [None, ''] else None
        salary_desc = str(data.get('salary_desc', '')).strip() if data.get('salary_desc') not in [None, ''] else None
        edu_req = str(data.get('edu_req', '')).strip() if data.get('edu_req') not in [None, ''] else None
        exp_req = str(data.get('exp_req', '')).strip() if data.get('exp_req') not in [None, ''] else None
        description = str(data.get('description', '')).strip() if data.get('description') not in [None, ''] else None

        # 处理JSON数组
        require_list = data.get('require_list')
        welfare_list = data.get('welfare_list')

        # 处理时间参数
        publish_time = data.get('publish_time')
        refresh_time = data.get('refresh_time')

        # 调用数据库操作
        job_id = job_prot.insert_job_post(
            boss_job_id=boss_job_id,
            title=title,
            company_id=company_id,
            city_id=city_id,
            category_id=category_id,
            emp_type=emp_type,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_desc=salary_desc,
            edu_req=edu_req,
            exp_req=exp_req,
            district=district,
            address=address,
            recruiter_id=recruiter_id,
            description=description,
            require_list=require_list,
            welfare_list=welfare_list,
            publish_time=publish_time,
            refresh_time=refresh_time,
            status=status
        )

        if job_id:
            return jsonify({
                "code": 200,
                "message": "职位发布成功",
                "data": {
                    "job_id": job_id
                }
            }), 200
        else:
            return jsonify({
                "code": 500,
                "message": "职位发布失败"
            }), 500

    except ValueError as ve:
        app.logger.error(f'参数类型错误：{ve}')
        return jsonify({
            'code': 400,
            'message': '参数类型错误，请检查输入格式'
        }), 400
    except Exception as e:
        app.logger.error(f'职位发布失败：{e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500


@app.route('/api/job_intro/job_intro_list', methods=['GET'])
def intro_list():
    '''
    查询所有岗位分类
    input ：none
    :return: [{id:1...}..]
    '''
    try:
        job_intro_list = job_category_simple.job_intro_list()
        return jsonify(job_intro_list), 200
    except Exception as e:
        app.logger.error(f'岗位分类以及介绍查询失败：{e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/forum/all_forum_data', methods=['GET'])
def forum_all_data():
    '''
    查询所有的评论
    input:none
    :return: [{id:1...}..]
    '''
    try:
        forum_all_data = forum_comments.forum_all()
        return jsonify(forum_all_data), 200
    except Exception as e:
        app.logger.error(f'论坛全部记录查询失败：{e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/forum/forum_one_category', methods=['POST'])
def forum_one_category_data():
    '''
    查询某一岗位分类下的评论
    input: category_id岗位id
    return：[{id:1...}..]
    '''
    try:
        data = request.get_json()
        if not data:
            app.logger.error('前端职位分类id信息为空')
            return jsonify({
                'code': 400,
                'message': '前端职位分类id信息为空'
            }), 400
        category_id = data.get('category_id', '').strip()
        forum_one_category_data_1 = forum_comments.forum_one_category(category_id)
        return jsonify(forum_one_category_data_1), 200
    except Exception as e:
        app.logger.error(f'论坛类别记录查询失败：{e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/forum/forum_all_first_talk', methods=['GET'])
def forum_all_first_talk_data():
    '''
    查询所有一级评论
        input:none
        return：[{id:1...}..]
    '''
    try:
        forum_data = forum_comments.forum_all_first_talk()
        return jsonify(forum_data), 200
    except Exception as e:
        app.logger.error(f'全部评论查询失败：{e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/forum/forums_back', methods=['POST'])
def forums_back_data():
    '''
    查询该评论的所有回复（二级评论）
        input:parent_id 被回复评论的id
        return：[{id:1...}..]
    '''
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '被回复评论id信息为空'
            }), 400
        parent_id = data.get('parent_id', '').strip()
        forum_data = forum_comments.forum_talks_back(parent_id)
        return jsonify(forum_data),200
    except Exception as e:
        app.logger.error(f'评论回复查询失败：{e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/forum/forums_add', methods=['POST'])
def forum_add():
    '''
    发表新的评论，提示该函数执行完后应立刻向后端获取新的怕评论来更新前端的信息
        input:category_id职位分类id,
              user_id发布评论的用户的id,
              parent_id所回复的评论的id，,
              content用户的评论内容,
              level，评论层级 1：一级评论，2：二级评论即回复,
              sort_order展示层级，是前端展示时候的有用数据
        return：none
    '''
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '用户输入的是空信息信息为空'
            }), 400
        for key in data.keys():
            if key != 'parent_id':
                value = data.get(key)
                if value == None:
                    print(f'后端接受到的{key}信息为空')
                    return jsonify({
                        'code': 300,
                        'message': f'后端接受到的{key}信息为空'
                    }), 300

        category_id = data.get('category_id','').strip()
        user_id = data.get('user_id','').strip()
        parent_id = data.get('parent_id','').strip()
        content = data.get('content','').strip()
        level = data.get('level','').strip()
        sort_order = data.get('sort_order','').strip()
        forum_comments.forum_add(category_id=category_id,
                                 user_id=user_id,
                                 parent_id=parent_id,
                                 content=content,
                                 level=level,
                                 sort_order=sort_order)
        return jsonify([{
            "code": 200
        }])
    except Exception as e:
        app.logger.error(f'评论发布失败：{e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/forum/forum_delete', methods=['POST'])
def forum_delete():
    '''
    删除评论
        input:id被删除评论的id
        return：none
    '''
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '被删除评论的id为空'
            }), 400
        id = data.get('id','').strip()
        forum_comments.forum_delete(id)
        return jsonify([{
            "code": 200
        }])
    except Exception as e:
        app.logger.error(f'评论删除失败：{e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/forum/forum_count', methods=['POST'])
def forum_count_data():
    '''
    计数工具
        input:  switch, all 返回全部的评论的数量
                        category 返回某一类岗位下的评论数
                        back 返回该条评论的回复数
                        user 返回该用户共发表的评论数
                category_id,
                parent_id,
                user_id
        return：'forum_count_num': forum_count_num,
                'code': 200,
                'message': '成功'
    '''
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '计数信息为空'
            }), 400
        switch = data.get('switch', '').strip()
        if not switch:
            return jsonify({
                'code': 300,
                'message': '计数选择为空'
            }), 300
        category_id = data.get('category_id', '').strip()
        parent_id = data.get('parent_id', '').strip()
        user_id = data.get('user_id', '').strip()
        forum_count_num = forum_comments.forum_count_all(switch=switch,
                                                         category_id=category_id,
                                                         parent_id=parent_id,
                                                         user_id=user_id)
        if forum_count_num == 'error':
            return jsonify({
                'code': 300,
                'message': 'switch数据传输出错'
            }), 300

        forum_data = {
            'forum_count_num': forum_count_num,
            'code': 200,
            'message': '成功'
        }
        return jsonify(forum_data)
    except Exception as e:
        app.logger.error(f'评论删除失败：{e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/user/register', methods=['POST'])
def user_register():
    """用户注册"""
    try:
        data = request.get_json()

        # 验证必填字段
        required_fields = ['mobile', 'password', 'sms_code']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'message': f'缺少必填字段: {field}',
                    'data': None
                }), 400

        # 验证手机号格式
        if not validate_mobile(data['mobile']):
            return jsonify({
                'code': 400,
                'message': '手机号格式不正确',
                'data': None
            }), 400

        # 验证密码强度
        password = data['password']
        if len(password) < 8:
            return jsonify({
                'code': 400,
                'message': '密码长度至少8位',
                'data': None
            }), 400

        # TODO: 验证短信验证码
        # 这里需要实现短信验证码验证逻辑
        sms_code_valid = True  # 假设验证通过
        if not sms_code_valid:
            return jsonify({
                'code': 400,
                'message': '短信验证码错误或已过期',
                'data': None
            }), 400

        # 检查手机号是否已注册
        exists = sys_user.check_user_exists(mobile=data['mobile'])
        if exists:
            return jsonify({
                'code': 400,
                'message': '该手机号已注册',
                'data': None
            }), 400

        # 生成用户ID（这里简化为时间戳，实际应用中应该使用雪花算法）
        user_id = int(datetime.now().timestamp() * 1000)

        # 密码加密
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # 构建用户数据
        user_data = {
            'user_id': user_id,
            'mobile': data['mobile'],
            'password_hash': password_hash,
            'status': 2,  # 未激活状态
            'register_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # 可选字段
        if 'email' in data and data['email']:
            if not validate_email(data['email']):
                return jsonify({
                    'code': 400,
                    'message': '邮箱格式不正确',
                    'data': None
                }), 400
            user_data['email'] = data['email']

        # 创建用户
        created_id = sys_user.create_user(user_data)

        if created_id:
            return jsonify({
                'code': 200,
                'message': '注册成功',
                'data': {
                    'user_id': user_id,
                    'mobile': data['mobile'],
                    'register_time': user_data['register_time']
                }
            })
        else:
            return jsonify({
                'code': 500,
                'message': '注册失败',
                'data': None
            }), 500

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'注册异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/login', methods=['POST'])
def user_login():
    """用户登录"""
    try:
        data = request.get_json()

        # 验证必填字段
        if 'mobile' not in data or not data['mobile']:
            return jsonify({
                'code': 400,
                'message': '请输入手机号',
                'data': None
            }), 400

        if 'password' not in data or not data['password']:
            return jsonify({
                'code': 400,
                'message': '请输入密码',
                'data': None
            }), 400

        # 获取设备信息
        device_model = request.headers.get('X-Device-Model', 'Unknown')
        device_type = request.headers.get('X-Device-Type', '0')
        login_ip = request.remote_addr

        # 查询用户
        print(data['mobile'])
        user = sys_user.get_user_by_field('mobile', data['mobile'])

        if not user:
            return jsonify({
                'code': 400,
                'message': '用户不存在',
                'data': None
            }), 400

        # 验证密码
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        if password_hash != user['password_hash']:
            return jsonify({
                'code': 400,
                'message': '密码错误',
                'data': None
            }), 400

        # 验证账号状态
        if user['status'] == 0:
            return jsonify({
                'code': 403,
                'message': '账号已被禁用',
                'data': None
            }), 403

        if user['status'] == 3:
            return jsonify({
                'code': 403,
                'message': '账号已被锁定',
                'data': None
            }), 403

        # 更新登录信息
        sys_user.update_last_login(
            user['user_id'],
            login_ip,
            device_model,
            device_type
        )

        # 生成JWT令牌
        token_payload = {
            'user_id': user['user_id'],
            'mobile': user['mobile'],
            'exp': datetime.now().timestamp() + 7 * 24 * 3600  # 7天过期
        }


        # token = jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        access_token = create_access_token(identity=str(user['user_id']))

        # 返回用户信息（排除敏感信息）
        user_info = {
            'user_id': user['user_id'],
            'mobile': user['mobile'],
            'email': user['email'],
            'real_name': user['real_name'],
            'avatar_url': user['avatar_url'],
            'status': user['status'],
            'job_status': user['job_status'],
            'last_login_time': user['last_login_time']
        }

        print('shi-1')
        print(user_info)
        print('shi-1')

        return jsonify({
            'code': 200,
            'message': '登录成功',
            'data': {
                'token': access_token,
                'user_info': user_info
            }
        })

    except Exception as e:
        app.logger.error(f'登录异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'登录异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/profile', methods=['GET'])
@login_required
def get_user_profile():
    """获取当前用户个人信息"""
    try:
        user_id = g.user_id
        # 查询用户信息
        user = sys_user.get_user_by_field('user_id', user_id)
        if not user:
            return jsonify({
                'code': 404,
                'message': '用户不存在',
                'data': None
            }), 404

        # 组织返回数据（排除敏感信息）
        profile_data = {
            'user_id': user['user_id'],
            'mobile': user['mobile'],
            'email': user['email'],
            'real_name': user['real_name'],
            'gender': user['gender'],
            'birth_date': user['birth_date'],
            'education_level': user['education_level'],
            'major': user['major'],
            'enrollment_year': user['enrollment_year'],
            'graduation_year': user['graduation_year'],
            'bio': user['bio'],
            'avatar_url': user['avatar_url'],
            'status': user['status'],
            'job_status': user['job_status'],
            'register_time': user['register_time'],
            'last_login_time': user['last_login_time']
        }


        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': profile_data
        })

    except Exception as e:
        print(f'获取个人信息异常: {str(e)}')
        app.logger.error(f'获取个人信息异常: {str(e)}')
        return jsonify({
            'code': 500,
            'message': f'获取个人信息异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/profile', methods=['PUT'])
@login_required
def update_user_profile():
    """更新个人信息"""
    try:
        user_id = g.user_id
        data = request.get_json()

        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据不能为空',
                'data': None
            }), 400

        # 不允许更新的字段
        protected_fields = ['user_id', 'mobile', 'password_hash', 'status', 'register_time', 'created_at', 'updated_at',
                            'deleted_at', 'is_deleted']

        # 过滤出允许更新的字段
        update_data = {}
        for key, value in data.items():
            if key not in protected_fields and value is not None:
                update_data[key] = value

        # 验证邮箱格式（如果提供）
        if 'email' in update_data and update_data['email']:
            if not validate_email(update_data['email']):
                return jsonify({
                    'code': 400,
                    'message': '邮箱格式不正确',
                    'data': None
                }), 400

        # 检查邮箱是否已被其他用户使用
        if 'email' in update_data and update_data['email']:
            exists = sys_user.check_user_exists(email=update_data['email'], exclude_user_id=user_id)
            if exists:
                return jsonify({
                    'code': 400,
                    'message': '该邮箱已被其他用户使用',
                    'data': None
                }), 400

        # 更新用户信息
        success = sys_user.update_user_profile(user_id, update_data)

        if success:
            # 重新查询更新后的信息
            user = sys_user.get_user_by_field('user_id', user_id)
            updated_profile = {
                'real_name': user['real_name'],
                'email': user['email'],
                'gender': user['gender'],
                'birth_date': user['birth_date'],
                'education_level': user['education_level'],
                'major': user['major'],
                'bio': user['bio'],
                'avatar_url': user['avatar_url'],
                'updated_at': user['updated_at']
            }

            return jsonify({
                'code': 200,
                'message': '更新成功',
                'data': updated_profile
            })
        else:
            return jsonify({
                'code': 500,
                'message': '更新失败',
                'data': None
            }), 500

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新个人信息异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/password', methods=['PUT'])
@login_required
def update_password():
    """修改密码"""
    try:
        user_id = g.user_id
        data = request.get_json()

        # 验证必填字段
        required_fields = ['old_password', 'new_password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'message': f'缺少必填字段: {field}',
                    'data': None
                }), 400

        old_password = data['old_password']
        new_password = data['new_password']

        # 验证新密码强度
        if len(new_password) < 8:
            return jsonify({
                'code': 400,
                'message': '新密码长度至少8位',
                'data': None
            }), 400

        # 查询用户信息
        user = sys_user.get_user_by_field('user_id', user_id)

        if not user:
            return jsonify({
                'code': 404,
                'message': '用户不存在',
                'data': None
            }), 404

        # 验证旧密码
        old_password_hash = hashlib.sha256(old_password.encode()).hexdigest()
        if old_password_hash != user['password_hash']:
            return jsonify({
                'code': 400,
                'message': '原密码错误',
                'data': None
            }), 400

        # 生成新密码哈希
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()

        # 更新密码
        update_data = {
            'password_hash': new_password_hash
        }

        success = sys_user.update_user_profile(user_id, update_data)

        if success:
            return jsonify({
                'code': 200,
                'message': '密码修改成功',
                'data': {
                    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        else:
            return jsonify({
                'code': 500,
                'message': '密码修改失败',
                'data': None
            }), 500

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'修改密码异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/avatar', methods=['POST'])
@login_required
def update_avatar():
    """更新头像"""
    try:
        user_id = g.user_id
        data = request.get_json()

        if 'avatar_url' not in data or not data['avatar_url']:
            return jsonify({
                'code': 400,
                'message': '缺少头像URL',
                'data': None
            }), 400

        avatar_url = data['avatar_url']

        # 更新头像
        update_data = {
            'avatar_url': avatar_url
        }

        success = sys_user.update_user_profile(user_id, update_data)

        if success:
            return jsonify({
                'code': 200,
                'message': '头像更新成功',
                'data': {
                    'avatar_url': avatar_url,
                    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        else:
            return jsonify({
                'code': 500,
                'message': '头像更新失败',
                'data': None
            }), 500

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'更新头像异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/status', methods=['GET'])
@login_required
def get_user_status():
    """获取用户状态"""
    try:
        user_id = g.user_id

        # 查询用户状态
        user = sys_user.get_user_by_field('user_id', user_id)

        if not user:
            return jsonify({
                'code': 404,
                'message': '用户不存在',
                'data': None
            }), 404

        status_info = {
            'user_id': user['user_id'],
            'status': user['status'],
            'status_text': {
                0: '禁用',
                1: '正常',
                2: '未激活',
                3: '锁定'
            }.get(user['status'], '未知'),
            'job_status': user['job_status'],
            'job_status_text': {
                0: '待业',
                1: '实习中',
                2: '应届求职'
            }.get(user['job_status'], '未知'),
            'last_login_time': user['last_login_time'],
            'last_device_type': user['last_device_type']
        }

        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': status_info
        })

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取用户状态异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/logout', methods=['POST'])
@login_required
def user_logout():
    """用户登出"""
    try:
        # 这里可以记录登出日志，或使当前token失效
        # 实际应用中可能需要将token加入黑名单

        return jsonify({
            'code': 200,
            'message': '登出成功',
            'data': {
                'logout_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'登出异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/search', methods=['GET'])
def search_users():
    """搜索用户（公开接口，返回有限信息）"""
    try:
        keyword = request.args.get('keyword', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))

        # 搜索用户
        result = sys_user.search_users(
            keyword=keyword if keyword else None,
            status=1,  # 只搜索正常状态的用户
            page=page,
            page_size=page_size
        )
        print(result)

        # 过滤敏感信息，只返回公开信息
        public_users = []
        for user in result['users']:
            public_users.append({
                'user_id': user['user_id'],
                'real_name': user['real_name'],
                'avatar_url': user['avatar_url'],
                'bio': user['bio'],
                'education_level': user['education_level'],
                'major': user['major'],
                'graduation_year': user['graduation_year'],
                'job_status': user['job_status']
            })

        return jsonify({
            'code': 200,
            'message': '搜索成功',
            'data': {
                'users': public_users,
                'total': result['total'],
                'page': result['page'],
                'page_size': result['page_size'],
                'total_pages': result['total_pages']
            }
        })

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'搜索用户异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/public/<user_id>', methods=['GET'])
def get_public_profile(user_id):
    """获取用户公开信息"""
    try:
        # 查询用户信息（只返回正常状态的用户）
        user = sys_user.get_user_by_field('user_id', user_id)

        if not user or user['status'] != 1:  # 只返回正常状态的用户
            return jsonify({
                'code': 404,
                'message': '用户不存在或不可见',
                'data': None
            }), 404

        # 返回公开信息
        public_profile = {
            'user_id': user['user_id'],
            'real_name': user['real_name'],
            'avatar_url': user['avatar_url'],
            'bio': user['bio'],
            'education_level': user['education_level'],
            'major': user['major'],
            'enrollment_year': user['enrollment_year'],
            'graduation_year': user['graduation_year'],
            'job_status': user['job_status']
        }

        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': public_profile
        })

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取公开信息异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/user/statistics', methods=['GET'])
@login_required
def get_user_statistics():
    """获取用户统计信息（仅管理员或用户自己可见）"""
    try:
        user_id = g.user_id

        # 这里可以根据需要统计各种数据
        # 示例：统计各类用户数量

        total_users = sys_user.user_count_all('all')
        active_users = sys_user.user_count_all('active')
        disabled_users = sys_user.user_count_all('status', status=0)

        statistics = {
            'total_users': total_users,
            'active_users': active_users,
            'disabled_users': disabled_users,
            'job_seekers': sys_user.user_count_all('job_status', job_status=0),
            'interns': sys_user.user_count_all('job_status', job_status=1),
            'fresh_graduates': sys_user.user_count_all('job_status', job_status=2),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': statistics
        })

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取统计信息异常: {str(e)}',
            'data': None
        }), 500

# 简历基本信息路由
@app.route('/api/resume/basic', methods=['POST'])
@jwt_required()
def create_or_update_resume():
    """创建或更新简历基本信息"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # 验证必填字段
        required_fields = ['real_name', 'phone', 'email', 'education_level', 'school_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'message': f'{field}为必填字段',
                    'data': None
                }), 400

        # 检查是否已有简历
        existing_resume = resume_manager.resumes.get_resume_by_user(user_id)

        if existing_resume:
            # 更新简历
            success = resume_manager.resumes.update_resume(user_id, data)
            if success:
                return jsonify({
                    'code': 200,
                    'message': '简历更新成功',
                    'data': {'resume_id': existing_resume['id']}
                })
            else:
                return jsonify({
                    'code': 500,
                    'message': '简历更新失败',
                    'data': None
                }), 500
        else:
            # 创建简历
            resume_id = resume_manager.resumes.create_resume(user_id, data)
            if resume_id:
                return jsonify({
                    'code': 200,
                    'message': '简历创建成功',
                    'data': {'resume_id': resume_id}
                })
            else:
                return jsonify({
                    'code': 500,
                    'message': '简历创建失败，可能已存在简历',
                    'data': None
                }), 500

    except Exception as e:
        current_app.logger.error(f'创建或更新简历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/basic', methods=['GET'])
@jwt_required()
def get_resume():
    """获取简历基本信息"""
    try:
        user_id = get_jwt_identity()
        

        resume = resume_manager.resumes.get_resume_by_user(user_id)

        if not resume:
            return jsonify({
                'code': 404,
                'message': '未找到简历信息',
                'data': None
            }), 404

        return jsonify({
            'code': 200,
            'message': '获取简历成功',
            'data': resume
        })

    except Exception as e:
        current_app.logger.error(f'获取简历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/basic', methods=['DELETE'])
@jwt_required()
def delete_resume():
    """删除简历"""
    try:
        user_id = get_jwt_identity()
        

        success = resume_manager.resumes.delete_resume(user_id)

        if success:
            return jsonify({
                'code': 200,
                'message': '简历删除成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 500,
                'message': '简历删除失败',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'删除简历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


# 证书管理路由
@app.route('/api/resume/certificates', methods=['POST'])
@jwt_required()
def add_certificate():
    """添加证书"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # 验证必填字段
        required_fields = ['cert_name', 'cert_type']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'message': f'{field}为必填字段',
                    'data': None
                }), 400

        
        cert_id = resume_manager.certificates.add_certificate(user_id, data)

        if cert_id:
            return jsonify({
                'code': 200,
                'message': '证书添加成功',
                'data': {'cert_id': cert_id}
            })
        else:
            return jsonify({
                'code': 500,
                'message': '证书添加失败，请先创建简历',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'添加证书异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/certificates', methods=['GET'])
@jwt_required()
def get_certificates():
    """获取用户证书列表"""
    try:
        user_id = get_jwt_identity()
        cert_type = request.args.get('cert_type')

        
        certificates = resume_manager.certificates.get_user_certificates(user_id, cert_type)

        return jsonify({
            'code': 200,
            'message': '获取证书列表成功',
            'data': certificates
        })

    except Exception as e:
        current_app.logger.error(f'获取证书列表异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/certificates/<int:cert_id>', methods=['PUT'])
@jwt_required()
def update_certificate(cert_id):
    """更新证书信息"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        
        success = resume_manager.certificates.update_certificate(cert_id, user_id, data)

        if success:
            return jsonify({
                'code': 200,
                'message': '证书更新成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 500,
                'message': '证书更新失败',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'更新证书异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/api/resume/certificates/<int:cert_id>', methods=['DELETE'])
@jwt_required()
def delete_certificate(cert_id):
    """删除证书"""
    try:
        user_id = get_jwt_identity()

        
        success = resume_manager.certificates.delete_certificate(cert_id, user_id)

        if success:
            return jsonify({
                'code': 200,
                'message': '证书删除成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 500,
                'message': '证书删除失败',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'删除证书异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


# 校园经历路由
@app.route('/api/resume/campus-experience', methods=['POST'])
@jwt_required()
def upsert_campus_experience():
    """更新或创建校园经历"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        
        experience_id = resume_manager.campus_experiences.upsert_campus_experience(user_id, data)

        if experience_id:
            return jsonify({
                'code': 200,
                'message': '校园经历保存成功',
                'data': {'experience_id': experience_id}
            })
        else:
            return jsonify({
                'code': 500,
                'message': '校园经历保存失败',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'保存校园经历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/campus-experience', methods=['GET'])
@jwt_required()
def get_campus_experience():
    """获取校园经历"""
    try:
        user_id = get_jwt_identity()

        
        experience = resume_manager.campus_experiences.get_campus_experience(user_id)

        if experience:
            return jsonify({
                'code': 200,
                'message': '获取校园经历成功',
                'data': experience
            })
        else:
            return jsonify({
                'code': 404,
                'message': '未找到校园经历',
                'data': None
            }), 404

    except Exception as e:
        current_app.logger.error(f'获取校园经历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


# 实习经历路由
@app.route('/api/resume/internships', methods=['POST'])
@jwt_required()
def add_internship():
    """添加实习经历"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # 验证必填字段
        required_fields = ['company_name', 'position', 'start_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'message': f'{field}为必填字段',
                    'data': None
                }), 400

        
        internship_id = resume_manager.internships.add_internship(user_id, data)

        if internship_id:
            return jsonify({
                'code': 200,
                'message': '实习经历添加成功',
                'data': {'internship_id': internship_id}
            })
        else:
            return jsonify({
                'code': 500,
                'message': '实习经历添加失败',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'添加实习经历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/internships', methods=['GET'])
@jwt_required()
def get_internships():
    """获取实习经历列表"""
    try:
        user_id = get_jwt_identity()

        
        internships = resume_manager.internships.get_user_internships(user_id)

        return jsonify({
            'code': 200,
            'message': '获取实习经历成功',
            'data': internships
        })

    except Exception as e:
        current_app.logger.error(f'获取实习经历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/internships/<int:internship_id>', methods=['PUT'])
@jwt_required()
def update_internship(internship_id):
    """更新实习经历"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        
        success = resume_manager.internships.update_internship(internship_id, user_id, data)

        if success:
            return jsonify({
                'code': 200,
                'message': '实习经历更新成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 500,
                'message': '实习经历更新失败',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'更新实习经历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/internships/<int:internship_id>', methods=['DELETE'])
@jwt_required()
def delete_internship(internship_id):
    """删除实习经历"""
    try:
        user_id = get_jwt_identity()

        
        success = resume_manager.internships.delete_internship(internship_id, user_id)

        if success:
            return jsonify({
                'code': 200,
                'message': '实习经历删除成功',
                'data': None
            })
        else:
            return jsonify({
                'code': 500,
                'message': '实习经历删除失败',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'删除实习经历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


# 求职意向路由
@app.route('/api/resume/job-intention', methods=['POST'])
@jwt_required()
def upsert_job_intention():
    """更新或创建求职意向"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # 验证必填字段
        required_fields = ['target_industries', 'target_positions', 'salary_min', 'salary_max']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'message': f'{field}为必填字段',
                    'data': None
                }), 400

        
        intention_id = resume_manager.job_intentions.upsert_job_intention(user_id, data)

        if intention_id:
            return jsonify({
                'code': 200,
                'message': '求职意向保存成功',
                'data': {'intention_id': intention_id}
            })
        else:
            return jsonify({
                'code': 500,
                'message': '求职意向保存失败',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'保存求职意向异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/job-intention', methods=['GET'])
@jwt_required()
def get_job_intention():
    """获取求职意向"""
    try:
        user_id = get_jwt_identity()

        
        intention = resume_manager.job_intentions.get_job_intention(user_id)

        if intention:
            return jsonify({
                'code': 200,
                'message': '获取求职意向成功',
                'data': intention
            })
        else:
            return jsonify({
                'code': 404,
                'message': '未找到求职意向',
                'data': None
            }), 404

    except Exception as e:
        current_app.logger.error(f'获取求职意向异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


# 求职偏好路由
@app.route('/api/resume/job-preference', methods=['POST'])
@jwt_required()
def upsert_job_preference():
    """更新或创建求职偏好"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        
        preference_id = resume_manager.job_preferences.upsert_job_preference(user_id, data)

        if preference_id:
            return jsonify({
                'code': 200,
                'message': '求职偏好保存成功',
                'data': {'preference_id': preference_id}
            })
        else:
            return jsonify({
                'code': 500,
                'message': '求职偏好保存失败',
                'data': None
            }), 500

    except Exception as e:
        current_app.logger.error(f'保存求职偏好异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/resume/job-preference', methods=['GET'])
@jwt_required()
def get_job_preference():
    """获取求职偏好"""
    try:
        user_id = get_jwt_identity()

        
        preference = resume_manager.job_preferences.get_job_preference(user_id)

        if preference:
            return jsonify({
                'code': 200,
                'message': '获取求职偏好成功',
                'data': preference
            })
        else:
            return jsonify({
                'code': 404,
                'message': '未找到求职偏好',
                'data': None
            }), 404

    except Exception as e:
        current_app.logger.error(f'获取求职偏好异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


# 完整简历获取
@app.route('/api/resume/complete', methods=['GET'])
@jwt_required()
def get_complete_resume():
    """获取用户完整的简历信息"""
    try:
        user_id = get_jwt_identity()

        
        complete_resume = resume_manager.get_complete_resume(user_id)

        # 检查是否有基本信息
        if not complete_resume.get('basic_info'):
            return jsonify({
                'code': 404,
                'message': '请先创建简历基本信息',
                'data': None
            }), 404

        return jsonify({
            'code': 200,
            'message': '获取完整简历成功',
            'data': complete_resume
        })

    except Exception as e:
        current_app.logger.error(f'获取完整简历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


# 简历搜索（需要管理员权限）
@app.route('/api/resume/search', methods=['POST'])
@jwt_required()
def search_resumes():
    """搜索简历（需要管理员权限）"""
    try:
        # 这里可以添加管理员权限验证
        # 比如检查用户角色是否为管理员

        data = request.get_json()

        
        resumes = resume_manager.search_resumes(data)

        return jsonify({
            'code': 200,
            'message': '搜索简历成功',
            'data': {
                'resumes': resumes,
                'total': len(resumes)
            }
        })

    except Exception as e:
        current_app.logger.error(f'搜索简历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


# 简历统计
@app.route('/api/resume/stats', methods=['GET'])
@jwt_required()
def get_resume_stats():
    """获取简历统计信息（需要管理员权限）"""
    try:
        # 这里可以添加管理员权限验证

        
        stats = resume_manager.get_resume_stats()

        # 获取证书统计
        cert_stats = resume_manager.certificates.get_certificate_stats(get_jwt_identity())

        # 获取实习统计
        internship_stats = resume_manager.internships.get_internship_stats(get_jwt_identity())

        # 获取行业分布
        industry_distribution = resume_manager.internships.get_industry_distribution()

        # 获取期望城市分布
        city_distribution = resume_manager.job_intentions.get_city_distribution()

        # 获取薪资统计
        salary_stats = resume_manager.job_intentions.get_salary_range_stats()

        # 获取工作偏好统计
        work_preference_stats = resume_manager.job_preferences.get_work_preference_stats()

        complete_stats = {
            **stats,
            'cert_stats': cert_stats,
            'internship_stats': internship_stats,
            'industry_distribution': industry_distribution,
            'city_distribution': city_distribution,
            'salary_stats': salary_stats,
            'work_preference_stats': work_preference_stats
        }

        return jsonify({
            'code': 200,
            'message': '获取统计信息成功',
            'data': complete_stats
        })

    except Exception as e:
        current_app.logger.error(f'获取简历统计异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


# 批量操作（需要管理员权限）
@app.route('/api/resume/batch-update', methods=['POST'])
@jwt_required()
def batch_update_resumes():
    """批量更新简历（需要管理员权限）"""
    try:
        # 这里可以添加管理员权限验证

        data = request.get_json()

        if 'update_data' not in data or 'conditions' not in data:
            return jsonify({
                'code': 400,
                'message': 'update_data和conditions为必填字段',
                'data': None
            }), 400

        
        count = resume_manager.batch_update_resumes(data['update_data'], data['conditions'])

        return jsonify({
            'code': 200,
            'message': f'批量更新成功，共更新{count}条记录',
            'data': {'affected_rows': count}
        })

    except Exception as e:
        current_app.logger.error(f'批量更新简历异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500

def admin_required(f):
    """管理员权限装饰器"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 验证管理员身份
        is_admin = request.headers.get('X-Admin-Token') or g.get('is_admin')
        if not is_admin:
            return jsonify({'code': 403, 'message': '无权限操作'}), 403
        return f(*args, **kwargs)

    return decorated_function


# ==================== 投诉类型相关接口 ====================

@app.route('/api/complaint/types', methods=['GET'])
def get_complaint_types():
    '''
    :input: none
    :return: [{type_code: 1, type_name: "功能", sort_order: 0}]
    获取所有启用的投诉类型列表
    '''
    try:
        types_data = type_manager.get_all_types()

        if types_data is None:
            return jsonify({
                'code': 500,
                'message': '获取投诉类型失败'
            }), 500

        return jsonify({
            'code': 200,
            'data': types_data,
            'message': 'success'
        }), 200

    except Exception as e:
        print(f'获取投诉类型列表失败: {e}')
        app.logger.error(f'获取投诉类型列表失败: {e}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500


# ==================== 用户反馈相关接口（用户端） ====================

@app.route('/api/feedback/list', methods=['GET'])
@login_required
def get_user_feedback_list():
    '''
    :input:
        - query参数: is_resolved(可选,0/1), page(默认1), limit(默认20)
    :return: [{id: 1, complaint_type: 2, description: "...", create_time: "..."}]
    获取当前登录用户的反馈列表
    '''
    try:
        # 获取查询参数
        is_resolved = request.args.get('is_resolved', type=int)
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        offset = (page - 1) * limit

        ##  feedback_manager = UserFeedbackManager(db.connection)
        list_data = feedback_manager.get_feedback_list(
            user_id=g.user_id,
            is_resolved=is_resolved,
            limit=limit,
            offset=offset
        )

        if list_data is None:
            return jsonify({
                'code': 500,
                'message': '获取反馈列表失败'
            }), 500

        return jsonify({
            'code': 200,
            'data': list_data,
            'message': 'success'
        }), 200

    except Exception as e:
        app.logger.error(f'获取用户反馈列表失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500


@app.route('/api/feedback/detail/<int:feedback_id>', methods=['GET'])
@login_required
def get_feedback_detail(feedback_id):
    '''
    :input: feedback_id (路径参数)
    :return: {id: 1, complaint_type: 2, description: "...", feedback_content: "..."}
    获取单条反馈详情（只能查看自己的）
    '''
    try:
        ##  feedback_manager = UserFeedbackManager(db.connection)
        detail_data = feedback_manager.get_feedback_by_id(feedback_id)

        if detail_data is None:
            return jsonify({
                'code': 404,
                'message': '反馈不存在'
            }), 404

        # 权限校验：只能查看自己的反馈
        if detail_data['user_id'] != g.user_id:
            return jsonify({
                'code': 403,
                'message': '无权查看该反馈'
            }), 403

        return jsonify({
            'code': 200,
            'data': detail_data,
            'message': 'success'
        }), 200

    except Exception as e:
        app.logger.error(f'获取反馈详情失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500


@app.route('/api/feedback/submit', methods=['POST'])
@login_required
def submit_feedback():
    '''
    :input: {
        "complaint_type": 2,        # 必填，投诉类型代码
        "description": "BUG描述",    # 必填，投诉内容
        "image_url_1": "...",       # 可选，图片1
        "image_url_2": "...",       # 可选，图片2
        "image_url_3": "...",       # 可选，图片3
        "priority": 1               # 可选，优先级1-3，默认1
    }
    :return: {feedback_id: 123}
    提交用户反馈/投诉
    '''
    try:
        data = request.get_json()

        # 参数校验
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求参数不能为空'
            }), 400

        complaint_type = data.get('complaint_type')
        description = data.get('description', '').strip()

        if not complaint_type:
            return jsonify({
                'code': 400,
                'message': '投诉类型不能为空'
            }), 400

        if not description or len(description) < 10:
            return jsonify({
                'code': 400,
                'message': '投诉描述不能少于10个字符'
            }), 400

        if len(description) > 2000:
            return jsonify({
                'code': 400,
                'message': '投诉描述不能超过2000个字符'
            }), 400

        # 验证投诉类型是否有效
        # type_manager = ComplaintTypeManager(db.connection)
        type_info = type_manager.get_type_by_code(complaint_type)
        if not type_info or type_info['is_active'] != 1:
            return jsonify({
                'code': 400,
                'message': '无效的投诉类型'
            }), 400

        # 提交反馈
        ##  feedback_manager = UserFeedbackManager(db.connection)
        feedback_id = feedback_manager.add_feedback(
            user_id=g.user_id,
            complaint_type=complaint_type,
            description=description,
            image_url_1=data.get('image_url_1'),
            image_url_2=data.get('image_url_2'),
            image_url_3=data.get('image_url_3'),
            priority=data.get('priority', 1)
        )

        if feedback_id is None:
            return jsonify({
                'code': 500,
                'message': '提交反馈失败'
            }), 500

        return jsonify({
            'code': 200,
            'data': {'feedback_id': feedback_id},
            'message': '反馈提交成功'
        }), 200

    except Exception as e:
        app.logger.error(f'提交用户反馈失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500


@app.route('/api/feedback/update/<int:feedback_id>', methods=['PUT'])
@login_required
def update_user_feedback(feedback_id):
    '''
    :input: {
        "description": "更新后的描述",   # 可选
        "priority": 2                    # 可选
    }
    :return: {success: true}
    更新未解决的反馈（只能修改自己的未解决反馈）
    '''
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求参数不能为空'
            }), 400

        # 先查询确认权限和状态
        ##  feedback_manager = UserFeedbackManager(db.connection)
        detail = feedback_manager.get_feedback_by_id(feedback_id)

        if not detail:
            return jsonify({
                'code': 404,
                'message': '反馈不存在'
            }), 404

        if detail['user_id'] != g.user_id:
            return jsonify({
                'code': 403,
                'message': '无权修改该反馈'
            }), 403

        if detail['is_resolved'] == 1:
            return jsonify({
                'code': 400,
                'message': '已解决的反馈不能修改'
            }), 400

        # 执行更新
        description = data.get('description', '').strip() if data.get('description') else None
        priority = data.get('priority')

        success = feedback_manager.update_feedback(
            feedback_id=feedback_id,
            description=description,
            priority=priority
        )

        if not success:
            return jsonify({
                'code': 500,
                'message': '更新失败'
            }), 500

        return jsonify({
            'code': 200,
            'data': {'success': True},
            'message': '更新成功'
        }), 200

    except Exception as e:
        app.logger.error(f'更新用户反馈失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500


# ==================== 管理后台接口（管理员端） ====================

@app.route('/api/admin/feedback/list', methods=['GET'])
@admin_required
def admin_get_feedback_list():
    '''
    :input:
        - query参数:
            user_id(可选),
            complaint_type(可选),
            is_resolved(可选,0/1),
            page(默认1),
            limit(默认20)
    :return: [{id: 1, user_id: 100, complaint_type_name: "BUG", ...}]
    管理员获取全部反馈列表（带筛选）
    '''
    try:
        # 获取查询参数
        user_id = request.args.get('user_id', type=int)
        complaint_type = request.args.get('complaint_type', type=int)
        is_resolved = request.args.get('is_resolved', type=int)
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        offset = (page - 1) * limit

       #  feedback_manager = UserFeedbackManager(db.connection)
        list_data = feedback_manager.get_feedback_list(
            user_id=user_id,
            complaint_type=complaint_type,
            is_resolved=is_resolved,
            limit=limit,
            offset=offset
        )

        if list_data is None:
            return jsonify({
                'code': 500,
                'message': '获取反馈列表失败'
            }), 500

        return jsonify({
            'code': 200,
            'data': list_data,
            'message': 'success'
        }), 200

    except Exception as e:
        app.logger.error(f'管理员获取反馈列表失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500


@app.route('/api/admin/feedback/resolve/<int:feedback_id>', methods=['POST'])
@admin_required
def admin_resolve_feedback(feedback_id):
    '''
    :input: {
        "feedback_content": "问题已修复，请更新APP"   # 必填，回复内容
    }
    :return: {success: true}
    管理员解决反馈并回复
    '''
    try:
        data = request.get_json()

        if not data or not data.get('feedback_content', '').strip():
            return jsonify({
                'code': 400,
                'message': '回复内容不能为空'
            }), 400

        feedback_content = data.get('feedback_content', '').strip()

        if len(feedback_content) > 1000:
            return jsonify({
                'code': 400,
                'message': '回复内容不能超过1000个字符'
            }), 400

        # 获取管理员ID（从g或token中解析）
        resolved_by = g.get('admin_id', 1)  # 默认值，实际应从登录信息获取

       #  feedback_manager = UserFeedbackManager(db.connection)
        success = feedback_manager.resolve_feedback(
            feedback_id=feedback_id,
            resolved_by=resolved_by,
            feedback_content=feedback_content
        )

        if not success:
            return jsonify({
                'code': 400,
                'message': '解决反馈失败，可能反馈不存在或已解决'
            }), 400

        return jsonify({
            'code': 200,
            'data': {'success': True},
            'message': '反馈已解决'
        }), 200

    except Exception as e:
        app.logger.error(f'管理员解决反馈失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500


@app.route('/api/admin/feedback/detail/<int:feedback_id>', methods=['GET'])
@admin_required
def admin_get_feedback_detail(feedback_id):
    '''
    :input: feedback_id (路径参数)
    :return: 反馈详情（包含用户信息）
    管理员查看反馈详情
    '''
    try:
       #  feedback_manager = UserFeedbackManager(db.connection)
        detail_data = feedback_manager.get_feedback_by_id(feedback_id)

        if detail_data is None:
            return jsonify({
                'code': 404,
                'message': '反馈不存在'
            }), 404

        return jsonify({
            'code': 200,
            'data': detail_data,
            'message': 'success'
        }), 200

    except Exception as e:
        app.logger.error(f'管理员获取反馈详情失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

@app.route('/api/job/favorite/add', methods=['POST'])
def add_favorite():
    """
    添加岗位收藏
    input: {
        "user_id": 1,
        "job_id": 1001,
        "remarks": "备注信息（可选）"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求参数不能为空'}), 400

        user_id = data.get('user_id')
        job_id = data.get('job_id')
        remarks = data.get('remarks', None)

        if not user_id or not job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 job_id 不能为空'}), 400

        # 调用收藏类方法
        result = favorite_jobs.add_favorite(user_id, job_id, remarks)

        if result['success']:
            return jsonify({
                'code': 200,
                'message': result['message'],
                'data': {'id': result.get('id')}
            }), 200
        else:
            return jsonify({
                'code': 400,
                'message': result['message']
            }), 400

    except Exception as e:
        app.logger.error(f'添加收藏失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/favorite/cancel', methods=['POST'])
def cancel_favorite():
    """
    取消岗位收藏（软删除）
    input: {
        "user_id": 1,
        "boss_job_id": 1001
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求参数不能为空'}), 400

        user_id = data.get('user_id')
        boss_job_id = data.get('boss_job_id')

        if not user_id or not boss_job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 boss_job_id 不能为空'}), 400

        result = favorite_jobs.cancel_favorite(user_id, boss_job_id)

        if result['success']:
            return jsonify({
                'code': 200,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'code': 404,
                'message': result['message']
            }), 404

    except Exception as e:
        app.logger.error(f'取消收藏失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/favorite/list', methods=['GET'])
def get_user_favorites():
    """
    获取用户收藏列表
    query params:
        user_id: 用户ID（必填）
        include_canceled: 是否包含已取消的（可选，默认false）0或1
    """
    try:
        user_id = request.args.get('user_id', type=int)
        include_canceled = request.args.get('include_canceled', '0') == '1'

        if not user_id:
            return jsonify({'code': 400, 'message': 'user_id 不能为空'}), 400

        result = favorite_jobs.get_user_favorites(user_id, include_canceled)

        if result is not None:
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'data': result
            }), 200
        else:
            return jsonify({
                'code': 500,
                'message': '获取收藏列表失败'
            }), 500

    except Exception as e:
        app.logger.error(f'获取收藏列表失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/favorite/check', methods=['GET'])
def check_is_favorite():
    """
    检查用户是否已收藏某岗位
    query params:
        user_id: 用户ID
        boss_job_id: 岗位ID
    """
    try:
        user_id = request.args.get('user_id', type=int)
        boss_job_id = request.args.get('boss_job_id', type=int)

        if not user_id or not boss_job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 boss_job_id 不能为空'}), 400

        is_favorite = favorite_jobs.check_is_favorite(user_id, boss_job_id)

        return jsonify({
            'code': 200,
            'message': '查询成功',
            'data': {'is_favorite': is_favorite}
        }), 200

    except Exception as e:
        app.logger.error(f'检查收藏状态失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/favorite/update_remarks', methods=['POST'])
def update_favorite_remarks():
    """
    更新收藏备注
    input: {
        "user_id": 1,
        "boss_job_id": 1001,
        "remarks": "新的备注内容"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求参数不能为空'}), 400

        user_id = data.get('user_id')
        boss_job_id = data.get('boss_job_id')
        remarks = data.get('remarks', '')

        if not user_id or not boss_job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 boss_job_id 不能为空'}), 400

        result = favorite_jobs.update_remarks(user_id, boss_job_id, remarks)

        if result['success']:
            return jsonify({
                'code': 200,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'code': 404,
                'message': result['message']
            }), 404

    except Exception as e:
        app.logger.error(f'更新收藏备注失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/favorite/detail', methods=['GET'])
def get_favorite_detail():
    """
    获取单条收藏详情
    query params:
        user_id: 用户ID
        boss_job_id: 岗位ID
    """
    try:
        user_id = request.args.get('user_id', type=int)
        boss_job_id = request.args.get('boss_job_id', type=int)

        if not user_id or not boss_job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 boss_job_id 不能为空'}), 400

        result = favorite_jobs.get_favorite_detail(user_id, boss_job_id)

        if result:
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'data': result
            }), 200
        else:
            return jsonify({
                'code': 404,
                'message': '未找到收藏记录'
            }), 404

    except Exception as e:
        app.logger.error(f'获取收藏详情失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/favorite/batch_cancel', methods=['POST'])
def batch_cancel_favorites():
    """
    批量取消收藏
    input: {
        "user_id": 1,
        "boss_job_id_list": [1001, 1002, 1003]
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求参数不能为空'}), 400

        user_id = data.get('user_id')
        boss_job_id_list = data.get('boss_job_id_list', [])

        if not user_id:
            return jsonify({'code': 400, 'message': 'user_id 不能为空'}), 400

        if not boss_job_id_list or not isinstance(boss_job_id_list, list):
            return jsonify({'code': 400, 'message': 'boss_job_id_list 必须是数组且不能为空'}), 400

        result = favorite_jobs.batch_cancel_favorites(user_id, boss_job_id_list)

        if result['success']:
            return jsonify({
                'code': 200,
                'message': result['message'],
                'data': {'affected_rows': result.get('affected_rows', 0)}
            }), 200
        else:
            return jsonify({
                'code': 400,
                'message': result['message']
            }), 400

    except Exception as e:
        app.logger.error(f'批量取消收藏失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


# ==================== 投递功能路由 ====================

@app.route('/api/job/deliver/add', methods=['POST'])
def add_deliver():
    """
    添加岗位投递
    input: {
        "user_id": 1,
        "job_id": 1001,
        "remarks": "备注信息（可选）"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求参数不能为空'}), 400

        user_id = data.get('user_id')
        job_id = data.get('job_id')
        remarks = data.get('remarks', None)

        if not user_id or not job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 job_id 不能为空'}), 400

        result = deliver_jobs.add_deliver(user_id, job_id, remarks)

        if result['success']:
            return jsonify({
                'code': 200,
                'message': result['message'],
                'data': {'id': result.get('id')}
            }), 200
        else:
            return jsonify({
                'code': 400,
                'message': result['message']
            }), 400

    except Exception as e:
        app.logger.error(f'添加投递失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/deliver/cancel', methods=['POST'])
def cancel_deliver():
    """
    取消岗位投递（软删除）
    input: {
        "user_id": 1,
        "boss_job_id": 1001
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求参数不能为空'}), 400

        user_id = data.get('user_id')
        boss_job_id = data.get('boss_job_id')

        if not user_id or not boss_job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 boss_job_id 不能为空'}), 400

        result = deliver_jobs.cancel_deliver(user_id, boss_job_id)

        if result['success']:
            return jsonify({
                'code': 200,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'code': 404,
                'message': result['message']
            }), 404

    except Exception as e:
        app.logger.error(f'取消投递失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/deliver/list', methods=['GET'])
def get_user_delivers():
    """
    获取用户投递列表
    query params:
        user_id: 用户ID（必填）
        include_canceled: 是否包含已取消的（可选，默认false）0或1
    """
    try:
        user_id = request.args.get('user_id', type=int)
        include_canceled = request.args.get('include_canceled', '0') == '1'

        if not user_id:
            return jsonify({'code': 400, 'message': 'user_id 不能为空'}), 400

        result = deliver_jobs.get_user_delivers(user_id, include_canceled)

        if result is not None:
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'data': result
            }), 200
        else:
            return jsonify({
                'code': 500,
                'message': '获取投递列表失败'
            }), 500

    except Exception as e:
        app.logger.error(f'获取投递列表失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/deliver/check', methods=['GET'])
def check_is_deliver():
    """
    检查用户是否已投递某岗位
    query params:
        user_id: 用户ID
        boss_job_id: 岗位ID
    """
    try:
        user_id = request.args.get('user_id', type=int)
        boss_job_id = request.args.get('boss_job_id', type=int)

        if not user_id or not boss_job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 boss_job_id 不能为空'}), 400

        is_deliver = deliver_jobs.check_is_deliver(user_id, boss_job_id)

        return jsonify({
            'code': 200,
            'message': '查询成功',
            'data': {'is_deliver': is_deliver}
        }), 200

    except Exception as e:
        app.logger.error(f'检查投递状态失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/deliver/update_remarks', methods=['POST'])
def update_deliver_remarks():
    """
    更新投递备注
    input: {
        "user_id": 1,
        "boss_job_id": 1001,
        "remarks": "新的备注内容"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求参数不能为空'}), 400

        user_id = data.get('user_id')
        boss_job_id = data.get('boss_job_id')
        remarks = data.get('remarks', '')

        if not user_id or not boss_job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 boss_job_id 不能为空'}), 400

        result = deliver_jobs.update_remarks(user_id, boss_job_id, remarks)

        if result['success']:
            return jsonify({
                'code': 200,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'code': 404,
                'message': result['message']
            }), 404

    except Exception as e:
        app.logger.error(f'更新投递备注失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/deliver/detail', methods=['GET'])
def get_deliver_detail():
    """
    获取单条投递详情
    query params:
        user_id: 用户ID
        boss_job_id: 岗位ID
    """
    try:
        user_id = request.args.get('user_id', type=int)
        boss_job_id = request.args.get('boss_job_id', type=int)

        if not user_id or not boss_job_id:
            return jsonify({'code': 400, 'message': 'user_id 和 boss_job_id 不能为空'}), 400

        result = deliver_jobs.get_deliver_detail(user_id, boss_job_id)

        if result:
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'data': result
            }), 200
        else:
            return jsonify({
                'code': 404,
                'message': '未找到投递记录'
            }), 404

    except Exception as e:
        app.logger.error(f'获取投递详情失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


@app.route('/api/job/deliver/batch_cancel', methods=['POST'])
def batch_cancel_delivers():
    """
    批量取消投递
    input: {
        "user_id": 1,
        "boss_job_id_list": [1001, 1002, 1003]
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'message': '请求参数不能为空'}), 400

        user_id = data.get('user_id')
        boss_job_id_list = data.get('boss_job_id_list', [])

        if not user_id:
            return jsonify({'code': 400, 'message': 'user_id 不能为空'}), 400

        if not boss_job_id_list or not isinstance(boss_job_id_list, list):
            return jsonify({'code': 400, 'message': 'boss_job_id_list 必须是数组且不能为空'}), 400

        result = deliver_jobs.batch_cancel_delivers(user_id, boss_job_id_list)

        if result['success']:
            return jsonify({
                'code': 200,
                'message': result['message'],
                'data': {'affected_rows': result.get('affected_rows', 0)}
            }), 200
        else:
            return jsonify({
                'code': 400,
                'message': result['message']
            }), 400

    except Exception as e:
        app.logger.error(f'批量取消投递失败: {str(e)}')
        return jsonify({'code': 500, 'message': '服务器内部错误'}), 500



def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file():
    """保存上传的PDF文件并返回文件路径"""
    if 'pdf_file' not in request.files:
        return None, 'No PDF file uploaded'

    file = request.files['pdf_file']
    if file.filename == '':
        return None, 'No file selected'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath, None
    else:
        return None, 'File type not allowed. Only PDF files are accepted.'


@app.route('/api/ai/ask_by_pdf_job_id', methods=['POST'])
@jwt_required()
def api_ask_by_pdf_and_job_id():
    """使用PDF文件和职位ID进行分析"""
    try:
        # 检查文件上传
        if 'pdf_file' not in request.files:
            return jsonify({
                'code': 400,
                'message': '请上传PDF简历文件',
                'data': None
            }), 400

        # 获取job_id
        job_id = request.form.get('job_id')
        if not job_id:
            return jsonify({
                'code': 400,
                'message': '请提供职位ID',
                'data': None
            }), 400

        # 保存PDF文件
        pdf_path, error = save_uploaded_file()
        if error:
            return jsonify({
                'code': 400,
                'message': error,
                'data': None
            }), 400

        # 调用AI分析函数
        ai_answer = ai_job_demo.ask_by_pdf_and_job_id(pdf_path, job_id)

        # 清理临时文件
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except:
            pass

        return jsonify({
            'code': 200,
            'message': '分析成功',
            'data': {
                'analysis': ai_answer
            }
        }),200

    except Exception as e:
        current_app.logger.error(f'PDF+职位ID分析异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/ask_by_pdf_job_text', methods=['POST'])
@jwt_required()
def api_ask_by_pdf_and_job_text():
    """使用PDF文件和职位文本进行分析"""
    try:
        # 检查文件上传
        if 'pdf_file' not in request.files:
            return jsonify({
                'code': 400,
                'message': '请上传PDF简历文件',
                'data': None
            }), 400

        # 获取job_text
        job_text = request.form.get('job_text')
        if not job_text:
            return jsonify({
                'code': 400,
                'message': '请提供职位描述文本',
                'data': None
            }), 400

        # 保存PDF文件
        pdf_path, error = save_uploaded_file()
        if error:
            return jsonify({
                'code': 400,
                'message': error,
                'data': None
            }), 400

        # 调用AI分析函数
        ai_answer = ai_job_demo.ask_by_pdf_and_job_text(pdf_path, job_text)

        # 清理临时文件
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except:
            pass

        return jsonify({
            'code': 200,
            'message': '分析成功',
            'data': {
                'analysis': ai_answer
            }
        }),200

    except Exception as e:
        current_app.logger.error(f'PDF+职位文本分析异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/ask_by_user_job_text', methods=['POST'])
@jwt_required()
def api_ask_by_user_id_and_job_text():
    """使用用户ID和职位文本进行分析"""
    try:
        user_id = get_jwt_identity()

        # 获取job_text
        data = request.get_json()
        if not data or 'job_text' not in data:
            return jsonify({
                'code': 400,
                'message': '请提供职位描述文本',
                'data': None
            }), 400

        job_text = data['job_text']

        # 调用AI分析函数
        ai_answer = ai_job_demo.ask_by_user_id_and_job_text(user_id, job_text)

        return jsonify({
            'code': 200,
            'message': '分析成功',
            'data': {
                'analysis': ai_answer
            }
        }),200

    except Exception as e:
        current_app.logger.error(f'用户ID+职位文本分析异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/ask_by_user_job_id', methods=['GET'])
@jwt_required()
def api_ask_by_user_id_and_job_id():
    """使用用户ID和职位ID进行分析"""
    try:
        user_id = get_jwt_identity()

        # 获取job_id
        job_id = request.args.get('job_id')
        if not job_id:
            return jsonify({
                'code': 400,
                'message': '请提供职位ID',
                'data': None
            }), 400

        # 调用AI分析函数
        ai_answer = ai_job_demo.ask_by_user_id_and_job_id(user_id, job_id)

        return jsonify({
            'code': 200,
            'message': '分析成功',
            'data': {
                'analysis': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'用户ID+职位ID分析异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/chat', methods=['POST'])
@jwt_required()
def api_chat():
    """AI对话接口"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'code': 400,
                'message': '请输入对话内容',
                'data': None
            }), 400

        user_message = data['message']

        # 调用AI对话函数
        ai_answer = ai_job_demo.chat(user_message)

        return jsonify({
            'code': 200,
            'message': '对话成功',
            'data': {
                'response': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'AI对话异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/resume_evaluation', methods=['GET'])
@jwt_required()
def api_resume_evaluation_by_user_id():
    """简历评估（使用用户ID）"""
    try:
        user_id = get_jwt_identity()

        # 调用简历评估函数
        ai_answer = ai_job_demo.resume_evalu_by_user_id(user_id)

        return jsonify({
            'code': 200,
            'message': '评估成功',
            'data': {
                'evaluation': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'简历评估异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/resume_evaluation_text', methods=['POST'])
@jwt_required()
def api_resume_evaluation_by_text():
    """简历评估（使用简历文本）"""
    try:
        # 检查文件上传
        if 'pdf_file' not in request.files:
            return jsonify({
                'code': 400,
                'message': '请上传PDF简历文件',
                'data': None
            }), 400

        # 保存PDF文件
        pdf_path, error = save_uploaded_file()

        # 调用简历评估函数
        ai_answer = ai_job_demo.resume_evalu_by_user_pdf(pdf_path)

        return jsonify({
            'code': 200,
            'message': '评估成功',
            'data': {
                'evaluation': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'简历文本评估异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/success_rate_pdf_job_id', methods=['POST'])
@jwt_required()
def api_success_rate_by_pdf_and_job_id():
    """成功率分析（PDF+职位ID）"""
    try:
        # 检查文件上传
        if 'pdf_file' not in request.files:
            return jsonify({
                'code': 400,
                'message': '请上传PDF简历文件',
                'data': None
            }), 400

        # 获取job_id
        job_id = request.form.get('job_id')
        if not job_id:
            return jsonify({
                'code': 400,
                'message': '请提供职位ID',
                'data': None
            }), 400

        # 保存PDF文件
        pdf_path, error = save_uploaded_file()
        if error:
            return jsonify({
                'code': 400,
                'message': error,
                'data': None
            }), 400

        # 调用成功率分析函数
        ai_answer = ai_job_demo.success_rate_by_pdf_and_job_id(pdf_path, job_id)

        # 清理临时文件
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except:
            pass

        return jsonify({
            'code': 200,
            'message': '分析成功',
            'data': {
                'analysis': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'PDF+职位ID成功率分析异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/success_rate_pdf_job_text', methods=['POST'])
@jwt_required()
def api_success_rate_by_pdf_and_job_text():
    """成功率分析（PDF+职位文本）"""
    try:
        # 检查文件上传
        if 'pdf_file' not in request.files:
            return jsonify({
                'code': 400,
                'message': '请上传PDF简历文件',
                'data': None
            }), 400

        # 获取job_text
        job_text = request.form.get('job_text')
        if not job_text:
            return jsonify({
                'code': 400,
                'message': '请提供职位描述文本',
                'data': None
            }), 400

        # 保存PDF文件
        pdf_path, error = save_uploaded_file()
        if error:
            return jsonify({
                'code': 400,
                'message': error,
                'data': None
            }), 400

        # 调用成功率分析函数
        ai_answer = ai_job_demo.success_rate_by_pdf_and_job_text(pdf_path, job_text)

        # 清理临时文件
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except:
            pass

        return jsonify({
            'code': 200,
            'message': '分析成功',
            'data': {
                'analysis': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'PDF+职位文本成功率分析异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/success_rate_user_job_text', methods=['POST'])
@jwt_required()
def api_success_rate_by_user_id_and_job_text():
    """成功率分析（用户ID+职位文本）"""
    try:
        user_id = get_jwt_identity()

        # 获取job_text
        data = request.get_json()
        if not data or 'job_text' not in data:
            return jsonify({
                'code': 400,
                'message': '请提供职位描述文本',
                'data': None
            }), 400

        job_text = data['job_text']

        # 调用成功率分析函数
        ai_answer = ai_job_demo.success_rate_by_user_id_and_job_text(user_id, job_text)

        return jsonify({
            'code': 200,
            'message': '分析成功',
            'data': {
                'analysis': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'用户ID+职位文本成功率分析异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/success_rate_user_job_id', methods=['GET'])
@jwt_required()
def api_success_rate_by_user_id_and_job_id():
    """成功率分析（用户ID+职位ID）"""
    try:
        user_id = get_jwt_identity()

        # 获取job_id
        job_id = request.args.get('job_id')
        if not job_id:
            return jsonify({
                'code': 400,
                'message': '请提供职位ID',
                'data': None
            }), 400

        # 调用成功率分析函数
        ai_answer = ai_job_demo.success_rate_by_user_id_and_job_id(user_id, job_id)

        return jsonify({
            'code': 200,
            'message': '分析成功',
            'data': {
                'analysis': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'用户ID+职位ID成功率分析异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/university_plan_pdf_job_id', methods=['POST'])
@jwt_required()
def api_university_plan_by_pdf_and_job_id():
    """大学生活规划（PDF+职位ID）"""
    try:
        # 检查文件上传
        if 'pdf_file' not in request.files:
            return jsonify({
                'code': 400,
                'message': '请上传PDF简历文件',
                'data': None
            }), 400

        # 获取job_id和user_grade
        job_id = request.form.get('job_id')
        user_grade = request.form.get('user_grade')

        if not job_id:
            return jsonify({
                'code': 400,
                'message': '请提供职位ID',
                'data': None
            }), 400

        if not user_grade:
            return jsonify({
                'code': 400,
                'message': '请提供学生年级',
                'data': None
            }), 400

        # 保存PDF文件
        pdf_path, error = save_uploaded_file()
        if error:
            return jsonify({
                'code': 400,
                'message': error,
                'data': None
            }), 400

        # 调用大学生活规划函数
        ai_answer = ai_job_demo.uni_plan_by_pdf_and_job_id(pdf_path, job_id, user_grade)

        # 清理临时文件
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except:
            pass

        return jsonify({
            'code': 200,
            'message': '规划生成成功',
            'data': {
                'plan': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'PDF+职位ID大学生活规划异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/university_plan_pdf_job_text', methods=['POST'])
@jwt_required()
def api_university_plan_by_pdf_and_job_text():
    """大学生活规划（PDF+职位文本）"""
    try:
        # 检查文件上传
        if 'pdf_file' not in request.files:
            return jsonify({
                'code': 400,
                'message': '请上传PDF简历文件',
                'data': None
            }), 400

        # 获取job_text和user_grade
        job_text = request.form.get('job_text')
        user_grade = request.form.get('user_grade')

        if not job_text:
            return jsonify({
                'code': 400,
                'message': '请提供职位描述文本',
                'data': None
            }), 400

        if not user_grade:
            return jsonify({
                'code': 400,
                'message': '请提供学生年级',
                'data': None
            }), 400

        # 保存PDF文件
        pdf_path, error = save_uploaded_file()
        if error:
            return jsonify({
                'code': 400,
                'message': error,
                'data': None
            }), 400

        # 调用大学生活规划函数
        ai_answer = ai_job_demo.uni_plan_by_pdf_and_job_text(pdf_path, job_text, user_grade)

        # 清理临时文件
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except:
            pass

        return jsonify({
            'code': 200,
            'message': '规划生成成功',
            'data': {
                'plan': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'PDF+职位文本大学生活规划异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/university_plan_user_job_text', methods=['POST'])
@jwt_required()
def api_university_plan_by_user_id_and_job_text():
    """大学生活规划（用户ID+职位文本）"""
    try:
        user_id = get_jwt_identity()

        # 获取job_text和user_grade
        data = request.get_json()
        if not data or 'job_text' not in data or 'user_grade' not in data:
            return jsonify({
                'code': 400,
                'message': '请提供职位描述文本和学生年级',
                'data': None
            }), 400

        job_text = data['job_text']
        user_grade = data['user_grade']

        # 调用大学生活规划函数
        ai_answer = ai_job_demo.uni_plan_by_user_id_and_job_text(user_id, job_text, user_grade)

        return jsonify({
            'code': 200,
            'message': '规划生成成功',
            'data': {
                'plan': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'用户ID+职位文本大学生活规划异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500


@app.route('/api/ai/university_plan_user_job_id', methods=['GET'])
@jwt_required()
def api_university_plan_by_user_id_and_job_id():
    """大学生活规划（用户ID+职位ID）"""
    try:
        user_id = get_jwt_identity()

        # 获取job_id和user_grade
        job_id = request.args.get('job_id')
        user_grade = request.args.get('user_grade')

        if not job_id:
            return jsonify({
                'code': 400,
                'message': '请提供职位ID',
                'data': None
            }), 400

        if not user_grade:
            return jsonify({
                'code': 400,
                'message': '请提供学生年级',
                'data': None
            }), 400

        # 调用大学生活规划函数
        ai_answer = ai_job_demo.uni_plan_by_user_id_and_job_id(user_id, job_id, user_grade)

        return jsonify({
            'code': 200,
            'message': '规划生成成功',
            'data': {
                'plan': ai_answer
            }
        })

    except Exception as e:
        current_app.logger.error(f'用户ID+职位ID大学生活规划异常：{e}')
        return jsonify({
            'code': 500,
            'message': f'服务器异常: {str(e)}',
            'data': None
        }), 500

# ==================== 1. 文本 + 文本（原有功能保留）====================

@app.route('/api/ai/interview/start/text', methods=['POST'])
def start_interview_text():
    """
    方式1：简历文本 + 岗位文本
    POST /api/ai/interview/start/text

    Body: {
        "resume_text": "简历内容...",
        "job_text": "岗位描述..."
    }
    """
    try:
        data = request.get_json() or {}
        resume_text = data.get('resume_text', '').strip()
        job_text = data.get('job_text', '').strip()

        if not resume_text or not job_text:
            return jsonify({'error': 'resume_text 和 job_text 不能为空'}), 400

        return _create_interview_session(resume_text, job_text, 'text', 'text')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== 2. PDF 文件 + 岗位文本 ====================

@app.route('/api/ai/interview/start/pdf-text', methods=['POST'])
def start_interview_pdf_text():
    """
    方式2：PDF简历 + 岗位文本
    POST /api/ai/interview/start/pdf-text

    Body: {
        "resume_file": "base64编码的PDF",
        "job_text": "岗位描述..."
    }
    """
    try:
        data = request.get_json() or {}

        # 解析PDF
        resume_text, error = _parse_pdf_base64(data.get('resume_file'))
        if error:
            return jsonify({'error': error}), 400

        job_text = data.get('job_text', '').strip()
        if not job_text:
            return jsonify({'error': 'job_text 不能为空'}), 400

        return _create_interview_session(resume_text, job_text, 'pdf', 'text')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== 3. PDF 文件 + 岗位ID ====================

@app.route('/api/ai/interview/start/pdf-jobid', methods=['POST'])
def start_interview_pdf_jobid():
    """
    方式3：PDF简历 + 岗位ID
    POST /api/ai/interview/start/pdf-jobid

    Body: {
        "resume_file": "base64编码的PDF",
        "job_id": "123"
    }
    """
    try:
        data = request.get_json() or {}

        # 解析PDF
        resume_text, error = _parse_pdf_base64(data.get('resume_file'))
        if error:
            return jsonify({'error': error}), 400

        # 从数据库获取岗位
        job_id = data.get('job_id')
        job_text, error = _get_job_from_db(job_id)
        if error:
            return jsonify({'error': error}), 400

        return _create_interview_session(resume_text, job_text, 'pdf', 'database', job_id=job_id)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== 4. 用户ID + 岗位ID（全数据库） ====================

@app.route('/api/ai/interview/start/userid-jobid', methods=['POST'])
def start_interview_userid_jobid():
    """
    方式4：用户ID + 岗位ID（全部从数据库获取）
    POST /api/ai/interview/start/userid-jobid

    Body: {
        "user_id": "user_123",
        "job_id": "job_456"
    }
    """
    try:
        data = request.get_json() or {}

        # 从数据库获取简历
        user_id = data.get('user_id')
        resume_text, error = _get_resume_from_db(user_id)
        if error:
            return jsonify({'error': error}), 400

        # 从数据库获取岗位
        job_id = data.get('job_id')
        job_text, error = _get_job_from_db(job_id)
        if error:
            return jsonify({'error': error}), 400

        return _create_interview_session(
            resume_text, job_text, 'database', 'database',
            user_id=user_id, job_id=job_id
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== 5. 用户ID + 岗位文本 ====================

@app.route('/api/ai/interview/start/userid-text', methods=['POST'])
def start_interview_userid_text():
    """
    方式5：用户ID（数据库简历） + 岗位文本
    POST /api/ai/interview/start/userid-text

    Body: {
        "user_id": "user_123",
        "job_text": "岗位描述..."
    }
    """
    try:
        data = request.get_json() or {}

        # 从数据库获取简历
        user_id = data.get('user_id')
        resume_text, error = _get_resume_from_db(user_id)
        if error:
            return jsonify({'error': error}), 400

        job_text = data.get('job_text', '').strip()
        if not job_text:
            return jsonify({'error': 'job_text 不能为空'}), 400

        return _create_interview_session(
            resume_text, job_text, 'database', 'text',
            user_id=user_id
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== 6. 简历文本 + 岗位ID ====================

@app.route('/api/ai/interview/start/text-jobid', methods=['POST'])
def start_interview_text_jobid():
    """
    方式6：简历文本 + 岗位ID
    POST /api/ai/interview/start/text-jobid

    Body: {
        "resume_text": "简历内容...",
        "job_id": "123"
    }
    """
    try:
        data = request.get_json() or {}

        resume_text = data.get('resume_text', '').strip()
        if not resume_text:
            return jsonify({'error': 'resume_text 不能为空'}), 400

        # 从数据库获取岗位
        job_id = data.get('job_id')
        job_text, error = _get_job_from_db(job_id)
        if error:
            return jsonify({'error': error}), 400

        return _create_interview_session(resume_text, job_text, 'text', 'database', job_id=job_id)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== 私有工具函数 ====================

def _parse_pdf_base64(base64_data):
    """
    解析base64 PDF文件，返回 (text, error)
    """
    if not base64_data:
        return None, 'resume_file 不能为空'

    try:
        # 解码base64
        pdf_bytes = base64.b64decode(base64_data)

        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name

        # 提取文本
        text = manager.Ai_job.extract_pdf_text(tmp_path)

        # 清理
        try:
            os.unlink(tmp_path)
        except:
            pass

        if not text or not text.strip():
            return None, 'PDF内容为空或解析失败'

        return text, None

    except Exception as e:
        return None, f'PDF解析失败: {str(e)}'


def _get_resume_from_db(user_id):
    """
    从数据库获取简历文本，返回 (text, error)
    """
    if not user_id:
        return None, 'user_id 不能为空'

    try:
        text = manager.Ai_job.get_user_app_text(user_id)
        if not text or not text.strip():
            return None, '数据库中未找到该用户的简历'
        return text, None
    except Exception as e:
        return None, f'获取简历失败: {str(e)}'


def _get_job_from_db(job_id):
    """
    从数据库获取岗位文本，返回 (text, error)
    """
    if not job_id:
        return None, 'job_id 不能为空'

    try:
        text = manager.Ai_job.get_job_text_in_db(job_id)
        if not text or not text.strip():
            return None, '数据库中未找到该岗位信息'
        return text, None
    except Exception as e:
        return None, f'获取岗位信息失败: {str(e)}'


def _create_interview_session(resume_text, job_text, resume_source, job_source,
                              user_id=None, job_id=None):
    """
    统一创建面试会话的核心逻辑 - 等待语音合成成功后返回
    """
    # 创建会话
    session_id = manager.create_session(resume_text, job_text)
    session = manager.get_session(session_id)

    # 记录来源信息
    session['resume_source'] = resume_source
    session['job_source'] = job_source
    session['user_id'] = user_id
    session['job_id'] = job_id

    # 获取AI第一个问题
    ai_response = manager.only_chat(session['messages'])
    first_question = manager.extract_ai_text(ai_response)

    if not first_question:
        # 清理会话
        manager.delete_session(session_id)
        return jsonify({'error': 'AI生成问题失败'}), 500

    # 更新会话
    manager.append_message(session_id, f"面试官：{first_question}")
    manager.add_to_history(session_id, 'interviewer', first_question)
    manager.increment_question(session_id)

    # 生成语音 - 必须成功才返回
    audio_url, error = _generate_audio_sync(session_id, first_question)

    if error:
        # TTS失败，清理会话并返回错误
        manager.delete_session(session_id)
        return jsonify({
            'error': f'语音合成失败: {error}',
            'question': first_question  # 可选：返回文本以便调试
        }), 500

    return jsonify({
        'code': 200,
        'session_id': session_id,
        'question': first_question,
        'audio_url': audio_url,
        'stage': session['stage'],
        'question_number': 1,
        'resume_source': resume_source,
        'job_source': job_source,
        'user_id': user_id,
        'job_id': job_id
    }), 200


def _generate_audio_sync(session_id, text):
    """
    同步生成TTS音频，返回 (audio_url, error)
    成功: (url, None)
    失败: (None, error_message)
    """
    try:
        filename = f"question_{session_id}_{int(time.time())}.mp3"
        audio_dir = os.path.join('static', 'audio')
        audio_path = os.path.join(audio_dir, filename)
        os.makedirs(audio_dir, exist_ok=True)

        # 调用TTS生成（同步等待完成）
        manager.generate_tts(text, audio_path)

        # 验证文件是否成功生成
        if not os.path.exists(audio_path):
            return None, "音频文件生成失败"

        # 验证文件大小（避免生成空文件）
        if os.path.getsize(audio_path) == 0:
            os.remove(audio_path)  # 清理空文件
            return None, "音频文件为空"

        audio_url = f'/static/audio/{filename}'
        return audio_url, None

    except Exception as e:
        error_msg = str(e)
        print(f"TTS生成失败: {error_msg}")
        return None, error_msg


@app.route('/api/ai/interview/<session_id>/transcribe', methods=['POST'])
def transcribe_audio(session_id):
    """
    语音听写接口 - 将用户音频转为文本
    POST /api/interview/{session_id}/transcribe
    Content-Type: multipart/form-data
    Body: audio_file (MP3/PCM, max 60s)
    Response: {
        "text": "识别的文本内容",
        "confidence": 0.95
    }
    """
    try:
        # 验证会话
        session = manager.get_session(session_id)
        if not session:
            return jsonify({'error': '会话不存在或已过期'}), 404

        if session['stage'] == 'ended':
            return jsonify({'error': '面试已结束'}), 400

        # 获取上传的音频文件
        if 'audio_file' not in request.files:
            return jsonify({'error': '未找到音频文件'}), 400

        audio_file = request.files['audio_file']
        print(f'audio_file:{audio_file}')

        # 保存临时文件
        temp_filename = f"temp_{session_id}_{int(time.time())}.wav"
        temp_path = os.path.join('temp', temp_filename)
        os.makedirs('temp', exist_ok=True)
        audio_file.save(temp_path)

        # 调用语音识别（demo_microphone_recognition 的替代）
        # 这里需要实现一个接收文件路径的语音识别函数
        recognized_text = manager.speech_to_text(temp_path)

        # 清理临时文件
        os.remove(temp_path)

        return jsonify({
            'code': 200,
            'text': recognized_text,
            'confidence': 0.95,  # 置信度，根据实际ASR返回
            'session_id': session_id
        }), 200

    except Exception as e:
        app.logger.error(f'出错：{e}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai/interview/<session_id>/answer', methods=['POST'])
def process_answer(session_id):
    """
    处理用户回答并返回AI追问
    POST /api/ai/interview/{session_id}/answer
    Body: {
        "user_text": "用户回答文本",
        "end_interview": false  // 是否结束面试
    }
    Response: {
        "question": "AI的下一个问题",
        "audio_url": "语音合成音频URL",
        "stage": "current_stage",
        "is_ended": false
    }
    """
    try:
        session = manager.get_session(session_id)
        if not session:
            return jsonify({'error': '会话不存在'}), 404

        data = request.get_json()
        user_text = data.get('user_text', '')
        end_interview = data.get('end_interview', False)

        # 检查结束条件
        if end_interview or "面试结束" in user_text or "我没有问题了" in user_text:
            return manager.end_interview_session(session_id, user_text)

        # 记录用户回答
        manager.append_message(session_id, f"候选人：{user_text}")
        manager.add_to_history(session_id, 'candidate', user_text)

        # 构建追问提示
        current_stage = manager.update_stage(session_id)
        prompt_suffix = f"\n\n当前处于{current_stage}，请继续提问。记住：只问一个问题，自然且有针对性。"

        full_context = session['messages'] + prompt_suffix

        # 调用AI
        ai_response = manager.only_chat(full_context)

        next_question = manager.extract_ai_text(ai_response)

        # 更新状态
        manager.append_message(session_id, f"面试官：{next_question}")
        manager.add_to_history(session_id, 'interviewer', next_question)
        manager.increment_question(session_id)

        # 语音合成（同步执行）
        audio_filename = f"question_{session_id}_{int(time.time())}.mp3"
        audio_path = os.path.join('static', 'audio', audio_filename)
        manager.generate_tts(next_question, audio_path)  # 改为同步调用
        print(f'next_question:{next_question}')

        return jsonify({
            'code': 200,
            'question': next_question,
            'audio_url': f'/static/audio/{audio_filename}',
            'stage': session['stage'],
            'question_number': session['question_count'],
            'is_ended': False
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/interview/<session_id>/report', methods=['GET'])
def download_report(session_id):
    """下载面试报告"""
    report_path = os.path.join('reports', f'{session_id}.json')
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({'error': '报告不存在'}), 404


@app.route('/api/ai/interview/<session_id>/history', methods=['GET'])
def get_history(session_id):
    """获取面试聊天记录"""
    session = manager.get_session(session_id)
    if not session:
        return jsonify({'error': '会话不存在'}), 404

    return jsonify({
        'code': 200,
        'session_id': session_id,
        'current_stage': session['stage'],
        'history': session['history']
    }),200



@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    try:
        # 测试数据库连接
        db.session.execute(text('SELECT 1'))
        db_status = '正常'
    except Exception as e:
        db_status = f'异常: {str(e)}'

    return jsonify({
        'code': 200,
        'message': '服务正常',
        'data': {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'database': db_status,
            'service': '运行正常'
        }
    }),200


if __name__ == '__main__':
    if __name__ == '__main__':
        os.makedirs('static/audio', exist_ok=True)
        os.makedirs('temp', exist_ok=True)
        os.makedirs('reports', exist_ok=True)
        # 在启动时创建数据库表
        with app.app_context():
            try:
                db.create_all()
                app.logger.info("数据库表创建成功")
            except Exception as e:
                app.logger.error(f"数据库表创建失败: {str(e)}")

        print(f"服务器启动在: http://localhost:5000")
        print(f"健康检查: http://localhost:5000/api/health")
        print(f"数据库连接: {app.config['SQLALCHEMY_DATABASE_URI']}")


        # 启动服务器
        print("=" * 50)
        print("DeepSeek Flask 后端服务")
        print("=" * 50)
        print("访问地址: http://localhost:5000")
        print("API测试: http://localhost:5000/api/test")
        print("聊天接口: POST http://localhost:5000/api/chat")
        print("状态检查: GET http://localhost:5000/api/status")
        print("文件上传: POST http://localhost:5000/api/upload")
        print("文件访问: GET http://localhost:5000/uploads/<filename>")
        print("=" * 50)

        try:
            app.run(
                host='0.0.0.0',
                port=5000,
                debug=True,
                threaded=True
            )
        except Exception as e:
            app.logger.error(f"服务器启动失败: {str(e)}")