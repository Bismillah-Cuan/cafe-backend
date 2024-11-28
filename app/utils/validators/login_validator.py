from pydantic import BaseModel, FieldValidationInfo, field_validator
import re

class LoginValidator(BaseModel):
    username: str
    password: str
    
    @field_validator('password')
    def validate_password(cls, password: str, info: FieldValidationInfo):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one number.')
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter.')
        return password