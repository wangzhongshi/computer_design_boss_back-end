from sql_data_demo import EndDemoDatabase, Sys_user


db = EndDemoDatabase(host='localhost', user='root', password='123456')
# a = Job_prot(db.connection)
# a.fetch_some_job_posts_all()
# a.fetch_one_job_all_data_posts('1')
# a.fetch_some_job_posts_some('1001')
# a.fetch_job_list_by_two_given(emp_type='1', category_id='1001')
# a.search_job_by_user_input('后端开发')
# b = Job_category_simple(db.connection)
# b.job_intro_list()
# c = Forum_comments(db.connection)
# c.forum_all()
# c.forum_one_category('1')
# c.forum_all_first_talk()
# c.forum_talks_back('63')
# c.forum_add('2','1', '69', '你说的特别的对', '2','2')
# c.forum_delete(73)
# c.forum_all_by_user('1')
# c.forum_count_all('all','1','1','2')s
# d = Sys_user(db.connection)
# d.user_count_all('all')
# d.get_user_by_field('user_id', '1143526543212345678')
# d.update_user_status('1143526543212345678', '0')
# d.update_last_login('1143526543212345678', '192.168.1.120', 'xiaomi 17', '2')
# user_data = {
#
# }
# d.create_user()
class Test_Sys_user(Sys_user):
    # 这里是你原有的数据库连接和方法

    def debug_user_count_all(self):
        '''测试用户统计功能'''
        print("=== 调试用户统计功能 ===")

        # 测试用例1：统计所有用户
        count = self.user_count_all('all')
        print(f"1. 全部用户数量: {count}")

        # 测试用例2：统计活跃用户
        count = self.user_count_all('active')
        print(f"2. 活跃用户数量: {count}")

        # 测试用例3：按状态统计
        count = self.user_count_all('status', status=1)
        print(f"3. 状态为1（正常）的用户数量: {count}")

        # 测试用例4：按求职状态统计
        count = self.user_count_all('job_status', job_status=0)
        print(f"4. 求职状态为0（待业）的用户数量: {count}")

        # 测试用例5：错误参数
        count = self.user_count_all('wrong')
        print(f"5. 错误参数返回: {count}")

        print("=== 调试完成 ===\n")
        return True

    def debug_get_user_by_field(self):
        '''测试根据字段获取用户'''
        print("=== 调试按字段查询用户 ===")

        # 测试用例1：通过user_id查询
        user = self.get_user_by_field('user_id', '1143526543212345678')
        print(f"1. 通过user_id查询结果: {'找到用户' if user else '未找到'}")
        if user:
            print(f"   用户信息: ID={user.get('user_id')}, 手机={user.get('mobile')}")

        # 测试用例2：通过手机号查询
        user = self.get_user_by_field('mobile', '13800138000')
        print(f"2. 通过手机号查询结果: {'找到用户' if user else '未找到'}")

        # 测试用例3：通过邮箱查询
        user = self.get_user_by_field('email', 'test@example.com')
        print(f"3. 通过邮箱查询结果: {'找到用户' if user else '未找到'}")

        # 测试用例4：查询不存在的用户
        user = self.get_user_by_field('mobile', '99999999999')
        print(f"4. 查询不存在的手机号: {'找到用户' if user else '未找到'}")

        # 测试用例5：查询已删除的用户
        user = self.get_user_by_field('mobile', '13800138000', include_deleted=True)
        print(f"5. 查询已删除用户: {'找到用户' if user else '未找到'}")

        print("=== 调试完成 ===\n")
        return True

    def debug_update_user_status(self):
        '''测试更新用户状态'''
        print("=== 调试更新用户状态 ===")

        # 测试用例1：正常更新
        success = self.update_user_status('1143526543212345678', 0)
        print(f"1. 更新用户状态为禁用: {'成功' if success else '失败'}")

        # 测试用例2：更新为正常状态
        success = self.update_user_status('1143526543212345678', 1)
        print(f"2. 更新用户状态为正常: {'成功' if success else '失败'}")

        # 测试用例3：更新不存在的用户
        success = self.update_user_status('9999999999999999999', 1)
        print(f"3. 更新不存在的用户: {'成功' if success else '失败'}")

        # 测试用例4：更新已删除的用户
        # 先创建一个用户然后删除，再尝试更新
        print(f"4. 更新已删除用户: 需要先创建测试数据")

        print("=== 调试完成 ===\n")
        return True

    def debug_update_last_login(self):
        '''测试更新最后登录信息'''
        print("=== 调试更新最后登录信息 ===")

        test_cases = [
            {
                'user_id': '1143526543212345678',
                'login_ip': '192.168.1.100',
                'device_model': 'iPhone 13 Pro',
                'device_type': 3
            },
            {
                'user_id': '1143526543212345679',
                'login_ip': '10.0.0.1',
                'device_model': 'Xiaomi 12',
                'device_type': 2
            }
        ]

        for i, test_data in enumerate(test_cases, 1):
            success = self.update_last_login(
                test_data['user_id'],
                test_data['login_ip'],
                test_data['device_model'],
                test_data['device_type']
            )
            print(f"{i}. 更新用户 {test_data['user_id']} 登录信息: {'成功' if success else '失败'}")

        print("=== 调试完成 ===\n")
        return True

    def debug_create_user(self):
        '''测试创建用户'''
        print("=== 调试创建用户 ===")

        # 测试用例1：正常创建用户
        user_data = {
            'user_id': '1143526543212345680',
            'mobile': '13800138001',
            'email': 'newuser@example.com',
            'password_hash': 'hashed_password_123',
            'real_name': '测试用户',
            'gender': 1,
            'status': 1
        }

        user_id = self.create_user(user_data)
        print(f"1. 创建新用户: {'成功，ID=' + str(user_id) if user_id else '失败'}")

        # 测试用例2：创建用户（必填字段缺失）
        incomplete_data = {
            'user_id': '1143526543212345681',
            'mobile': '13800138002'
            # 缺少password_hash
        }

        user_id = self.create_user(incomplete_data)
        print(f"2. 创建缺少必填字段的用户: {'成功' if user_id else '失败（预期失败）'}")

        # 测试用例3：创建重复手机号的用户
        duplicate_data = {
            'user_id': '1143526543212345682',
            'mobile': '13800138001',  # 重复的手机号
            'password_hash': 'hashed_password_456'
        }

        try:
            user_id = self.create_user(duplicate_data)
            print(f"3. 创建重复手机号的用户: {'成功' if user_id else '失败'}")
        except Exception as e:
            print(f"3. 创建重复手机号的用户: 失败（预期失败），错误: {str(e)}")

        print("=== 调试完成 ===\n")
        return True

    def debug_search_users(self):
        '''测试搜索用户'''
        print("=== 调试搜索用户 ===")

        # 测试用例1：搜索所有用户
        result = self.search_users(page=1, page_size=10)
        print(f"1. 搜索所有用户（第1页）:")
        print(f"   总数: {result['total']}, 当前页数量: {len(result['users'])}, 总页数: {result['total_pages']}")

        # 测试用例2：按关键词搜索
        result = self.search_users(keyword='李思', page=1, page_size=5)
        print(f"2. 按关键词'1380013'搜索:")
        print(f"   找到 {result['total']} 个用户")

        # 测试用例3：按状态搜索
        result = self.search_users(status=1, page=1, page_size=3)
        print(f"3. 搜索状态为1的用户:")
        print(f"   找到 {result['total']} 个用户")

        # 测试用例4：分页测试
        result = self.search_users(page=2, page_size=3)
        print(f"4. 第2页，每页3条:")
        print(f"   当前页用户数: {len(result['users'])}")

        print("=== 调试完成 ===\n")
        return True

    def debug_soft_delete_user(self):
        '''测试软删除用户'''
        print("=== 调试软删除用户 ===")

        # 首先创建一个测试用户
        test_user_data = {
            'user_id': '1143526543212345689',
            'mobile': '13800138999',
            'password_hash': 'test_hash_delete'
        }

        # 创建用户
        created_id = self.create_user(test_user_data)
        if created_id:
            print(f"1. 创建测试用户成功: {test_user_data['mobile']}")

            # 测试删除
            success = self.soft_delete_user(test_user_data['user_id'])
            print(f"2. 软删除用户: {'成功' if success else '失败'}")

            # 验证删除后无法查询到（is_deleted=0）
            user = self.get_user_by_field('mobile', test_user_data['mobile'])
            print(f"3. 删除后查询用户（is_deleted=0）: {'找到用户' if user else '未找到（预期）'}")

            # 验证删除后可以查询到（include_deleted=True）
            user = self.get_user_by_field('mobile', test_user_data['mobile'], include_deleted=True)
            print(f"4. 删除后查询用户（包含已删除）: {'找到用户' if user else '未找到'}")
        else:
            print(f"1. 创建测试用户失败，跳过删除测试")

        print("=== 调试完成 ===\n")
        return True

    def debug_update_user_profile(self):
        '''测试更新用户信息'''
        print("=== 调试更新用户信息 ===")

        # 测试用例1：更新多个字段
        profile_data = {
            'real_name': '张测试',
            'gender': 1,
            'birth_date': '1995-05-20',
            'education_level': '本科',
            'major': '计算机科学',
            'bio': '这是一个测试用户的个人简介'
        }

        success = self.update_user_profile('1143526543212345678', profile_data)
        print(f"1. 更新多个个人信息字段: {'成功' if success else '失败'}")

        # 测试用例2：更新单个字段
        profile_data = {
            'avatar_url': 'https://example.com/avatar/new.jpg'
        }

        success = self.update_user_profile('1143526543212345678', profile_data)
        print(f"2. 更新头像URL: {'成功' if success else '失败'}")

        # 测试用例3：更新不存在的用户
        profile_data = {
            'real_name': '不存在用户'
        }

        success = self.update_user_profile('9999999999999999999', profile_data)
        print(f"3. 更新不存在的用户: {'成功' if success else '失败（预期）'}")

        # 测试用例4：更新空数据
        success = self.update_user_profile('1143526543212345678', {})
        print(f"4. 更新空数据: {'成功' if success else '失败（预期）'}")

        print("=== 调试完成 ===\n")
        return True

    def debug_check_user_exists(self):
        '''测试检查用户是否存在'''
        print("=== 调试检查用户是否存在 ===")

        # 测试用例1：检查已存在的手机号
        exists = self.check_user_exists(mobile='13800138000')
        print(f"1. 检查手机号13800138000是否存在: {'存在' if exists else '不存在'}")

        # 测试用例2：检查不存在的手机号
        exists = self.check_user_exists(mobile='99999999999')
        print(f"2. 检查手机号99999999999是否存在: {'存在' if exists else '不存在（预期）'}")

        # 测试用例3：检查邮箱
        exists = self.check_user_exists(email='test@example.com')
        print(f"3. 检查邮箱test@example.com是否存在: {'存在' if exists else '不存在'}")

        # 测试用例4：同时检查手机号和邮箱
        exists = self.check_user_exists(mobile='13800138000', email='test@example.com')
        print(f"4. 同时检查手机号和邮箱: {'存在' if exists else '不存在'}")

        # 测试用例5：检查时排除特定用户
        exists = self.check_user_exists(
            mobile='13800138000',
            exclude_user_id='1143526543212345679'
        )
        print(f"5. 检查手机号但排除用户1143526543212345679: {'存在' if exists else '不存在'}")

        print("=== 调试完成 ===\n")
        return True

    def debug_all_functions(self):
        '''调试所有功能（集成测试）'''
        print("========== 开始全面调试所有用户功能 ==========")

        # 记录开始时间
        import time
        start_time = time.time()

        # 依次运行所有调试函数
        tests = [
            self.debug_user_count_all,
            self.debug_get_user_by_field,
            self.debug_update_user_status,
            self.debug_update_last_login,
            self.debug_create_user,
            self.debug_search_users,
            self.debug_soft_delete_user,
            self.debug_update_user_profile,
            self.debug_check_user_exists
        ]

        results = []
        for i, test_func in enumerate(tests, 1):
            print(f"\n[{i}/{len(tests)}] 运行 {test_func.__name__}...")
            try:
                result = test_func()
                results.append((test_func.__name__, result, None))
                print(f"✓ {test_func.__name__} 完成")
            except Exception as e:
                results.append((test_func.__name__, False, str(e)))
                print(f"✗ {test_func.__name__} 失败: {str(e)}")

        # 输出总结报告
        print(f"\n{'=' * 50}")
        print("调试总结报告:")
        print(f"{'=' * 50}")

        success_count = sum(1 for _, success, _ in results if success)
        total_time = time.time() - start_time

        print(f"总测试数: {len(results)}")
        print(f"成功数: {success_count}")
        print(f"失败数: {len(results) - success_count}")
        print(f"总耗时: {total_time:.2f}秒")

        # 显示失败的测试
        failures = [(name, error) for name, success, error in results if not success]
        if failures:
            print("\n失败的测试:")
            for name, error in failures:
                print(f"  - {name}: {error}")

        print(f"{'=' * 50}")
        print("全面调试完成!")

        return success_count == len(results)

    def setup_test_data(self):
        '''设置测试数据（用于调试前准备）'''
        print("=== 设置测试数据 ===")

        # 创建一些测试用户
        test_users = [
            {
                'user_id': '1143526543212345678',
                'mobile': '13800138000',
                'email': 'user1@example.com',
                'password_hash': 'hash1',
                'real_name': '张三',
                'status': 1,
                'job_status': 0
            },
            {
                'user_id': '1143526543212345679',
                'mobile': '13800138111',
                'email': 'user2@example.com',
                'password_hash': 'hash2',
                'real_name': '李四',
                'status': 1,
                'job_status': 1
            },
            {
                'user_id': '1143526543212345677',
                'mobile': '13800138222',
                'email': 'user3@example.com',
                'password_hash': 'hash3',
                'real_name': '王五',
                'status': 0,  # 禁用状态
                'job_status': 2
            }
        ]

        created_count = 0
        for user_data in test_users:
            try:
                # 先检查是否已存在
                existing = self.get_user_by_field('user_id', user_data['user_id'])
                if not existing:
                    user_id = self.create_user(user_data)
                    if user_id:
                        created_count += 1
                        print(f"创建测试用户: {user_data['mobile']}")
                else:
                    print(f"测试用户已存在: {user_data['mobile']}")
            except Exception as e:
                print(f"创建测试用户失败 {user_data['mobile']}: {str(e)}")

        print(f"测试数据设置完成，创建了 {created_count} 个新用户")
        return True

