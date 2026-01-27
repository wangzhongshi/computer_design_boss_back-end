import pymysql
from pymysql import Error
import json

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


from pymysql.cursors import DictCursor  # 或者对应库的 DictCursor

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
            base_sql = """
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


