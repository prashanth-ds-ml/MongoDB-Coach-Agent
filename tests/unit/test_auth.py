from unittest.mock import MagicMock, patch


def test_database_create_and_authenticate_user():
    from certcoach.core import database

    inserted = {}
    users_col = MagicMock()
    users_col.find_one.side_effect = [None, inserted]

    def insert_one(doc):
        inserted.update(doc)

    users_col.insert_one.side_effect = insert_one

    with patch.object(database, "users_col", users_col):
        ok, user = database.create_user("User@Example.com", "strongpass", "User")
        assert ok is True
        assert user["email"] == "user@example.com"
        assert "password_hash" not in user

        ok, authed = database.authenticate_user("user@example.com", "strongpass")
        assert ok is True
        assert authed["_id"] == user["_id"]


def test_auth_session_roundtrip(tmp_path):
    from certcoach.core import auth

    session_file = tmp_path / "session.json"
    user = {"_id": "u1", "email": "u@example.com", "display_name": "User"}

    with patch.object(auth, "SESSION_FILE", str(session_file)):
        auth.save_session(user)
        assert auth.get_session_user_id() == "u1"
        auth.clear_session()
        assert auth.get_session_user_id() == "local_user_1"
