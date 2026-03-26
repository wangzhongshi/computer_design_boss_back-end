#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量导入头像图片到 sys_user 表
支持从文件夹读取图片，批量分配给表中的【所有】用户（无论状态如何）
"""

import os
import pymysql
import random
from pathlib import Path
from typing import List, Tuple, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AvatarImporter:
    def __init__(
            self,
            host: str = 'localhost',
            port: int = 3306,
            user: str = 'root',
            password: str = '123456',
            database: str = 'boss_job',
            charset: str = 'utf8mb4'
    ):
        """初始化数据库连接"""
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()
        logger.info("数据库连接成功")

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("数据库连接已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def load_images_from_folder(self, folder_path: str) -> List[Tuple[str, bytes, str]]:
        """
        从文件夹加载图片文件

        Args:
            folder_path: 图片文件夹路径

        Returns:
            List[Tuple[文件名, 二进制数据, 格式]]
        """
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"文件夹不存在: {folder_path}")

        # 支持的图片格式
        supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}

        images = []
        for file_path in folder.iterdir():
            if file_path.suffix.lower() in supported_formats:
                try:
                    with open(file_path, 'rb') as f:
                        image_data = f.read()

                    # 检测图片格式
                    img_format = self._detect_image_format(image_data, file_path.suffix)

                    images.append((
                        file_path.name,
                        image_data,
                        img_format
                    ))
                    logger.info(f"加载图片: {file_path.name} ({len(image_data)} bytes)")

                except Exception as e:
                    logger.error(f"读取图片失败 {file_path}: {e}")

        logger.info(f"共加载 {len(images)} 张图片")
        return images

    def _detect_image_format(self, data: bytes, fallback_ext: str) -> str:
        """通过文件头检测图片格式"""
        # 文件头魔数
        if data.startswith(b'\x89PNG'):
            return 'png'
        elif data.startswith(b'\xff\xd8\xff'):
            return 'jpg'
        elif data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
            return 'gif'
        elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
            return 'webp'
        elif data.startswith(b'BM'):
            return 'bmp'
        else:
            # 使用文件扩展名
            return fallback_ext.lower().replace('.', '') or 'png'

    def get_all_users(self) -> List[dict]:
        """
        【关键修改】获取所有用户，无论状态如何（包括已删除、已禁用等）

        Returns:
            所有用户列表
        """
        sql = """
            SELECT user_id, real_name, mobile, gender, status, is_deleted
            FROM sys_user
            ORDER BY user_id ASC
        """
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        logger.info(f"找到 {len(users)} 个用户（包含所有状态）")

        # 显示用户状态分布
        status_count = {}
        for u in users:
            key = f"status={u['status']}, deleted={u['is_deleted']}"
            status_count[key] = status_count.get(key, 0) + 1

        logger.info("用户状态分布:")
        for status, count in sorted(status_count.items()):
            logger.info(f"  {status}: {count}人")

        return users

    def get_users_without_avatar(self, limit: Optional[int] = None) -> List[dict]:
        """
        获取没有头像的用户列表（不过滤状态，只看avatar字段）

        Args:
            limit: 限制返回数量，None表示返回所有

        Returns:
            用户列表
        """
        sql = """
            SELECT user_id, real_name, mobile, gender, status, is_deleted
            FROM sys_user
            WHERE (avatar IS NULL OR avatar_size = 0 OR avatar_size IS NULL)
            ORDER BY user_id ASC
        """
        if limit:
            sql += f" LIMIT {limit}"

        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        logger.info(f"找到 {len(users)} 个没有头像的用户")
        return users

    def assign_avatars(
            self,
            images: List[Tuple[str, bytes, str]],
            users: List[dict],
            mode: str = 'sequential',  # 'sequential', 'random', 'by_gender'
    ) -> int:
        """
        分配头像给用户【强制更新，无论之前是否有头像】

        Args:
            images: 图片列表 [(文件名, 数据, 格式), ...]
            users: 用户列表
            mode: 分配模式
                - 'sequential': 按顺序分配（用户1->图片1，用户2->图片2...）
                - 'random': 随机分配
                - 'by_gender': 根据性别分配不同头像（需要图片命名包含gender标识）

        Returns:
            成功更新的用户数
        """
        if not images or not users:
            logger.warning("图片或用户列表为空")
            return 0

        success_count = 0
        skip_count = 0

        # 准备更新SQL - 强制更新所有用户
        update_sql = """
            UPDATE sys_user 
            SET avatar = %s,
                avatar_format = %s,
                avatar_size = %s,
                updated_at = NOW()
            WHERE user_id = %s
        """

        for i, user in enumerate(users):
            # 选择图片
            if mode == 'random':
                img_info = random.choice(images)
            elif mode == 'by_gender':
                # 尝试根据性别匹配（图片名包含 male/female）
                gender = user.get('gender', 0)
                filtered = [
                    img for img in images
                    if (gender == 1 and 'male' in img[0].lower() and 'female' not in img[0].lower()) or
                       (gender == 2 and 'female' in img[0].lower()) or
                       (gender == 0 and 'unknown' in img[0].lower())
                ]
                img_info = random.choice(filtered) if filtered else images[i % len(images)]
            else:  # sequential
                img_info = images[i % len(images)]  # 循环使用图片

            filename, image_data, img_format = img_info

            try:
                self.cursor.execute(update_sql, (
                    image_data,
                    img_format,
                    len(image_data),
                    user['user_id']
                ))

                if self.cursor.rowcount > 0:
                    success_count += 1
                    status_info = f"[status={user.get('status', '?')}, deleted={user.get('is_deleted', '?')}]"
                    logger.info(
                        f"[{success_count}] 用户 {user.get('real_name', 'N/A')} "
                        f"({user['user_id']}) {status_info} <- {filename}"
                    )
                else:
                    skip_count += 1
                    logger.warning(f"跳过用户 {user['user_id']} (无变化)")

                # 每10个提交一次，避免大事务
                if success_count % 10 == 0:
                    self.conn.commit()

            except Exception as e:
                logger.error(f"更新用户 {user['user_id']} 失败: {e}")
                self.conn.rollback()

        # 最终提交
        self.conn.commit()
        logger.info(f"成功为 {success_count} 个用户分配头像，跳过 {skip_count} 个")
        return success_count

    def verify_update(self, sample_size: int = 5):
        """验证更新结果"""
        # 显示最新更新的用户
        sql = """
            SELECT user_id, real_name, avatar_format, avatar_size, 
                   status, is_deleted, updated_at
            FROM sys_user
            WHERE avatar IS NOT NULL
            ORDER BY updated_at DESC
            LIMIT %s
        """
        self.cursor.execute(sql, (sample_size,))
        results = self.cursor.fetchall()

        print("\n" + "=" * 70)
        print("更新验证（最新更新的用户）:")
        print("=" * 70)
        for row in results:
            status_str = f"status={row['status']}, deleted={row['is_deleted']}"
            print(f"用户: {row['real_name'] or 'N/A'}")
            print(f"  ID: {row['user_id']}")
            print(f"  状态: {status_str}")
            print(f"  格式: {row['avatar_format']}")
            print(f"  大小: {row['avatar_size']:,} bytes ({row['avatar_size'] / 1024:.1f} KB)")
            print(f"  更新时间: {row['updated_at']}")
            print("-" * 40)

        # 统计 - 所有用户
        stats_sql = """
            SELECT 
                COUNT(*) as total_users,
                SUM(CASE WHEN avatar IS NOT NULL AND avatar_size > 0 THEN 1 ELSE 0 END) as with_avatar,
                SUM(CASE WHEN avatar IS NULL OR avatar_size = 0 OR avatar_size IS NULL THEN 1 ELSE 0 END) as without_avatar,
                AVG(avatar_size) as avg_size
            FROM sys_user
        """
        self.cursor.execute(stats_sql)
        stats = self.cursor.fetchone()

        print(f"\n【总体统计 - 所有用户】:")
        print(f"  总用户数: {stats['total_users']}")
        print(f"  有头像: {stats['with_avatar']} ({stats['with_avatar'] / stats['total_users'] * 100:.1f}%)")
        print(f"  无头像: {stats['without_avatar']}")
        if stats['avg_size']:
            print(f"  平均头像大小: {stats['avg_size'] / 1024:.1f} KB")

        # 按状态统计
        detail_sql = """
            SELECT 
                status,
                is_deleted,
                COUNT(*) as total,
                SUM(CASE WHEN avatar IS NOT NULL AND avatar_size > 0 THEN 1 ELSE 0 END) as with_avatar
            FROM sys_user
            GROUP BY status, is_deleted
            ORDER BY is_deleted, status
        """
        self.cursor.execute(detail_sql)
        details = self.cursor.fetchall()

        print(f"\n【按状态统计】:")
        for d in details:
            pct = d['with_avatar'] / d['total'] * 100 if d['total'] > 0 else 0
            print(f"  status={d['status']}, deleted={d['is_deleted']}: "
                  f"{d['with_avatar']}/{d['total']} 有头像 ({pct:.0f}%)")

        print("=" * 70)

    def export_avatar_to_file(self, user_id: int, output_path: str):
        """将用户头像导出到文件（用于验证）"""
        sql = "SELECT avatar, avatar_format FROM sys_user WHERE user_id = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()

        if result and result['avatar']:
            ext = result['avatar_format'] or 'png'
            filepath = f"{output_path}/avatar_{user_id}.{ext}"
            with open(filepath, 'wb') as f:
                f.write(result['avatar'])
            logger.info(f"头像已导出: {filepath}")
            return filepath
        else:
            logger.warning(f"用户 {user_id} 没有头像")
            return None


def main():
    """主程序"""
    # ==================== 配置区域 ====================

    # 数据库配置（请修改为你的配置）
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123456',  # 修改这里
        'database': 'boss_job'  # 修改这里
    }

    # 图片文件夹路径（修改为你的路径）
    AVATAR_FOLDER = 'user_pic'  # 例如: '/home/user/avatars' 或 'C:\\Users\\xxx\\avatars'

    # 运行模式选择
    MODE = 'sequential'  # 'sequential':顺序分配, 'random':随机分配, 'by_gender':按性别分配

    # =================================================

    # 检查路径
    if not os.path.exists(AVATAR_FOLDER):
        print(f"错误: 图片文件夹不存在: {AVATAR_FOLDER}")
        print("请创建文件夹并放入头像图片")
        return

    # 执行导入
    with AvatarImporter(**DB_CONFIG) as importer:
        # 1. 加载图片
        images = importer.load_images_from_folder(AVATAR_FOLDER)

        if len(images) == 0:
            logger.error("没有找到任何图片，退出")
            return

        # 2. 【关键】获取所有用户，无论状态如何
        users = importer.get_all_users()

        if not users:
            logger.info("数据库中没有用户")
            return

        # 3. 分配头像
        print(f"\n开始为所有用户分配头像...")
        print(f"图片数量: {len(images)}")
        print(f"用户数量: {len(users)}")
        print(f"分配模式: {MODE}")
        print("-" * 60)

        count = importer.assign_avatars(images, users, mode=MODE)

        # 4. 验证结果
        print()
        importer.verify_update(sample_size=5)

        # 5. 导出示例验证（导出前3个用户的头像）
        export_dir = './exported_avatars'
        os.makedirs(export_dir, exist_ok=True)
        for i, user in enumerate(users[:3]):
            importer.export_avatar_to_file(user['user_id'], export_dir)
        print(f"\n示例头像已导出到: {export_dir}/")


if __name__ == '__main__':
    main()