# # 创建Sys_user实例（假设已经初始化了数据库连接）
# sys_user = Test_Sys_user(db.connection)
#
# # 方法1：运行单个调试函数
# sys_user.debug_user_count_all()
#
# # 方法2：运行所有调试
# sys_user.debug_all_functions()
#
# # 方法3：先设置测试数据，再调试
# sys_user.setup_test_data()
# sys_user.debug_all_functions()

import pymysql
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from sql_data_demo import ResumeManager

class ResumeDebugger:
    def __init__(self, host='localhost', user='root', password='', database='your_database'):
        """初始化数据库连接"""
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        # 初始化所有管理器
        self.resume_manager = ResumeManager(self.connection)
        self.resumes = self.resume_manager.resumes
        self.certificates = self.resume_manager.certificates
        self.campus_experiences = self.resume_manager.campus_experiences
        self.internships = self.resume_manager.internships
        self.job_intentions = self.resume_manager.job_intentions
        self.job_preferences = self.resume_manager.job_preferences

        # 测试用户ID
        self.test_user_id = '1143526543212345678'

    def print_separator(self, title):
        """打印分隔符"""
        print("\n" + "=" * 60)
        print(f" {title} ")
        print("=" * 60)

    def test_resume_operations(self):
        """测试简历基本操作"""
        self.print_separator("测试简历基本操作")

        # 测试数据
        resume_data = {
            'real_name': '张三',
            'gender': '1',
            'birth_date': '2000-01-01',
            'phone': '13800138000',
            'email': 'zhangsan@example.com',
            'wechat': 'zhangsan123',
            'city': '北京',
            'education_level': '本科',
            'school_name': '清华大学',
            'major': '计算机科学与技术',
            'graduation_year': 2023,
            'gpa': 3.8,
            'resume_file_url': '/uploads/resumes/zhangsan.pdf',
            'resume_file_name': '张三_简历.pdf',
            'resume_format': 'pdf',
            'self_introduction': '热爱编程，熟悉Python和Java开发'
        }

        # 1. 创建简历
        print("1. 创建简历:")
        resume_id = self.resumes.create_resume(self.test_user_id, resume_data)
        print('stop_point_one')
        if resume_id:
            print(f"   成功创建简历，ID: {resume_id}")
        else:
            print("   简历已存在或创建失败")

        # 2. 获取简历
        print("\n2. 获取简历:")
        resume = self.resumes.get_resume_by_user(self.test_user_id)
        if resume:
            print(f"   姓名: {resume.get('real_name')}")
            print(f"   学校: {resume.get('school_name')}")
            print(f"   专业: {resume.get('major')}")
            print(f"   GPA: {resume.get('gpa')}")
        else:
            print("   获取简历失败")

        # 3. 更新简历
        print("\n3. 更新简历:")
        update_data = {
            'gpa': 3.9,
            'self_introduction': '热爱编程，熟悉Python和Java开发，有丰富的项目经验'
        }
        if self.resumes.update_resume(self.test_user_id, update_data):
            print("   简历更新成功")
            # 验证更新
            updated_resume = self.resumes.get_resume_by_user(self.test_user_id)
            print(f"   更新后GPA: {updated_resume.get('gpa')}")
        else:
            print("   简历更新失败")

        # 4. 统计简历数量
        print("\n4. 统计简历数量:")
        stats = self.resumes.get_resume_count_by_user()
        print(f"   总数: {stats.get('total_count', 0)}")
        print(f"   本科: {stats.get('bachelor_count', 0)}")
        print(f"   硕士: {stats.get('master_count', 0)}")

        # 5. 测试重复创建
        print("\n5. 测试重复创建:")
        result = self.resumes.create_resume(self.test_user_id, resume_data)
        if result is None:
            print("   正确：用户已有简历，返回None")

    def test_certificate_operations(self):
        """测试证书操作"""
        self.print_separator("测试证书操作")

        # 测试数据
        cert_data_list = [
            {
                'cert_type': 'english',
                'cert_name': '英语六级',
                'cert_level': 'CET-6',
                'issue_date': '2021-06-01',
                'issuing_authority': '教育部考试中心',
                'certificate_no': 'CET621000001'
            },
            {
                'cert_type': 'computer',
                'cert_name': '计算机二级',
                'cert_level': '二级',
                'issue_date': '2020-12-01',
                'issuing_authority': '教育部考试中心',
                'certificate_no': 'MS202000001'
            },
            {
                'cert_type': 'professional',
                'cert_name': '注册会计师',
                'cert_level': '专业阶段',
                'issue_date': '2022-03-01',
                'expiry_date': '2025-03-01',
                'issuing_authority': '中国注册会计师协会',
                'certificate_no': 'CPA202200001'
            }
        ]

        # 1. 添加证书
        print("1. 添加证书:")
        cert_ids = []
        for cert_data in cert_data_list:
            cert_id = self.certificates.add_certificate(self.test_user_id, cert_data)
            if cert_id:
                cert_ids.append(cert_id)
                print(f"   添加证书: {cert_data['cert_name']}, ID: {cert_id}")

        # 2. 获取证书列表
        print("\n2. 获取证书列表:")
        all_certs = self.certificates.get_user_certificates(self.test_user_id)
        print(f"   证书总数: {len(all_certs)}")
        for cert in all_certs:
            print(f"   - {cert['cert_name']} ({cert['cert_type']})")

        # 3. 按类型获取证书
        print("\n3. 按类型获取英语证书:")
        english_certs = self.certificates.get_user_certificates(self.test_user_id, 'english')
        print(f"   英语证书数量: {len(english_certs)}")

        # 4. 获取证书详情
        print("\n4. 获取证书详情:")
        if cert_ids:
            cert_detail = self.certificates.get_certificate_by_id(cert_ids[0], self.test_user_id)
            if cert_detail:
                print(f"   证书名称: {cert_detail['cert_name']}")
                print(f"   证书编号: {cert_detail['certificate_no']}")

        # 5. 更新证书
        print("\n5. 更新证书:")
        if cert_ids:
            update_data = {'cert_level': 'CET-6（优秀）'}
            if self.certificates.update_certificate(cert_ids[0], self.test_user_id, update_data):
                print("   证书更新成功")

        # 6. 获取证书统计
        print("\n6. 证书统计:")
        cert_stats = self.certificates.get_certificate_stats(self.test_user_id)
        print(f"   总数: {cert_stats.get('total_count', 0)}")
        print(f"   英语证书: {cert_stats.get('english_count', 0)}")
        print(f"   计算机证书: {cert_stats.get('computer_count', 0)}")
        print(f"   专业证书: {cert_stats.get('professional_count', 0)}")

        # 7. 删除证书（可选，根据需要启用）
        # print("\n7. 删除证书:")
        # if cert_ids:
        #     if self.certificates.delete_certificate(cert_ids[-1], self.test_user_id):
        #         print(f"   删除证书ID: {cert_ids[-1]}")

    def test_campus_experience_operations(self):
        """测试校园经历操作"""
        self.print_separator("测试校园经历操作")

        # 测试数据
        campus_data = {
            'has_student_union': 1,
            'student_union_details': '曾任学生会主席，组织多次校园活动',
            'has_club': 1,
            'club_details': '计算机协会会长，组织编程比赛',
            'has_scholarship': 1,
            'scholarship_details': '国家奖学金一次，校级奖学金三次',
            'has_honor': 1,
            'honor_details': '优秀学生干部，三好学生'
        }

        # 1. 创建/更新校园经历
        print("1. 创建/更新校园经历:")
        experience_id = self.campus_experiences.upsert_campus_experience(self.test_user_id, campus_data)
        if experience_id:
            print(f"   校园经历ID: {experience_id}")

        # 2. 获取校园经历
        print("\n2. 获取校园经历:")
        experience = self.campus_experiences.get_campus_experience(self.test_user_id)
        if experience:
            print(f"   是否有学生会经历: {'是' if experience['has_student_union'] else '否'}")
            print(f"   奖学金详情: {experience['scholarship_details']}")

        # 3. 更新校园经历
        print("\n3. 更新校园经历:")
        update_data = {
            'has_scholarship': 1,
            'scholarship_details': '国家奖学金一次，校级奖学金五次'
        }
        if self.campus_experiences.upsert_campus_experience(self.test_user_id, update_data):
            print("   校园经历更新成功")
            # 验证更新
            updated_exp = self.campus_experiences.get_campus_experience(self.test_user_id)
            print(f"   更新后奖学金详情: {updated_exp['scholarship_details']}")

    def test_internship_operations(self):
        """测试实习经历操作"""
        self.print_separator("测试实习经历操作")

        # 测试数据
        internship_data_list = [
            {
                'company_name': '阿里巴巴',
                'position': '后端开发实习生',
                'industry': '互联网',
                'start_date': '2022-06-01',
                'end_date': '2022-09-01',
                'is_current': 0,
                'is_related': 1,
                'work_content': '参与微服务架构开发，负责订单模块',
                'achievements': '完成订单系统的重构，提升性能30%'
            },
            {
                'company_name': '腾讯',
                'position': '前端开发实习生',
                'industry': '互联网',
                'start_date': '2021-07-01',
                'end_date': '2021-10-01',
                'is_current': 0,
                'is_related': 1,
                'work_content': '参与微信小程序开发，负责用户界面',
                'achievements': '优化页面加载速度，用户体验评分提升20%'
            },
            {
                'company_name': '字节跳动',
                'position': '数据分析实习生',
                'industry': '互联网',
                'start_date': '2023-01-01',
                'end_date': '2023-06-01',
                'is_current': 1,
                'is_related': 1,
                'work_content': '分析用户行为数据，提供产品优化建议',
                'achievements': '建立用户流失预测模型，准确率达85%'
            }
        ]

        # 1. 添加实习经历
        print("1. 添加实习经历:")
        internship_ids = []
        for data in internship_data_list:
            internship_id = self.internships.add_internship(self.test_user_id, data)
            if internship_id:
                internship_ids.append(internship_id)
                print(f"   添加实习: {data['company_name']} - {data['position']}")

        # 2. 获取实习列表
        print("\n2. 获取实习列表:")
        all_internships = self.internships.get_user_internships(self.test_user_id)
        print(f"   实习总数: {len(all_internships)}")
        for i, intern in enumerate(all_internships, 1):
            print(
                f"   {i}. {intern['company_name']} - {intern['position']} ({intern['start_date']} 至 {intern['end_date']})")

        # 3. 获取实习详情
        print("\n3. 获取实习详情:")
        if internship_ids:
            detail = self.internships.get_internship_by_id(internship_ids[0], self.test_user_id)
            if detail:
                print(f"   公司: {detail['company_name']}")
                print(f"   职位: {detail['position']}")
                print(f"   工作内容: {detail['work_content'][:50]}...")

        # 4. 更新实习经历
        print("\n4. 更新实习经历:")
        if internship_ids:
            update_data = {
                'position': '高级后端开发实习生',
                'work_content': '参与微服务架构开发，负责订单和支付模块'
            }
            if self.internships.update_internship(internship_ids[0], self.test_user_id, update_data):
                print("   实习经历更新成功")

        # 5. 获取实习统计
        print("\n5. 获取实习统计:")
        stats = self.internships.get_internship_stats(self.test_user_id)
        if stats:
            print(f"   总实习次数: {stats.get('total_count', 0)}")
            print(f"   相关实习次数: {stats.get('related_count', 0)}")

        # 6. 获取行业分布
        print("\n6. 获取行业分布:")
        industry_dist = self.internships.get_industry_distribution()
        for item in industry_dist:
            print(f"   {item['industry']}: {item['count']}")

        # 7. 删除实习经历（可选，根据需要启用）
        # print("\n7. 删除实习经历:")
        # if internship_ids:
        #     if self.internships.delete_internship(internship_ids[-1], self.test_user_id):
        #         print(f"   删除实习ID: {internship_ids[-1]}")

    def test_job_intention_operations(self):
        """测试求职意向操作"""
        self.print_separator("测试求职意向操作")

        # 测试数据
        intention_data = {
            'target_industries': ['互联网', '金融科技', '人工智能'],
            'industry_priority': '互联网',
            'target_positions': ['后端开发', '数据分析', '算法工程师'],
            'position_priority': '后端开发',
            'target_cities': ['北京', '上海', '深圳'],
            'city_priority': '北京',
            'salary_min': 15000,
            'salary_max': 25000,
            'salary_type': 'monthly',
            'salary_negotiable': 1,
            'availability': '立即到岗',
            'available_date': '2023-07-01'
        }

        # 1. 创建/更新求职意向
        print("1. 创建/更新求职意向:")
        intention_id = self.job_intentions.upsert_job_intention(self.test_user_id, intention_data)
        if intention_id:
            print(f"   求职意向ID: {intention_id}")

        # 2. 获取求职意向
        print("\n2. 获取求职意向:")
        intention = self.job_intentions.get_job_intention(self.test_user_id)
        if intention:
            print(f"   目标行业: {intention['target_industries']}")
            print(f"   首选行业: {intention['industry_priority']}")
            print(f"   目标职位: {intention['target_positions']}")
            print(f"   薪资范围: {intention['salary_min']} - {intention['salary_max']} 元/月")

        # 3. 获取城市分布
        print("\n3. 获取城市分布:")
        city_dist = self.job_intentions.get_city_distribution()
        for city in city_dist:
            print(f"   {city['city_priority']}: {city['count']}")

        # 4. 获取薪资统计
        print("\n4. 获取薪资统计:")
        salary_stats = self.job_intentions.get_salary_range_stats()
        print(f"   平均最低薪资: {salary_stats.get('avg_min_salary', 0):.2f}")
        print(f"   平均最高薪资: {salary_stats.get('avg_max_salary', 0):.2f}")

    def test_job_preference_operations(self):
        """测试求职偏好操作"""
        self.print_separator("测试求职偏好操作")

        # 测试数据
        preference_data = {
            'accept_intern_to_full': 1,
            'accept_remote_city': 0,
            'need_campus_referral': 1,
            'accept_overtime': 1,
            'accept_business_trip': 1,
            'company_size_preference': '大型企业（500人以上）',
            'work_type_preference': '全职',
            'other_preferences': '希望有良好的培训机制和晋升空间'
        }

        # 1. 创建/更新求职偏好
        print("1. 创建/更新求职偏好:")
        preference_id = self.job_preferences.upsert_job_preference(self.test_user_id, preference_data)
        if preference_id:
            print(f"   求职偏好ID: {preference_id}")

        # 2. 获取求职偏好
        print("\n2. 获取求职偏好:")
        preference = self.job_preferences.get_job_preference(self.test_user_id)
        if preference:
            print(f"   是否接受转正: {'是' if preference['accept_intern_to_full'] else '否'}")
            print(f"   是否接受远程城市: {'是' if preference['accept_remote_city'] else '否'}")
            print(f"   公司规模偏好: {preference['company_size_preference']}")
            print(f"   工作类型偏好: {preference['work_type_preference']}")

        # 3. 获取工作偏好统计
        print("\n3. 获取工作偏好统计:")
        pref_stats = self.job_preferences.get_work_preference_stats()
        print(f"   平均接受转正率: {pref_stats.get('avg_accept_intern_to_full', 0) * 100:.1f}%")
        print(f"   平均接受加班率: {pref_stats.get('avg_accept_overtime', 0) * 100:.1f}%")

    def test_resume_manager(self):
        """测试简历管理器综合功能"""
        self.print_separator("测试简历管理器综合功能")

        # 1. 获取完整简历
        print("1. 获取完整简历信息:")
        complete_resume = self.resume_manager.get_complete_resume(self.test_user_id)

        if complete_resume:
            print(f"   基本信息: {'已填写' if complete_resume['basic_info'] else '未填写'}")
            print(f"   证书数量: {len(complete_resume['certificates'])}")
            print(f"   实习经历数量: {len(complete_resume['internships'])}")
            print(f"   校园经历: {'已填写' if complete_resume['campus_experiences'] else '未填写'}")
            print(f"   求职意向: {'已填写' if complete_resume['job_intention'] else '未填写'}")
            print(f"   求职偏好: {'已填写' if complete_resume['job_preference'] else '未填写'}")

        # 2. 搜索简历
        print("\n2. 搜索简历:")
        filters = {
            'education_level': '本科',
            'city': '北京',
            'has_internship': True,
            'limit': 5
        }
        search_results = self.resume_manager.search_resumes(filters)
        print(f"   搜索到 {len(search_results)} 份简历")
        if search_results:
            print("   前3条结果:")
            for i, result in enumerate(search_results[:3], 1):
                print(
                    f"   {i}. {result.get('real_name', '未知')} - {result.get('school_name', '未知学校')} - {result.get('major', '未知专业')}")

        # 3. 获取简历统计
        print("\n3. 获取简历统计:")
        resume_stats = self.resume_manager.get_resume_stats()
        print(f"   总简历数: {resume_stats.get('total_resumes', 0)}")
        print(f"   总用户数: {resume_stats.get('total_users', 0)}")
        print(f"   总证书数: {resume_stats.get('total_certificates', 0)}")
        print(f"   总实习经历数: {resume_stats.get('total_internships', 0)}")
        print(f"   平均实习次数: {resume_stats.get('avg_internship_count', 0):.1f}")

        # 4. 批量更新（示例）
        print("\n4. 批量更新测试:")
        update_data = {'city': '上海'}
        conditions = {'graduation_year': 2023}
        updated_count = self.resume_manager.batch_update_resumes(update_data, conditions)
        print(f"   批量更新了 {updated_count} 条记录")

    def test_integration_flow(self):
        """测试完整的简历创建流程"""
        self.print_separator("测试完整简历创建流程")

        # 创建一个测试用户（假设ID为999）
        test_user_id = 999

        print(f"使用测试用户ID: {test_user_id}")

        # 1. 创建简历
        resume_data = {
            'real_name': '李四',
            'gender': '女',
            'birth_date': '1999-05-15',
            'phone': '13900139000',
            'email': 'lisi@example.com',
            'city': '上海',
            'education_level': '硕士',
            'school_name': '复旦大学',
            'major': '金融学',
            'graduation_year': 2024,
            'gpa': 3.7,
            'self_introduction': '金融专业硕士，有丰富的实习经验'
        }

        resume_id = self.resumes.create_resume(test_user_id, resume_data)
        print(f"1. 创建简历: {'成功' if resume_id else '失败'}")

        # 2. 添加证书
        cert_data = {
            'cert_type': 'professional',
            'cert_name': 'CFA一级',
            'cert_level': '一级',
            'issue_date': '2022-12-01',
            'issuing_authority': 'CFA协会'
        }
        cert_id = self.certificates.add_certificate(test_user_id, cert_data)
        print(f"2. 添加证书: {'成功' if cert_id else '失败'}")

        # 3. 添加实习经历
        intern_data = {
            'company_name': '招商银行',
            'position': '金融实习生',
            'industry': '金融',
            'start_date': '2023-02-01',
            'end_date': '2023-08-01',
            'work_content': '参与信贷分析，协助客户经理进行市场调研'
        }
        intern_id = self.internships.add_internship(test_user_id, intern_data)
        print(f"3. 添加实习经历: {'成功' if intern_id else '失败'}")

        # 4. 设置求职意向
        intention_data = {
            'target_industries': ['金融', '投资'],
            'target_positions': ['金融分析师', '投资顾问'],
            'target_cities': ['上海', '香港'],
            'salary_min': 20000,
            'salary_max': 35000
        }
        intention_id = self.job_intentions.upsert_job_intention(test_user_id, intention_data)
        print(f"4. 设置求职意向: {'成功' if intention_id else '失败'}")

        # 5. 获取完整简历
        complete = self.resume_manager.get_complete_resume(test_user_id)
        print(f"5. 获取完整简历: {'成功' if complete['basic_info'] else '失败'}")

        # 清理测试数据（可选）
        # self.resumes.delete_resume(test_user_id)

    def cleanup_test_data(self):
        """清理测试数据"""
        self.print_separator("清理测试数据")

        # 注意：这将会删除所有相关数据
        confirm = input("确定要删除所有测试数据吗？(yes/no): ")
        if confirm.lower() == 'yes':
            self.resumes.delete_resume(self.test_user_id)
            print("测试数据已清理")
        else:
            print("取消清理操作")

    def run_all_tests(self):
        """运行所有测试"""
        try:
            print("开始测试简历管理系统...")

            # 按顺序运行所有测试
            self.test_resume_operations()
            self.test_certificate_operations()
            self.test_campus_experience_operations()
            self.test_internship_operations()
            self.test_job_intention_operations()
            self.test_job_preference_operations()
            self.test_resume_manager()

            # 完整流程测试（可选）
            # self.test_integration_flow()

            print("\n" + "=" * 60)
            print(" 所有测试完成！ ")
            print("=" * 60)

        except Exception as e:
            print(f"测试过程中出现异常: {e}")
        finally:
            self.connection.close()
            print("数据库连接已关闭")

    def quick_test(self):
        """快速测试主要功能"""
        self.print_separator("快速测试")

        try:
            # 测试连接
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("✓ 数据库连接正常")

            # 测试简历操作
            test_data = {
                'real_name': '测试用户',
                'education_level': '本科',
                'school_name': '测试大学',
                'major': '测试专业'
            }

            # 先尝试删除可能存在的测试数据
            self.resumes.delete_resume(self.test_user_id)

            # 创建简历
            resume_id = self.resumes.create_resume(self.test_user_id, test_data)
            if resume_id:
                print("✓ 简历创建成功")

                # 获取简历
                resume = self.resumes.get_resume_by_user(self.test_user_id)
                if resume:
                    print(f"✓ 简历获取成功: {resume.get('real_name')}")

                    # 测试简历管理器
                    complete = self.resume_manager.get_complete_resume(self.test_user_id)
                    if complete:
                        print("✓ 完整简历获取成功")
                    else:
                        print("✗ 完整简历获取失败")
                else:
                    print("✗ 简历获取失败")
            else:
                print("✗ 简历创建失败")

        except Exception as e:
            print(f"✗ 测试失败: {e}")


