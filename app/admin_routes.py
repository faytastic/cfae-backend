from flask import Blueprint, render_template
from app.db import get_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/submissions", methods=["GET"])
def submissions():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, created_at
        FROM cfae_contacts
        ORDER BY created_at DESC
        FETCH FIRST 50 ROWS ONLY
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("submissions.html", rows=rows)
