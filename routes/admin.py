from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from extensions import db
from models.content import (
    Category, Topic, TopicContent, Question, QuestionOption,
    Company, RecruitmentLink, CompanyAssessment, CompanyAssessmentQuestion,
    ModelPaper, Test, TestQuestion, TestAttempt, AttemptAnswer, Bookmark,
    UserProgress, CodingLanguage, CodingProblem, CodingTestCase,
    DSAProblem, InterviewQuestion, Achievement, UserAchievement, Resume,
    CodingSubmission, CodingProgress,
)
from models.user import User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.app_context_processor
def admin_template_helpers():
    return {'_field_value': _field_value, '_display_value': _display_value, 'relation_choices': _relation_choices}


def admin_required(f):
    @wraps(f)
    @login_required
    def w(*a, **k):
        if current_user.role != 'admin':
            abort(403)
        return f(*a, **k)
    return w


# ---------------------------------------------------------------------------
# Admin resource registry. These are the database-backed parts of PlacePrep
# that an administrator can manage from the browser without editing code.
# ---------------------------------------------------------------------------

def _choices(model, label_attr='name'):
    return [(x.id, getattr(x, label_attr, str(x.id))) for x in model.query.order_by(model.id).all()]


RESOURCE_CONFIG = {
    'categories': {
        'title': 'Categories', 'icon': 'layers', 'model': Category,
        'fields': [
            ('name', 'Name', 'text', True),
            ('kind', 'Type', 'select', True, [('aptitude','Aptitude'), ('reasoning','Reasoning'), ('general','General')]),
        ],
        'columns': ['id', 'name', 'kind'],
    },
    'topics': {
        'title': 'Topics', 'icon': 'book-open', 'model': Topic,
        'fields': [
            ('name', 'Name', 'text', True), ('slug', 'Slug', 'text', True),
            ('category_id', 'Category', 'relation', False, Category),
            ('description', 'Description', 'textarea', False),
        ], 'columns': ['id', 'name', 'slug', 'category_id'],
    },
    'topic-content': {
        'title': 'Topic Content', 'icon': 'file-text', 'model': TopicContent,
        'fields': [
            ('topic_id', 'Topic', 'relation_unique', True, Topic),
            ('introduction', 'Introduction', 'textarea', False),
            ('concepts', 'Basic Concepts', 'textarea', False),
            ('formulas', 'Important Formulas', 'textarea', False),
            ('shortcuts', 'Short Tricks & Logic', 'textarea', False),
            ('examples', 'Solved Examples', 'textarea', False),
            ('placement_notes', 'Placement Questions / Notes', 'textarea', False),
            ('faq', 'FAQ', 'textarea', False),
        ], 'columns': ['id', 'topic_id'],
    },
    'questions': {
        'title': 'Practice Questions', 'icon': 'circle-help', 'model': Question,
        'fields': [
            ('question', 'Question', 'textarea', True), ('explanation', 'Explanation', 'textarea', False),
            ('category_id', 'Category', 'relation', False, Category), ('topic_id', 'Topic', 'relation', False, Topic),
            ('difficulty', 'Difficulty', 'select', True, [('Easy','Easy'),('Medium','Medium'),('Hard','Hard')]),
            ('correct_answer', 'Correct Answer', 'select', True, [('A','A'),('B','B'),('C','C'),('D','D')]),
            ('tags', 'Tags', 'text', False), ('active', 'Published / Active', 'checkbox', False),
            ('option_A', 'Option A', 'text', False), ('option_B', 'Option B', 'text', False),
            ('option_C', 'Option C', 'text', False), ('option_D', 'Option D', 'text', False),
        ], 'columns': ['id','question','difficulty','correct_answer','active','topic_id'],
    },
    'companies': {
        'title': 'Companies', 'icon': 'building-2', 'model': Company,
        'fields': [
            ('name','Company Name','text',True), ('logo','Logo URL / Icon','text',False),
            ('overview','Overview','textarea',False), ('eligibility','Eligibility','textarea',False),
            ('pattern','Selection Pattern','textarea',False), ('stages','Stages','textarea',False),
        ], 'columns': ['id','name','pattern'],
    },
    'recruitment-links': {
        'title': 'Recruitment Links', 'icon': 'external-link', 'model': RecruitmentLink,
        'fields': [('company_id','Company','relation_unique',True,Company),('url','URL','url',True),('label','Label','text',False),('verified_at','Verified At','datetime',False)],
        'columns': ['id','company_id','url','label'],
    },
    'company-assessments': {
        'title': 'Company Assessments', 'icon': 'clipboard-check', 'model': CompanyAssessment,
        'fields': [('company_id','Company','relation',True,Company),('title','Title','text',True),('topic','Topic','text',False),('duration_minutes','Duration (minutes)','number',False),('description','Description','textarea',False)],
        'columns': ['id','company_id','title','topic','duration_minutes'],
    },
    'assessment-questions': {
        'title': 'Assessment Question Mapping', 'icon': 'list-plus', 'model': CompanyAssessmentQuestion,
        'fields': [('assessment_id','Assessment','relation',True,CompanyAssessment),('question_id','Question','relation',True,Question),('position','Position','number',False)],
        'columns': ['id','assessment_id','question_id','position'],
    },
    'model-papers': {
        'title': 'Company Model Papers', 'icon': 'files', 'model': ModelPaper,
        'fields': [('company_id','Company','relation',True,Company),('title','Title','text',True),('status','Status','select',True,[('Published','Published'),('Coming Soon','Coming Soon'),('Draft','Draft')])],
        'columns': ['id','company_id','title','status'],
    },
    'tests': {
        'title': 'Mock Tests', 'icon': 'timer', 'model': Test,
        'fields': [('title','Title','text',True),('company_id','Company','relation',False,Company),('category','Category','text',False),('topic_id','Topic','relation',False,Topic),('difficulty','Difficulty','select',False,[('Easy','Easy'),('Medium','Medium'),('Hard','Hard')]),('duration_minutes','Duration (minutes)','number',False),('published','Published','checkbox',False),('instructions','Instructions','textarea',False)],
        'columns': ['id','title','category','difficulty','duration_minutes','published'],
    },
    'test-questions': {
        'title': 'Mock Test Question Mapping', 'icon': 'list-checks', 'model': TestQuestion,
        'fields': [('test_id','Test','relation',True,Test),('question_id','Question','relation',True,Question),('position','Position','number',False)],
        'columns': ['id','test_id','question_id','position'],
    },
    'coding-languages': {
        'title': 'Coding Languages', 'icon': 'code-2', 'model': CodingLanguage,
        'fields': [('name','Name','text',True),('slug','Slug','text',True),('icon','Icon','text',False),('problem_count','Problem Count','number',False)],
        'columns': ['id','name','slug','problem_count'],
    },
    'coding-problems': {
        'title': 'Coding Problems', 'icon': 'terminal-square', 'model': CodingProblem,
        'fields': [('title','Title','text',True),('difficulty','Difficulty','select',True,[('Easy','Easy'),('Medium','Medium'),('Hard','Hard')]),('description','Description','textarea',True),('starter_code','Starter Code','textarea',False),('tags','Tags','text',False),('language_id','Language','relation',False,CodingLanguage),('category','Category','text',False),('placement_level','Placement Level','select',False,[('Basic','Basic'),('Intermediate','Intermediate'),('Advanced','Advanced')]),('input_format','Input Format','textarea',False),('output_format','Output Format','textarea',False),('constraints','Constraints','textarea',False),('examples','Examples','textarea',False),('solution_reference','Solution Reference','textarea',False),('time_limit_ms','Time Limit (ms)','number',False),('memory_limit_mb','Memory Limit (MB)','number',False)],
        'columns': ['id','title','difficulty','category','placement_level','language_id'],
    },
    'coding-test-cases': {
        'title': 'Coding Test Cases', 'icon': 'test-tube-2', 'model': CodingTestCase,
        'fields': [('problem_id','Coding Problem','relation',True,CodingProblem),('input','Input','textarea',False),('expected_output','Expected Output','textarea',False),('hidden','Hidden Test Case','checkbox',False)],
        'columns': ['id','problem_id','hidden','expected_output'],
    },
    'dsa-problems': {
        'title': 'DSA Problems', 'icon': 'binary', 'model': DSAProblem,
        'fields': [('title','Title','text',True),('category','Category','text',False),('difficulty','Difficulty','select',False,[('Easy','Easy'),('Medium','Medium'),('Hard','Hard')]),('statement','Problem Statement','textarea',True),('examples','Examples','textarea',False),('explanation','Explanation','textarea',False),('approach','Approach','textarea',False),('complexity','Complexity','text',False),('tags','Tags','text',False)],
        'columns': ['id','title','category','difficulty'],
    },
    'interview-questions': {
        'title': 'Interview Questions', 'icon': 'messages-square', 'model': InterviewQuestion,
        'fields': [('category','Category','select',True,[('HR','HR'),('Technical','Technical')]),('topic','Topic','text',False),('question','Question','textarea',True),('interviewer_checking','What Interviewer Checks','textarea',False),('how_to_answer','How To Answer','textarea',False),('sample_answer','Sample Answer','textarea',False),('follow_up','Follow-up','textarea',False),('company','Company','text',False)],
        'columns': ['id','category','topic','question','company'],
    },
    'achievements': {
        'title': 'Achievements', 'icon': 'trophy', 'model': Achievement,
        'fields': [('name','Name','text',True),('description','Description','textarea',False),('xp','XP','number',False)],
        'columns': ['id','name','xp'],
    },
    'users': {
        'title': 'Users & Admins', 'icon': 'users', 'model': User,
        'fields': [('name','Name','text',True),('email','Email','email',True),('password','Password','password',False),('role','Role','select',True,[('student','Student'),('admin','Administrator')]),('xp','XP','number',False),('streak','Streak','number',False)],
        'columns': ['id','name','email','role','xp','streak','created_at'],
    },
}

