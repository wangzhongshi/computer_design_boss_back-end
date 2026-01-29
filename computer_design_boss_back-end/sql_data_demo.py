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


class ComplaintTypeManager:
    """投诉类型字典表管理类"""

    def __init__(self, db_connection):
        self.connection = db_connection

    def get_all_types(self):
        """获取所有投诉类型（启用的）"""
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    SELECT type_code, type_name, sort_order 
                    FROM complaint_type 
                    WHERE is_active = 1 
                    ORDER BY sort_order ASC, type_code ASC
                """
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print('获取投诉类型列表失败:', e)
            return None

    def get_type_by_code(self, type_code):
        """根据类型代码获取投诉类型"""
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    SELECT type_code, type_name, sort_order, is_active 
                    FROM complaint_type 
                    WHERE type_code = %s
                """
                cursor.execute(sql, (type_code,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f'获取投诉类型(type_code={type_code})失败:', e)
            return None

    def add_type(self, type_code, type_name, sort_order=0):
        """添加新的投诉类型"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO complaint_type (type_code, type_name, sort_order) 
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (type_code, type_name, sort_order))
                self.connection.commit()
                return True
        except Exception as e:
            print('添加投诉类型失败:', e)
            self.connection.rollback()
            return False

    def update_type(self, type_code, type_name=None, sort_order=None, is_active=None):
        """更新投诉类型"""
        try:
            with self.connection.cursor() as cursor:
                fields = []
                values = []

                if type_name is not None:
                    fields.append("type_name = %s")
                    values.append(type_name)
                if sort_order is not None:
                    fields.append("sort_order = %s")
                    values.append(sort_order)
                if is_active is not None:
                    fields.append("is_active = %s")
                    values.append(is_active)

                if not fields:
                    return True

                sql = f"UPDATE complaint_type SET {', '.join(fields)} WHERE type_code = %s"
                values.append(type_code)
                cursor.execute(sql, tuple(values))
                self.connection.commit()
                return True
        except Exception as e:
            print('更新投诉类型失败:', e)
            self.connection.rollback()
            return False


class UserFeedbackManager:
    """用户投诉及反馈表管理类"""

    def __init__(self, db_connection):
        self.connection = db_connection

    def get_feedback_list(self, user_id=None, complaint_type=None, is_resolved=None, limit=20, offset=0):
        """获取反馈列表，支持条件筛选"""
        try:
            with self.connection.cursor(DictCursor) as cursor:
                conditions = []
                values = []

                if user_id is not None:
                    conditions.append("f.user_id = %s")
                    values.append(user_id)
                if complaint_type is not None:
                    conditions.append("f.complaint_type = %s")
                    values.append(complaint_type)
                if is_resolved is not None:
                    conditions.append("f.is_resolved = %s")
                    values.append(is_resolved)

                where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

                sql = f"""
                    SELECT 
                        f.id, f.user_id, f.complaint_type, 
                        ct.type_name as complaint_type_name,
                        f.description, f.image_url_1, f.image_url_2, f.image_url_3,
                        f.feedback_content, f.is_resolved, f.priority,
                        f.create_time, f.update_time, f.resolve_time, f.resolved_by
                    FROM user_feedback f
                    LEFT JOIN complaint_type ct ON f.complaint_type = ct.type_code
                    {where_clause}
                    ORDER BY f.create_time DESC
                    LIMIT %s OFFSET %s
                """
                values.extend([limit, offset])
                cursor.execute(sql, tuple(values))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print('获取反馈列表失败:', e)
            return None

    def get_feedback_by_id(self, feedback_id):
        """根据ID获取单个反馈详情"""
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    SELECT 
                        f.*, ct.type_name as complaint_type_name
                    FROM user_feedback f
                    LEFT JOIN complaint_type ct ON f.complaint_type = ct.type_code
                    WHERE f.id = %s
                """
                cursor.execute(sql, (feedback_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f'获取反馈详情(id={feedback_id})失败:', e)
            return None

    def add_feedback(self, user_id, complaint_type, description,
                     image_url_1=None, image_url_2=None, image_url_3=None, priority=1):
        """添加用户反馈"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO user_feedback 
                    (user_id, complaint_type, description, image_url_1, image_url_2, image_url_3, priority)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (user_id, complaint_type, description,
                                     image_url_1, image_url_2, image_url_3, priority))
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print('添加用户反馈失败:', e)
            self.connection.rollback()
            return None

    def update_feedback(self, feedback_id, description=None, priority=None):
        """更新反馈信息（仅限未解决前）"""
        try:
            with self.connection.cursor() as cursor:
                fields = []
                values = []

                if description is not None:
                    fields.append("description = %s")
                    values.append(description)
                if priority is not None:
                    fields.append("priority = %s")
                    values.append(priority)

                if not fields:
                    return True

                sql = f"UPDATE user_feedback SET {', '.join(fields)} WHERE id = %s AND is_resolved = 0"
                values.append(feedback_id)

                cursor.execute(sql, tuple(values))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print('更新反馈失败:', e)
            self.connection.rollback()
            return False

    def resolve_feedback(self, feedback_id, resolved_by, feedback_content):
        """解决反馈（管理员操作）"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE user_feedback 
                    SET is_resolved = 1, 
                        resolved_by = %s, 
                        feedback_content = %s,
                        resolve_time = NOW()
                    WHERE id = %s AND is_resolved = 0
                """
                cursor.execute(sql, (resolved_by, feedback_content, feedback_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print('解决反馈失败:', e)
            self.connection.rollback()
            return False

    def get_user_feedback_stats(self, user_id):
        """获取用户的反馈统计"""
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN is_resolved = 1 THEN 1 ELSE 0 END) as resolved,
                        SUM(CASE WHEN is_resolved = 0 THEN 1 ELSE 0 END) as unresolved
                    FROM user_feedback 
                    WHERE user_id = %s
                """
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f'获取用户反馈统计失败:', e)
            return None

    def delete_feedback(self, feedback_id):
        """删除反馈（谨慎使用）"""
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM user_feedback WHERE id = %s"
                cursor.execute(sql, (feedback_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print('删除反馈失败:', e)
            self.connection.rollback()
            return False


from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional


class JobSchema(BaseModel):
    id: int
    title: str
    salary_min: float  # 自动转换
    salary_max: float
    salary_desc: str

    class Config:
        from_attributes = True
        # 或者使用 json_encoders 自定义
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class UserFavoriteJobs:
    def __init__(self, db_connection):
        self.connection = db_connection
        self.db = EndDemoDatabase(host='localhost', user='root', password='123456')
        self.job_prot = Job_prot(self.db.connection)

    def add_favorite(self, user_id, job_id, remarks=None):
        """
        添加岗位收藏（支持软删除后的重新收藏）
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                # 先查询是否已有记录
                check_sql = """
                    SELECT id, is_canceled FROM user_favorite_jobs 
                    WHERE user_id = %s AND boss_job_id = %s
                """
                cursor.execute(check_sql, (user_id, job_id))
                existing = cursor.fetchone()

                job_snapshot = self.job_prot.fetch_one_job_all_data_posts(job_id)[0]
                job_snapshot = JobSchema.model_validate(job_snapshot).model_dump()

                # ✅ 关键修复：将字典转为 JSON 字符串
                job_snapshot_json = json.dumps(job_snapshot, ensure_ascii=False)

                if existing:
                    if existing['is_canceled'] == 1:
                        update_sql = """
                            UPDATE user_favorite_jobs 
                            SET is_canceled = 0, 
                                job_snapshot = %s,
                                remarks = %s,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = %s
                        """
                        cursor.execute(update_sql, (job_snapshot_json, remarks, existing['id']))
                        self.connection.commit()
                        return {'success': True, 'message': '重新收藏成功', 'id': existing['id']}
                    else:
                        return {'success': False, 'message': '该岗位已在收藏列表中'}
                else:
                    insert_sql = """
                        INSERT INTO user_favorite_jobs 
                        (user_id, boss_job_id, job_snapshot, remarks) 
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_sql, (user_id, job_id, job_snapshot_json, remarks))
                    self.connection.commit()
                    return {'success': True, 'message': '收藏成功', 'id': cursor.lastrowid}

        except Exception as e:
            self.connection.rollback()
            print('添加收藏失败:', e)
            return {'success': False, 'message': f'添加收藏失败: {str(e)}'}

    def cancel_favorite(self, user_id, boss_job_id):
        """
        取消收藏（软删除）
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    UPDATE user_favorite_jobs 
                    SET is_canceled = 1, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
                """
                cursor.execute(sql, (user_id, boss_job_id))
                self.connection.commit()

                if cursor.rowcount > 0:
                    return {'success': True, 'message': '取消收藏成功'}
                else:
                    return {'success': False, 'message': '未找到有效的收藏记录'}

        except Exception as e:
            self.connection.rollback()
            print('取消收藏失败:', e)
            return {'success': False, 'message': f'取消收藏失败: {str(e)}'}

    def get_user_favorites(self, user_id, include_canceled=False):
        """
        获取用户的收藏列表
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                if include_canceled:
                    sql = """
                        SELECT id, user_id, boss_job_id, is_canceled, 
                               job_snapshot, remarks, created_at, updated_at
                        FROM user_favorite_jobs 
                        WHERE user_id = %s
                        ORDER BY created_at DESC
                    """
                    cursor.execute(sql, (user_id,))
                else:
                    sql = """
                        SELECT id, user_id, boss_job_id, 
                               job_snapshot, remarks, created_at, updated_at
                        FROM user_favorite_jobs 
                        WHERE user_id = %s AND is_canceled = 0
                        ORDER BY created_at DESC
                    """
                    cursor.execute(sql, (user_id,))

                result = cursor.fetchall()
                return result

        except Exception as e:
            print('查询用户收藏列表失败:', e)
            return None

    def check_is_favorite(self, user_id, boss_job_id):
        """
        检查用户是否已收藏某岗位
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    SELECT id FROM user_favorite_jobs 
                    WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
                """
                cursor.execute(sql, (user_id, boss_job_id))
                result = cursor.fetchone()
                return result is not None

        except Exception as e:
            print('检查收藏状态失败:', e)
            return False

    def update_remarks(self, user_id, boss_job_id, remarks):
        """
        更新收藏备注
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    UPDATE user_favorite_jobs 
                    SET remarks = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
                """
                cursor.execute(sql, (remarks, user_id, boss_job_id))
                self.connection.commit()

                if cursor.rowcount > 0:
                    return {'success': True, 'message': '备注更新成功'}
                else:
                    return {'success': False, 'message': '未找到有效的收藏记录'}

        except Exception as e:
            self.connection.rollback()
            print('更新备注失败:', e)
            return {'success': False, 'message': f'更新备注失败: {str(e)}'}

    def get_favorite_detail(self, user_id, boss_job_id):
        """
        获取单条收藏详情
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    SELECT id, user_id, boss_job_id, is_canceled,
                           job_snapshot, remarks, created_at, updated_at
                    FROM user_favorite_jobs 
                    WHERE user_id = %s AND boss_job_id = %s
                """
                cursor.execute(sql, (user_id, boss_job_id))
                result = cursor.fetchone()
                return result

        except Exception as e:
            print('查询收藏详情失败:', e)
            return None

    def batch_cancel_favorites(self, user_id, boss_job_id_list):
        """
        批量取消收藏
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                format_strings = ','.join(['%s'] * len(boss_job_id_list))
                sql = f"""
                    UPDATE user_favorite_jobs 
                    SET is_canceled = 1, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND boss_job_id IN ({format_strings}) AND is_canceled = 0
                """
                cursor.execute(sql, (user_id,) + tuple(boss_job_id_list))
                self.connection.commit()

                return {
                    'success': True,
                    'message': f'成功取消 {cursor.rowcount} 条收藏',
                    'affected_rows': cursor.rowcount
                }

        except Exception as e:
            self.connection.rollback()
            print('批量取消收藏失败:', e)
            return {'success': False, 'message': f'批量取消收藏失败: {str(e)}'}

class UserDeliverJobs:
    def __init__(self, db_connection):
        self.connection = db_connection
        self.db = EndDemoDatabase(host='localhost', user='root', password='123456')
        self.job_prot = Job_prot(self.db.connection)

    def add_deliver(self, user_id, job_id, remarks=None):
        """
        添加岗位收藏（支持软删除后的重新收藏）
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                # 先查询是否已有记录
                check_sql = """
                    SELECT id, is_canceled FROM user_deliver_jobs 
                    WHERE user_id = %s AND boss_job_id = %s
                """
                cursor.execute(check_sql, (user_id, job_id))
                existing = cursor.fetchone()

                job_snapshot = self.job_prot.fetch_one_job_all_data_posts(job_id)[0]
                job_snapshot = JobSchema.model_validate(job_snapshot).model_dump()

                # ✅ 关键修复：将字典转为 JSON 字符串
                job_snapshot_json = json.dumps(job_snapshot, ensure_ascii=False)

                if existing:
                    if existing['is_canceled'] == 1:
                        update_sql = """
                            UPDATE user_deliver_jobs 
                            SET is_canceled = 0, 
                                job_snapshot = %s,
                                remarks = %s,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = %s
                        """
                        cursor.execute(update_sql, (job_snapshot_json, remarks, existing['id']))
                        self.connection.commit()
                        return {'success': True, 'message': '重新收藏成功', 'id': existing['id']}
                    else:
                        return {'success': False, 'message': '该岗位已在收藏列表中'}
                else:
                    insert_sql = """
                        INSERT INTO user_deliver_jobs 
                        (user_id, boss_job_id, job_snapshot, remarks) 
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_sql, (user_id, job_id, job_snapshot_json, remarks))
                    self.connection.commit()
                    return {'success': True, 'message': '收藏成功', 'id': cursor.lastrowid}

        except Exception as e:
            self.connection.rollback()
            print('添加收藏失败:', e)
            return {'success': False, 'message': f'添加收藏失败: {str(e)}'}

    def cancel_deliver(self, user_id, boss_job_id):
        """
        取消投递（软删除）
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    UPDATE user_deliver_jobs 
                    SET is_canceled = 1, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
                """
                cursor.execute(sql, (user_id, boss_job_id))
                self.connection.commit()

                if cursor.rowcount > 0:
                    return {'success': True, 'message': '取消投递成功'}
                else:
                    return {'success': False, 'message': '未找到有效的投递记录'}

        except Exception as e:
            self.connection.rollback()
            print('取消投递失败:', e)
            return {'success': False, 'message': f'取消投递失败: {str(e)}'}

    def get_user_delivers(self, user_id, include_canceled=False):
        """
        获取用户的投递列表
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                if include_canceled:
                    sql = """
                        SELECT id, user_id, boss_job_id, is_canceled, 
                               job_snapshot, remarks, created_at, updated_at
                        FROM user_deliver_jobs 
                        WHERE user_id = %s
                        ORDER BY created_at DESC
                    """
                    cursor.execute(sql, (user_id,))
                else:
                    sql = """
                        SELECT id, user_id, boss_job_id, 
                               job_snapshot, remarks, created_at, updated_at
                        FROM user_deliver_jobs 
                        WHERE user_id = %s AND is_canceled = 0
                        ORDER BY created_at DESC
                    """
                    cursor.execute(sql, (user_id,))

                result = cursor.fetchall()
                return result

        except Exception as e:
            print('查询用户投递列表失败:', e)
            return None

    def check_is_deliver(self, user_id, boss_job_id):
        """
        检查用户是否已投递某岗位
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    SELECT id FROM user_deliver_jobs 
                    WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
                """
                cursor.execute(sql, (user_id, boss_job_id))
                result = cursor.fetchone()
                return result is not None

        except Exception as e:
            print('检查投递状态失败:', e)
            return False

    def update_remarks(self, user_id, boss_job_id, remarks):
        """
        更新投递备注
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    UPDATE user_deliver_jobs 
                    SET remarks = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
                """
                cursor.execute(sql, (remarks, user_id, boss_job_id))
                self.connection.commit()

                if cursor.rowcount > 0:
                    return {'success': True, 'message': '备注更新成功'}
                else:
                    return {'success': False, 'message': '未找到有效的投递记录'}

        except Exception as e:
            self.connection.rollback()
            print('更新备注失败:', e)
            return {'success': False, 'message': f'更新备注失败: {str(e)}'}

    def get_deliver_detail(self, user_id, boss_job_id):
        """
        获取单条投递详情
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                sql = """
                    SELECT id, user_id, boss_job_id, is_canceled,
                           job_snapshot, remarks, created_at, updated_at
                    FROM user_deliver_jobs 
                    WHERE user_id = %s AND boss_job_id = %s
                """
                cursor.execute(sql, (user_id, boss_job_id))
                result = cursor.fetchone()
                return result

        except Exception as e:
            print('查询投递详情失败:', e)
            return None

    def batch_cancel_delivers(self, user_id, boss_job_id_list):
        """
        批量取消投递
        """
        try:
            with self.connection.cursor(DictCursor) as cursor:
                format_strings = ','.join(['%s'] * len(boss_job_id_list))
                sql = f"""
                    UPDATE user_deliver_jobs 
                    SET is_canceled = 1, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND boss_job_id IN ({format_strings}) AND is_canceled = 0
                """
                cursor.execute(sql, (user_id,) + tuple(boss_job_id_list))
                self.connection.commit()

                return {
                    'success': True,
                    'message': f'成功取消 {cursor.rowcount} 条投递',
                    'affected_rows': cursor.rowcount
                }

        except Exception as e:
            self.connection.rollback()
            print('批量取消投递失败:', e)
            return {'success': False, 'message': f'批量取消投递失败: {str(e)}'}

