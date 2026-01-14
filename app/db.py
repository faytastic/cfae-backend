import os
import oracledb


def get_connection():
    wallet_dir = os.getenv("CFAEATP_WALLET_DIR", "/home/opc/wallets/cfae-atp")
    admin_password = os.getenv("CFAEATP_ADMIN_PASSWORD")

    if not admin_password:
        raise RuntimeError("Missing env var: CFAEATP_ADMIN_PASSWORD")

    dsn = os.getenv("CFAEATP_DSN", "cfaeatp_high")

    return oracledb.connect(
        user="ADMIN",
        password=admin_password,
        dsn=dsn,
        config_dir=wallet_dir,
        wallet_location=wallet_dir,
        wallet_password=admin_password,
    )
