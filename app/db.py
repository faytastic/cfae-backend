import os
import oracledb


def get_connection():
    dsn = os.getenv("CFAEATP_DSN")
    password = os.getenv("CFAEATP_ADMIN_PASSWORD")
    user = os.getenv("CFAEATP_USER", "ADMIN")

    if not dsn:
        raise RuntimeError("Missing env var: CFAEATP_DSN")
    if not password:
        raise RuntimeError("Missing env var: CFAEATP_ADMIN_PASSWORD")

    # Walletless TLS: do not use config_dir, wallet_location, wallet_password, or TNS aliases.
    return oracledb.connect(
        user=user,
        password=password,
        dsn=dsn,
        ssl_server_dn_match=True,
    )
