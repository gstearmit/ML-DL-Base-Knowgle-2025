import os
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()

class DatabaseMigrator:
    def __init__(self):
        # Lấy thông tin kết nối từ biến môi trường
        self.db_params = {
            'dbname': os.getenv('DB_NAME', 'enterprise_llm'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'host': os.getenv('DB_HOST', 'localhost')
        }
        
        # Đường dẫn đến thư mục migrations
        self.migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    
    def _get_connection(self):
        """Tạo kết nối đến cơ sở dữ liệu"""
        return psycopg2.connect(**self.db_params)
    
    def _create_migrations_table(self, conn):
        """Tạo bảng theo dõi migrations"""
        with conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(255) PRIMARY KEY,
                applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()
    
    def _get_applied_migrations(self, conn):
        """Lấy danh sách migrations đã được áp dụng"""
        with conn.cursor() as cursor:
            cursor.execute("SELECT version FROM schema_migrations")
            return {row[0] for row in cursor.fetchall()}
    
    def _mark_migration_applied(self, conn, migration_file):
        """Đánh dấu migration đã được áp dụng"""
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO schema_migrations (version) VALUES (%s)",
                (migration_file,)
            )
            conn.commit()
    
    def migrate(self):
        """Thực hiện migrations"""
        conn = self._get_connection()
        try:
            # Tạo bảng theo dõi migrations
            self._create_migrations_table(conn)
            
            # Lấy danh sách migrations đã áp dụng
            applied_migrations = self._get_applied_migrations(conn)
            
            # Lấy danh sách file migrations
            migration_files = sorted(
                [f for f in os.listdir(self.migrations_dir) if f.endswith('.sql')],
                key=lambda x: int(x.split('_')[0])
            )
            
            # Thực hiện migrations chưa được áp dụng
            for migration_file in migration_files:
                if migration_file not in applied_migrations:
                    migration_path = os.path.join(self.migrations_dir, migration_file)
                    
                    with open(migration_path, 'r') as f:
                        migration_sql = f.read()
                    
                    with conn.cursor() as cursor:
                        try:
                            cursor.execute(migration_sql)
                            conn.commit()
                            
                            # Đánh dấu migration đã được áp dụng
                            self._mark_migration_applied(conn, migration_file)
                            print(f"Áp dụng migration: {migration_file}")
                        except Exception as e:
                            conn.rollback()
                            print(f"Lỗi khi áp dụng migration {migration_file}: {e}")
                            raise
            
            print("Migrations hoàn tất.")
        
        except Exception as e:
            print(f"Lỗi trong quá trình migrations: {e}")
        
        finally:
            conn.close()
    
    def rollback(self, steps=1):
        """Hoàn tác migrations"""
        conn = self._get_connection()
        try:
            # Lấy danh sách migrations đã áp dụng
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT version 
                    FROM schema_migrations 
                    ORDER BY applied_at DESC 
                    LIMIT %s
                """, (steps,))
                migrations_to_rollback = [row[0] for row in cursor.fetchall()]
            
            # Thực hiện rollback
            for migration_file in migrations_to_rollback:
                migration_path = os.path.join(self.migrations_dir, migration_file)
                
                with open(migration_path, 'r') as f:
                    migration_sql = f.read()
                
                # Tìm và thực thi các câu lệnh DROP
                drop_statements = [
                    line.strip() for line in migration_sql.split('\n') 
                    if line.strip().startswith('DROP')
                ]
                
                with conn.cursor() as cursor:
                    try:
                        for drop_stmt in drop_statements:
                            cursor.execute(drop_stmt)
                        
                        # Xóa migration khỏi bảng theo dõi
                        cursor.execute(
                            "DELETE FROM schema_migrations WHERE version = %s", 
                            (migration_file,)
                        )
                        
                        conn.commit()
                        print(f"Hoàn tác migration: {migration_file}")
                    
                    except Exception as e:
                        conn.rollback()
                        print(f"Lỗi khi hoàn tác migration {migration_file}: {e}")
                        raise
            
            print("Hoàn tác migrations hoàn tất.")
        
        except Exception as e:
            print(f"Lỗi trong quá trình hoàn tác migrations: {e}")
        
        finally:
            conn.close()

def main():
    """Điểm nhập chính cho script"""
    migrator = DatabaseMigrator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'migrate':
            migrator.migrate()
        elif command == 'rollback':
            steps = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            migrator.rollback(steps)
        else:
            print("Sử dụng: python manage_db.py [migrate|rollback] [số bước rollback]")
    else:
        print("Sử dụng: python manage_db.py [migrate|rollback] [số bước rollback]")

if __name__ == '__main__':
    main()
