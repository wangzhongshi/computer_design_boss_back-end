from pymysql import Error
import json
from pymysql.cursors import DictCursor
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel
from decimal import Decimal
from flask import g
from dbutils.pooled_db import PooledDB
import pymysql
from contextlib import contextmanager
from datetime import datetime
from set_up import config

# 配置类（假设结构）
class Config:
    def __init__(self):
        self.set_db_host = 'localhost'
        self.set_db_prot = 3306
        self.set_db_user = 'root'
        self.set_db_password = 'password'
        self.set_db_name = 'boss_job'

config_data = config()


class DatabasePool:
    """数据库连接池管理器"""
    _pool = None

    @classmethod
    def init_pool(cls):
        """初始化连接池（应用启动时调用一次）"""
        if cls._pool is None:
            cls._pool = PooledDB(
                creator=pymysql,
                maxconnections=200,
                mincached=5,
                maxcached=100,
                blocking=True,
                ping=1,
                host=config_data.set_db_host,
                port=config_data.set_db_prot,
                user=config_data.set_db_user,
                password=config_data.set_db_password,
                database=getattr(config_data, 'set_db_name', 'boss_job'),
                charset='utf8mb4',
                cursorclass=DictCursor,
                autocommit=True
            )
            print(f"[{datetime.now()}] [INFO] DatabasePool: 连接池初始化完成")
        return cls._pool

    @classmethod
    def get_connection(cls):
        """从连接池获取连接"""
        if cls._pool is None:
            cls.init_pool()
        return cls._pool.connection()


# 初始化连接池
DatabasePool.init_pool()


class BaseManager:
    """管理类基类：每个实例独立获取连接"""

    def __init__(self):
        self._connection = None

    @property
    def connection(self):
        """延迟获取连接：每次使用时从连接池获取"""
        # 优先从 Flask g 对象获取（同请求复用）
        if hasattr(g, 'db_connection'):
            return g.db_connection

        # 否则从连接池获取新连接
        conn = DatabasePool.get_connection()
        g.db_connection = conn  # 存储到 g 中，同请求复用
        return conn

    @contextmanager
    def get_cursor(self, cursor_class=DictCursor):
        """上下文管理器获取游标，自动关闭"""
        conn = self.connection
        cursor = conn.cursor(cursor_class) if cursor_class else conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def execute_query(self, sql: str, params: Optional[Tuple] = None) -> List[Dict]:
        """执行查询的通用方法"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchall()
        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] {self.__class__.__name__}.execute_query: SQL执行失败 | SQL: {sql} | 参数: {params} | 错误: {e}")
            raise

    def execute_one(self, sql: str, params: Optional[Tuple] = None) -> Optional[Dict]:
        """执行查询返回单条"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchone()
        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] {self.__class__.__name__}.execute_one: SQL执行失败 | SQL: {sql} | 参数: {params} | 错误: {e}")
            raise

    def execute_update(self, sql: str, params: Optional[Tuple] = None) -> int:
        """执行更新/插入/删除"""
        conn = self.connection
        cursor = conn.cursor()
        try:
            result = cursor.execute(sql, params or ())
            conn.commit()
            print(f"[{datetime.now()}] [INFO] {self.__class__.__name__}.execute_update: 影响行数 {result}")
            return result
        except Exception as e:
            conn.rollback()
            print(
                f"[{datetime.now()}] [ERROR] {self.__class__.__name__}.execute_update: 事务回滚 | SQL: {sql} | 参数: {params} | 错误: {e}")
            raise
        finally:
            cursor.close()


class Job_prot(BaseManager):
    """职位信息操作类"""

    def __init__(self):
        super().__init__()

    def fetch_some_job_posts_all(self) -> Optional[List[Dict]]:
        """
        获取全部职位列表信息
        :return: 职位列表或None
        """
        try:
            columns = [
                'id', 'title', 'salary_min', 'salary_max', 'edu_req',
                'exp_req', 'emp_type', 'company', 'city', 'welfare_list', 'publish_time'
            ]
            select_clause = ", ".join(f"`{c}`" for c in columns)
            sql = f"SELECT {select_clause} FROM job_post"

            result = self.execute_query(sql)
            print(f"[{datetime.now()}] [INFO] Job_prot.fetch_some_job_posts_all: 成功获取 {len(result)} 条职位记录")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Job_prot.fetch_some_job_posts_all: 查询失败 | 错误: {e}")
            return None

    def fetch_one_big_type_job_posts(self, category_ids: Optional[List[int]] = None) -> Optional[List[Dict]]:
        """
        获取某一类工作的信息
        :param category_ids: 分类ID列表，如 [101, 102, ...] 整数列表
        :return: 职位列表或None
        """
        try:
            # 默认分类ID列表
            default_categories = [101, 102, 103, 104, 105, 106, 108, 200, 300]
            if category_ids is None:
                category_ids = default_categories

            # 类型转换和验证
            if isinstance(category_ids, (int, str)):
                category_ids = [int(category_ids)]
            else:
                category_ids = [int(cid) for cid in category_ids if str(cid).isdigit()]

            if not category_ids:
                print(f"[{datetime.now()}] [WARN] Job_prot.fetch_one_big_type_job_posts: 无效的分类ID参数")
                return []

            columns = [
                'id', 'title', 'salary_min', 'salary_max', 'edu_req',
                'exp_req', 'emp_type', 'company', 'city', 'welfare_list', 'publish_time'
            ]
            select_clause = ", ".join(f"`{c}`" for c in columns)
            placeholders = ', '.join(['%s'] * len(category_ids))

            sql = f"""
                SELECT {select_clause} 
                FROM job_post 
                WHERE category_id IN ({placeholders}) AND status = 1
            """

            result = self.execute_query(sql, tuple(category_ids))
            print(
                f"[{datetime.now()}] [INFO] Job_prot.fetch_one_big_type_job_posts: 分类 {category_ids} 获取 {len(result)} 条记录")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Job_prot.fetch_one_big_type_job_posts: 查询失败 | 参数: {category_ids} | 错误: {e}")
            return None

    def fetch_some_job_posts_some(self, category_id: int) -> Optional[List[Dict]]:
        """
        获取某一类工作的信息（单分类）
        :param category_id: 分类ID
        :return: 职位列表或None
        """
        try:
            columns = [
                'id', 'title', 'salary_min', 'salary_max', 'edu_req',
                'exp_req', 'emp_type', 'company', 'city', 'welfare_list', 'publish_time'
            ]
            select_clause = ", ".join(f"`{c}`" for c in columns)
            sql = f"SELECT {select_clause} FROM job_post WHERE category_id = %s"

            result = self.execute_query(sql, (category_id,))
            print(
                f"[{datetime.now()}] [INFO] Job_prot.fetch_some_job_posts_some: 分类ID {category_id} 获取 {len(result)} 条记录")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Job_prot.fetch_some_job_posts_some: 查询失败 | 分类ID: {category_id} | 错误: {e}")
            return None

    def fetch_job_list_by_two_given(self, emp_type: str, category_id: int) -> Optional[List[Dict]]:
        """
        获取指定雇佣类型和分类的职位列表（如全职-综合）
        :param emp_type: 雇佣类型
        :param category_id: 分类ID
        :return: 职位列表或None
        """
        try:
            columns = [
                'id', 'title', 'salary_min', 'salary_max', 'edu_req',
                'exp_req', 'emp_type', 'company_id', 'city_id', 'welfare_list', 'publish_time'
            ]
            select_clause = ", ".join(f"`{c}`" for c in columns)
            sql = f"""
                SELECT {select_clause} 
                FROM job_post 
                WHERE category_id = %s AND emp_type = %s
            """

            result = self.execute_query(sql, (category_id, emp_type))
            print(
                f"[{datetime.now()}] [INFO] Job_prot.fetch_job_list_by_two_given: 类型 {emp_type} + 分类 {category_id} 获取 {len(result)} 条记录")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Job_prot.fetch_job_list_by_two_given: 查询失败 | 参数: ({emp_type}, {category_id}) | 错误: {e}")
            return None

    def search_job_by_user_input(self, user_input: str) -> Optional[List[Dict]]:
        """
        通过用户输入搜索岗位
        :param user_input: 用户输入关键词
        :return: 职位列表或None
        """
        try:
            columns = [
                'id', 'title', 'salary_min', 'salary_max', 'edu_req',
                'exp_req', 'emp_type', 'company', 'city', 'welfare_list', 'publish_time'
            ]
            select_clause = ", ".join(f"`{c}`" for c in columns)
            sql = f"SELECT {select_clause} FROM job_post WHERE title LIKE %s"

            result = self.execute_query(sql, (f"%{user_input}%",))
            print(
                f"[{datetime.now()}] [INFO] Job_prot.search_job_by_user_input: 关键词 '{user_input}' 搜索到 {len(result)} 条记录")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Job_prot.search_job_by_user_input: 搜索失败 | 关键词: {user_input} | 错误: {e}")
            return None

    def fetch_one_job_all_data_posts(self, ones_id: int) -> Optional[List[Dict]]:
        """
        获取单个岗位的详细信息
        :param ones_id: 岗位ID
        :return: 岗位详情列表或None
        """
        try:
            sql = "SELECT * FROM job_post WHERE id = %s"
            result = self.execute_query(sql, (ones_id,))
            print(f"[{datetime.now()}] [INFO] Job_prot.fetch_one_job_all_data_posts: 岗位ID {ones_id} 查询成功")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Job_prot.fetch_one_job_all_data_posts: 查询失败 | 岗位ID: {ones_id} | 错误: {e}")
            return None

    def insert_job_post(self, boss_job_id: str, title: str, company_id: int, city_id: int,
                        category_id: int, emp_type: int = 1, salary_min: Optional[float] = None,
                        salary_max: Optional[float] = None, salary_desc: Optional[str] = None,
                        edu_req: Optional[str] = None, exp_req: Optional[str] = None,
                        district: Optional[str] = None, address: Optional[str] = None,
                        recruiter_id: Optional[int] = None, description: Optional[str] = None,
                        require_list: Optional[List] = None, welfare_list: Optional[List] = None,
                        publish_time: Optional[str] = None, refresh_time: Optional[str] = None,
                        status: int = 1) -> Optional[int]:
        """
        发布职位信息
        :return: 插入的职位ID或None
        """
        try:
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

            params = (
                boss_job_id, title, company_id, city_id, category_id, emp_type,
                salary_min, salary_max, salary_desc, edu_req, exp_req,
                district, address, recruiter_id, description,
                require_list_json, welfare_list_json, publish_time, refresh_time, status
            )

            with self.get_cursor(cursor_class=None) as cursor:
                cursor.execute(sql, params)
                job_id = cursor.lastrowid
                self.connection.commit()
                print(
                    f"[{datetime.now()}] [INFO] Job_prot.insert_job_post: 职位发布成功 | 职位ID: {job_id} | 标题: {title}")
                return job_id

        except Exception as e:
            self.connection.rollback()
            print(f"[{datetime.now()}] [ERROR] Job_prot.insert_job_post: 职位发布失败 | 标题: {title} | 错误: {e}")
            return None


