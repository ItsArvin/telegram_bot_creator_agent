def test_auth_module_imports():
    from app.api.auth import router
    from app.models import Session, User
    assert router is not None and Session is not None and User is not None
def test_password_roundtrip():
    from app.services.password import hash_password, verify_password
    hashed=hash_password("correct horse battery staple")
    assert hashed!="correct horse battery staple"
    assert verify_password("correct horse battery staple",hashed)
    assert not verify_password("wrong password",hashed)
