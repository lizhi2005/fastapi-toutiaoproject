from passlib.context import CryptContext

# 创建密码加密上下文，指定使用 bcrypt 算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 对明文密码进行加密，返回加密后的哈希密码
def get_hash_password(password: str):
    return pwd_context.hash(password)

# 验证明文密码与哈希密码是否匹配，返回布尔值
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)