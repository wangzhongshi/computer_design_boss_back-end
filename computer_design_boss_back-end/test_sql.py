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

# 创建Sys_user实例（假设已经初始化了数据库连接）
sys_user = Test_Sys_user(db.connection)

# 方法1：运行单个调试函数
sys_user.debug_user_count_all()

# 方法2：运行所有调试
sys_user.debug_all_functions()

# 方法3：先设置测试数据，再调试
sys_user.setup_test_data()
sys_user.debug_all_functions()