# Human-friendly grouping for the full-control console.
RESOURCE_GROUPS = [
    ('Learning Content', ['categories','topics','topic-content','questions']),
    ('Companies & Assessments', ['companies','recruitment-links','company-assessments','assessment-questions','model-papers']),
    ('Tests', ['tests','test-questions']),
    ('Coding Arena', ['coding-languages','coding-problems','coding-test-cases']),
    ('Career Preparation', ['dsa-problems','interview-questions','achievements']),
    ('Platform Administration', ['users']),
]


def _display_value(obj, field):
    value = getattr(obj, field, '')
    if field.endswith('_id') and value is not None:
        return str(value)
    if isinstance(value, bool):
        return 'Yes' if value else 'No'
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M')
    text = '' if value is None else str(value)
    return text if len(text) <= 90 else text[:87] + '…'


def _relation_choices(model):
    rows = model.query.order_by(model.id).all()
    if model is Question:
        return [(x.id, f'#{x.id} · {x.question[:70]}') for x in rows]
    if model is Test:
        return [(x.id, f'#{x.id} · {x.title}') for x in rows]
    if model is CompanyAssessment:
        return [(x.id, f'#{x.id} · {x.title}') for x in rows]
    if model is CodingProblem:
        return [(x.id, f'#{x.id} · {x.title}') for x in rows]
    if model is Topic:
        return [(x.id, f'#{x.id} · {x.name}') for x in rows]
    return [(x.id, getattr(x, 'name', getattr(x, 'title', f'#{x.id}'))) for x in rows]


