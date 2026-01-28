from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError, JWTDecodeError
from flask_sqlalchemy import SQLAlchemy
from datetime import  timedelta
import bcrypt
from dotenv import load_dotenv
from sqlalchemy import text, func
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import os
from X1_ws import think_speaker
import logging
from pathlib import Path
from sql_data_demo import EndDemoDatabase, Job_prot, Job_category_simple, Forum_comments, Sys_user, ResumeManager, ComplaintFeedbackManager
from flask import jsonify, request, g
from datetime import datetime
from sqlalchemy import text
import hashlib
# import jwt as pyjwt
import re
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from typing import Dict, List, Optional, Any
import json
from datetime import datetime


db = EndDemoDatabase(host='localhost', user='root', password='123456')
job_prot = Job_prot(db.connection)
job_category_simple = Job_category_simple(db.connection)
forum_comments = Forum_comments(db.connection)
sys_user = Sys_user(db.connection)
resume_manager = ResumeManager(db.connection)
manager = ComplaintFeedbackManager(db.connection)

think_speaker = think_speaker()

# 假设的JWT密钥和配置
JWT_SECRET = 'your-secret-key'
JWT_ALGORITHM = 'HS256'

app = Flask(__name__)
CORS(app)  # 允许跨域

# 存储聊天记录
chat_history = []
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
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

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'mysql+pymysql://root:123456@localhost:3306/end_demo')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 300,
    'pool_pre_ping': True,
}

# 初始化扩展
CORS(app, supports_credentials=True)
jwt = JWTManager(app)
db = SQLAlchemy(app)

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



@app.route('/api/complaint/types', methods=['GET'])
def get_complaint_types():
    """获取所有投诉类型"""
    try:
        
        types = manager.get_all_complaint_types()

        if types is None:
            return jsonify({
                'code': 500,
                'message': '获取投诉类型失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': types
        }), 200
    except Exception as e:
        app.logger.error(f'获取投诉类型失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/submit', methods=['POST'])
def submit_complaint():
    """用户提交投诉"""
    try:
        data = request.get_json()
        if not data:
            app.logger.error('未获取到投诉数据')
            return jsonify({
                'code': 400,
                'message': '请求参数不能为空'
            }), 400

        user_id = data.get('user_id')
        complaint_type = data.get('complaint_type')
        description = data.get('description', '').strip()
        image_urls = data.get('image_urls', [])
        priority = data.get('priority', 1)

        # 参数验证
        if not user_id or not complaint_type or not description:
            return jsonify({
                'code': 400,
                'message': 'user_id、complaint_type和description为必填项'
            }), 400

        if priority not in [1, 2, 3]:
            return jsonify({
                'code': 400,
                'message': 'priority参数无效，应为1、2或3'
            }), 400

        
        complaint_id = manager.submit_complaint(
            user_id=user_id,
            complaint_type=complaint_type,
            description=description,
            image_urls=image_urls,
            priority=priority
        )

        if complaint_id is None:
            return jsonify({
                'code': 500,
                'message': '提交投诉失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': '投诉提交成功',
            'data': {
                'complaint_id': complaint_id
            }
        }), 200
    except Exception as e:
        app.logger.error(f'提交投诉失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/user/<int:user_id>', methods=['GET'])
def get_user_complaints(user_id: int):
    """获取用户的所有投诉"""
    try:
        # 获取查询参数
        is_resolved = request.args.get('is_resolved')
        if is_resolved is not None:
            try:
                is_resolved = int(is_resolved)
                if is_resolved not in [0, 1]:
                    raise ValueError
            except ValueError:
                return jsonify({
                    'code': 400,
                    'message': 'is_resolved参数无效，应为0或1'
                }), 400

        
        complaints = manager.get_user_complaints(user_id=user_id, is_resolved=is_resolved)

        if complaints is None:
            return jsonify({
                'code': 500,
                'message': '获取用户投诉失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': complaints
        }), 200
    except Exception as e:
        app.logger.error(f'获取用户(user_id={user_id})投诉失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/<int:complaint_id>', methods=['GET'])
def get_complaint_detail(complaint_id: int):
    """根据投诉ID获取投诉详情"""
    try:
        
        complaint = manager.get_complaint_by_id(complaint_id)

        if complaint is None:
            return jsonify({
                'code': 404,
                'message': '投诉不存在'
            }), 404

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': complaint
        }), 200
    except Exception as e:
        app.logger.error(f'获取投诉(ID={complaint_id})详情失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/reply', methods=['POST'])
