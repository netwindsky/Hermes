from pymongo import MongoClient, errors
from typing import Any, Dict, List, Optional
import time

class MongoDBStorage:
    def __init__(self, uri: str, db_name: str, username: Optional[str] = None, password: Optional[str] = None):
        """
        初始化 MongoDB 存储类。

        :param uri: MongoDB 连接字符串。
        :param db_name: 数据库名称。
        :param username: 用户名。
        :param password: 密码。
        """
        if username and password:
            uri = f"mongodb://{username}:{password}@{uri.split('://')[1]}"
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def connect(self):
        """
        连接到 MongoDB 数据库。
        """
        try:
            # 尝试访问数据库以确保连接成功
            self.db.command("ping")
        except errors.PyMongoError as e:
            logger.error(f"Error connecting to MongoDB: {e}")

    def disconnect(self):
        """
        断开与 MongoDB 数据库的连接。
        """
        self.client.close()

    def save(self, table_name: str, data: Dict):
        try:
            self.db[table_name].insert_one(data)
        except errors.PyMongoError as e:
            logger.error(f"Error saving data to MongoDB: {e}")

    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """
        插入单个文档到指定集合。

        :param collection_name: 集合名称。
        :param document: 要插入的文档。
        :return: 插入文档的 ID。
        """
        try:
            result = self.db[collection_name].insert_one(document)
            return str(result.inserted_id)
        except errors.PyMongoError as e:
            logger.error(f"Error inserting document: {e}")
            return None

    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> Optional[List[str]]:
        """
        插入多个文档到指定集合。

        :param collection_name: 集合名称。
        :param documents: 要插入的文档列表。
        :return: 插入文档的 ID 列表。
        """
        try:
            result = self.db[collection_name].insert_many(documents)
            return [str(id) for id in result.inserted_ids]
        except errors.PyMongoError as e:
            logger.error(f"Error inserting documents: {e}")
            return None

    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        查找单个文档。

        :param collection_name: 集合名称。
        :param query: 查询条件。
        :return: 找到的文档。
        """
        try:
            return self.db[collection_name].find_one(query)
        except errors.PyMongoError as e:
            logger.error(f"Error finding document: {e}")
            return None

    def find(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        查找多个文档。

        :param collection_name: 集合名称。
        :param query: 查询条件。
        :return: 找到的文档列表。
        """
        try:
            return list(self.db[collection_name].find(query))
        except errors.PyMongoError as e:
            logger.error(f"Error finding documents: {e}")
            return []

    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """
        更新单个文档。

        :param collection_name: 集合名称。
        :param query: 查询条件。
        :param update: 更新内容。
        :return: 是否更新成功。
        """
        try:
            result = self.db[collection_name].update_one(query, update)
            return result.modified_count > 0
        except errors.PyMongoError as e:
            logger.error(f"Error updating document: {e}")
            return False

    def update_many(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """
        更新多个文档。

        :param collection_name: 集合名称。
        :param query: 查询条件。
        :param update: 更新内容。
        :return: 更新的文档数量。
        """
        try:
            result = self.db[collection_name].update_many(query, update)
            return result.modified_count
        except errors.PyMongoError as e:
            logger.error(f"Error updating documents: {e}")
            return 0

    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> bool:
        """
        删除单个文档。

        :param collection_name: 集合名称。
        :param query: 查询条件。
        :return: 是否删除成功。
        """
        try:
            result = self.db[collection_name].delete_one(query)
            return result.deleted_count > 0
        except errors.PyMongoError as e:
            logger.error(f"Error deleting document: {e}")
            return False

    def delete_many(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        删除多个文档。

        :param collection_name: 集合名称。
        :param query: 查询条件。
        :return: 删除的文档数量。
        """
        try:
            result = self.db[collection_name].delete_many(query)
            return result.deleted_count
        except errors.PyMongoError as e:
            logger.error(f"Error deleting documents: {e}")
            return 0

    def close(self):
        """
        关闭数据库连接。
        """
        self.client.close()