# # 使用示例
# if __name__ == "__main__":
#     # 配置数据库连接信息
#     db_config = {
#         'host': 'localhost',
#         'user': 'root',
#         'password': '123456',
#         'database': 'boss_job'
#     }
#
#     # 创建调试器实例
#     debugger = ResumeDebugger(**db_config)
#
#     # 选择测试模式
#     print("请选择测试模式：")
#     print("1. 完整测试")
#     print("2. 快速测试")
#     print("3. 清理测试数据")
#     print("4. 测试特定功能")
#
#     choice = input("请输入选择 (1-4): ")
#
#     if choice == '1':
#         debugger.run_all_tests()
#     elif choice == '2':
#         debugger.quick_test()
#     elif choice == '3':
#         debugger.cleanup_test_data()
#     elif choice == '4':
#         print("\n请选择要测试的功能：")
#         print("1. 简历基本操作")
#         print("2. 证书操作")
#         print("3. 实习经历操作")
#         print("4. 求职意向操作")
#         print("5. 综合功能测试")
#
#         func_choice = input("请输入选择 (1-5): ")
#
#         if func_choice == '1':
#             debugger.test_resume_operations()
#         elif func_choice == '2':
#             debugger.test_certificate_operations()
#         elif func_choice == '3':
#             debugger.test_internship_operations()
#         elif func_choice == '4':
#             debugger.test_job_intention_operations()
#         elif func_choice == '5':
#             debugger.test_resume_manager()
#     else:
#         print("无效选择")