def reply_complaint():
    """管理员回复投诉"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求参数不能为空'
            }), 400

        complaint_id = data.get('complaint_id')
        feedback_content = data.get('feedback_content', '').strip()
        resolved_by = data.get('resolved_by')
        mark_resolved = data.get('mark_resolved', True)

        # 参数验证
        if not complaint_id or not feedback_content or not resolved_by:
            return jsonify({
                'code': 400,
                'message': 'complaint_id、feedback_content和resolved_by为必填项'
            }), 400

        

        # 检查投诉是否存在
        if not manager.complaint_exists(complaint_id):
            return jsonify({
                'code': 404,
                'message': '投诉不存在'
            }), 404

        success = manager.reply_complaint(
            complaint_id=complaint_id,
            feedback_content=feedback_content,
            resolved_by=resolved_by,
            mark_resolved=mark_resolved
        )

        if not success:
            return jsonify({
                'code': 500,
                'message': '回复投诉失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': '回复成功'
        }), 200
    except Exception as e:
        app.logger.error(f'回复投诉失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/list', methods=['POST'])
def get_complaint_list():
    """管理员获取投诉列表(支持筛选和分页)"""
    try:
        data = request.get_json()
        if not data:
            # 如果没有传参数，使用空字典
            data = {}

        filters = data.get('filters', {})
        page = data.get('page', 1)
        page_size = data.get('page_size', 20)

        # 参数验证
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 20

        
        complaints, total = manager.get_complaint_list(
            filters=filters,
            page=page,
            page_size=page_size
        )

        if complaints is None:
            return jsonify({
                'code': 500,
                'message': '获取投诉列表失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'list': complaints,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
        }), 200
    except Exception as e:
        app.logger.error(f'获取投诉列表失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/statistics', methods=['GET'])
def get_complaint_statistics():
    """获取投诉统计信息"""
    try:
        
        statistics = manager.get_complaint_statistics()

        if statistics is None:
            return jsonify({
                'code': 500,
                'message': '获取投诉统计失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': statistics
        }), 200
    except Exception as e:
        app.logger.error(f'获取投诉统计失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/status', methods=['POST'])
def update_complaint_status():
    """更新投诉状态"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求参数不能为空'
            }), 400

        complaint_id = data.get('complaint_id')
        is_resolved = data.get('is_resolved')
        resolved_by = data.get('resolved_by')

        # 参数验证
        if not complaint_id or is_resolved is None:
            return jsonify({
                'code': 400,
                'message': 'complaint_id和is_resolved为必填项'
            }), 400

        if is_resolved not in [0, 1]:
            return jsonify({
                'code': 400,
                'message': 'is_resolved参数无效，应为0或1'
            }), 400

        

        # 检查投诉是否存在
        if not manager.complaint_exists(complaint_id):
            return jsonify({
                'code': 404,
                'message': '投诉不存在'
            }), 404

        success = manager.update_complaint_status(
            complaint_id=complaint_id,
            is_resolved=is_resolved,
            resolved_by=resolved_by
        )

        if not success:
            return jsonify({
                'code': 500,
                'message': '更新投诉状态失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': '更新成功'
        }), 200
    except Exception as e:
        app.logger.error(f'更新投诉状态失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/unresolved/count', methods=['GET'])
def get_unresolved_count():
    """获取未解决的投诉数量"""
    try:
        
        count = manager.get_unresolved_count()

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'unresolved_count': count
            }
        }), 200
    except Exception as e:
        app.logger.error(f'获取未解决投诉数量失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/recent', methods=['GET'])
def get_recent_complaints():
    """获取最近N天的投诉"""
    try:
        days = request.args.get('days', 7, type=int)

        if days < 1 or days > 365:
            return jsonify({
                'code': 400,
                'message': 'days参数应在1-365之间'
            }), 400

        
        complaints = manager.get_recent_complaints(days=days)

        if complaints is None:
            return jsonify({
                'code': 500,
                'message': '获取最近投诉失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': complaints
        }), 200
    except Exception as e:
        app.logger.error(f'获取最近投诉失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/high-priority', methods=['GET'])
def get_high_priority_complaints():
    """获取高优先级未解决投诉"""
    try:
        
        complaints = manager.get_high_priority_unresolved()

        if complaints is None:
            return jsonify({
                'code': 500,
                'message': '获取高优先级投诉失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': complaints
        }), 200
    except Exception as e:
        app.logger.error(f'获取高优先级投诉失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


@app.route('/api/complaint/type/add', methods=['POST'])
def add_complaint_type():
    """添加投诉类型"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求参数不能为空'
            }), 400

        type_name = data.get('type_name', '').strip()
        sort_order = data.get('sort_order', 0)

        if not type_name:
            return jsonify({
                'code': 400,
                'message': 'type_name为必填项'
            }), 400

        
        type_code = manager.add_complaint_type(
            type_name=type_name,
            sort_order=sort_order
        )

        if type_code is None:
            return jsonify({
                'code': 500,
                'message': '添加投诉类型失败'
            }), 500

        return jsonify({
            'code': 200,
            'message': '添加成功',
            'data': {
                'type_code': type_code
            }
        }), 200
    except Exception as e:
        app.logger.error(f'添加投诉类型失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500
    finally:
        if 'manager' in locals():
            manager.connection.close()


# 测试路由
@app.route('/api/complaint/test', methods=['GET'])
def test_complaint_api():
    """测试接口是否正常工作"""
    try:
        return jsonify({
            'code': 200,
            'message': '投诉反馈API服务正常运行',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        app.logger.error(f'测试接口异常: {str(e)}')
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

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
    })


if __name__ == '__main__':
    if __name__ == '__main__':
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