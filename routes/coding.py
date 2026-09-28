from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, request, abort, redirect, url_for
from flask_login import login_required, current_user
from models.content import CodingProblem, CodingLanguage, CodingSubmission, CodingProgress
from services.code_runner import run_test_cases
from extensions import db

coding_bp = Blueprint('coding', __name__, url_prefix='/coding')


def _language_or_404(slug):
    return CodingLanguage.query.filter_by(slug=slug).first_or_404()


def _user_progress_map():
    if not current_user.is_authenticated:
        return {}
    rows = CodingProgress.query.filter_by(user_id=current_user.id).all()
    return {r.problem_id: r.status for r in rows}


def _save_attempt(problem, language, code, result):
    if not current_user.is_authenticated:
        return
    status = result.get('status', 'error')
    total = int(result.get('total') or len(result.get('tests') or []))
    passed = int(result.get('passed') or sum(1 for t in result.get('tests', []) if t.get('passed')))
    db.session.add(CodingSubmission(
        user_id=current_user.id,
        problem_id=problem.id,
        language=language,
        code=code,
        status=status,
        runtime_ms=int(result.get('runtime_ms') or 0),
        memory_mb=float(result.get('memory_mb') or 0),
        passed=passed,
        total=total,
    ))
    progress = CodingProgress.query.filter_by(
        user_id=current_user.id, problem_id=problem.id
    ).first()
    if not progress:
        progress = CodingProgress(user_id=current_user.id, problem_id=problem.id)
        db.session.add(progress)
    progress.attempts = (progress.attempts or 0) + 1
    progress.last_runtime_ms = int(result.get('runtime_ms') or 0)
    if status == 'accepted':
        progress.status = 'solved'
    elif progress.status != 'solved':
        progress.status = 'attempted'
    db.session.commit()


@coding_bp.route('')
def index():
    languages = CodingLanguage.query.order_by(CodingLanguage.id).all()
    total = CodingProblem.query.count()
    return render_template('coding/index.html', languages=languages, total_problems=total)


@coding_bp.route('/dashboard')
@login_required
def dashboard():
    problems = CodingProblem.query.all()
    progress = CodingProgress.query.filter_by(user_id=current_user.id).all()
    submissions = CodingSubmission.query.filter_by(user_id=current_user.id).order_by(
        CodingSubmission.created_at.desc()
    ).limit(20).all()
    solved_ids = {p.problem_id for p in progress if p.status == 'solved'}
    attempted_ids = {p.problem_id for p in progress}
    easy = sum(1 for p in problems if p.id in solved_ids and p.difficulty == 'Easy')
    medium = sum(1 for p in problems if p.id in solved_ids and p.difficulty == 'Medium')
    hard = sum(1 for p in problems if p.id in solved_ids and p.difficulty == 'Hard')
    all_submissions = CodingSubmission.query.filter_by(user_id=current_user.id).all()
    accepted = sum(1 for s in all_submissions if s.status == 'accepted')
    total_submissions = len(all_submissions)
    total_passed = sum(s.passed or 0 for s in all_submissions)
    total_tests = sum(s.total or 0 for s in all_submissions)
    accuracy = round((total_passed / total_tests) * 100, 1) if total_tests else 0
    days = sorted({s.created_at.date() for s in all_submissions if s.created_at}, reverse=True)
    streak = 0
    cursor = datetime.utcnow().date()
    if days and days[0] == cursor:
        for d in days:
            if d == cursor - timedelta(days=streak):
                streak += 1
            else:
                break
    elif days and days[0] == cursor - timedelta(days=1):
        cursor = cursor - timedelta(days=1)
        for d in days:
            if d == cursor - timedelta(days=streak):
                streak += 1
            else:
                break
    topic_progress = {}
    for p in problems:
        topic = (p.tags.split(',')[0].strip() if p.tags else 'General')
        topic_progress.setdefault(topic, {'total': 0, 'solved': 0})
        topic_progress[topic]['total'] += 1
        if p.id in solved_ids:
            topic_progress[topic]['solved'] += 1
    return render_template(
        'coding/dashboard.html',
        total=len(problems), solved=len(solved_ids),
        attempted=len(attempted_ids), unsolved=max(0, len(problems)-len(attempted_ids)),
        easy=easy, medium=medium, hard=hard, streak=streak,
        accuracy=accuracy, total_submissions=total_submissions,
        accepted=accepted, coding_time=sum(s.runtime_ms or 0 for s in all_submissions),
        submissions=submissions, topic_progress=topic_progress,
    )


