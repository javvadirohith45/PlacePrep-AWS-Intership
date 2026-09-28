from flask import Blueprint,render_template,redirect,url_for,abort
from flask_login import login_required,current_user
from extensions import db
from models.content import Company,CompanyAssessment,CompanyAssessmentQuestion,Question,Test,TestQuestion
companies_bp=Blueprint('companies',__name__,url_prefix='/companies')
@companies_bp.route('')
def index(): return render_template('companies/index.html',companies=Company.query.order_by(Company.name).all())
@companies_bp.route('/<int:company_id>')
def detail(company_id): return render_template('companies/detail.html',company=Company.query.get_or_404(company_id))
@companies_bp.route('/<int:company_id>/assessments')
def assessments(company_id):
    c=Company.query.get_or_404(company_id); return render_template('companies/assessments.html',company=c,assessments=c.assessments)
@companies_bp.route('/<int:company_id>/assessment/<int:assessment_id>')
@login_required
def assessment(company_id,assessment_id):
    c=Company.query.get_or_404(company_id); a=CompanyAssessment.query.filter_by(id=assessment_id,company_id=c.id).first_or_404()
    # Build a real test only from questions explicitly mapped to this company assessment.
    title=f'{c.name} — {a.topic} Assessment'
    test=Test.query.filter_by(title=title,company_id=c.id,topic_id=None).first()
    if not test:
        test=Test(title=title,company_id=c.id,category='Company Assessment',difficulty='Medium',duration_minutes=60,published=True,instructions=f'60-minute {a.topic} assessment for {c.name}. Questions must be explicitly mapped to this assessment.');db.session.add(test);db.session.flush()
        mapped=CompanyAssessmentQuestion.query.filter_by(assessment_id=a.id).order_by(CompanyAssessmentQuestion.position).all()
        for i,m in enumerate(mapped,1):db.session.add(TestQuestion(test=test,question=m.question,position=i))
        db.session.commit()
    if len(test.questions)==0:
        return render_template('companies/assessment_empty.html',company=c,assessment=a)
    return redirect(url_for('mock.detail',test_id=test.id))
