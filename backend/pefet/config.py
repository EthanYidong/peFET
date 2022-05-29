import secrets

class Configuration():
  DATABASE='pefet.db'
  JWT_SECRET=secrets.token_bytes(64)