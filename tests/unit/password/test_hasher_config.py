from user_registration.password import Argon2Config, Argon2Hasher


def test_custom_argon2_configuration() -> None:
    config = Argon2Config(time_cost=2, memory_cost=32768, parallelism=2)
    hasher = Argon2Hasher(config)
    password = "StrongPassword123!"
    password_hash = hasher.hash(password)

    assert password_hash != password
    assert hasher.verify(password, password_hash) is True
    assert hasher.verify("wrong-password", password_hash) is False