class Job_category_simple(BaseManager):
    """职位分类操作类"""

    # 分类数据缓存
    CATEGORIES = [
        {"id": 100, "name": "技术开发类", "parent_id": None, "level": 1},
        {"id": 101, "name": "前端", "parent_id": 100, "level": 2},
        {"id": 102, "name": "后端", "parent_id": 100, "level": 2},
        {"id": 103, "name": "移动端", "parent_id": 100, "level": 2},
        {"id": 104, "name": "数据与AI", "parent_id": 100, "level": 2},
        {"id": 105, "name": "测试", "parent_id": 100, "level": 2},
        {"id": 106, "name": "运维/DevOps", "parent_id": 100, "level": 2},
        {"id": 107, "name": "网络安全", "parent_id": 100, "level": 2},
        {"id": 108, "name": "嵌入式/硬件", "parent_id": 100, "level": 2},
        {"id": 200, "name": "产品与设计类", "parent_id": None, "level": 1},
        {"id": 300, "name": "技术管理类", "parent_id": None, "level": 1}
    ]

    def find_name_by_id(self, target_id: int) -> Optional[str]:
        """
        根据ID查找分类名称
        :param target_id: 分类ID
        :return: 分类名称或None
        """
        for category in self.CATEGORIES:
            if category["id"] == target_id:
                return category["name"]
        return None

    def job_intro_list(self) -> Optional[List[Dict]]:
        """
        获取职位分类介绍列表
        :return: 分类列表或None
        """
        try:
            sql = "SELECT name, parent_id, intro FROM job_category_simple"
            result = self.execute_query(sql)

            # 处理parent_id为名称
            for line in result:
                parent_name = self.find_name_by_id(line['parent_id'])
                if parent_name and str(line['parent_id']).startswith('10'):
                    line['parent_id_all'] = f"技术开发类-{parent_name}"
                line['parent_id'] = parent_name

            print(f"[{datetime.now()}] [INFO] Job_category_simple.job_intro_list: 成功获取 {len(result)} 条分类记录")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Job_category_simple.job_intro_list: 查询失败 | 错误: {e}")
            return None


