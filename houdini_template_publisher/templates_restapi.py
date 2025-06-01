import psycopg2
from typing import Generator

class TemplatesRestApi:

    def __init__(self) -> None:
        self.db = psycopg2.connect(database='houmanager',
                        user='postgres',
                        password='1234',
                        host='localhost',
                        port='5432')
        self.db_cursor = self.db.cursor()

    def user_bundles(self):
        query = "SELECT id,name FROM bundles ORDER BY id;"
        self.db_cursor.execute(query)
        yield self.db_cursor.fetchall()

    def bundle_lists(self) -> Generator:
        query = "SELECT id,bundle FROM bundles_list ORDER BY id;"
        self.db_cursor.execute(query)
        yield self.db_cursor.fetchall()

    def categories(self) -> Generator:
        query = "SELECT id,category FROM categories ORDER BY id;"
        self.db_cursor.execute(query)
        yield self.db_cursor.fetchall()

    def contexts(self) -> Generator:
        query = "SELECT id,context FROM contexts ORDER BY id;"
        self.db_cursor.execute(query)
        yield self.db_cursor.fetchall()
    
    def tags(self) -> Generator:
        query = "SELECT id,tag FROM tags ORDER BY id;"
        self.db_cursor.execute(query)
        yield self.db_cursor.fetchall()
    
    def bundle_types(self) -> Generator:
        query = "SELECT id,bundle_type FROM bundle_types ORDER BY id;"
        self.db_cursor.execute(query)
        yield self.db_cursor.fetchall()

    def user_bundle_versions(self, 
                            bundle_name: str) -> Generator:
        query = f"SELECT version FROM bundles WHERE name = '{bundle_name}'"
        self.db_cursor.execute(query)
        yield self.db_cursor.fetchall()

    def bundle_types(self) -> Generator:
        query = "SELECT id,bundle_type FROM bundle_types ORDER BY id;"
        self.db_cursor.execute(query)
        yield self.db_cursor.fetchall()

    
    def bundle_tag_mtom_relation(self, bundle_id: int, tag_id: int):
        query = f"INSERT INTO bundles_tag(bundle_id, tag_id) VALUES({bundle_id}, {tag_id})"
        self.db_cursor.execute(query)
        self.db.commit()
    

    def insert_bundle(self, 
                                bundle_name: str,
                                description: str,
                                version: int,
                                artist: str,
                                file_path: str,
                                file_type: str,
                                frame_start: int,
                                frame_end: int,
                                img_path: str,
                                bundle_type_id: int,
                                bundle_list_id: int,
                                category_id: int,
                                context_id: int,
                                houdini_version_id: int,
                                frame_count: int) -> int:
        query = f"""
            INSERT INTO bundles(
                name, 
                description, 
                version, 
                artist, 
                file_path, 
                file_type, 
                frame_start, 
                frame_end, 
                img_path, 
                favorite, 
                bundle_type_id, 
                bundle_list_id, 
                category_id, 
                context_id, 
                houdini_version_id, 
                frame_count
            ) 
            VALUES(
                '{bundle_name}', 
                '{description}', 
                {version}, 
                '{artist}', 
                '{file_path}', 
                '{file_type}', 
                {frame_start}, 
                {frame_end}, 
                '{img_path}', 
                FALSE,
                {bundle_type_id}, 
                {bundle_list_id}, 
                {category_id}, 
                {context_id}, 
                {houdini_version_id}, 
                {frame_count}
            )
            RETURNING id
            """

        self.db_cursor.execute(query)
        self.id = self.db_cursor.fetchone()[0]  # Now this will work
        self.db.commit()
        return self.id

if __name__ == "__main__":
    template_rest_api = TemplatesRestApi()
    pass