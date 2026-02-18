from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import db

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/activities')
@login_required
def activities():
    conn = db.get_db()
    with conn.cursor() as cur:
        cur.execute("""
          SELECT * FROM activity
          WHERE user_id=%s ORDER BY timestamp DESC
        """, (current_user.id,))
        history = cur.fetchall()
    return render_template('activity.html', activities=history)

@activity_bp.route('/activity/<int:activity_id>')
@login_required
def activity_detail(activity_id):
    conn = db.get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        activity = cur.fetchone()

    # If user clicked a doctor/product link:
    doc_id  = request.args.get('doctor_id')
    prod_id = request.args.get('product_id')
    if doc_id or prod_id:
        with conn.cursor() as cur:
            if doc_id:
                cur.execute("UPDATE activity SET doctor_id=%s WHERE id=%s",
                            (int(doc_id), activity_id))
            if prod_id:
                cur.execute("UPDATE activity SET product_id=%s WHERE id=%s",
                            (int(prod_id), activity_id))
        conn.commit()
        return redirect(url_for('activity.activity_detail', activity_id=activity_id))

    return render_template('activity_detail.html', activity=activity)
