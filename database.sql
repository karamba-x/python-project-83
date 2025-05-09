CREATE TABLE IF NOT EXISTS urls (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS url_checks (
  id SERIAL PRIMARY KEY,
  url_id INT REFERENCES urls(id) ON DELETE CASCADE,
  status_code INT,
  h1 TEXT,
  title TEXT,
  description TEXT,
  created_at DATE DEFAULT CURRENT_DATE
);