# from sql_data_demo import ComplaintFeedbackManager
#
# def example_usage():
#     # 创建数据库连接
#     connection = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='123456',
#         database='boss_job',
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )
#
#     # 创建管理器实例
#     manager = ComplaintFeedbackManager(connection)
#
#     try:
#         # 示例1: 获取所有投诉类型
#         complaint_types = manager.get_all_complaint_types()
#         print(f"投诉类型: {complaint_types}")
#
#         # 示例2: 用户提交投诉
#         complaint_id = manager.submit_complaint(
#             user_id=1,
#             complaint_type=1,
#             description="测试投诉描述",
#             image_urls=["http://example.com/image1.jpg"],
#             priority=2
#         )
#         print(f"创建的投诉ID: {complaint_id}")
#
#         # 示例3: 获取用户投诉
#         user_complaints = manager.get_user_complaints(user_id=1)
#         print(f"用户投诉: {user_complaints}")
#
#         # 示例4: 获取投诉列表
#         complaints, total = manager.get_complaint_list(
#             filters={'is_resolved': 0},
#             page=1,
#             page_size=10
#         )
#         print(f"未解决投诉: {complaints}, 总数: {total}")
#
#         # 示例5: 获取统计信息
#         stats = manager.get_complaint_statistics()
#         print(f"统计信息: {stats}")
#
#     finally:
#         # 关闭连接
#         manager.close_connection()
#
#
# if __name__ == "__main__":
#     example_usage()
from sql_data_demo import Job_category_simple


job_category_simple = Job_category_simple(db.connection)
job_category_simple.job_intro_list()