class Forum_comments(BaseManager):
    """论坛评论操作类"""

    def forum_all(self) -> Optional[List[Dict]]:
        """
        查询所有评论
        :return: 评论列表或None
        """
        try:
            sql = "SELECT * FROM forum_comments"
            result = self.execute_query(sql)
            print(f"[{datetime.now()}] [INFO] Forum_comments.forum_all: 成功获取 {len(result)} 条评论")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Forum_comments.forum_all: 查询失败 | 错误: {e}")
            return None

    def forum_one_category(self, category_id: int) -> Optional[List[Dict]]:
        """
        查询某一类岗位下的评论
        :param category_id: 分类ID
        :return: 评论列表或None
        """
        try:
            sql = "SELECT * FROM forum_comments WHERE category_id = %s"
            result = self.execute_query(sql, (category_id,))
            print(
                f"[{datetime.now()}] [INFO] Forum_comments.forum_one_category: 分类 {category_id} 获取 {len(result)} 条评论")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Forum_comments.forum_one_category: 查询失败 | 分类ID: {category_id} | 错误: {e}")
            return None

    def forum_all_first_talk(self) -> Optional[List[Dict]]:
        """
        查询所有一级评论
        :return: 一级评论列表或None
        """
        try:
            sql = "SELECT * FROM forum_comments WHERE parent_id IS NULL"
            result = self.execute_query(sql)
            print(f"[{datetime.now()}] [INFO] Forum_comments.forum_all_first_talk: 成功获取 {len(result)} 条一级评论")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Forum_comments.forum_all_first_talk: 查询失败 | 错误: {e}")
            return None

    def forum_talks_back(self, parent_id: int) -> Optional[List[Dict]]:
        """
        查询某个评论的回复
        :param parent_id: 父评论ID
        :return: 回复列表或None
        """
        try:
            sql = "SELECT * FROM forum_comments WHERE parent_id = %s"
            result = self.execute_query(sql, (parent_id,))
            print(
                f"[{datetime.now()}] [INFO] Forum_comments.forum_talks_back: 父评论 {parent_id} 获取 {len(result)} 条回复")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Forum_comments.forum_talks_back: 查询失败 | 父评论ID: {parent_id} | 错误: {e}")
            return None

    def forum_add(self, category_id: int, user_id: int, parent_id: Optional[int],
                  content: str, level: int, sort_order: int) -> bool:
        """
        发布评论
        :return: 是否成功
        """
        try:
            # 把空串统一转成 None
            parent_id = parent_id if parent_id != '' else None

            sql = """
                INSERT INTO forum_comments
                (category_id, user_id, parent_id, content, level, sort_order)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            with self.get_cursor() as cursor:
                cursor.execute(sql, (category_id, user_id, parent_id, content, level, sort_order))
                self.connection.commit()
                print(
                    f"[{datetime.now()}] [INFO] Forum_comments.forum_add: 评论发布成功 | 用户: {user_id} | 分类: {category_id}")
                return True

        except Exception as e:
            self.connection.rollback()
            print(f"[{datetime.now()}] [ERROR] Forum_comments.forum_add: 发布失败 | 用户: {user_id} | 错误: {e}")
            return False

    def forum_delete(self, comment_id: int) -> bool:
        """
        删除评论（软删除）
        :param comment_id: 评论ID
        :return: 是否成功
        """
        try:
            sql = "UPDATE forum_comments SET is_deleted = 1 WHERE id = %s"
            affected = self.execute_update(sql, (comment_id,))

            if affected > 0:
                print(f"[{datetime.now()}] [INFO] Forum_comments.forum_delete: 评论 {comment_id} 删除成功")
                return True
            else:
                print(f"[{datetime.now()}] [WARN] Forum_comments.forum_delete: 评论 {comment_id} 不存在或已被删除")
                return False

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Forum_comments.forum_delete: 删除失败 | 评论ID: {comment_id} | 错误: {e}")
            return False

    def forum_all_by_user(self, user_id: int) -> Optional[List[Dict]]:
        """
        获取用户发布的所有评论（用于个人页展示）
        :param user_id: 用户ID
        :return: 评论列表或None
        """
        try:
            sql = "SELECT * FROM forum_comments WHERE user_id = %s"
            result = self.execute_query(sql, (user_id,))
            print(
                f"[{datetime.now()}] [INFO] Forum_comments.forum_all_by_user: 用户 {user_id} 获取 {len(result)} 条评论")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Forum_comments.forum_all_by_user: 查询失败 | 用户ID: {user_id} | 错误: {e}")
            return None

    def forum_count_all(self, switch: str, category_id: Optional[int] = None,
                        parent_id: Optional[int] = None, user_id: Optional[int] = None) -> Optional[int]:
        """
        统计评论数量
        :param switch: 'all'-全部, 'category'-分类, 'back'-回复, 'user'-用户
        :return: 评论数量或None
        """
        try:
            if switch == 'all':
                sql = "SELECT COUNT(*) as count FROM forum_comments"
                params = ()
            elif switch == 'category':
                sql = "SELECT COUNT(*) as count FROM forum_comments WHERE category_id = %s"
                params = (category_id,)
            elif switch == 'back':
                sql = "SELECT COUNT(*) as count FROM forum_comments WHERE parent_id = %s"
                params = (parent_id,)
            elif switch == 'user':
                sql = "SELECT COUNT(*) as count FROM forum_comments WHERE user_id = %s"
                params = (user_id,)
            else:
                print(f"[{datetime.now()}] [WARN] Forum_comments.forum_count_all: 无效的switch参数 '{switch}'")
                return None

            result = self.execute_one(sql, params)
            count = result['count'] if result else 0
            print(f"[{datetime.now()}] [INFO] Forum_comments.forum_count_all: [{switch}] 统计结果: {count}")
            return count

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Forum_comments.forum_count_all: 统计失败 | 参数: {switch} | 错误: {e}")
            return None


class Sys_user(BaseManager):
    """系统用户操作类"""

    def user_count_all(self, switch: str, status: Optional[int] = None,
                       job_status: Optional[int] = None, is_deleted: int = 0) -> Optional[int]:
        """
        统计用户数量
        :param switch: 'all'-全部, 'status'-按状态, 'job_status'-按求职状态, 'active'-活跃用户
        :return: 用户数量或None
        """
        try:
            conditions = ["is_deleted = %s"]
            params = [is_deleted]

            if switch == 'all':
                pass
            elif switch == 'status' and status is not None:
                conditions.append("status = %s")
                params.append(status)
            elif switch == 'job_status' and job_status is not None:
                conditions.append("job_status = %s")
                params.append(job_status)
            elif switch == 'active':
                conditions.append("status = 1")
            else:
                print(f"[{datetime.now()}] [WARN] Sys_user.user_count_all: 无效的switch参数 '{switch}'")
                return None

            sql = f"SELECT COUNT(*) as count FROM sys_user WHERE {' AND '.join(conditions)}"
            result = self.execute_one(sql, tuple(params))
            count = result['count'] if result else 0
            print(f"[{datetime.now()}] [INFO] Sys_user.user_count_all: [{switch}] 统计结果: {count}")
            return count

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Sys_user.user_count_all: 统计失败 | 错误: {e}")
            return None

    def get_user_by_field(self, field: str, value: Any, include_deleted: bool = False) -> Optional[Dict]:
        """
        根据指定字段获取用户信息
        :param field: 字段名 (user_id, mobile, email, id)
        :param value: 字段值
        :return: 用户信息或None
        """
        try:
            valid_fields = ['user_id', 'mobile', 'email', 'id']
            if field not in valid_fields:
                print(f"[{datetime.now()}] [WARN] Sys_user.get_user_by_field: 无效字段 '{field}'")
                return None

            conditions = [f"{field} = %s"]
            params = [value]

            if not include_deleted:
                conditions.append("is_deleted = 0")

            sql = f"SELECT * FROM sys_user WHERE {' AND '.join(conditions)}"
            result = self.execute_one(sql, tuple(params))
            print(
                f"[{datetime.now()}] [INFO] Sys_user.get_user_by_field: 通过 {field}={value} 查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Sys_user.get_user_by_field: 查询失败 | 字段: {field} | 错误: {e}")
            return None

    def update_user_status(self, user_id: str, status: int) -> bool:
        """
        更新用户状态
        :return: 是否成功
        """
        try:
            sql = """
                UPDATE sys_user 
                SET status = %s, updated_at = NOW() 
                WHERE user_id = %s AND is_deleted = 0
            """
            affected = self.execute_update(sql, (status, user_id))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Sys_user.update_user_status: 用户 {user_id} 状态更新为 {status} | {'成功' if success else '未找到用户'}")
            return success

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Sys_user.update_user_status: 更新失败 | 用户: {user_id} | 错误: {e}")
            return False

    def update_last_login(self, user_id: str, login_ip: str, device_model: str, device_type: str) -> bool:
        """
        更新用户最后登录信息
        :return: 是否成功
        """
        try:
            sql = """
                UPDATE sys_user 
                SET last_login_time = NOW(), last_login_ip = %s, 
                    last_device_model = %s, last_device_type = %s,
                    last_device_time = NOW(), updated_at = NOW()
                WHERE user_id = %s AND is_deleted = 0
            """
            affected = self.execute_update(sql, (login_ip, device_model, device_type, user_id))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Sys_user.update_last_login: 用户 {user_id} 登录信息更新{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Sys_user.update_last_login: 更新失败 | 用户: {user_id} | 错误: {e}")
            return False

    def create_user(self, user_data: Dict) -> Optional[int]:
        """
        创建新用户
        :return: 创建的用户ID或None
        """
        try:
            # 确保必填字段存在
            required_fields = ['user_id', 'mobile', 'password_hash']
            for field in required_fields:
                if field not in user_data:
                    print(f"[{datetime.now()}] [WARN] Sys_user.create_user: 缺少必填字段 '{field}'")
                    return None

            # 构建字段和值
            fields = []
            values = []

            for field, value in user_data.items():
                if value is not None:
                    fields.append(field)
                    values.append(value)

            placeholders = ', '.join(['%s'] * len(fields))
            sql = f"INSERT INTO sys_user ({', '.join(fields)}) VALUES ({placeholders})"

            with self.get_cursor(cursor_class=None) as cursor:
                cursor.execute(sql, tuple(values))
                user_id = cursor.lastrowid
                self.connection.commit()
                print(
                    f"[{datetime.now()}] [INFO] Sys_user.create_user: 用户创建成功 | ID: {user_id} | 手机号: {user_data.get('mobile')}")
                return user_id

        except Exception as e:
            self.connection.rollback()
            print(f"[{datetime.now()}] [ERROR] Sys_user.create_user: 创建失败 | 错误: {e}")
            return None

    def search_users(self, keyword: Optional[str] = None, status: int = 1,
                     page: int = 1, page_size: int = 20) -> Dict:
        """
        搜索用户（支持分页）
        :return: 包含用户列表和分页信息的字典
        """
        try:
            # 基础条件
            conditions = ["is_deleted = 0", "status = %s"]
            params = [status]

            # 关键词搜索
            if keyword:
                conditions.append("(mobile LIKE %s OR email LIKE %s OR real_name LIKE %s)")
                like_pattern = f"%{keyword}%"
                params.extend([like_pattern, like_pattern, like_pattern])

            where_clause = "WHERE " + " AND ".join(conditions)

            # 查询总数
            count_sql = f"SELECT COUNT(*) as total FROM sys_user {where_clause}"
            count_result = self.execute_one(count_sql, tuple(params))
            total = count_result['total'] if count_result else 0

            # 查询分页数据
            offset = (page - 1) * page_size
            data_sql = f"""
                SELECT * FROM sys_user {where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            query_params = params + [page_size, offset]
            users = self.execute_query(data_sql, tuple(query_params))

            result = {
                'users': users,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
            print(f"[{datetime.now()}] [INFO] Sys_user.search_users: 搜索完成 | 总数: {total} | 当前页: {page}")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Sys_user.search_users: 搜索失败 | 错误: {e}")
            return {
                'users': [], 'total': 0, 'page': page,
                'page_size': page_size, 'total_pages': 0
            }

    def soft_delete_user(self, user_id: str) -> bool:
        """
        软删除用户
        :return: 是否成功
        """
        try:
            sql = """
                UPDATE sys_user 
                SET is_deleted = 1, deleted_at = NOW(), updated_at = NOW()
                WHERE user_id = %s AND is_deleted = 0
            """
            affected = self.execute_update(sql, (user_id,))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Sys_user.soft_delete_user: 用户 {user_id} 软删除{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Sys_user.soft_delete_user: 删除失败 | 用户: {user_id} | 错误: {e}")
            return False

    def update_user_profile(self, user_id: str, profile_data: Dict) -> bool:
        """
        更新用户个人信息
        :return: 是否成功
        """
        try:
            if not profile_data:
                print(f"[{datetime.now()}] [WARN] Sys_user.update_user_profile: 更新数据为空")
                return False

            set_clauses = []
            params = []

            for field, value in profile_data.items():
                if value is not None:
                    set_clauses.append(f"{field} = %s")
                    params.append(value)

            if not set_clauses:
                return False

            params.append(user_id)
            sql = f"""
                UPDATE sys_user 
                SET {', '.join(set_clauses)}, updated_at = NOW()
                WHERE user_id = %s AND is_deleted = 0
            """

            affected = self.execute_update(sql, tuple(params))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Sys_user.update_user_profile: 用户 {user_id} 资料更新{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Sys_user.update_user_profile: 更新失败 | 用户: {user_id} | 错误: {e}")
            return False

    def check_user_exists(self, mobile: Optional[str] = None, email: Optional[str] = None,
                          exclude_user_id: Optional[str] = None) -> bool:
        """
        检查用户是否存在
        :return: 是否存在
        """
        try:
            conditions = ["is_deleted = 0"]
            params = []
            or_conditions = []

            if mobile:
                or_conditions.append("mobile = %s")
                params.append(mobile)
            if email:
                or_conditions.append("email = %s")
                params.append(email)

            if not or_conditions:
                return False

            conditions.append(f"({' OR '.join(or_conditions)})")

            if exclude_user_id:
                conditions.append("user_id != %s")
                params.append(exclude_user_id)

            sql = f"SELECT id FROM sys_user WHERE {' AND '.join(conditions)}"
            result = self.execute_one(sql, tuple(params))
            exists = result is not None
            print(
                f"[{datetime.now()}] [INFO] Sys_user.check_user_exists: 检查结果 - {'已存在' if exists else '不存在'}")
            return exists

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Sys_user.check_user_exists: 检查失败 | 错误: {e}")
            return False


class Resumes(BaseManager):
    """简历操作类"""

    def create_resume(self, user_id: int, resume_data: Dict) -> Optional[int]:
        """
        创建简历
        :return: 简历ID或None
        """
        try:
            # 检查是否已存在
            check_sql = "SELECT id FROM resumes WHERE user_id = %s"
            existing = self.execute_one(check_sql, (user_id,))
            if existing:
                print(f"[{datetime.now()}] [WARN] Resumes.create_resume: 用户 {user_id} 已存在简历")
                return None

            # 构建插入SQL
            valid_fields = [
                'real_name', 'gender', 'birth_date', 'phone', 'email',
                'wechat', 'city', 'education_level', 'school_name',
                'major', 'graduation_year', 'gpa', 'resume_file_url',
                'resume_file_name', 'resume_format', 'self_introduction'
            ]

            columns = ['user_id']
            values = [user_id]
            params = [user_id]

            for key, value in resume_data.items():
                if key in valid_fields and value is not None:
                    columns.append(key)
                    values.append(value)
                    params.append(value)

            placeholders = ', '.join(['%s'] * len(values))
            sql = f"INSERT INTO resumes ({', '.join(columns)}) VALUES ({placeholders})"

            with self.get_cursor(cursor_class=None) as cursor:
                cursor.execute(sql, tuple(params))
                resume_id = cursor.lastrowid
                self.connection.commit()
                print(
                    f"[{datetime.now()}] [INFO] Resumes.create_resume: 简历创建成功 | ID: {resume_id} | 用户: {user_id}")
                return resume_id

        except Exception as e:
            self.connection.rollback()
            print(f"[{datetime.now()}] [ERROR] Resumes.create_resume: 创建失败 | 用户: {user_id} | 错误: {e}")
            return None

    def get_resume_by_user(self, user_id: int) -> Optional[Dict]:
        """
        获取用户的简历
        :return: 简历信息或None
        """
        try:
            sql = """
                SELECT r.*, u.mobile, u.email as user_email, u.real_name as user_real_name
                FROM resumes r
                LEFT JOIN sys_user u ON r.user_id = u.user_id
                WHERE r.user_id = %s
            """
            result = self.execute_one(sql, (user_id,))
            print(
                f"[{datetime.now()}] [INFO] Resumes.get_resume_by_user: 用户 {user_id} 简历查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Resumes.get_resume_by_user: 查询失败 | 用户: {user_id} | 错误: {e}")
            return None

    def update_resume(self, user_id: int, update_data: Dict) -> bool:
        """
        更新简历
        :return: 是否成功
        """
        try:
            valid_fields = [
                'real_name', 'gender', 'birth_date', 'phone', 'email',
                'wechat', 'city', 'education_level', 'school_name',
                'major', 'graduation_year', 'gpa', 'resume_file_url',
                'resume_file_name', 'resume_format', 'self_introduction'
            ]

            set_clauses = []
            params = []

            for key, value in update_data.items():
                if key in valid_fields and value is not None:
                    set_clauses.append(f"{key} = %s")
                    params.append(value)

            if not set_clauses:
                print(f"[{datetime.now()}] [WARN] Resumes.update_resume: 无有效更新字段")
                return False

            params.append(user_id)
            sql = f"""
                UPDATE resumes 
                SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP 
                WHERE user_id = %s
            """

            affected = self.execute_update(sql, tuple(params))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Resumes.update_resume: 用户 {user_id} 简历更新{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Resumes.update_resume: 更新失败 | 用户: {user_id} | 错误: {e}")
            return False

    def delete_resume(self, user_id: int) -> bool:
        """
        删除简历
        :return: 是否成功
        """
        try:
            sql = "DELETE FROM resumes WHERE user_id = %s"
            affected = self.execute_update(sql, (user_id,))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Resumes.delete_resume: 用户 {user_id} 简历删除{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Resumes.delete_resume: 删除失败 | 用户: {user_id} | 错误: {e}")
            return False

    def get_resume_count_by_user(self) -> Dict:
        """
        统计用户简历数量
        :return: 统计字典
        """
        try:
            sql = """
                SELECT 
                    COUNT(*) as total_count,
                    COUNT(CASE WHEN education_level = '本科' THEN 1 END) as bachelor_count,
                    COUNT(CASE WHEN education_level = '硕士' THEN 1 END) as master_count,
                    COUNT(CASE WHEN education_level = '博士' THEN 1 END) as doctor_count
                FROM resumes
            """
            result = self.execute_one(sql)
            print(
                f"[{datetime.now()}] [INFO] Resumes.get_resume_count_by_user: 统计完成 | 总数: {result.get('total_count', 0)}")
            return result if result else {}

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Resumes.get_resume_count_by_user: 统计失败 | 错误: {e}")
            return {}


class Certificates(BaseManager):
    """证书操作类"""

    def add_certificate(self, user_id: int, cert_data: Dict) -> Optional[int]:
        """
        添加证书
        :return: 证书ID或None
        """
        try:
            # 检查简历是否存在
            check_sql = "SELECT id FROM resumes WHERE user_id = %s"
            if not self.execute_one(check_sql, (user_id,)):
                print(f"[{datetime.now()}] [WARN] Certificates.add_certificate: 用户 {user_id} 无简历记录")
                return None

            sql = """
                INSERT INTO certificates 
                (user_id, cert_type, cert_name, cert_level, issue_date, expiry_date, 
                 issuing_authority, certificate_no, attachment_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
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

            with self.get_cursor(cursor_class=None) as cursor:
                cursor.execute(sql, params)
                cert_id = cursor.lastrowid
                self.connection.commit()
                print(
                    f"[{datetime.now()}] [INFO] Certificates.add_certificate: 证书添加成功 | ID: {cert_id} | 用户: {user_id}")
                return cert_id

        except Exception as e:
            self.connection.rollback()
            print(f"[{datetime.now()}] [ERROR] Certificates.add_certificate: 添加失败 | 用户: {user_id} | 错误: {e}")
            return None

    def get_user_certificates(self, user_id: int, cert_type: Optional[str] = None) -> List[Dict]:
        """
        获取用户证书列表
        :return: 证书列表
        """
        try:
            if cert_type:
                sql = "SELECT * FROM certificates WHERE user_id = %s AND cert_type = %s ORDER BY issue_date DESC"
                params = (user_id, cert_type)
            else:
                sql = "SELECT * FROM certificates WHERE user_id = %s ORDER BY issue_date DESC"
                params = (user_id,)

            result = self.execute_query(sql, params)
            print(
                f"[{datetime.now()}] [INFO] Certificates.get_user_certificates: 用户 {user_id} 获取 {len(result)} 条证书记录")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Certificates.get_user_certificates: 查询失败 | 用户: {user_id} | 错误: {e}")
            return []

    def get_certificate_by_id(self, cert_id: int, user_id: int) -> Optional[Dict]:
        """
        根据ID获取证书详情
        :return: 证书详情或None
        """
        try:
            sql = "SELECT * FROM certificates WHERE id = %s AND user_id = %s"
            result = self.execute_one(sql, (cert_id, user_id))
            print(
                f"[{datetime.now()}] [INFO] Certificates.get_certificate_by_id: 证书 {cert_id} 查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Certificates.get_certificate_by_id: 查询失败 | 证书ID: {cert_id} | 错误: {e}")
            return None

    def update_certificate(self, cert_id: int, user_id: int, update_data: Dict) -> bool:
        """
        更新证书信息
        :return: 是否成功
        """
        try:
            valid_fields = [
                'cert_type', 'cert_name', 'cert_level', 'issue_date',
                'expiry_date', 'issuing_authority', 'certificate_no', 'attachment_url'
            ]

            set_clauses = []
            params = []

            for key, value in update_data.items():
                if key in valid_fields and value is not None:
                    set_clauses.append(f"{key} = %s")
                    params.append(value)

            if not set_clauses:
                return False

            params.extend([cert_id, user_id])
            sql = f"UPDATE certificates SET {', '.join(set_clauses)} WHERE id = %s AND user_id = %s"

            affected = self.execute_update(sql, tuple(params))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Certificates.update_certificate: 证书 {cert_id} 更新{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Certificates.update_certificate: 更新失败 | 证书ID: {cert_id} | 错误: {e}")
            return False

    def delete_certificate(self, cert_id: int, user_id: int) -> bool:
        """
        删除证书
        :return: 是否成功
        """
        try:
            sql = "DELETE FROM certificates WHERE id = %s AND user_id = %s"
            affected = self.execute_update(sql, (cert_id, user_id))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Certificates.delete_certificate: 证书 {cert_id} 删除{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Certificates.delete_certificate: 删除失败 | 证书ID: {cert_id} | 错误: {e}")
            return False

    def get_certificate_stats(self, user_id: int) -> Dict:
        """
        获取用户证书统计
        :return: 统计字典
        """
        try:
            sql = """
                SELECT 
                    COUNT(*) as total_count,
                    COUNT(CASE WHEN cert_type = 'english' THEN 1 END) as english_count,
                    COUNT(CASE WHEN cert_type = 'computer' THEN 1 END) as computer_count,
                    COUNT(CASE WHEN cert_type = 'professional' THEN 1 END) as professional_count
                FROM certificates 
                WHERE user_id = %s
            """
            result = self.execute_one(sql, (user_id,))
            print(f"[{datetime.now()}] [INFO] Certificates.get_certificate_stats: 用户 {user_id} 统计完成")
            return result if result else {}

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Certificates.get_certificate_stats: 统计失败 | 用户: {user_id} | 错误: {e}")
            return {}


class CampusExperiences(BaseManager):
    """校园经历操作类"""

    def upsert_campus_experience(self, user_id: int, experience_data: Dict) -> Optional[int]:
        """
        更新或插入校园经历
        :return: 记录ID或None
        """
        try:
            # 检查是否已存在
            check_sql = "SELECT id FROM campus_experiences WHERE user_id = %s"
            existing = self.execute_one(check_sql, (user_id,))

            if existing:
                # 更新
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
                params = (
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

                with self.get_cursor(cursor_class=None) as cursor:
                    cursor.execute(sql, params)
                    self.connection.commit()
                    print(
                        f"[{datetime.now()}] [INFO] CampusExperiences.upsert_campus_experience: 用户 {user_id} 校园经历更新成功")
                    return existing['id']
            else:
                # 插入
                sql = """
                    INSERT INTO campus_experiences 
                    (user_id, has_student_union, student_union_details, has_club, 
                     club_details, has_scholarship, scholarship_details, has_honor, honor_details)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
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

                with self.get_cursor(cursor_class=None) as cursor:
                    cursor.execute(sql, params)
                    exp_id = cursor.lastrowid
                    self.connection.commit()
                    print(
                        f"[{datetime.now()}] [INFO] CampusExperiences.upsert_campus_experience: 用户 {user_id} 校园经历创建成功 | ID: {exp_id}")
                    return exp_id

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] CampusExperiences.upsert_campus_experience: 操作失败 | 用户: {user_id} | 错误: {e}")
            return None

    def get_campus_experience(self, user_id: int) -> Optional[Dict]:
        """
        获取用户校园经历
        :return: 校园经历或None
        """
        try:
            sql = "SELECT * FROM campus_experiences WHERE user_id = %s"
            result = self.execute_one(sql, (user_id,))
            print(
                f"[{datetime.now()}] [INFO] CampusExperiences.get_campus_experience: 用户 {user_id} 查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] CampusExperiences.get_campus_experience: 查询失败 | 用户: {user_id} | 错误: {e}")
            return None


class Internships(BaseManager):
    """实习经历操作类"""

    def add_internship(self, user_id: int, internship_data: Dict) -> Optional[int]:
        """
        添加实习经历
        :return: 实习记录ID或None
        """
        try:
            sql = """
                INSERT INTO internships 
                (user_id, company_name, position, industry, start_date, end_date, 
                 is_current, is_related, work_content, achievements)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
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

            with self.get_cursor(cursor_class=None) as cursor:
                cursor.execute(sql, params)
                intern_id = cursor.lastrowid
                self.connection.commit()
                print(
                    f"[{datetime.now()}] [INFO] Internships.add_internship: 实习经历添加成功 | ID: {intern_id} | 用户: {user_id}")
                return intern_id

        except Exception as e:
            self.connection.rollback()
            print(f"[{datetime.now()}] [ERROR] Internships.add_internship: 添加失败 | 用户: {user_id} | 错误: {e}")
            return None

    def get_user_internships(self, user_id: int) -> List[Dict]:
        """
        获取用户实习经历列表
        :return: 实习经历列表
        """
        try:
            sql = """
                SELECT * FROM internships 
                WHERE user_id = %s 
                ORDER BY start_date DESC, end_date DESC
            """
            result = self.execute_query(sql, (user_id,))
            print(
                f"[{datetime.now()}] [INFO] Internships.get_user_internships: 用户 {user_id} 获取 {len(result)} 条实习记录")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Internships.get_user_internships: 查询失败 | 用户: {user_id} | 错误: {e}")
            return []

    def get_internship_by_id(self, internship_id: int, user_id: int) -> Optional[Dict]:
        """
        根据ID获取实习详情
        :return: 实习详情或None
        """
        try:
            sql = "SELECT * FROM internships WHERE id = %s AND user_id = %s"
            result = self.execute_one(sql, (internship_id, user_id))
            print(
                f"[{datetime.now()}] [INFO] Internships.get_internship_by_id: 实习 {internship_id} 查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Internships.get_internship_by_id: 查询失败 | 实习ID: {internship_id} | 错误: {e}")
            return None

    def update_internship(self, internship_id: int, user_id: int, update_data: Dict) -> bool:
        """
        更新实习经历
        :return: 是否成功
        """
        try:
            valid_fields = [
                'company_name', 'position', 'industry', 'start_date',
                'end_date', 'is_current', 'is_related', 'work_content', 'achievements'
            ]

            set_clauses = []
            params = []

            for key, value in update_data.items():
                if key in valid_fields and value is not None:
                    set_clauses.append(f"{key} = %s")
                    params.append(value)

            if not set_clauses:
                return False

            params.extend([internship_id, user_id])
            sql = f"UPDATE internships SET {', '.join(set_clauses)} WHERE id = %s AND user_id = %s"

            affected = self.execute_update(sql, tuple(params))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Internships.update_internship: 实习 {internship_id} 更新{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Internships.update_internship: 更新失败 | 实习ID: {internship_id} | 错误: {e}")
            return False

    def delete_internship(self, internship_id: int, user_id: int) -> bool:
        """
        删除实习经历
        :return: 是否成功
        """
        try:
            sql = "DELETE FROM internships WHERE id = %s AND user_id = %s"
            affected = self.execute_update(sql, (internship_id, user_id))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] Internships.delete_internship: 实习 {internship_id} 删除{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Internships.delete_internship: 删除失败 | 实习ID: {internship_id} | 错误: {e}")
            return False

    def get_internship_stats(self, user_id: int) -> Optional[Dict]:
        """
        获取实习统计信息
        :return: 统计信息或None
        """
        try:
            sql = "SELECT * FROM internship_stats WHERE user_id = %s"
            result = self.execute_one(sql, (user_id,))
            print(
                f"[{datetime.now()}] [INFO] Internships.get_internship_stats: 用户 {user_id} 统计查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] Internships.get_internship_stats: 查询失败 | 用户: {user_id} | 错误: {e}")
            return None

    def get_industry_distribution(self) -> List[Dict]:
        """
        获取实习行业分布
        :return: 行业分布列表
        """
        try:
            sql = """
                SELECT industry, COUNT(*) as count
                FROM internships
                WHERE industry IS NOT NULL AND industry != ''
                GROUP BY industry
                ORDER BY count DESC
                LIMIT 10
            """
            result = self.execute_query(sql)
            print(f"[{datetime.now()}] [INFO] Internships.get_industry_distribution: 获取 {len(result)} 个行业分布")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] Internships.get_industry_distribution: 查询失败 | 错误: {e}")
            return []


class JobIntentions(BaseManager):
    """求职意向操作类"""

    def upsert_job_intention(self, user_id: int, intention_data: Dict) -> Optional[int]:
        """
        更新或插入求职意向
        :return: 记录ID或None
        """
        try:
            # 处理JSON字段
            target_industries = json.dumps(intention_data.get('target_industries', []),
                                           ensure_ascii=False) if intention_data.get('target_industries') else None
            target_positions = json.dumps(intention_data.get('target_positions', []),
                                          ensure_ascii=False) if intention_data.get('target_positions') else None
            target_cities = json.dumps(intention_data.get('target_cities', []),
                                       ensure_ascii=False) if intention_data.get('target_cities') else None

            # 检查是否已存在
            check_sql = "SELECT id FROM job_intentions WHERE user_id = %s"
            existing = self.execute_one(check_sql, (user_id,))

            if existing:
                # 更新
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
                params = (
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

                with self.get_cursor(cursor_class=None) as cursor:
                    cursor.execute(sql, params)
                    self.connection.commit()
                    print(
                        f"[{datetime.now()}] [INFO] JobIntentions.upsert_job_intention: 用户 {user_id} 求职意向更新成功")
                    return existing['id']
            else:
                # 插入
                sql = """
                    INSERT INTO job_intentions 
                    (user_id, target_industries, industry_priority, target_positions, 
                     position_priority, target_cities, city_priority, salary_min, 
                     salary_max, salary_type, salary_negotiable, availability, available_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
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

                with self.get_cursor(cursor_class=None) as cursor:
                    cursor.execute(sql, params)
                    intention_id = cursor.lastrowid
                    self.connection.commit()
                    print(
                        f"[{datetime.now()}] [INFO] JobIntentions.upsert_job_intention: 用户 {user_id} 求职意向创建成功 | ID: {intention_id}")
                    return intention_id

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] JobIntentions.upsert_job_intention: 操作失败 | 用户: {user_id} | 错误: {e}")
            return None

    def get_job_intention(self, user_id: int) -> Optional[Dict]:
        """
        获取用户求职意向
        :return: 求职意向或None
        """
        try:
            sql = "SELECT * FROM job_intentions WHERE user_id = %s"
            result = self.execute_one(sql, (user_id,))

            # 解析JSON字段
            if result:
                for field in ['target_industries', 'target_positions', 'target_cities']:
                    if result.get(field):
                        try:
                            result[field] = json.loads(result[field])
                        except json.JSONDecodeError:
                            result[field] = []

            print(
                f"[{datetime.now()}] [INFO] JobIntentions.get_job_intention: 用户 {user_id} 查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] JobIntentions.get_job_intention: 查询失败 | 用户: {user_id} | 错误: {e}")
            return None

    def get_city_distribution(self) -> List[Dict]:
        """
        获取期望城市分布
        :return: 城市分布列表
        """
        try:
            sql = """
                SELECT city_priority, COUNT(*) as count
                FROM job_intentions
                WHERE city_priority IS NOT NULL AND city_priority != ''
                GROUP BY city_priority
                ORDER BY count DESC
                LIMIT 10
            """
            result = self.execute_query(sql)
            print(f"[{datetime.now()}] [INFO] JobIntentions.get_city_distribution: 获取 {len(result)} 个城市分布")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] JobIntentions.get_city_distribution: 查询失败 | 错误: {e}")
            return []

    def get_salary_range_stats(self) -> Dict:
        """
        获取薪资范围统计
        :return: 统计字典
        """
        try:
            sql = """
                SELECT 
                    AVG(salary_min) as avg_min_salary,
                    AVG(salary_max) as avg_max_salary,
                    MIN(salary_min) as min_salary_min,
                    MAX(salary_max) as max_salary_max
                FROM job_intentions
                WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL
            """
            result = self.execute_one(sql)
            print(f"[{datetime.now()}] [INFO] JobIntentions.get_salary_range_stats: 薪资统计完成")
            return result if result else {}

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] JobIntentions.get_salary_range_stats: 统计失败 | 错误: {e}")
            return {}


class JobPreferences(BaseManager):
    """求职偏好操作类"""

    def upsert_job_preference(self, user_id: int, preference_data: Dict) -> Optional[int]:
        """
        更新或插入求职偏好
        :return: 记录ID或None
        """
        try:
            # 检查是否已存在
            check_sql = "SELECT id FROM job_preferences WHERE user_id = %s"
            existing = self.execute_one(check_sql, (user_id,))

            if existing:
                # 更新
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
                params = (
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

                with self.get_cursor(cursor_class=None) as cursor:
                    cursor.execute(sql, params)
                    self.connection.commit()
                    print(
                        f"[{datetime.now()}] [INFO] JobPreferences.upsert_job_preference: 用户 {user_id} 求职偏好更新成功")
                    return existing['id']
            else:
                # 插入
                sql = """
                    INSERT INTO job_preferences 
                    (user_id, accept_intern_to_full, accept_remote_city, need_campus_referral,
                     accept_overtime, accept_business_trip, company_size_preference,
                     work_type_preference, other_preferences)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
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

                with self.get_cursor(cursor_class=None) as cursor:
                    cursor.execute(sql, params)
                    pref_id = cursor.lastrowid
                    self.connection.commit()
                    print(
                        f"[{datetime.now()}] [INFO] JobPreferences.upsert_job_preference: 用户 {user_id} 求职偏好创建成功 | ID: {pref_id}")
                    return pref_id

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] JobPreferences.upsert_job_preference: 操作失败 | 用户: {user_id} | 错误: {e}")
            return None

    def get_job_preference(self, user_id: int) -> Optional[Dict]:
        """
        获取用户求职偏好
        :return: 求职偏好或None
        """
        try:
            sql = "SELECT * FROM job_preferences WHERE user_id = %s"
            result = self.execute_one(sql, (user_id,))
            print(
                f"[{datetime.now()}] [INFO] JobPreferences.get_job_preference: 用户 {user_id} 查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] JobPreferences.get_job_preference: 查询失败 | 用户: {user_id} | 错误: {e}")
            return None

    def get_work_preference_stats(self) -> Dict:
        """
        获取工作偏好统计
        :return: 统计字典
        """
        try:
            sql = """
                SELECT 
                    AVG(accept_intern_to_full) as avg_accept_intern_to_full,
                    AVG(accept_remote_city) as avg_accept_remote_city,
                    AVG(need_campus_referral) as avg_need_campus_referral,
                    AVG(accept_overtime) as avg_accept_overtime,
                    AVG(accept_business_trip) as avg_accept_business_trip
                FROM job_preferences
            """
            result = self.execute_one(sql)
            print(f"[{datetime.now()}] [INFO] JobPreferences.get_work_preference_stats: 偏好统计完成")
            return result if result else {}

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] JobPreferences.get_work_preference_stats: 统计失败 | 错误: {e}")
            return {}


class ResumeManager(BaseManager):
    """简历管理器，提供综合操作"""

    def __init__(self):
        super().__init__()
        self.resumes = Resumes()
        self.certificates = Certificates()
        self.campus_experiences = CampusExperiences()
        self.internships = Internships()
        self.job_intentions = JobIntentions()
        self.job_preferences = JobPreferences()

    def get_complete_resume(self, user_id: int) -> Dict[str, Any]:
        """
        获取用户完整的简历信息
        :return: 完整简历信息字典
        """
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

            result['basic_info'] = self.resumes.get_resume_by_user(user_id)
            result['certificates'] = self.certificates.get_user_certificates(user_id)
            result['campus_experiences'] = self.campus_experiences.get_campus_experience(user_id)
            result['internships'] = self.internships.get_user_internships(user_id)
            result['internship_stats'] = self.internships.get_internship_stats(user_id)
            result['job_intention'] = self.job_intentions.get_job_intention(user_id)
            result['job_preference'] = self.job_preferences.get_job_preference(user_id)

            print(f"[{datetime.now()}] [INFO] ResumeManager.get_complete_resume: 用户 {user_id} 完整简历获取成功")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] ResumeManager.get_complete_resume: 获取失败 | 用户: {user_id} | 错误: {e}")
            return {}

    def search_resumes(self, filters: Dict) -> List[Dict]:
        """
        根据条件搜索简历
        :return: 简历列表
        """
        try:
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

            result = self.execute_query(base_sql, tuple(values))

            # 解析JSON字段
            for item in result:
                if item.get('target_cities'):
                    try:
                        item['target_cities'] = json.loads(item['target_cities'])
                    except json.JSONDecodeError:
                        item['target_cities'] = []

            print(f"[{datetime.now()}] [INFO] ResumeManager.search_resumes: 搜索完成 | 结果数: {len(result)}")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] ResumeManager.search_resumes: 搜索失败 | 错误: {e}")
            return []

    def get_resume_stats(self) -> Dict:
        """
        获取简历统计信息
        :return: 统计字典
        """
        try:
            sql = """
                SELECT 
                    (SELECT COUNT(*) FROM resumes) as total_resumes,
                    (SELECT COUNT(DISTINCT user_id) FROM resumes) as total_users,
                    (SELECT COUNT(*) FROM certificates) as total_certificates,
                    (SELECT COUNT(*) FROM internships) as total_internships,
                    (SELECT AVG(total_count) FROM internship_stats) as avg_internship_count
            """
            result = self.execute_one(sql)
            print(f"[{datetime.now()}] [INFO] ResumeManager.get_resume_stats: 统计完成")
            return result if result else {}

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] ResumeManager.get_resume_stats: 统计失败 | 错误: {e}")
            return {}

    def batch_update_resumes(self, update_data: Dict, conditions: Dict) -> int:
        """
        批量更新简历
        :return: 影响行数
        """
        try:
            valid_fields = ['education_level', 'major', 'city']
            set_clauses = []
            set_values = []

            for key, value in update_data.items():
                if key in valid_fields and value is not None:
                    set_clauses.append(f"{key} = %s")
                    set_values.append(value)

            if not set_clauses:
                print(f"[{datetime.now()}] [WARN] ResumeManager.batch_update_resumes: 无有效更新字段")
                return 0

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
            values = set_values + where_values

            sql = f"UPDATE resumes SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE {where_sql}"

            affected = self.execute_update(sql, tuple(values))
            print(f"[{datetime.now()}] [INFO] ResumeManager.batch_update_resumes: 批量更新完成 | 影响行数: {affected}")
            return affected

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] ResumeManager.batch_update_resumes: 更新失败 | 错误: {e}")
            return 0


class ComplaintTypeManager(BaseManager):
    """投诉类型字典表管理类"""

    def get_all_types(self) -> Optional[List[Dict]]:
        """
        获取所有启用的投诉类型
        :return: 类型列表或None
        """
        try:
            sql = """
                SELECT type_code, type_name, sort_order 
                FROM complaint_type 
                WHERE is_active = 1 
                ORDER BY sort_order ASC, type_code ASC
            """
            result = self.execute_query(sql)
            print(f"[{datetime.now()}] [INFO] ComplaintTypeManager.get_all_types: 获取 {len(result)} 种投诉类型")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] ComplaintTypeManager.get_all_types: 查询失败 | 错误: {e}")
            return None

    def get_type_by_code(self, type_code: str) -> Optional[Dict]:
        """
        根据类型代码获取投诉类型
        :return: 类型信息或None
        """
        try:
            sql = """
                SELECT type_code, type_name, sort_order, is_active 
                FROM complaint_type 
                WHERE type_code = %s
            """
            result = self.execute_one(sql, (type_code,))
            print(
                f"[{datetime.now()}] [INFO] ComplaintTypeManager.get_type_by_code: 类型 {type_code} 查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] ComplaintTypeManager.get_type_by_code: 查询失败 | 类型码: {type_code} | 错误: {e}")
            return None

    def add_type(self, type_code: str, type_name: str, sort_order: int = 0) -> bool:
        """
        添加新的投诉类型
        :return: 是否成功
        """
        try:
            sql = """
                INSERT INTO complaint_type (type_code, type_name, sort_order) 
                VALUES (%s, %s, %s)
            """
            with self.get_cursor(cursor_class=None) as cursor:
                cursor.execute(sql, (type_code, type_name, sort_order))
                self.connection.commit()
                print(f"[{datetime.now()}] [INFO] ComplaintTypeManager.add_type: 投诉类型 {type_code} 添加成功")
                return True

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] ComplaintTypeManager.add_type: 添加失败 | 类型码: {type_code} | 错误: {e}")
            return False

    def update_type(self, type_code: str, type_name: Optional[str] = None,
                    sort_order: Optional[int] = None, is_active: Optional[int] = None) -> bool:
        """
        更新投诉类型
        :return: 是否成功
        """
        try:
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

            values.append(type_code)
            sql = f"UPDATE complaint_type SET {', '.join(fields)} WHERE type_code = %s"

            affected = self.execute_update(sql, tuple(values))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] ComplaintTypeManager.update_type: 类型 {type_code} 更新{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] ComplaintTypeManager.update_type: 更新失败 | 类型码: {type_code} | 错误: {e}")
            return False


class UserFeedbackManager(BaseManager):
    """用户投诉及反馈表管理类"""

    def get_feedback_list(self, user_id: Optional[int] = None, complaint_type: Optional[str] = None,
                          is_resolved: Optional[int] = None, limit: int = 20, offset: int = 0) -> Optional[List[Dict]]:
        """
        获取反馈列表，支持条件筛选
        :return: 反馈列表或None
        """
        try:
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

            result = self.execute_query(sql, tuple(values))
            print(f"[{datetime.now()}] [INFO] UserFeedbackManager.get_feedback_list: 获取 {len(result)} 条反馈记录")
            return result

        except Exception as e:
            print(f"[{datetime.now()}] [ERROR] UserFeedbackManager.get_feedback_list: 查询失败 | 错误: {e}")
            return None

    def get_feedback_by_id(self, feedback_id: int) -> Optional[Dict]:
        """
        根据ID获取单个反馈详情
        :return: 反馈详情或None
        """
        try:
            sql = """
                SELECT 
                    f.*, ct.type_name as complaint_type_name
                FROM user_feedback f
                LEFT JOIN complaint_type ct ON f.complaint_type = ct.type_code
                WHERE f.id = %s
            """
            result = self.execute_one(sql, (feedback_id,))
            print(
                f"[{datetime.now()}] [INFO] UserFeedbackManager.get_feedback_by_id: 反馈 {feedback_id} 查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserFeedbackManager.get_feedback_by_id: 查询失败 | 反馈ID: {feedback_id} | 错误: {e}")
            return None

    def add_feedback(self, user_id: int, complaint_type: str, description: str,
                     image_url_1: Optional[str] = None, image_url_2: Optional[str] = None,
                     image_url_3: Optional[str] = None, priority: int = 1) -> Optional[int]:
        """
        添加用户反馈
        :return: 反馈ID或None
        """
        try:
            sql = """
                INSERT INTO user_feedback 
                (user_id, complaint_type, description, image_url_1, image_url_2, image_url_3, priority)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (user_id, complaint_type, description, image_url_1, image_url_2, image_url_3, priority)

            with self.get_cursor(cursor_class=None) as cursor:
                cursor.execute(sql, params)
                feedback_id = cursor.lastrowid
                self.connection.commit()
                print(
                    f"[{datetime.now()}] [INFO] UserFeedbackManager.add_feedback: 反馈添加成功 | ID: {feedback_id} | 用户: {user_id}")
                return feedback_id

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] UserFeedbackManager.add_feedback: 添加失败 | 用户: {user_id} | 错误: {e}")
            return None

    def update_feedback(self, feedback_id: int, description: Optional[str] = None,
                        priority: Optional[int] = None) -> bool:
        """
        更新反馈信息（仅限未解决前）
        :return: 是否成功
        """
        try:
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

            values.append(feedback_id)
            sql = f"UPDATE user_feedback SET {', '.join(fields)} WHERE id = %s AND is_resolved = 0"

            affected = self.execute_update(sql, tuple(values))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] UserFeedbackManager.update_feedback: 反馈 {feedback_id} 更新{'成功' if success else '失败或未找到/已解决'}")
            return success

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserFeedbackManager.update_feedback: 更新失败 | 反馈ID: {feedback_id} | 错误: {e}")
            return False

    def resolve_feedback(self, feedback_id: int, resolved_by: str, feedback_content: str) -> bool:
        """
        解决反馈（管理员操作）
        :return: 是否成功
        """
        try:
            sql = """
                UPDATE user_feedback 
                SET is_resolved = 1, 
                    resolved_by = %s, 
                    feedback_content = %s,
                    resolve_time = NOW()
                WHERE id = %s AND is_resolved = 0
            """
            affected = self.execute_update(sql, (resolved_by, feedback_content, feedback_id))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] UserFeedbackManager.resolve_feedback: 反馈 {feedback_id} 解决{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserFeedbackManager.resolve_feedback: 操作失败 | 反馈ID: {feedback_id} | 错误: {e}")
            return False

    def get_user_feedback_stats(self, user_id: int) -> Optional[Dict]:
        """
        获取用户的反馈统计
        :return: 统计字典或None
        """
        try:
            sql = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN is_resolved = 1 THEN 1 ELSE 0 END) as resolved,
                    SUM(CASE WHEN is_resolved = 0 THEN 1 ELSE 0 END) as unresolved
                FROM user_feedback 
                WHERE user_id = %s
            """
            result = self.execute_one(sql, (user_id,))
            print(f"[{datetime.now()}] [INFO] UserFeedbackManager.get_user_feedback_stats: 用户 {user_id} 统计完成")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserFeedbackManager.get_user_feedback_stats: 统计失败 | 用户: {user_id} | 错误: {e}")
            return None

    def delete_feedback(self, feedback_id: int) -> bool:
        """
        删除反馈（谨慎使用）
        :return: 是否成功
        """
        try:
            sql = "DELETE FROM user_feedback WHERE id = %s"
            affected = self.execute_update(sql, (feedback_id,))
            success = affected > 0
            print(
                f"[{datetime.now()}] [INFO] UserFeedbackManager.delete_feedback: 反馈 {feedback_id} 删除{'成功' if success else '失败'}")
            return success

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserFeedbackManager.delete_feedback: 删除失败 | 反馈ID: {feedback_id} | 错误: {e}")
            return False


class JobSchema(BaseModel):
    """职位数据模型"""
    id: int
    title: str
    salary_min: float
    salary_max: float
    salary_desc: str

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class UserFavoriteJobs(BaseManager):
    """用户收藏职位操作类"""

    def __init__(self):
        super().__init__()
        # 注意：这里移除了直接创建 Job_prot 实例，改为在方法中按需获取
        self._job_prot = None

    @property
    def job_prot(self):
        """延迟初始化 Job_prot"""
        if self._job_prot is None:
            self._job_prot = Job_prot()
        return self._job_prot

    def add_favorite(self, user_id: int, job_id: int, remarks: Optional[str] = None) -> Dict:
        """
        添加岗位收藏（支持软删除后的重新收藏）
        :return: 操作结果字典
        """
        try:
            # 先查询是否已有记录
            check_sql = """
                SELECT id, is_canceled FROM user_favorite_jobs 
                WHERE user_id = %s AND boss_job_id = %s
            """
            existing = self.execute_one(check_sql, (user_id, job_id))

            # 获取职位快照
            job_data = self.job_prot.fetch_one_job_all_data_posts(job_id)
            if not job_data:
                return {'success': False, 'message': '职位不存在'}

            job_snapshot = JobSchema.model_validate(job_data[0]).model_dump()
            job_snapshot_json = json.dumps(job_snapshot, ensure_ascii=False)

            if existing:
                if existing['is_canceled'] == 1:
                    # 重新激活
                    update_sql = """
                        UPDATE user_favorite_jobs 
                        SET is_canceled = 0, 
                            job_snapshot = %s,
                            remarks = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """
                    self.execute_update(update_sql, (job_snapshot_json, remarks, existing['id']))
                    print(
                        f"[{datetime.now()}] [INFO] UserFavoriteJobs.add_favorite: 用户 {user_id} 重新收藏职位 {job_id}")
                    return {'success': True, 'message': '重新收藏成功', 'id': existing['id']}
                else:
                    return {'success': False, 'message': '该岗位已在收藏列表中'}
            else:
                # 新增收藏
                insert_sql = """
                    INSERT INTO user_favorite_jobs 
                    (user_id, boss_job_id, job_snapshot, remarks) 
                    VALUES (%s, %s, %s, %s)
                """
                with self.get_cursor(cursor_class=None) as cursor:
                    cursor.execute(insert_sql, (user_id, job_id, job_snapshot_json, remarks))
                    new_id = cursor.lastrowid
                    self.connection.commit()
                    print(
                        f"[{datetime.now()}] [INFO] UserFavoriteJobs.add_favorite: 用户 {user_id} 收藏职位 {job_id} 成功")
                    return {'success': True, 'message': '收藏成功', 'id': new_id}

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] UserFavoriteJobs.add_favorite: 收藏失败 | 用户: {user_id} | 职位: {job_id} | 错误: {e}")
            return {'success': False, 'message': f'添加收藏失败: {str(e)}'}

    def cancel_favorite(self, user_id: int, boss_job_id: int) -> Dict:
        """
        取消收藏（软删除）
        :return: 操作结果字典
        """
        try:
            sql = """
                UPDATE user_favorite_jobs 
                SET is_canceled = 1, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
            """
            affected = self.execute_update(sql, (user_id, boss_job_id))

            if affected > 0:
                print(
                    f"[{datetime.now()}] [INFO] UserFavoriteJobs.cancel_favorite: 用户 {user_id} 取消收藏职位 {boss_job_id}")
                return {'success': True, 'message': '取消收藏成功'}
            else:
                return {'success': False, 'message': '未找到有效的收藏记录'}

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] UserFavoriteJobs.cancel_favorite: 操作失败 | 用户: {user_id} | 职位: {boss_job_id} | 错误: {e}")
            return {'success': False, 'message': f'取消收藏失败: {str(e)}'}

    def get_user_favorites(self, user_id: int, include_canceled: bool = False) -> Optional[List[Dict]]:
        """
        获取用户的收藏列表
        :return: 收藏列表或None
        """
        try:
            if include_canceled:
                sql = """
                    SELECT id, user_id, boss_job_id, is_canceled, 
                           job_snapshot, remarks, created_at, updated_at
                    FROM user_favorite_jobs 
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """
            else:
                sql = """
                    SELECT id, user_id, boss_job_id, 
                           job_snapshot, remarks, created_at, updated_at
                    FROM user_favorite_jobs 
                    WHERE user_id = %s AND is_canceled = 0
                    ORDER BY created_at DESC
                """

            result = self.execute_query(sql, (user_id,))
            print(
                f"[{datetime.now()}] [INFO] UserFavoriteJobs.get_user_favorites: 用户 {user_id} 获取 {len(result)} 条收藏")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserFavoriteJobs.get_user_favorites: 查询失败 | 用户: {user_id} | 错误: {e}")
            return None

    def check_is_favorite(self, user_id: int, boss_job_id: int) -> bool:
        """
        检查用户是否已收藏某岗位
        :return: 是否已收藏
        """
        try:
            sql = """
                SELECT id FROM user_favorite_jobs 
                WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
            """
            result = self.execute_one(sql, (user_id, boss_job_id))
            is_fav = result is not None
            print(
                f"[{datetime.now()}] [INFO] UserFavoriteJobs.check_is_favorite: 用户 {user_id} 职位 {boss_job_id} 收藏状态: {is_fav}")
            return is_fav

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserFavoriteJobs.check_is_favorite: 检查失败 | 用户: {user_id} | 职位: {boss_job_id} | 错误: {e}")
            return False

    def update_remarks(self, user_id: int, boss_job_id: int, remarks: str) -> Dict:
        """
        更新收藏备注
        :return: 操作结果字典
        """
        try:
            sql = """
                UPDATE user_favorite_jobs 
                SET remarks = %s, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
            """
            affected = self.execute_update(sql, (remarks, user_id, boss_job_id))

            if affected > 0:
                print(
                    f"[{datetime.now()}] [INFO] UserFavoriteJobs.update_remarks: 用户 {user_id} 职位 {boss_job_id} 备注更新成功")
                return {'success': True, 'message': '备注更新成功'}
            else:
                return {'success': False, 'message': '未找到有效的收藏记录'}

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] UserFavoriteJobs.update_remarks: 更新失败 | 用户: {user_id} | 职位: {boss_job_id} | 错误: {e}")
            return {'success': False, 'message': f'更新备注失败: {str(e)}'}

    def get_favorite_detail(self, user_id: int, boss_job_id: int) -> Optional[Dict]:
        """
        获取单条收藏详情
        :return: 收藏详情或None
        """
        try:
            sql = """
                SELECT id, user_id, boss_job_id, is_canceled,
                       job_snapshot, remarks, created_at, updated_at
                FROM user_favorite_jobs 
                WHERE user_id = %s AND boss_job_id = %s
            """
            result = self.execute_one(sql, (user_id, boss_job_id))
            print(
                f"[{datetime.now()}] [INFO] UserFavoriteJobs.get_favorite_detail: 用户 {user_id} 职位 {boss_job_id} 详情查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserFavoriteJobs.get_favorite_detail: 查询失败 | 用户: {user_id} | 职位: {boss_job_id} | 错误: {e}")
            return None

    def batch_cancel_favorites(self, user_id: int, boss_job_id_list: List[int]) -> Dict:
        """
        批量取消收藏
        :return: 操作结果字典
        """
        try:
            if not boss_job_id_list:
                return {'success': True, 'message': '无操作项', 'affected_rows': 0}

            placeholders = ','.join(['%s'] * len(boss_job_id_list))
            sql = f"""
                UPDATE user_favorite_jobs 
                SET is_canceled = 1, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND boss_job_id IN ({placeholders}) AND is_canceled = 0
            """
            params = (user_id,) + tuple(boss_job_id_list)
            affected = self.execute_update(sql, params)

            print(
                f"[{datetime.now()}] [INFO] UserFavoriteJobs.batch_cancel_favorites: 用户 {user_id} 批量取消 {affected} 条收藏")
            return {
                'success': True,
                'message': f'成功取消 {affected} 条收藏',
                'affected_rows': affected
            }

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] UserFavoriteJobs.batch_cancel_favorites: 批量操作失败 | 用户: {user_id} | 错误: {e}")
            return {'success': False, 'message': f'批量取消收藏失败: {str(e)}'}


class UserDeliverJobs(BaseManager):
    """用户投递职位操作类"""

    def __init__(self):
        super().__init__()
        self._job_prot = None

    @property
    def job_prot(self):
        """延迟初始化 Job_prot"""
        if self._job_prot is None:
            self._job_prot = Job_prot()
        return self._job_prot

    def add_deliver(self, user_id: int, job_id: int, remarks: Optional[str] = None) -> Dict:
        """
        添加岗位投递（支持软删除后的重新投递）
        :return: 操作结果字典
        """
        try:
            # 先查询是否已有记录
            check_sql = """
                SELECT id, is_canceled FROM user_deliver_jobs 
                WHERE user_id = %s AND boss_job_id = %s
            """
            existing = self.execute_one(check_sql, (user_id, job_id))

            # 获取职位快照
            job_data = self.job_prot.fetch_one_job_all_data_posts(job_id)
            if not job_data:
                return {'success': False, 'message': '职位不存在'}

            job_snapshot = JobSchema.model_validate(job_data[0]).model_dump()
            job_snapshot_json = json.dumps(job_snapshot, ensure_ascii=False)

            if existing:
                if existing['is_canceled'] == 1:
                    # 重新激活
                    update_sql = """
                        UPDATE user_deliver_jobs 
                        SET is_canceled = 0, 
                            job_snapshot = %s,
                            remarks = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """
                    self.execute_update(update_sql, (job_snapshot_json, remarks, existing['id']))
                    print(
                        f"[{datetime.now()}] [INFO] UserDeliverJobs.add_deliver: 用户 {user_id} 重新投递职位 {job_id}")
                    return {'success': True, 'message': '重新投递成功', 'id': existing['id']}
                else:
                    return {'success': False, 'message': '该岗位已在投递列表中'}
            else:
                # 新增投递
                insert_sql = """
                    INSERT INTO user_deliver_jobs 
                    (user_id, boss_job_id, job_snapshot, remarks) 
                    VALUES (%s, %s, %s, %s)
                """
                with self.get_cursor(cursor_class=None) as cursor:
                    cursor.execute(insert_sql, (user_id, job_id, job_snapshot_json, remarks))
                    new_id = cursor.lastrowid
                    self.connection.commit()
                    print(
                        f"[{datetime.now()}] [INFO] UserDeliverJobs.add_deliver: 用户 {user_id} 投递职位 {job_id} 成功")
                    return {'success': True, 'message': '投递成功', 'id': new_id}

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] UserDeliverJobs.add_deliver: 投递失败 | 用户: {user_id} | 职位: {job_id} | 错误: {e}")
            return {'success': False, 'message': f'添加投递失败: {str(e)}'}

    def cancel_deliver(self, user_id: int, boss_job_id: int) -> Dict:
        """
        取消投递（软删除）
        :return: 操作结果字典
        """
        try:
            sql = """
                UPDATE user_deliver_jobs 
                SET is_canceled = 1, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
            """
            affected = self.execute_update(sql, (user_id, boss_job_id))

            if affected > 0:
                print(
                    f"[{datetime.now()}] [INFO] UserDeliverJobs.cancel_deliver: 用户 {user_id} 取消投递职位 {boss_job_id}")
                return {'success': True, 'message': '取消投递成功'}
            else:
                return {'success': False, 'message': '未找到有效的投递记录'}

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] UserDeliverJobs.cancel_deliver: 操作失败 | 用户: {user_id} | 职位: {boss_job_id} | 错误: {e}")
            return {'success': False, 'message': f'取消投递失败: {str(e)}'}

    def get_user_delivers(self, user_id: int, include_canceled: bool = False) -> Optional[List[Dict]]:
        """
        获取用户的投递列表
        :return: 投递列表或None
        """
        try:
            if include_canceled:
                sql = """
                    SELECT id, user_id, boss_job_id, is_canceled, 
                           job_snapshot, remarks, created_at, updated_at
                    FROM user_deliver_jobs 
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """
            else:
                sql = """
                    SELECT id, user_id, boss_job_id, 
                           job_snapshot, remarks, created_at, updated_at
                    FROM user_deliver_jobs 
                    WHERE user_id = %s AND is_canceled = 0
                    ORDER BY created_at DESC
                """

            result = self.execute_query(sql, (user_id,))
            print(
                f"[{datetime.now()}] [INFO] UserDeliverJobs.get_user_delivers: 用户 {user_id} 获取 {len(result)} 条投递记录")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserDeliverJobs.get_user_delivers: 查询失败 | 用户: {user_id} | 错误: {e}")
            return None

    def check_is_deliver(self, user_id: int, boss_job_id: int) -> bool:
        """
        检查用户是否已投递某岗位
        :return: 是否已投递
        """
        try:
            sql = """
                SELECT id FROM user_deliver_jobs 
                WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
            """
            result = self.execute_one(sql, (user_id, boss_job_id))
            is_delivered = result is not None
            print(
                f"[{datetime.now()}] [INFO] UserDeliverJobs.check_is_deliver: 用户 {user_id} 职位 {boss_job_id} 投递状态: {is_delivered}")
            return is_delivered

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserDeliverJobs.check_is_deliver: 检查失败 | 用户: {user_id} | 职位: {boss_job_id} | 错误: {e}")
            return False

    def update_remarks(self, user_id: int, boss_job_id: int, remarks: str) -> Dict:
        """
        更新投递备注
        :return: 操作结果字典
        """
        try:
            sql = """
                UPDATE user_deliver_jobs 
                SET remarks = %s, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND boss_job_id = %s AND is_canceled = 0
            """
            affected = self.execute_update(sql, (remarks, user_id, boss_job_id))

            if affected > 0:
                print(
                    f"[{datetime.now()}] [INFO] UserDeliverJobs.update_remarks: 用户 {user_id} 职位 {boss_job_id} 备注更新成功")
                return {'success': True, 'message': '备注更新成功'}
            else:
                return {'success': False, 'message': '未找到有效的投递记录'}

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] UserDeliverJobs.update_remarks: 更新失败 | 用户: {user_id} | 职位: {boss_job_id} | 错误: {e}")
            return {'success': False, 'message': f'更新备注失败: {str(e)}'}

    def get_deliver_detail(self, user_id: int, boss_job_id: int) -> Optional[Dict]:
        """
        获取单条投递详情
        :return: 投递详情或None
        """
        try:
            sql = """
                SELECT id, user_id, boss_job_id, is_canceled,
                       job_snapshot, remarks, created_at, updated_at
                FROM user_deliver_jobs 
                WHERE user_id = %s AND boss_job_id = %s
            """
            result = self.execute_one(sql, (user_id, boss_job_id))
            print(
                f"[{datetime.now()}] [INFO] UserDeliverJobs.get_deliver_detail: 用户 {user_id} 职位 {boss_job_id} 详情查询{'成功' if result else '未找到'}")
            return result

        except Exception as e:
            print(
                f"[{datetime.now()}] [ERROR] UserDeliverJobs.get_deliver_detail: 查询失败 | 用户: {user_id} | 职位: {boss_job_id} | 错误: {e}")
            return None

    def batch_cancel_delivers(self, user_id: int, boss_job_id_list: List[int]) -> Dict:
        """
        批量取消投递
        :return: 操作结果字典
        """
        try:
            if not boss_job_id_list:
                return {'success': True, 'message': '无操作项', 'affected_rows': 0}

            placeholders = ','.join(['%s'] * len(boss_job_id_list))
            sql = f"""
                UPDATE user_deliver_jobs 
                SET is_canceled = 1, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND boss_job_id IN ({placeholders}) AND is_canceled = 0
            """
            params = (user_id,) + tuple(boss_job_id_list)
            affected = self.execute_update(sql, params)

            print(
                f"[{datetime.now()}] [INFO] UserDeliverJobs.batch_cancel_delivers: 用户 {user_id} 批量取消 {affected} 条投递")
            return {
                'success': True,
                'message': f'成功取消 {affected} 条投递',
                'affected_rows': affected
            }

        except Exception as e:
            self.connection.rollback()
            print(
                f"[{datetime.now()}] [ERROR] UserDeliverJobs.batch_cancel_delivers: 批量操作失败 | 用户: {user_id} | 错误: {e}")
            return {'success': False, 'message': f'批量取消投递失败: {str(e)}'}