@coding_bp.route('/language/<slug>')
def language(slug):
    lang = _language_or_404(slug)
    problems = CodingProblem.query.filter_by(language_id=lang.id).order_by(CodingProblem.id).all()
    progress = _user_progress_map()
    return render_template('coding/language.html', language=lang, problems=problems, progress=progress)


@coding_bp.route('/problems')
def problems():
    query = request.args.get('q', '').strip()
    difficulty = request.args.get('difficulty', 'all')
    topic = request.args.get('topic', 'all')
    status = request.args.get('status', 'all')
    level = request.args.get('level', 'all')
    category = request.args.get('category', 'all')
    page = max(1, request.args.get('page', 1, type=int))
    per_page = 24
    q = CodingProblem.query
    if query:
        like = f"%{query}%"
        from sqlalchemy import or_
        q = q.filter(or_(
            CodingProblem.title.ilike(like),
            CodingProblem.description.ilike(like),
            CodingProblem.tags.ilike(like)
        ))
    if difficulty != 'all':
        q = q.filter_by(difficulty=difficulty)
    if topic != 'all':
        q = q.filter(CodingProblem.tags.ilike(f"%{topic}%"))
    if level != 'all':
        q = q.filter_by(placement_level=level)
    if category != 'all':
        q = q.filter_by(category=category)
    progress = _user_progress_map()
    if status != 'all':
        ids = {pid for pid, st in progress.items() if (status == 'solved' and st == 'solved') or (status == 'attempted' and st == 'attempted')}
        if status in ('solved', 'attempted'):
            q = q.filter(CodingProblem.id.in_(ids)) if ids else q.filter(CodingProblem.id == -1)
        elif status == 'unsolved':
            q = q.filter(~CodingProblem.id.in_(set(progress))) if progress else q
    items = q.order_by(CodingProblem.id).paginate(page=page, per_page=per_page, error_out=False)
    all_db = CodingProblem.query.all()
    topics = sorted({(p.tags.split(',')[0].strip() if p.tags else 'General') for p in all_db})
    categories = sorted({p.category or 'General Placement' for p in all_db})
    return render_template('coding/problems.html', problems=items.items, pagination=items,
                           topics=topics, progress=progress, query=query,
                           difficulty=difficulty, topic=topic, status=status, level=level,
                           category=category, categories=categories)


@coding_bp.route('/<int:problem_id>')
def problem(problem_id):
    p = CodingProblem.query.get_or_404(problem_id)
    if not p.language:
        abort(404)
    siblings = CodingProblem.query.filter_by(language_id=p.language_id).order_by(CodingProblem.id).all()
    idx = next((i for i, item in enumerate(siblings) if item.id == p.id), 0)
    previous = siblings[idx - 1] if idx > 0 else None
    following = siblings[idx + 1] if idx + 1 < len(siblings) else None
    random_problem = siblings[(idx * 37 + 11) % len(siblings)] if siblings else None
    progress = CodingProgress.query.filter_by(user_id=current_user.id, problem_id=p.id).first() if current_user.is_authenticated else None
    attempted = bool(progress)
    return render_template('coding/problem.html', problem=p, previous=previous, following=following,
                           random_problem=random_problem, progress=progress, attempted=attempted, languages=CodingLanguage.query.order_by(CodingLanguage.id).all())



@coding_bp.route('/switch/<int:problem_id>/<slug>')
def switch_language(problem_id, slug):
    source = CodingProblem.query.get_or_404(problem_id)
    lang = _language_or_404(slug)
    base_title = source.title.split(' · ', 1)[-1]
    target = CodingProblem.query.filter_by(language_id=lang.id, title=f'{lang.name} · {base_title}').first()
    if target:
        return render_template('coding/problem.html', problem=target, previous=None, following=None,
                               random_problem=None, progress=None, attempted=False, languages=CodingLanguage.query.order_by(CodingLanguage.id).all())
    return redirect(url_for('coding.language', slug=slug))


