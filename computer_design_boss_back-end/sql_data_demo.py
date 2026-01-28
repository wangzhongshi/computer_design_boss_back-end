from pymysql import Error
import json
from typing import Optional, List, Dict, Any
import pymysql
from pymysql.cursors import DictCursor
from pymysql.cursors import DictCursor
from datetime import datetime
from typing import Optional, List, Dict, Any

class EndDemoDatabase:
    """end_demo数据库操作类"""

    def __init__(self, host='localhost', user='root', password='123456', database='boss_job'):
        """
        初始化数据库连接

        Args:
            host: 数据库主机
            user: 用户名
            password: 密码
            database: 数据库名
        """
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("数据库连接成功！")
        except Error as e:
            print(f"数据库连接失败: {e}")
            raise


    def __del__(self):
        """析构函数，确保连接关闭"""
        try:
            self.close()
        except:
            # 忽略所有析构函数中的异常
            pass



class Job_prot:
    def __init__(self, db_connection):
        self.connection = db_connection

    def fetch_some_job_posts_all(self):
        '''
        用于获取全部职位列表的信息
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                columns = ['id',
                           "title",
                           "salary_min",
                           "salary_max",
                           "edu_req",
                           "exp_req",
                           'emp_type']
                select_clause = ", ".join(f"`{c}`" for c in columns)
                sql = f"SELECT {select_clause} FROM job_post"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('全部职位列表信息表查询失败:',e)
            return None

    def fetch_some_job_posts_some(self, category_id):
        '''
        用于获取某一类工作的信息
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                columns = ['id',
                           "title",
                           "salary_min",
                           "salary_max",
                           "edu_req",
                           "exp_req",
                           'emp_type']
                select_clause = ", ".join(f"`{c}`" for c in columns)
                sql = f"SELECT {select_clause} FROM job_post where category_id='{category_id}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('某一类工作列表查询失败:',e)
            return None

    def fetch_job_list_by_two_given(self, emp_type, category_id):
        '''
        用于输出类似于全职-综合的列表
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                columns = ['id',
                           "title",
                           "salary_min",
                           "salary_max",
                           "edu_req",
                           "exp_req",
                           'emp_type']
                select_clause = ", ".join(f"`{c}`" for c in columns)
                sql = f"SELECT {select_clause} FROM job_post where category_id='{category_id}' and emp_type='{emp_type}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('全职-综合列表查询失败:',e)
            return None

    def search_job_by_user_input(self, user_input):
        '''
        搜索功能通过用户的输入来检索相应的岗位
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                columns = ['id',
                           "title",
                           "salary_min",
                           "salary_max",
                           "edu_req",
                           "exp_req",
                           'emp_type']
                select_clause = ", ".join(f"`{c}`" for c in columns)
                sql = f"SELECT {select_clause} FROM job_post where title like '%{user_input}%'"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('全职-综合列表查询失败:', e)
            return None

    def fetch_one_job_all_data_posts(self, ones_id):
        """
        用于根据前端提供的信息，输出岗位的详细信息
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = f"SELECT * FROM job_post where id='{ones_id}'"
                # sql = f"SELECT * FROM job_post where title='{ones_title}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('职位展示页详细信息查询失败:', e)
            return None

    def insert_job_post(self, boss_job_id, title, company_id, city_id, category_id, emp_type=1,
                        salary_min=None, salary_max=None, salary_desc=None, edu_req=None, exp_req=None,
                        district=None, address=None, recruiter_id=None, description=None,
                        require_list=None, welfare_list=None, publish_time=None, refresh_time=None,
                        status=1):
        '''
        发布职位信息
        :param boss_job_id: Boss 直聘平台原始ID
        :param title: 岗位名称
        :param company_id: 所属公司（关联 company 表）
        :param city_id: 城市ID（关联 city 表）
        :param category_id: 职位类别ID
        :param emp_type: 1=全职 2=兼职 3=实习
        :param salary_min: 薪资下限（元/月）
        :param salary_max: 薪资上限（元/月）
        :param salary_desc: 原始薪资文本
        :param edu_req: 学历要求
        :param exp_req: 经验要求
        :param district: 区县/商圈
        :param address: 详细工作地址
        :param recruiter_id: 招聘者ID
        :param description: 职位描述
        :param require_list: 任职要求数组（JSON格式）
        :param welfare_list: 福利标签数组（JSON格式）
        :param publish_time: 发布时间
        :param refresh_time: 刷新时间
        :param status: 1=在招 2=下架 3=暂停
        :return: 插入的职位ID或None
        '''
        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO job_post 
                (boss_job_id, title, company_id, city_id, category_id, emp_type,
                 salary_min, salary_max, salary_desc, edu_req, exp_req,
                 district, address, recruiter_id, description,
                 require_list, welfare_list, publish_time, refresh_time, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                # 处理JSON数据
                require_list_json = json.dumps(require_list, ensure_ascii=False) if require_list else None
                welfare_list_json = json.dumps(welfare_list, ensure_ascii=False) if welfare_list else None

                cursor.execute(sql, (
                    boss_job_id, title, company_id, city_id, category_id, emp_type,
                    salary_min, salary_max, salary_desc, edu_req, exp_req,
                    district, address, recruiter_id, description,
                    require_list_json, welfare_list_json, publish_time, refresh_time, status
                ))

                job_id = cursor.lastrowid
                self.connection.commit()
                print(f'职位发布成功，职位ID: {job_id}')
                return job_id

        except Exception as e:
            print(f'职位发布失败: {e}')
            self.connection.rollback()
            return None

class Job_category_simple:
    def __init__(self, db_connection):
        self.connection = db_connection

    def job_intro_list(self):
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = f"SELECT name, parent_id, intro FROM job_category_simple"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('全部职位列表信息表查询失败:', e)
            return None


class Forum_comments:
    def __init__(self, db_connection):
        self.connection = db_connection

    def forum_all(self):
        '''
        查询所有分类
        :return:
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = f"SELECT * FROM forum_comments"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('全部评论查询失败:', e)
            return None

    def forum_one_category(self, category_id):
        '''
        查询某一类岗位下的评
        :param category_id:
        :return:
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = f"SELECT * FROM forum_comments where category_id='{category_id}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('全部评论查询失败:', e)
            return None

    def forum_all_first_talk(self):
        '''
        查询所有一级评论
        :return:
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = f"SELECT * FROM forum_comments WHERE parent_id IS NULL;"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('全部评论查询失败:', e)
            return None

    def forum_talks_back(self, parent_id):
        '''
        查询某一个评论的回复
        :param parent_id:
        :return:
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = f"SELECT * FROM forum_comments WHERE parent_id='{parent_id}';"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('全部评论查询失败:', e)
            return None

    def forum_add(self, category_id, user_id, parent_id, content, level, sort_order):
        '''
        发布评论
        :param category_id:
        :param user_id:
        :param parent_id:
        :param content:
        :param level:
        :param sort_order:
        :return:none
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                # 把空串统一转成 None
                parent_id = parent_id if parent_id != '' else None

                sql = """
                INSERT INTO forum_comments
                (category_id, user_id, parent_id, content, level, sort_order)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql,
                               (category_id, user_id, parent_id, content, level, sort_order))
                self.connection.commit()
                print('成功')
        except Exception as e:
            print('全部评论查询失败:', e)
            return None

    def forum_delete(self, id):
        '''
        删除评论
        :param id:
        :return: none
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = f"""UPDATE forum_comments
                          SET is_deleted = 1
                          WHERE id = '{id}'"""
                cursor.execute(sql)
                self.connection.commit()
                print('成功')
        except Exception as e:
            print('全部评论查询失败:', e)
            return None

    def forum_all_by_user(self, user_id):
        '''
        用于个人页展示发布过的评论
        :param user_id:
        :return:
        '''
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = f"""select * from forum_comments where user_id='{user_id}'"""
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        except Exception as e:
            print('全部评论查询失败:', e)
            return None

    def forum_count_all(self, switch, category_id=None, parent_id=None, user_id=None):
        '''
        这个函数可以查询全部评论数，与改岗位有关的评论数，某条评论的回复数，用户发布的评论数
        :param switch:
        :param category_id:
        :param parent_id:
        :param user_id:
        :return: 一个int，值为评论数
        '''
        try:
            if switch == 'all':
                sql = f'select id from forum_comments'
            elif switch == 'category':
                sql = f"select id from forum_comments where category_id='{category_id}'"
            elif switch == 'back':
                sql = f"select id from forum_comments where parent_id='{parent_id}'"
            elif switch == 'user':
                sql = f"select id from forum_comments where user_id='{user_id}'"
            else:
                return 'error'

            with self.connection.cursor(DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                print(len(result))
                return len(result)
        except Exception as e:
            print('评论计数查询失败:', e)
            return None


class Sys_user:
    def __init__(self, db_connection):
        self.connection = db_connection

    def user_count_all(self, switch, status=None, job_status=None, is_deleted=0):
        '''
        统计用户数量
        :param switch: 'all'-全部用户, 'status'-按状态, 'job_status'-按求职状态, 'active'-活跃用户
        :param status: 账号状态（switch为'status'时使用）
        :param job_status: 求职状态（switch为'job_status'时使用）
        :param is_deleted: 是否删除，默认0-未删除
        :return: 用户数量
        '''
        try:
            sql = f"select id from sys_user where is_deleted='{is_deleted}'"

            if switch == 'all':
                pass
            elif switch == 'status' and status is not None:
                sql += f" and status='{status}'"
            elif switch == 'job_status' and job_status is not None:
                sql += f" and job_status='{job_status}'"
            elif switch == 'active':
                sql += f" and status='1'"
            else:
                return 'error'

            with self.connection.cursor(DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                print(len(result))
                return len(result)
        except Exception as e:
            print('用户数量统计失败:', e)
            return None

    def get_user_by_field(self, field, value, include_deleted=False):
        '''
        根据指定字段获取用户信息
        :param field: 字段名，支持：user_id, mobile, email, id
        :param value: 字段值
        :param include_deleted: 是否包含已删除用户
        :return: 用户信息字典或None
        '''
        try:
            valid_fields = ['user_id', 'mobile', 'email', 'id']
            if field not in valid_fields:
                return None

            sql = f"select * from sys_user where {field}='{value}'"
            if not include_deleted:
                sql += f" and is_deleted='0'"

            with self.connection.cursor(DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result)
                return result
        except Exception as e:
            print(f'根据{field}查询用户失败:', e)
            return None

    def update_user_status(self, user_id, status):
        '''
        更新用户状态
        :param user_id: 用户业务ID
        :param status: 新的状态值
        :return: 是否成功
        '''
        try:
            sql = f"""
            update sys_user 
            set status='{status}', updated_at=NOW() 
            where user_id='{user_id}' and is_deleted='0'
            """

            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                print('成功')
                return cursor.rowcount > 0
        except Exception as e:
            print('更新用户状态失败:', e)
            self.connection.rollback()
            return False

    def update_last_login(self, user_id, login_ip, device_model, device_type):
        '''
        更新用户最后登录信息
        :param user_id: 用户业务ID
        :param login_ip: 登录IP
        :param device_model: 设备型号
        :param device_type: 设备类型
        :return: 是否成功
        '''
        try:
            sql = f"""
            update sys_user 
            set last_login_time=NOW(), last_login_ip='{login_ip}', 
                last_device_model='{device_model}', last_device_type='{device_type}',
                last_device_time=NOW(), updated_at=NOW()
            where user_id='{user_id}' and is_deleted='0'
            """

            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                print('成功')
                return cursor.rowcount > 0
        except Exception as e:
            print('更新最后登录信息失败:', e)
            self.connection.rollback()
            return False

    def create_user(self, user_data):
        '''
        创建新用户
        :param user_data: 用户数据字典
        :return: 创建的用户ID或None
        '''
        try:
            # 确保必填字段存在
            required_fields = ['user_id', 'mobile', 'password_hash']
            for field in required_fields:
                if field not in user_data:
                    return None

            # 构建字段和值
            fields = []
            values = []

            for field, value in user_data.items():
                if value is not None:
                    fields.append(field)
                    if isinstance(value, str):
                        values.append(f"'{value}'")
                    else:
                        values.append(f"{value}")

            fields_str = ', '.join(fields)
            values_str = ', '.join(values)

            sql = f"insert into sys_user ({fields_str}) values ({values_str})"

            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                print(cursor.lastrowid)
                return cursor.lastrowid
        except Exception as e:
            print('创建用户失败:', e)
            self.connection.rollback()
            return None

    def search_users(self, keyword=None, status=1, page=1, page_size=20):
        '''
        搜索用户（支持分页）
        :param keyword: 搜索关键词（匹配mobile, email, real_name）
        :param status: 账号状态，默认1-正常
        :param page: 页码
        :param page_size: 每页数量
        :return: 用户列表和总数
        '''
        try:
            # 基础查询
            # base_sql = f"""
            # from sys_user
            # where is_deleted='0' and status='{status}'
            # """
            print(status)
            base_sql = f"""
                        from sys_user 
                        where is_deleted='0' and status='{status}'
                        """

            # 关键词搜索条件
            if keyword:
                base_sql += f"""
                and (mobile like '%{keyword}%' 
                    or email like '%{keyword}%' 
                    or real_name like '%{keyword}%')
                """

            # 获取总数
            count_sql = f"select count(*) as total {base_sql}"

            # 获取分页数据
            offset = (page - 1) * page_size
            data_sql = f"""
            select * {base_sql}
            order by created_at desc
            limit {page_size} offset {offset}
            """

            with self.connection.cursor(DictCursor) as cursor:
                # 查询总数
                cursor.execute(count_sql)
                total_result = cursor.fetchone()
                total = total_result['total'] if total_result else 0

                # 查询数据
                cursor.execute(data_sql)
                users = cursor.fetchall()
                result = {
                    'users': users,
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': (total + page_size - 1) // page_size
                }
                print(result)
                return result
        except Exception as e:
            print('搜索用户失败:', e)
            return {'users': [], 'total': 0, 'page': page, 'page_size': page_size, 'total_pages': 0}

    def soft_delete_user(self, user_id):
        '''
        软删除用户
        :param user_id: 用户业务ID
        :return: 是否成功
        '''
        try:
            sql = f"""
            update sys_user 
            set is_deleted='1', deleted_at=NOW(), updated_at=NOW()
            where user_id='{user_id}' and is_deleted='0'
            """

            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                print('成功')
                return cursor.rowcount > 0
        except Exception as e:
            print('软删除用户失败:', e)
            self.connection.rollback()
            return False

    def update_user_profile(self, user_id, profile_data):
        '''
        更新用户个人信息
        :param user_id: 用户业务ID
        :param profile_data: 要更新的个人信息字典
        :return: 是否成功
        '''
        try:
            if not profile_data:
                return False

            # 构建SET子句
            set_clauses = []
            for field, value in profile_data.items():
                if value is not None:
                    if isinstance(value, str):
                        set_clauses.append(f"{field}='{value}'")
                    else:
                        set_clauses.append(f"{field}={value}")

            if not set_clauses:
                return False

            set_str = ', '.join(set_clauses)
            sql = f"""
            update sys_user 
            set {set_str}, updated_at=NOW()
            where user_id='{user_id}' and is_deleted='0'
            """

            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                print('成功')
                return cursor.rowcount > 0
        except Exception as e:
            print('更新用户信息失败:', e)
            self.connection.rollback()
            return False

    def check_user_exists(self, mobile=None, email=None, exclude_user_id=None):
        '''
        检查用户是否存在（用于注册时验证手机号/邮箱是否已注册）
        :param mobile: 手机号
        :param email: 邮箱
        :param exclude_user_id: 排除的用户ID（用于修改信息时检查）
        :return: 是否存在
        '''
        try:
            sql = "select id from sys_user where is_deleted='0' and ("
            conditions = []

            if mobile:
                conditions.append(f"mobile='{mobile}'")
            if email:
                conditions.append(f"email='{email}'")

            if not conditions:
                return False

            sql += " or ".join(conditions)
            sql += ")"

            if exclude_user_id:
                sql += f" and user_id!='{exclude_user_id}'"

            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                print('成功')
                return result is not None
        except Exception as e:
            print('检查用户存在性失败:', e)
            return False

class Resumes:
    def __init__(self, db_connection):
        self.connection = db_connection

    def create_resume(self, user_id: int, resume_data: Dict) -> Optional[int]:
        """创建简历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # 检查用户是否已有简历
                check_sql = "SELECT id FROM resumes WHERE user_id = %s"
                cursor.execute(check_sql, (user_id,))
                existing = cursor.fetchone()

                if existing:
                    return None  # 用户已存在简历

                # 构建插入SQL
                columns = ['user_id']
                values = [user_id]
                placeholders = ['%s']

                for key, value in resume_data.items():
                    if key in ['real_name', 'gender', 'birth_date', 'phone', 'email',
                               'wechat', 'city', 'education_level', 'school_name',
                               'major', 'graduation_year', 'gpa', 'resume_file_url',
                               'resume_file_name', 'resume_format', 'self_introduction']:
                        columns.append(key)
                        values.append(value)
                        placeholders.append('%s')

                sql = f"INSERT INTO resumes ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
                cursor.execute(sql, values)
                self.connection.commit()

                return cursor.lastrowid
        except Exception as e:
            print('创建简历失败:', e)
            return None

    def get_resume_by_user(self, user_id: int) -> Optional[Dict]:
        """获取用户的简历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT r.*, u.mobile, u.email as user_email, u.real_name as user_real_name
                FROM resumes r
                LEFT JOIN sys_user u ON r.user_id = u.user_id
                WHERE r.user_id = %s
                """
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取简历失败:', e)
            return None

    def update_resume(self, user_id: int, update_data: Dict) -> bool:
        """更新简历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # 构建更新SQL
                set_clauses = []
                values = []

                for key, value in update_data.items():
                    if key in ['real_name', 'gender', 'birth_date', 'phone', 'email',
                               'wechat', 'city', 'education_level', 'school_name',
                               'major', 'graduation_year', 'gpa', 'resume_file_url',
                               'resume_file_name', 'resume_format', 'self_introduction']:
                        set_clauses.append(f"{key} = %s")
                        values.append(value)

                if not set_clauses:
                    return False

                values.append(user_id)
                sql = f"UPDATE resumes SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s"
                cursor.execute(sql, values)
                self.connection.commit()

                return cursor.rowcount > 0
        except Exception as e:
            print('更新简历失败:', e)
            return False

    def delete_resume(self, user_id: int) -> bool:
        """删除简历（级联删除所有相关数据）"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "DELETE FROM resumes WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print('删除简历失败:', e)
            return False

    def get_resume_count_by_user(self) -> Dict:
        """统计用户简历数量"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT 
                    COUNT(*) as total_count,
                    COUNT(CASE WHEN education_level = '本科' THEN 1 END) as bachelor_count,
                    COUNT(CASE WHEN education_level = '硕士' THEN 1 END) as master_count,
                    COUNT(CASE WHEN education_level = '博士' THEN 1 END) as doctor_count
                FROM resumes
                """
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('统计简历数量失败:', e)
            return {}


class Certificates:
    def __init__(self, db_connection):
        self.connection = db_connection

    def add_certificate(self, user_id: int, cert_data: Dict) -> Optional[int]:
        """添加证书"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # 检查简历是否存在
                check_sql = "SELECT id FROM resumes WHERE user_id = %s"
                cursor.execute(check_sql, (user_id,))
                if not cursor.fetchone():
                    return None

                # 插入证书
                sql = """
                INSERT INTO certificates 
                (user_id, cert_type, cert_name, cert_level, issue_date, expiry_date, 
                 issuing_authority, certificate_no, attachment_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    user_id,
                    cert_data.get('cert_type'),
                    cert_data.get('cert_name'),
                    cert_data.get('cert_level'),
                    cert_data.get('issue_date'),
                    cert_data.get('expiry_date'),
                    cert_data.get('issuing_authority'),
                    cert_data.get('certificate_no'),
                    cert_data.get('attachment_url')
                )

                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print('添加证书失败:', e)
            return None

    def get_user_certificates(self, user_id: int, cert_type: Optional[str] = None) -> List[Dict]:
        """获取用户证书列表"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                if cert_type:
                    sql = "SELECT * FROM certificates WHERE user_id = %s AND cert_type = %s ORDER BY issue_date DESC"
                    cursor.execute(sql, (user_id, cert_type))
                else:
                    sql = "SELECT * FROM certificates WHERE user_id = %s ORDER BY issue_date DESC"
                    cursor.execute(sql, (user_id,))

                result = cursor.fetchall()
                return result
        except Exception as e:
            print('获取证书列表失败:', e)
            return []

    def get_certificate_by_id(self, cert_id: int, user_id: int) -> Optional[Dict]:
        """根据ID获取证书详情"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM certificates WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (cert_id, user_id))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取证书详情失败:', e)
            return None

    def update_certificate(self, cert_id: int, user_id: int, update_data: Dict) -> bool:
        """更新证书信息"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                set_clauses = []
                values = []

                for key, value in update_data.items():
                    if key in ['cert_type', 'cert_name', 'cert_level', 'issue_date',
                               'expiry_date', 'issuing_authority', 'certificate_no', 'attachment_url']:
                        set_clauses.append(f"{key} = %s")
                        values.append(value)

                if not set_clauses:
                    return False

                values.extend([cert_id, user_id])
                sql = f"UPDATE certificates SET {', '.join(set_clauses)} WHERE id = %s AND user_id = %s"
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print('更新证书失败:', e)
            return False

    def delete_certificate(self, cert_id: int, user_id: int) -> bool:
        """删除证书"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "DELETE FROM certificates WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (cert_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print('删除证书失败:', e)
            return False

    def get_certificate_stats(self, user_id: int) -> Dict:
        """获取用户证书统计"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT 
                    COUNT(*) as total_count,
                    COUNT(CASE WHEN cert_type = 'english' THEN 1 END) as english_count,
                    COUNT(CASE WHEN cert_type = 'computer' THEN 1 END) as computer_count,
                    COUNT(CASE WHEN cert_type = 'professional' THEN 1 END) as professional_count
                FROM certificates 
                WHERE user_id = %s
                """
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取证书统计失败:', e)
            return {}


class CampusExperiences:
    def __init__(self, db_connection):
        self.connection = db_connection

    def upsert_campus_experience(self, user_id: int, experience_data: Dict) -> Optional[int]:
        """更新或插入校园经历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # 检查是否已存在记录
                check_sql = "SELECT id FROM campus_experiences WHERE user_id = %s"
                cursor.execute(check_sql, (user_id,))
                existing = cursor.fetchone()

                if existing:
                    # 更新现有记录
                    sql = """
                    UPDATE campus_experiences SET
                    has_student_union = %s,
                    student_union_details = %s,
                    has_club = %s,
                    club_details = %s,
                    has_scholarship = %s,
                    scholarship_details = %s,
                    has_honor = %s,
                    honor_details = %s,
                    updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                    """
                    values = (
                        experience_data.get('has_student_union', 0),
                        experience_data.get('student_union_details'),
                        experience_data.get('has_club', 0),
                        experience_data.get('club_details'),
                        experience_data.get('has_scholarship', 0),
                        experience_data.get('scholarship_details'),
                        experience_data.get('has_honor', 0),
                        experience_data.get('honor_details'),
                        user_id
                    )
                    cursor.execute(sql, values)
                    self.connection.commit()
                    return existing['id']
                else:
                    # 插入新记录
                    sql = """
                    INSERT INTO campus_experiences 
                    (user_id, has_student_union, student_union_details, has_club, 
                     club_details, has_scholarship, scholarship_details, has_honor, honor_details)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        user_id,
                        experience_data.get('has_student_union', 0),
                        experience_data.get('student_union_details'),
                        experience_data.get('has_club', 0),
                        experience_data.get('club_details'),
                        experience_data.get('has_scholarship', 0),
                        experience_data.get('scholarship_details'),
                        experience_data.get('has_honor', 0),
                        experience_data.get('honor_details')
                    )
                    cursor.execute(sql, values)
                    self.connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            print('更新校园经历失败:', e)
            return None

    def get_campus_experience(self, user_id: int) -> Optional[Dict]:
        """获取用户校园经历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM campus_experiences WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取校园经历失败:', e)
            return None


class Internships:
    def __init__(self, db_connection):
        self.connection = db_connection

    def add_internship(self, user_id: int, internship_data: Dict) -> Optional[int]:
        """添加实习经历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                INSERT INTO internships 
                (user_id, company_name, position, industry, start_date, end_date, 
                 is_current, is_related, work_content, achievements)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    user_id,
                    internship_data.get('company_name'),
                    internship_data.get('position'),
                    internship_data.get('industry'),
                    internship_data.get('start_date'),
                    internship_data.get('end_date'),
                    internship_data.get('is_current', 0),
                    internship_data.get('is_related', 0),
                    internship_data.get('work_content'),
                    internship_data.get('achievements')
                )

                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print('添加实习经历失败:', e)
            return None

    def get_user_internships(self, user_id: int) -> List[Dict]:
        """获取用户实习经历列表"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT * FROM internships 
                WHERE user_id = %s 
                ORDER BY start_date DESC, end_date DESC
                """
                cursor.execute(sql, (user_id,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print('获取实习经历失败:', e)
            return []

    def get_internship_by_id(self, internship_id: int, user_id: int) -> Optional[Dict]:
        """根据ID获取实习详情"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM internships WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (internship_id, user_id))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取实习详情失败:', e)
            return None

    def update_internship(self, internship_id: int, user_id: int, update_data: Dict) -> bool:
        """更新实习经历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                set_clauses = []
                values = []

                for key, value in update_data.items():
                    if key in ['company_name', 'position', 'industry', 'start_date',
                               'end_date', 'is_current', 'is_related', 'work_content', 'achievements']:
                        set_clauses.append(f"{key} = %s")
                        values.append(value)

                if not set_clauses:
                    return False

                values.extend([internship_id, user_id])
                sql = f"UPDATE internships SET {', '.join(set_clauses)} WHERE id = %s AND user_id = %s"
                cursor.execute(sql, values)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print('更新实习经历失败:', e)
            return False

    def delete_internship(self, internship_id: int, user_id: int) -> bool:
        """删除实习经历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "DELETE FROM internships WHERE id = %s AND user_id = %s"
                cursor.execute(sql, (internship_id, user_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print('删除实习经历失败:', e)
            return False

    def get_internship_stats(self, user_id: int) -> Optional[Dict]:
        """获取实习统计信息"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM internship_stats WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取实习统计失败:', e)
            return None

    def get_industry_distribution(self) -> List[Dict]:
        """获取实习行业分布"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT industry, COUNT(*) as count
                FROM internships
                WHERE industry IS NOT NULL AND industry != ''
                GROUP BY industry
                ORDER BY count DESC
                LIMIT 10
                """
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print('获取行业分布失败:', e)
            return []


class JobIntentions:
    def __init__(self, db_connection):
        self.connection = db_connection

    def upsert_job_intention(self, user_id: int, intention_data: Dict) -> Optional[int]:
        """更新或插入求职意向"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # 处理JSON字段
                target_industries = json.dumps(intention_data.get('target_industries', [])) if intention_data.get(
                    'target_industries') else None
                target_positions = json.dumps(intention_data.get('target_positions', [])) if intention_data.get(
                    'target_positions') else None
                target_cities = json.dumps(intention_data.get('target_cities', [])) if intention_data.get(
                    'target_cities') else None

                # 检查是否已存在记录
                check_sql = "SELECT id FROM job_intentions WHERE user_id = %s"
                cursor.execute(check_sql, (user_id,))
                existing = cursor.fetchone()

                if existing:
                    # 更新现有记录
                    sql = """
                    UPDATE job_intentions SET
                    target_industries = %s,
                    industry_priority = %s,
                    target_positions = %s,
                    position_priority = %s,
                    target_cities = %s,
                    city_priority = %s,
                    salary_min = %s,
                    salary_max = %s,
                    salary_type = %s,
                    salary_negotiable = %s,
                    availability = %s,
                    available_date = %s,
                    updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                    """
                    values = (
                        target_industries,
                        intention_data.get('industry_priority'),
                        target_positions,
                        intention_data.get('position_priority'),
                        target_cities,
                        intention_data.get('city_priority'),
                        intention_data.get('salary_min'),
                        intention_data.get('salary_max'),
                        intention_data.get('salary_type', 'monthly'),
                        intention_data.get('salary_negotiable', 1),
                        intention_data.get('availability'),
                        intention_data.get('available_date'),
                        user_id
                    )
                    cursor.execute(sql, values)
                    self.connection.commit()
                    return existing['id']
                else:
                    # 插入新记录
                    sql = """
                    INSERT INTO job_intentions 
                    (user_id, target_industries, industry_priority, target_positions, 
                     position_priority, target_cities, city_priority, salary_min, 
                     salary_max, salary_type, salary_negotiable, availability, available_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        user_id,
                        target_industries,
                        intention_data.get('industry_priority'),
                        target_positions,
                        intention_data.get('position_priority'),
                        target_cities,
                        intention_data.get('city_priority'),
                        intention_data.get('salary_min'),
                        intention_data.get('salary_max'),
                        intention_data.get('salary_type', 'monthly'),
                        intention_data.get('salary_negotiable', 1),
                        intention_data.get('availability'),
                        intention_data.get('available_date')
                    )
                    cursor.execute(sql, values)
                    self.connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            print('更新求职意向失败:', e)
            return None

    def get_job_intention(self, user_id: int) -> Optional[Dict]:
        """获取用户求职意向"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM job_intentions WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()

                # 解析JSON字段
                if result:
                    if result['target_industries']:
                        result['target_industries'] = json.loads(result['target_industries'])
                    if result['target_positions']:
                        result['target_positions'] = json.loads(result['target_positions'])
                    if result['target_cities']:
                        result['target_cities'] = json.loads(result['target_cities'])

                return result
        except Exception as e:
            print('获取求职意向失败:', e)
            return None

    def get_city_distribution(self) -> List[Dict]:
        """获取期望城市分布"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # 由于city_priority是单个值，我们可以直接统计
                sql = """
                SELECT city_priority, COUNT(*) as count
                FROM job_intentions
                WHERE city_priority IS NOT NULL AND city_priority != ''
                GROUP BY city_priority
                ORDER BY count DESC
                LIMIT 10
                """
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print('获取城市分布失败:', e)
            return []

    def get_salary_range_stats(self) -> Dict:
        """获取薪资范围统计"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT 
                    AVG(salary_min) as avg_min_salary,
                    AVG(salary_max) as avg_max_salary,
                    MIN(salary_min) as min_salary_min,
                    MAX(salary_max) as max_salary_max
                FROM job_intentions
                WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL
                """
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取薪资统计失败:', e)
            return {}


class JobPreferences:
    def __init__(self, db_connection):
        self.connection = db_connection

    def upsert_job_preference(self, user_id: int, preference_data: Dict) -> Optional[int]:
        """更新或插入求职偏好"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # 检查是否已存在记录
                check_sql = "SELECT id FROM job_preferences WHERE user_id = %s"
                cursor.execute(check_sql, (user_id,))
                existing = cursor.fetchone()

                if existing:
                    # 更新现有记录
                    sql = """
                    UPDATE job_preferences SET
                    accept_intern_to_full = %s,
                    accept_remote_city = %s,
                    need_campus_referral = %s,
                    accept_overtime = %s,
                    accept_business_trip = %s,
                    company_size_preference = %s,
                    work_type_preference = %s,
                    other_preferences = %s,
                    updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                    """
                    values = (
                        preference_data.get('accept_intern_to_full', 1),
                        preference_data.get('accept_remote_city', 0),
                        preference_data.get('need_campus_referral', 1),
                        preference_data.get('accept_overtime'),
                        preference_data.get('accept_business_trip'),
                        preference_data.get('company_size_preference'),
                        preference_data.get('work_type_preference'),
                        preference_data.get('other_preferences'),
                        user_id
                    )
                    cursor.execute(sql, values)
                    self.connection.commit()
                    return existing['id']
                else:
                    # 插入新记录
                    sql = """
                    INSERT INTO job_preferences 
                    (user_id, accept_intern_to_full, accept_remote_city, need_campus_referral,
                     accept_overtime, accept_business_trip, company_size_preference,
                     work_type_preference, other_preferences)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        user_id,
                        preference_data.get('accept_intern_to_full', 1),
                        preference_data.get('accept_remote_city', 0),
                        preference_data.get('need_campus_referral', 1),
                        preference_data.get('accept_overtime'),
                        preference_data.get('accept_business_trip'),
                        preference_data.get('company_size_preference'),
                        preference_data.get('work_type_preference'),
                        preference_data.get('other_preferences')
                    )
                    cursor.execute(sql, values)
                    self.connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            print('更新求职偏好失败:', e)
            return None

    def get_job_preference(self, user_id: int) -> Optional[Dict]:
        """获取用户求职偏好"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM job_preferences WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取求职偏好失败:', e)
            return None

    def get_work_preference_stats(self) -> Dict:
        """获取工作偏好统计"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT 
                    AVG(accept_intern_to_full) as avg_accept_intern_to_full,
                    AVG(accept_remote_city) as avg_accept_remote_city,
                    AVG(need_campus_referral) as avg_need_campus_referral,
                    AVG(accept_overtime) as avg_accept_overtime,
                    AVG(accept_business_trip) as avg_accept_business_trip
                FROM job_preferences
                """
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取工作偏好统计失败:', e)
            return {}


class ResumeManager:
    """简历管理器，提供综合操作"""

    def __init__(self, db_connection):
        self.connection = db_connection
        self.resumes = Resumes(db_connection)
        self.certificates = Certificates(db_connection)
        self.campus_experiences = CampusExperiences(db_connection)
        self.internships = Internships(db_connection)
        self.job_intentions = JobIntentions(db_connection)
        self.job_preferences = JobPreferences(db_connection)

    def get_complete_resume(self, user_id: int) -> Dict[str, Any]:
        """获取用户完整的简历信息"""
        try:
            result = {
                'basic_info': None,
                'certificates': [],
                'campus_experiences': None,
                'internships': [],
                'job_intention': None,
                'job_preference': None,
                'internship_stats': None
            }

            # 获取基本信息
            result['basic_info'] = self.resumes.get_resume_by_user(user_id)

            # 获取证书
            result['certificates'] = self.certificates.get_user_certificates(user_id)

            # 获取校园经历
            result['campus_experiences'] = self.campus_experiences.get_campus_experience(user_id)

            # 获取实习经历
            result['internships'] = self.internships.get_user_internships(user_id)

            # 获取实习统计
            result['internship_stats'] = self.internships.get_internship_stats(user_id)

            # 获取求职意向
            result['job_intention'] = self.job_intentions.get_job_intention(user_id)

            # 获取求职偏好
            result['job_preference'] = self.job_preferences.get_job_preference(user_id)

            return result
        except Exception as e:
            print('获取完整简历失败:', e)
            return {}

    def search_resumes(self, filters: Dict) -> List[Dict]:
        """根据条件搜索简历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                base_sql = """
                SELECT 
                    r.*, 
                    u.real_name as user_name,
                    u.mobile,
                    j.salary_min,
                    j.salary_max,
                    j.target_cities,
                    is_stats.total_count as internship_count,
                    is_stats.related_count as related_internship_count
                FROM resumes r
                LEFT JOIN sys_user u ON r.user_id = u.user_id
                LEFT JOIN job_intentions j ON r.user_id = j.user_id
                LEFT JOIN internship_stats is_stats ON r.user_id = is_stats.user_id
                WHERE 1=1
                """
                values = []

                # 添加过滤条件
                if filters.get('education_level'):
                    base_sql += " AND r.education_level = %s"
                    values.append(filters['education_level'])

                if filters.get('graduation_year'):
                    base_sql += " AND r.graduation_year = %s"
                    values.append(filters['graduation_year'])

                if filters.get('school_name'):
                    base_sql += " AND r.school_name LIKE %s"
                    values.append(f"%{filters['school_name']}%")

                if filters.get('city'):
                    base_sql += " AND r.city = %s"
                    values.append(filters['city'])

                if filters.get('major'):
                    base_sql += " AND r.major LIKE %s"
                    values.append(f"%{filters['major']}%")

                if filters.get('has_internship'):
                    base_sql += " AND EXISTS (SELECT 1 FROM internships i WHERE i.user_id = r.user_id)"

                if filters.get('min_internship_count'):
                    base_sql += " AND is_stats.total_count >= %s"
                    values.append(filters['min_internship_count'])

                if filters.get('min_salary'):
                    base_sql += " AND (j.salary_min >= %s OR j.salary_max >= %s)"
                    values.append(filters['min_salary'])
                    values.append(filters['min_salary'])

                # 排序
                order_by = filters.get('order_by', 'r.updated_at')
                order_dir = filters.get('order_dir', 'DESC')
                base_sql += f" ORDER BY {order_by} {order_dir}"

                # 分页
                if filters.get('limit'):
                    base_sql += " LIMIT %s"
                    values.append(filters['limit'])

                if filters.get('offset'):
                    base_sql += " OFFSET %s"
                    values.append(filters['offset'])

                cursor.execute(base_sql, values)
                result = cursor.fetchall()

                # 解析JSON字段
                for item in result:
                    if item.get('target_cities'):
                        item['target_cities'] = json.loads(item['target_cities'])

                return result
        except Exception as e:
            print('搜索简历失败:', e)
            return []

    def get_resume_stats(self) -> Dict:
        """获取简历统计信息"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT 
                    (SELECT COUNT(*) FROM resumes) as total_resumes,
                    (SELECT COUNT(DISTINCT user_id) FROM resumes) as total_users,
                    (SELECT COUNT(*) FROM certificates) as total_certificates,
                    (SELECT COUNT(*) FROM internships) as total_internships,
                    (SELECT AVG(total_count) FROM internship_stats) as avg_internship_count
                """
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        except Exception as e:
            print('获取简历统计失败:', e)
            return {}

    def batch_update_resumes(self, update_data: Dict, conditions: Dict) -> int:
        """批量更新简历"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # 构建更新SQL
                set_clauses = []
                set_values = []

                for key, value in update_data.items():
                    if key in ['education_level', 'major', 'city']:
                        set_clauses.append(f"{key} = %s")
                        set_values.append(value)

                if not set_clauses:
                    return 0

                # 构建条件SQL
                where_clauses = []
                where_values = []

                if conditions.get('education_level'):
                    where_clauses.append("education_level = %s")
                    where_values.append(conditions['education_level'])

                if conditions.get('graduation_year'):
                    where_clauses.append("graduation_year = %s")
                    where_values.append(conditions['graduation_year'])

                if conditions.get('city'):
                    where_clauses.append("city = %s")
                    where_values.append(conditions['city'])

                where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

                # 执行更新
                values = set_values + where_values
                sql = f"UPDATE resumes SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE {where_sql}"

                cursor.execute(sql, values)
                self.connection.commit()

                return cursor.rowcount
        except Exception as e:
            print('批量更新简历失败:', e)
            return 0


import pymysql
from pymysql.cursors import DictCursor
from typing import List, Dict, Any, Optional
from datetime import datetime


class ComplaintFeedbackManager:
    def __init__(self, db_connection):
        """
        初始化投诉反馈管理器
        Args:
            db_connection: pymysql 数据库连接对象
        """
        self.connection = db_connection

    def _execute_query(self, sql: str, params: tuple = None, fetch_all: bool = False, fetch_one: bool = False):
        """
        通用查询执行方法
        Args:
            sql: SQL语句
            params: 参数元组
            fetch_all: 是否获取所有结果
            fetch_one: 是否获取单个结果
        Returns:
            查询结果
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                cursor.execute(sql, params or ())
                if fetch_all:
                    return cursor.fetchall()
                elif fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.rowcount
        except pymysql.Error as e:
            print(f'数据库查询失败: {e}')
            return None

    def _execute_update(self, sql: str, params: tuple = None):
        """
        通用更新执行方法
        Args:
            sql: SQL语句
            params: 参数元组
        Returns:
            是否成功
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params or ())
                self.connection.commit()
                return cursor.rowcount > 0
        except pymysql.Error as e:
            print(f'数据库更新失败: {e}')
            self.connection.rollback()
            return False

    # 1. 获取所有投诉类型
    def get_all_complaint_types(self):
        """
        获取所有投诉类型
        Returns: 投诉类型列表
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                SELECT type_code, type_name, sort_order, is_active
                FROM complaint_type
                WHERE is_active = 1
                ORDER BY sort_order, type_code;
                """
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except pymysql.Error as e:
            print(f'获取投诉类型失败: {e}')
            return None

    # 2. 根据类型代码获取类型信息
    def get_complaint_type_by_code(self, type_code: int):
        """
        根据类型代码获取投诉类型信息
        Args:
            type_code: 投诉类型代码
        Returns: 投诉类型信息
        """
        sql = """
        SELECT type_code, type_name 
        FROM complaint_type 
        WHERE type_code = %s AND is_active = 1
        """
        return self._execute_query(sql, (type_code,), fetch_one=True)

    # 3. 用户提交投诉
    def submit_complaint(self, user_id: int, complaint_type: int,
                         description: str, image_urls: List[str] = None,
                         priority: int = 1):
        """
        用户提交投诉
        Args:
            user_id: 用户ID
            complaint_type: 投诉类型代码
            description: 投诉描述
            image_urls: 图片URL列表(最多3个)
            priority: 优先级(1-低, 2-中, 3-高)
        Returns: 插入的投诉ID
        """
        try:
            # 处理图片URL
            image_url_1 = image_urls[0] if image_urls and len(image_urls) > 0 else None
            image_url_2 = image_urls[1] if image_urls and len(image_urls) > 1 else None
            image_url_3 = image_urls[2] if image_urls and len(image_urls) > 2 else None

            sql = """
            INSERT INTO user_feedback 
            (user_id, complaint_type, description, image_url_1, image_url_2, image_url_3, priority)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            with self.connection.cursor() as cursor:
                cursor.execute(sql, (user_id, complaint_type, description,
                                     image_url_1, image_url_2, image_url_3, priority))
                self.connection.commit()
                return cursor.lastrowid
        except pymysql.Error as e:
            print(f'提交投诉失败: {e}')
            self.connection.rollback()
            return None

    # 4. 获取用户的所有投诉
    def get_user_complaints(self, user_id: int, is_resolved: Optional[int] = None):
        """
        获取指定用户的所有投诉
        Args:
            user_id: 用户ID
            is_resolved: 解决状态(0-未解决, 1-已解决, None-全部)
        Returns: 投诉列表
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                base_sql = """
                SELECT uf.*, ct.type_name 
                FROM user_feedback uf
                LEFT JOIN complaint_type ct ON uf.complaint_type = ct.type_code
                WHERE uf.user_id = %s
                """
                params = [user_id]

                if is_resolved is not None:
                    base_sql += " AND uf.is_resolved = %s"
                    params.append(is_resolved)

                base_sql += " ORDER BY uf.create_time DESC"

                cursor.execute(base_sql, tuple(params))
                return cursor.fetchall()
        except pymysql.Error as e:
            print(f'获取用户(user_id={user_id})投诉失败: {e}')
            return None

    # 5. 根据投诉ID获取投诉详情
    def get_complaint_by_id(self, complaint_id: int):
        """
        根据ID获取投诉详情
        Args:
            complaint_id: 投诉ID
        Returns: 投诉详情
        """
        sql = """
        SELECT uf.*, ct.type_name,
               su.username as resolved_by_name
        FROM user_feedback uf
        LEFT JOIN complaint_type ct ON uf.complaint_type = ct.type_code
        LEFT JOIN sys_user su ON uf.resolved_by = su.user_id
        WHERE uf.id = %s
        """
        return self._execute_query(sql, (complaint_id,), fetch_one=True)

    # 6. 管理员回复投诉
    def reply_complaint(self, complaint_id: int, feedback_content: str,
                        resolved_by: int, mark_resolved: bool = True):
        """
        管理员回复投诉
        Args:
            complaint_id: 投诉ID
            feedback_content: 回复内容
            resolved_by: 解决人ID
            mark_resolved: 是否标记为已解决
        Returns: 是否成功
        """
        try:
            # 如果标记为已解决，需要设置解决时间
            if mark_resolved:
                sql = """
                UPDATE user_feedback 
                SET feedback_content = %s, 
                    resolved_by = %s, 
                    is_resolved = 1, 
                    resolve_time = NOW(),
                    update_time = NOW()
                WHERE id = %s
                """
            else:
                sql = """
                UPDATE user_feedback 
                SET feedback_content = %s, 
                    resolved_by = %s,
                    update_time = NOW()
                WHERE id = %s
                """

            return self._execute_update(sql, (feedback_content, resolved_by, complaint_id))
        except pymysql.Error as e:
            print(f'回复投诉(ID={complaint_id})失败: {e}')
            return False

    # 7. 更新投诉状态
    def update_complaint_status(self, complaint_id: int, is_resolved: int,
                                resolved_by: Optional[int] = None):
        """
        更新投诉解决状态
        Args:
            complaint_id: 投诉ID
            is_resolved: 解决状态(0-未解决, 1-已解决)
            resolved_by: 解决人ID(可选)
        Returns: 是否成功
        """
        try:
            if is_resolved == 1:
                # 标记为已解决，设置解决时间和解决人
                sql = """
                UPDATE user_feedback 
                SET is_resolved = %s, 
                    resolve_time = NOW(),
                    resolved_by = %s,
                    update_time = NOW()
                WHERE id = %s
                """
                params = (is_resolved, resolved_by, complaint_id)
            else:
                # 标记为未解决，清空解决时间和解决人
                sql = """
                UPDATE user_feedback 
                SET is_resolved = %s, 
                    resolve_time = NULL,
                    resolved_by = NULL,
                    update_time = NOW()
                WHERE id = %s
                """
                params = (is_resolved, complaint_id)

            return self._execute_update(sql, params)
        except pymysql.Error as e:
            print(f'更新投诉(ID={complaint_id})状态失败: {e}')
            return False

    # 8. 更新投诉优先级
    def update_complaint_priority(self, complaint_id: int, priority: int):
        """
        更新投诉优先级
        Args:
            complaint_id: 投诉ID
            priority: 优先级(1-低, 2-中, 3-高)
        Returns: 是否成功
        """
        sql = """
        UPDATE user_feedback 
        SET priority = %s, update_time = NOW()
        WHERE id = %s
        """
        return self._execute_update(sql, (priority, complaint_id))

    # 9. 管理员获取投诉列表(支持多种筛选条件)
    def get_complaint_list(self, filters: Dict[str, Any] = None,
                           page: int = 1, page_size: int = 20):
        """
        管理员获取投诉列表(支持筛选和分页)
        Args:
            filters: 筛选条件字典
                    {
                        'user_id': 用户ID,
                        'complaint_type': 投诉类型,
                        'is_resolved': 解决状态,
                        'priority': 优先级,
                        'start_date': 开始日期,
                        'end_date': 结束日期
                    }
            page: 页码
            page_size: 每页数量
        Returns: (投诉列表, 总数量)
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                # 基础查询SQL
                base_sql = """
                SELECT SQL_CALC_FOUND_ROWS 
                       uf.*, ct.type_name,
                       su.username as user_name
                FROM user_feedback uf
                LEFT JOIN complaint_type ct ON uf.complaint_type = ct.type_code
                LEFT JOIN sys_user su ON uf.user_id = su.user_id
                WHERE 1=1
                """
                params = []

                # 动态添加筛选条件
                if filters:
                    if filters.get('user_id'):
                        base_sql += " AND uf.user_id = %s"
                        params.append(filters['user_id'])

                    if filters.get('complaint_type'):
                        base_sql += " AND uf.complaint_type = %s"
                        params.append(filters['complaint_type'])

                    if filters.get('is_resolved') is not None:
                        base_sql += " AND uf.is_resolved = %s"
                        params.append(filters['is_resolved'])

                    if filters.get('priority'):
                        base_sql += " AND uf.priority = %s"
                        params.append(filters['priority'])

                    if filters.get('start_date'):
                        base_sql += " AND uf.create_time >= %s"
                        params.append(filters['start_date'])

                    if filters.get('end_date'):
                        base_sql += " AND uf.create_time <= %s"
                        params.append(filters['end_date'])

                # 排序和分页
                base_sql += " ORDER BY uf.priority DESC, uf.create_time DESC"
                base_sql += " LIMIT %s OFFSET %s"

                offset = (page - 1) * page_size
                params.extend([page_size, offset])

                cursor.execute(base_sql, tuple(params))
                result = cursor.fetchall()

                # 获取总记录数
                cursor.execute("SELECT FOUND_ROWS() as total")
                total = cursor.fetchone()['total']

                return result, total
        except pymysql.Error as e:
            print(f'获取投诉列表失败: {e}')
            return None, 0

    # 10. 获取投诉统计信息
    def get_complaint_statistics(self):
        """
        获取投诉统计信息
        Returns: 统计信息字典
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                # 按类型统计
                sql_type = """
                SELECT ct.type_name, COUNT(uf.id) as count
                FROM complaint_type ct
                LEFT JOIN user_feedback uf ON ct.type_code = uf.complaint_type
                WHERE ct.is_active = 1
                GROUP BY ct.type_code, ct.type_name
                ORDER BY ct.sort_order
                """
                cursor.execute(sql_type)
                type_stats = cursor.fetchall()

                # 按状态统计
                sql_status = """
                SELECT 
                    SUM(CASE WHEN is_resolved = 0 THEN 1 ELSE 0 END) as unresolved_count,
                    SUM(CASE WHEN is_resolved = 1 THEN 1 ELSE 0 END) as resolved_count,
                    COUNT(*) as total_count
                FROM user_feedback
                """
                cursor.execute(sql_status)
                status_stats = cursor.fetchone()

                # 按优先级统计
                sql_priority = """
                SELECT 
                    priority,
                    COUNT(*) as count
                FROM user_feedback
                GROUP BY priority
                ORDER BY priority DESC
                """
                cursor.execute(sql_priority)
                priority_stats = cursor.fetchall()

                # 最近一周投诉趋势
                sql_trend = """
                SELECT 
                    DATE(create_time) as date,
                    COUNT(*) as count
                FROM user_feedback
                WHERE create_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
                GROUP BY DATE(create_time)
                ORDER BY date
                """
                cursor.execute(sql_trend)
                trend_stats = cursor.fetchall()

                return {
                    'type_stats': type_stats,
                    'status_stats': status_stats,
                    'priority_stats': priority_stats,
                    'trend_stats': trend_stats
                }
        except pymysql.Error as e:
            print(f'获取投诉统计失败: {e}')
            return None

    # 11. 删除投诉
    def delete_complaint(self, complaint_id: int):
        """
        删除投诉
        Args:
            complaint_id: 投诉ID
        Returns: 是否成功
        """
        sql = "DELETE FROM user_feedback WHERE id = %s"
        return self._execute_update(sql, (complaint_id,))

    # 12. 批量更新投诉状态
    def batch_update_status(self, complaint_ids: List[int], is_resolved: int,
                            resolved_by: Optional[int] = None):
        """
        批量更新投诉状态
        Args:
            complaint_ids: 投诉ID列表
            is_resolved: 解决状态
            resolved_by: 解决人ID
        Returns: 成功更新的数量
        """
        if not complaint_ids:
            return 0

        try:
            with self.connection.cursor() as cursor:
                placeholders = ','.join(['%s'] * len(complaint_ids))

                if is_resolved == 1:
                    sql = f"""
                    UPDATE user_feedback 
                    SET is_resolved = %s, 
                        resolve_time = NOW(),
                        resolved_by = %s,
                        update_time = NOW()
                    WHERE id IN ({placeholders})
                    """
                    params = [is_resolved, resolved_by] + complaint_ids
                else:
                    sql = f"""
                    UPDATE user_feedback 
                    SET is_resolved = %s, 
                        resolve_time = NULL,
                        resolved_by = NULL,
                        update_time = NOW()
                    WHERE id IN ({placeholders})
                    """
                    params = [is_resolved] + complaint_ids

                cursor.execute(sql, tuple(params))
                self.connection.commit()
                return cursor.rowcount
        except pymysql.Error as e:
            print(f'批量更新投诉状态失败: {e}')
            self.connection.rollback()
            return 0

    # 13. 获取未解决的投诉数量
    def get_unresolved_count(self):
        """
        获取未解决的投诉数量
        Returns: 未解决投诉数量
        """
        sql = "SELECT COUNT(*) as count FROM user_feedback WHERE is_resolved = 0"
        result = self._execute_query(sql, fetch_one=True)
        return result['count'] if result else 0

    # 14. 获取最近N天的投诉
    def get_recent_complaints(self, days: int = 7):
        """
        获取最近N天的投诉
        Args:
            days: 天数
        Returns: 投诉列表
        """
        sql = """
        SELECT uf.*, ct.type_name, su.username as user_name
        FROM user_feedback uf
        LEFT JOIN complaint_type ct ON uf.complaint_type = ct.type_code
        LEFT JOIN sys_user su ON uf.user_id = su.user_id
        WHERE uf.create_time >= DATE_SUB(NOW(), INTERVAL %s DAY)
        ORDER BY uf.create_time DESC
        """
        return self._execute_query(sql, (days,), fetch_all=True)

    # 15. 获取高优先级未解决投诉
    def get_high_priority_unresolved(self):
        """
        获取高优先级未解决投诉
        Returns: 高优先级未解决投诉列表
        """
        sql = """
        SELECT uf.*, ct.type_name, su.username as user_name
        FROM user_feedback uf
        LEFT JOIN complaint_type ct ON uf.complaint_type = ct.type_code
        LEFT JOIN sys_user su ON uf.user_id = su.user_id
        WHERE uf.is_resolved = 0 AND uf.priority >= 2
        ORDER BY uf.priority DESC, uf.create_time ASC
        """
        return self._execute_query(sql, fetch_all=True)

    # 16. 检查投诉是否存在
    def complaint_exists(self, complaint_id: int):
        """
        检查投诉是否存在
        Args:
            complaint_id: 投诉ID
        Returns: 是否存在
        """
        sql = "SELECT 1 FROM user_feedback WHERE id = %s"
        result = self._execute_query(sql, (complaint_id,), fetch_one=True)
        return result is not None

    # 17. 获取用户未解决投诉数量
    def get_user_unresolved_count(self, user_id: int):
        """
        获取用户未解决投诉数量
        Args:
            user_id: 用户ID
        Returns: 未解决投诉数量
        """
        sql = "SELECT COUNT(*) as count FROM user_feedback WHERE user_id = %s AND is_resolved = 0"
        result = self._execute_query(sql, (user_id,), fetch_one=True)
        return result['count'] if result else 0

    # 18. 添加投诉类型
    def add_complaint_type(self, type_name: str, sort_order: int = 0):
        """
        添加投诉类型
        Args:
            type_name: 类型名称
            sort_order: 排序顺序
        Returns: 插入的类型代码
        """
        try:
            # 获取当前最大的type_code
            sql_max = "SELECT MAX(type_code) as max_code FROM complaint_type"
            result = self._execute_query(sql_max, fetch_one=True)
            max_code = result['max_code'] if result else 0
            new_code = max_code + 1

            sql = """
            INSERT INTO complaint_type (type_code, type_name, sort_order, is_active)
            VALUES (%s, %s, %s, 1)
            """

            with self.connection.cursor() as cursor:
                cursor.execute(sql, (new_code, type_name, sort_order))
                self.connection.commit()
                return new_code
        except pymysql.Error as e:
            print(f'添加投诉类型失败: {e}')
            self.connection.rollback()
            return None

    # 19. 更新投诉类型状态
    def update_complaint_type_status(self, type_code: int, is_active: int):
        """
        更新投诉类型状态
        Args:
            type_code: 类型代码
            is_active: 是否激活(0-否, 1-是)
        Returns: 是否成功
        """
        sql = """
        UPDATE complaint_type 
        SET is_active = %s
        WHERE type_code = %s
        """
        return self._execute_update(sql, (is_active, type_code))



