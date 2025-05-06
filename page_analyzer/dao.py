import psycopg2
from psycopg2.extras import RealDictCursor


class UrlDAO:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def save(self, url):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id FROM urls WHERE name=%s", (url,))
                row = cur.fetchone()

                if row:
                    return row['id'], True

                cur.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id;",
                            (url,))
                new_id = cur.fetchone()['id']
                conn.commit()
                return new_id, False

    def get_by_id(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id=%s", (url_id,))
                return cur.fetchone()

    def get_all(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        urls.id, 
                        urls.name, 
                        uc.status_code,
                        uc.created_at AS last_check_date
                    FROM urls
                    LEFT JOIN (
                        SELECT DISTINCT ON (url_id)
                            url_id,
                            status_code,
                            created_at
                        FROM url_checks
                        ORDER BY url_id, created_at DESC
                    ) AS uc ON urls.id = uc.url_id
                    ORDER BY urls.id DESC;
                """)
                return cur.fetchall()

    def create_url_check(self, url_id, status_code, h1, title, description):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
            INSERT INTO url_checks (url_id, status_code, h1, title, description)
            VALUES (%s, %s, %s, %s, %s);
            """, (url_id, status_code, h1, title, description))
                conn.commit()

    def get_checks_by_url_id(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC",
                            (url_id,))
                return cur.fetchall()
