
class UrlDAO:
    def __init__(self, conn):
        self.conn = conn

    def save(self, url):
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1 FROM urls WHERE name=%s", (url,))
            row = cur.fetchone()

            if row:
                return row[0], True

            cur.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id;", (url,))
            new_id = cur.fetchone()[0]
            self.conn.commit()
            return new_id, False

    def get_by_id(self, id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE id=%s", (id,))
            return cur.fetchone()

    def get_all(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM urls ORDER BY id DESC")
            return cur.fetchall()