def _field_value(field, obj):
    name, *_ = field
    if name == 'password':
        return ''
    if name.startswith('option_') and isinstance(obj, Question):
        label = name[-1]
        option = next((o for o in obj.options if o.label == label), None)
        return option.text if option else ''
    return getattr(obj, name, '')


def _save_resource(cfg, obj=None):
    model = cfg['model']
    if obj is None:
        obj = model()
        db.session.add(obj)
    for field in cfg['fields']:
        name, label, ftype, required, *extra = field
        raw = request.form.get(name, '')
        if name == 'password' and not raw:
            continue
        if ftype in ('relation','relation_unique'):
            setattr(obj, name, int(raw) if raw else None)
        elif ftype == 'number':
            setattr(obj, name, int(raw) if raw not in ('', None) else 0)
        elif ftype == 'checkbox':
            setattr(obj, name, request.form.get(name) == 'on')
        elif ftype == 'datetime':
            if raw:
                try: setattr(obj, name, datetime.fromisoformat(raw))
                except ValueError: setattr(obj, name, datetime.utcnow())
        elif name == 'password':
            obj.password_hash = generate_password_hash(raw)
        elif hasattr(obj, name):
            setattr(obj, name, raw)
    db.session.flush()
    if isinstance(obj, Question):
        for label in 'ABCD':
            text = request.form.get(f'option_{label}', '').strip()
            option = next((o for o in obj.options if o.label == label), None)
            if text:
                if option: option.text = text
                else: db.session.add(QuestionOption(question=obj, label=label, text=text))
            elif option:
                db.session.delete(option)
    db.session.commit()
    return obj


