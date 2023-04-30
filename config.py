class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    # postgres://test_y49s_user:wJKnItKoR7mP2YEKwyLc5iOQSZynP38F@dpg-ch727v2k728iqr28s9ag-a.oregon-postgres.render.com/test_y49s
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 2}
    PWD_HASH_SALT = b'234234fewdfdcdwcqed3efqefqewqfdcdc'
    PWD_HASH_ITERATIONS = 100_000
    JWT_SECRET = "wf3r2r23f3f23f3"
    JWT_ALGORITHM = "HS256"
