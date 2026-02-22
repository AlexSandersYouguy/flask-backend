WITH role_sel AS (
    SELECT id FROM roles WHERE role_name = %s
)
INSERT INTO users (username, password_hash, role_id)
VALUES (%s, %s, (SELECT id FROM role_sel))
RETURNING id;