@admin_bp.route('')
@admin_required
def index():
    return render_template(
        'admin/index.html',
        users_count=User.query.count(),
        questions=Question.query.count(),
        tests=Test.query.count(),
        companies=Company.query.count(),
        coding=CodingProblem.query.count(),
        dsa=DSAProblem.query.count(),
        interviews=InterviewQuestion.query.count(),
        resources=RESOURCE_CONFIG,
        groups=RESOURCE_GROUPS,
    )


@admin_bp.route('/manage/<resource>', methods=['GET', 'POST'])
@admin_required
def manage(resource):
    cfg = RESOURCE_CONFIG.get(resource)
    if not cfg:
        abort(404)
    if request.method == 'POST':
        try:
            obj = _save_resource(cfg)
            flash(f'{cfg["title"][:-1] if cfg["title"].endswith("s") else cfg["title"]} created successfully.', 'success')
            return redirect(url_for('admin.manage', resource=resource, edit=obj.id))
        except (ValueError, TypeError, IntegrityError) as exc:
            db.session.rollback()
            flash(f'Could not save this item. Check required fields and duplicate values. {exc}', 'error')
    objects = cfg['model'].query.order_by(cfg['model'].id.desc()).all()
    edit_id = request.args.get('edit', type=int)
    edit_obj = cfg['model'].query.get(edit_id) if edit_id else None
    return render_template('admin/manage.html', resource=resource, cfg=cfg, objects=objects, edit_obj=edit_obj, groups=RESOURCE_GROUPS, resources=RESOURCE_CONFIG, relation_cache={})


@admin_bp.route('/manage/<resource>/edit/<int:item_id>', methods=['POST'])
@admin_required
def edit_resource(resource, item_id):
    cfg = RESOURCE_CONFIG.get(resource)
    if not cfg: abort(404)
    obj = cfg['model'].query.get_or_404(item_id)
    try:
        _save_resource(cfg, obj)
        flash(f'{cfg["title"][:-1] if cfg["title"].endswith("s") else cfg["title"]} updated successfully.', 'success')
    except (ValueError, TypeError, IntegrityError) as exc:
        db.session.rollback()
        flash(f'Could not update this item. {exc}', 'error')
    return redirect(url_for('admin.manage', resource=resource, edit=item_id))


