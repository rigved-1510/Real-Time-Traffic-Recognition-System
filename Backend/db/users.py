from db.connection import execute_query


# ── CRUD helpers for the `users` table ─────────────────────────────────────────

def create_user(username: str, email: str, password_hash: str, role: str = "user") -> int:
    sql = """
        INSERT INTO users (username, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(sql, (username, email, password_hash, role), commit=True)


def get_user_by_id(user_id: int) -> dict | None:
    return execute_query(
        "SELECT * FROM users WHERE user_id = %s", (user_id,), fetch="one"
    )


def get_user_by_email(email: str) -> dict | None:
    return execute_query(
        "SELECT * FROM users WHERE email = %s", (email,), fetch="one"
    )


def get_user_by_username(username: str) -> dict | None:
    return execute_query(
        "SELECT * FROM users WHERE username = %s", (username,), fetch="one"
    )


def update_last_login(user_id: int):
    execute_query(
        "UPDATE users SET last_login_at = NOW(), failed_login_attempts = 0, account_locked_until = NULL WHERE user_id = %s",
        (user_id,), commit=True
    )


def increment_failed_attempts(user_id: int):
    execute_query(
        "UPDATE users SET failed_login_attempts = failed_login_attempts + 1 WHERE user_id = %s",
        (user_id,), commit=True
    )


def lock_account(user_id: int, until_dt):
    execute_query(
        "UPDATE users SET account_locked_until = %s WHERE user_id = %s",
        (until_dt, user_id), commit=True
    )


def unlock_account(user_id: int):
    execute_query(
        "UPDATE users SET account_locked_until = NULL, failed_login_attempts = 0 WHERE user_id = %s",
        (user_id,), commit=True
    )


def set_totp_secret(user_id: int, secret: str):
    execute_query(
        "UPDATE users SET totp_secret = %s WHERE user_id = %s",
        (secret, user_id), commit=True
    )


def enable_2fa(user_id: int):
    execute_query(
        "UPDATE users SET is_2fa_enabled = 1 WHERE user_id = %s",
        (user_id,), commit=True
    )


def disable_2fa(user_id: int):
    execute_query(
        "UPDATE users SET is_2fa_enabled = 0, totp_secret = NULL WHERE user_id = %s",
        (user_id,), commit=True
    )


def update_password(user_id: int, new_hash: str):
    execute_query(
        "UPDATE users SET password_hash = %s WHERE user_id = %s",
        (new_hash, user_id), commit=True
    )


def update_profile(user_id: int, username: str, email: str):
    execute_query(
        "UPDATE users SET username = %s, email = %s WHERE user_id = %s",
        (username, email, user_id), commit=True
    )


def list_users(limit: int = 100, offset: int = 0) -> list:
    return execute_query(
        """SELECT user_id, username, email, role, is_2fa_enabled,
                  failed_login_attempts, account_locked_until,
                  email_verified, created_at, last_login_at
           FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s""",
        (limit, offset), fetch="all"
    )


def admin_update_user(user_id: int, role: str = None, email_verified: bool = None):
    parts, params = [], []
    if role is not None:
        parts.append("role = %s"); params.append(role)
    if email_verified is not None:
        parts.append("email_verified = %s"); params.append(int(email_verified))
    if not parts:
        return
    params.append(user_id)
    execute_query(f"UPDATE users SET {', '.join(parts)} WHERE user_id = %s", params, commit=True)


def delete_user(user_id: int):
    execute_query("DELETE FROM users WHERE user_id = %s", (user_id,), commit=True)


def get_user_count() -> int:
    row = execute_query("SELECT COUNT(*) AS cnt FROM users", fetch="one")
    return row["cnt"] if row else 0


# ── Backup codes ────────────────────────────────────────────────────────────────

def save_backup_codes(user_id: int, code_hashes: list[str]):
    from db.connection import execute_many
    execute_many(
        "INSERT INTO backup_codes (user_id, code_hash) VALUES (%s, %s)",
        [(user_id, h) for h in code_hashes]
    )



def get_unused_backup_codes(user_id: int) -> list:
    return execute_query(
        "SELECT * FROM backup_codes WHERE user_id = %s AND used = 0",
        (user_id,), fetch="all"
    )


def mark_backup_code_used(code_id: int):
    execute_query(
        "UPDATE backup_codes SET used = 1, used_at = NOW() WHERE code_id = %s",
        (code_id,), commit=True
    )
