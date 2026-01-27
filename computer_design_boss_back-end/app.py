from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
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
from sql_data_demo import EndDemoDatabase, Job_prot, Job_category_simple, Forum_comments

db = EndDemoDatabase(host='localhost', user='root', password='123456')
job_prot = Job_prot(db.connection)
job_category_simple = Job_category_simple(db.connection)
forum_comments = Forum_comments(db.connection)

think_speaker = think_speaker()

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