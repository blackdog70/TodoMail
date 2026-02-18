from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect,
    url_for,
    jsonify,
)
from flask_login import login_required, current_user
from .auth import users
from .i18n import translations

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('index.html')


@bp.route('/set_language/<lang>')
def set_language(lang: str):
    if lang in translations:
        session['lang'] = lang
        if current_user.is_authenticated and current_user.id in users:
            users[current_user.id]['language'] = lang
    return redirect(request.referrer or url_for('main.index'))


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = users[current_user.id]
    servers = user.setdefault('mail_servers', [])
    if request.method == 'POST':
        servers.append(
            {
                'protocol': request.form.get('protocol', 'imap'),
                'server': request.form.get('server', ''),
                'port': request.form.get('port', ''),
                'username': request.form.get('username', ''),
                'password': request.form.get('password', ''),
            }
        )
        return redirect(url_for('main.settings'))
    return render_template('settings.html', servers=servers)


@bp.route('/test_mail', methods=['POST'])
@login_required
def test_mail():
    data = request.get_json() or {}
    server = data.get('server')
    port = int(data.get('port', 0))
    username = data.get('username')
    password = data.get('password')
    protocol = data.get('protocol', 'imap')

    success = True
    try:
        if protocol == 'imap':
            import imaplib
            with imaplib.IMAP4(server, port) as imap:
                if username and password:
                    imap.login(username, password)
        elif protocol == 'pop3':
            import poplib
            with poplib.POP3(server, port, timeout=5) as pop:
                if username and password:
                    pop.user(username)
                    pop.pass_(password)
        else:
            success = False
    except Exception:
        success = False
    return jsonify({'success': success})
