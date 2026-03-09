from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str = "admin"
    db_password: str = "secret"
    db_dsn: str = "mydb_high"           # TNS alias from tnsnames.ora in the wallet
    wallet_dir: str = "/path/to/wallet" # directory containing cwallet.sso, tnsnames.ora, etc.
    wallet_password: str = ""           # only required for PKCS12 (.p12) wallets; leave blank for SSO

    model_config = {"env_file": ".env", "env_prefix": "ORACLE_"}


settings = Settings()
