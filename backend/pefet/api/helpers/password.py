from password_validator import PasswordValidator

def validate(password):
  schema = PasswordValidator()

  schema\
    .min(8)\
    .max(40)\
    .has().no().spaces()

  return schema.validate(password)