def _run(problem_id, submit=False):
    problem = CodingProblem.query.get_or_404(problem_id)
    data = request.get_json(silent=True) or {}
    code = (data.get('code') or '').strip()
    if not code:
        return jsonify({'status': 'error', 'message': 'Write code before running.'}), 400
    language = problem.language.slug
    cases = sorted(problem.test_cases, key=lambda c: (c.hidden, c.id))
    if not submit:
        cases = [c for c in cases if not c.hidden]
    payload = [{'input': c.input or '', 'expected': c.expected_output or '', 'hidden': c.hidden} for c in cases]
    if not payload:
        return jsonify({'status': 'error', 'message': 'No test cases are configured for this problem.'}), 409
    result = run_test_cases(language, code, payload, timeout=max(2, int((problem.time_limit_ms or 2000) / 1000) + 1))
    result['mode'] = 'submit' if submit else 'run'
    result['problem_id'] = problem.id
    result['difficulty'] = problem.difficulty
    result['memory_mb'] = float(result.get('memory_mb') or problem.memory_limit_mb or 0)
    if result.get('status') not in {'unconfigured', 'unsupported'}:
        _save_attempt(problem, language, code, result)
    return jsonify(result)


@coding_bp.route('/<int:problem_id>/run', methods=['POST'])
@login_required
def run(problem_id):
    return _run(problem_id, submit=False)


@coding_bp.route('/<int:problem_id>/submit', methods=['POST'])
@login_required
def submit(problem_id):
    return _run(problem_id, submit=True)


@coding_bp.route('/<int:problem_id>/custom-test', methods=['POST'])
@login_required
def custom_test(problem_id):
    problem = CodingProblem.query.get_or_404(problem_id)
    data = request.get_json(silent=True) or {}
    code = (data.get('code') or '').strip()
    test_input = data.get('input') or ''
    if not code:
        return jsonify({'status': 'error', 'message': 'Write code before running a custom test.'}), 400
    result = run_test_cases(problem.language.slug, code, [{'input': test_input, 'expected': '', 'hidden': False}],
                            timeout=max(2, int((problem.time_limit_ms or 2000) / 1000) + 1))
    # Custom tests are execution diagnostics, not accepted submissions.
    if result.get('tests'):
        t = result['tests'][0]
        result['custom_output'] = t.get('actual', '')
        result['custom_error'] = t.get('stderr', '') or t.get('message', '')
        result['status'] = 'custom_completed' if t.get('status') == 'passed' else t.get('status', 'error')
        result['message'] = 'Custom test executed' if t.get('status') == 'passed' else (t.get('message') or 'Custom test failed')
    return jsonify(result)


@coding_bp.route('/api/problems')
def api_problems():
    items = CodingProblem.query.order_by(CodingProblem.id).all()
    return jsonify([{
        'id': p.id, 'title': p.title, 'difficulty': p.difficulty,
        'topic': p.tags, 'language': p.language.slug if p.language else None
    } for p in items])


@coding_bp.route('/api/problems/<int:problem_id>')
def api_problem(problem_id):
    p = CodingProblem.query.get_or_404(problem_id)
    return jsonify({
        'id': p.id, 'title': p.title, 'difficulty': p.difficulty,
        'description': p.description, 'input_format': p.input_format,
        'output_format': p.output_format, 'constraints': p.constraints,
        'examples': p.examples, 'starter_code': p.starter_code,
        'language': p.language.slug if p.language else None,
        'tags': p.tags
    })


@coding_bp.route('/api/coding/problems')
def api_coding_problems():
    return api_problems()


@coding_bp.route('/api/coding/problems/<int:problem_id>')
def api_coding_problem(problem_id):
    return api_problem(problem_id)


@coding_bp.route('/api/coding/progress')
@login_required
def api_coding_progress():
    return api_progress()


@coding_bp.route('/api/coding/submissions')
@login_required
def api_coding_submissions():
    return api_submissions()


@coding_bp.route('/api/progress')
@login_required
def api_progress():
    rows = CodingProgress.query.filter_by(user_id=current_user.id).all()
    return jsonify({'solved': [r.problem_id for r in rows if r.status == 'solved'],
                    'attempted': [r.problem_id for r in rows if r.status == 'attempted']})


@coding_bp.route('/api/submissions')
@login_required
def api_submissions():
    rows = CodingSubmission.query.filter_by(user_id=current_user.id).order_by(CodingSubmission.created_at.desc()).limit(100).all()
    return jsonify([{
        'id': s.id, 'problem_id': s.problem_id, 'problem': s.problem.title,
        'language': s.language, 'status': s.status, 'runtime_ms': s.runtime_ms,
        'memory_mb': s.memory_mb, 'passed': s.passed, 'total': s.total,
        'created_at': s.created_at.isoformat() if s.created_at else None
    } for s in rows])