@admin_bp.route('/manage/<resource>/delete/<int:item_id>', methods=['POST'])
@admin_required
def delete_resource(resource, item_id):
    cfg = RESOURCE_CONFIG.get(resource)
    if not cfg: abort(404)
    obj = cfg['model'].query.get_or_404(item_id)
    try:
        # Explicit dependency cleanup makes the Delete button genuinely useful
        # for an administrator while keeping unrelated content intact.
        if isinstance(obj, User):
            TestAttempt.query.filter_by(user_id=obj.id).delete(synchronize_session=False)
            CodingSubmission.query.filter_by(user_id=obj.id).delete(synchronize_session=False)
            CodingProgress.query.filter_by(user_id=obj.id).delete(synchronize_session=False)
            Bookmark.query.filter_by(user_id=obj.id).delete(synchronize_session=False)
            UserProgress.query.filter_by(user_id=obj.id).delete(synchronize_session=False)
            UserAchievement.query.filter_by(user_id=obj.id).delete(synchronize_session=False)
            Resume.query.filter_by(user_id=obj.id).delete(synchronize_session=False)
        elif isinstance(obj, Question):
            QuestionOption.query.filter_by(question_id=obj.id).delete(synchronize_session=False)
            TestQuestion.query.filter_by(question_id=obj.id).delete(synchronize_session=False)
            CompanyAssessmentQuestion.query.filter_by(question_id=obj.id).delete(synchronize_session=False)
            AttemptAnswer.query.filter_by(question_id=obj.id).delete(synchronize_session=False)
            Bookmark.query.filter_by(question_id=obj.id).delete(synchronize_session=False)
        elif isinstance(obj, Topic):
            TopicContent.query.filter_by(topic_id=obj.id).delete(synchronize_session=False)
            UserProgress.query.filter_by(topic_id=obj.id).delete(synchronize_session=False)
            Question.query.filter_by(topic_id=obj.id).update({'topic_id': None}, synchronize_session=False)
            Test.query.filter_by(topic_id=obj.id).update({'topic_id': None}, synchronize_session=False)
        elif isinstance(obj, Category):
            Topic.query.filter_by(category_id=obj.id).update({'category_id': None}, synchronize_session=False)
            Question.query.filter_by(category_id=obj.id).update({'category_id': None}, synchronize_session=False)
        elif isinstance(obj, Company):
            RecruitmentLink.query.filter_by(company_id=obj.id).delete(synchronize_session=False)
            assessments = CompanyAssessment.query.filter_by(company_id=obj.id).all()
            for a in assessments:
                CompanyAssessmentQuestion.query.filter_by(assessment_id=a.id).delete(synchronize_session=False)
            CompanyAssessment.query.filter_by(company_id=obj.id).delete(synchronize_session=False)
            ModelPaper.query.filter_by(company_id=obj.id).delete(synchronize_session=False)
            Test.query.filter_by(company_id=obj.id).update({'company_id': None}, synchronize_session=False)
        elif isinstance(obj, CompanyAssessment):
            CompanyAssessmentQuestion.query.filter_by(assessment_id=obj.id).delete(synchronize_session=False)
        elif isinstance(obj, Test):
            attempts = TestAttempt.query.filter_by(test_id=obj.id).all()
            for a in attempts:
                AttemptAnswer.query.filter_by(attempt_id=a.id).delete(synchronize_session=False)
            TestAttempt.query.filter_by(test_id=obj.id).delete(synchronize_session=False)
            TestQuestion.query.filter_by(test_id=obj.id).delete(synchronize_session=False)
        elif isinstance(obj, CodingProblem):
            CodingTestCase.query.filter_by(problem_id=obj.id).delete(synchronize_session=False)
            CodingSubmission.query.filter_by(problem_id=obj.id).delete(synchronize_session=False)
            CodingProgress.query.filter_by(problem_id=obj.id).delete(synchronize_session=False)
        elif isinstance(obj, CodingLanguage):
            CodingProblem.query.filter_by(language_id=obj.id).update({'language_id': None}, synchronize_session=False)
        elif isinstance(obj, Achievement):
            UserAchievement.query.filter_by(achievement_id=obj.id).delete(synchronize_session=False)
        db.session.delete(obj)
        db.session.commit()
        flash(f'{cfg["title"][:-1] if cfg["title"].endswith("s") else cfg["title"]} deleted.', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Delete was blocked because other records still depend on this item. Remove the dependent records first.', 'error')
    return redirect(url_for('admin.manage', resource=resource))


# Backward-compatible routes used by the existing UI.
@admin_bp.route('/questions')
@admin_required
def questions():
    return redirect(url_for('admin.manage', resource='questions'))


@admin_bp.route('/questions/new', methods=['POST'])
@admin_required
def new_question():
    return manage('questions')


@admin_bp.route('/companies')
@admin_required
def companies():
    return redirect(url_for('admin.manage', resource='companies'))
