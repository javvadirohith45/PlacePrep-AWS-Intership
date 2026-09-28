from datetime import datetime
from extensions import db

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(100),unique=True); kind=db.Column(db.String(50))
class Topic(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(150)); category_id=db.Column(db.Integer,db.ForeignKey('category.id')); slug=db.Column(db.String(160),unique=True); description=db.Column(db.Text,default='')
    category=db.relationship('Category',backref='topics')
class TopicContent(db.Model):
    id=db.Column(db.Integer,primary_key=True); topic_id=db.Column(db.Integer,db.ForeignKey('topic.id'),unique=True); introduction=db.Column(db.Text,default=''); concepts=db.Column(db.Text,default=''); formulas=db.Column(db.Text,default=''); shortcuts=db.Column(db.Text,default=''); examples=db.Column(db.Text,default=''); placement_notes=db.Column(db.Text,default=''); faq=db.Column(db.Text,default='')
    topic=db.relationship('Topic',backref=db.backref('content',uselist=False,cascade='all,delete-orphan'))
class Question(db.Model):
    id=db.Column(db.Integer,primary_key=True); question=db.Column(db.Text,nullable=False); explanation=db.Column(db.Text,default=''); category_id=db.Column(db.Integer,db.ForeignKey('category.id')); topic_id=db.Column(db.Integer,db.ForeignKey('topic.id')); difficulty=db.Column(db.String(20),default='Medium'); correct_answer=db.Column(db.String(10)); tags=db.Column(db.String(500),default=''); active=db.Column(db.Boolean,default=True); created_at=db.Column(db.DateTime,default=datetime.utcnow)
    category=db.relationship('Category'); topic=db.relationship('Topic')
class QuestionOption(db.Model):
    id=db.Column(db.Integer,primary_key=True); question_id=db.Column(db.Integer,db.ForeignKey('question.id')); label=db.Column(db.String(1)); text=db.Column(db.Text); question=db.relationship('Question',backref='options')
class Company(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),unique=True); logo=db.Column(db.String(255),default=''); overview=db.Column(db.Text,default=''); eligibility=db.Column(db.Text,default=''); pattern=db.Column(db.Text,default=''); stages=db.Column(db.Text,default='')
class RecruitmentLink(db.Model):
    id=db.Column(db.Integer,primary_key=True); company_id=db.Column(db.Integer,db.ForeignKey('company.id'),unique=True); url=db.Column(db.String(500)); label=db.Column(db.String(180),default='Official careers / recruitment'); verified_at=db.Column(db.DateTime,default=datetime.utcnow); company=db.relationship('Company',backref=db.backref('recruitment_link',uselist=False,cascade='all,delete-orphan'))
class CompanyAssessment(db.Model):
    id=db.Column(db.Integer,primary_key=True); company_id=db.Column(db.Integer,db.ForeignKey('company.id')); title=db.Column(db.String(180)); topic=db.Column(db.String(150)); duration_minutes=db.Column(db.Integer,default=60); description=db.Column(db.Text,default=''); company=db.relationship('Company',backref='assessments')
class CompanyAssessmentQuestion(db.Model):
    id=db.Column(db.Integer,primary_key=True); assessment_id=db.Column(db.Integer,db.ForeignKey('company_assessment.id')); question_id=db.Column(db.Integer,db.ForeignKey('question.id')); position=db.Column(db.Integer); assessment=db.relationship('CompanyAssessment',backref=db.backref('questions',cascade='all,delete-orphan')); question=db.relationship('Question')
class ModelPaper(db.Model):
    id=db.Column(db.Integer,primary_key=True); company_id=db.Column(db.Integer,db.ForeignKey('company.id')); title=db.Column(db.String(180)); status=db.Column(db.String(40),default='Coming Soon'); company=db.relationship('Company',backref='model_papers')
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(180)); company_id=db.Column(db.Integer,db.ForeignKey('company.id')); category=db.Column(db.String(80)); topic_id=db.Column(db.Integer,db.ForeignKey('topic.id')); difficulty=db.Column(db.String(20)); duration_minutes=db.Column(db.Integer,default=30); published=db.Column(db.Boolean,default=True); instructions=db.Column(db.Text,default=''); company=db.relationship('Company'); topic=db.relationship('Topic'); questions=db.relationship('TestQuestion',back_populates='test',cascade='all,delete-orphan')
class TestQuestion(db.Model):
    id=db.Column(db.Integer,primary_key=True); test_id=db.Column(db.Integer,db.ForeignKey('test.id')); question_id=db.Column(db.Integer,db.ForeignKey('question.id')); position=db.Column(db.Integer); test=db.relationship('Test',back_populates='questions'); question=db.relationship('Question')
class TestAttempt(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id')); test_id=db.Column(db.Integer,db.ForeignKey('test.id')); started_at=db.Column(db.DateTime,default=datetime.utcnow); submitted_at=db.Column(db.DateTime); score=db.Column(db.Float,default=0); correct=db.Column(db.Integer,default=0); wrong=db.Column(db.Integer,default=0); skipped=db.Column(db.Integer,default=0); time_taken=db.Column(db.Integer,default=0); user=db.relationship('User'); test=db.relationship('Test')
class AttemptAnswer(db.Model):
    id=db.Column(db.Integer,primary_key=True); attempt_id=db.Column(db.Integer,db.ForeignKey('test_attempt.id')); question_id=db.Column(db.Integer,db.ForeignKey('question.id')); answer=db.Column(db.String(20)); marked_review=db.Column(db.Boolean,default=False); question=db.relationship('Question'); attempt=db.relationship('TestAttempt',backref=db.backref('answers',cascade='all,delete-orphan'))
class Bookmark(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id')); question_id=db.Column(db.Integer,db.ForeignKey('question.id')); created_at=db.Column(db.DateTime,default=datetime.utcnow); question=db.relationship('Question')
class UserProgress(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id')); topic_id=db.Column(db.Integer,db.ForeignKey('topic.id')); solved=db.Column(db.Integer,default=0); correct=db.Column(db.Integer,default=0); wrong=db.Column(db.Integer,default=0); seconds=db.Column(db.Integer,default=0); user=db.relationship('User'); topic=db.relationship('Topic')
class CodingLanguage(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(80),unique=True); slug=db.Column(db.String(80),unique=True); icon=db.Column(db.String(80),default='code-2'); problem_count=db.Column(db.Integer,default=0)
class CodingProblem(db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(180)); difficulty=db.Column(db.String(20)); description=db.Column(db.Text); starter_code=db.Column(db.Text,default=''); tags=db.Column(db.String(300),default=''); language_id=db.Column(db.Integer,db.ForeignKey('coding_language.id')); input_format=db.Column(db.Text,default=''); output_format=db.Column(db.Text,default=''); constraints=db.Column(db.Text,default=''); examples=db.Column(db.Text,default=''); solution_reference=db.Column(db.Text,default=''); time_limit_ms=db.Column(db.Integer,default=2000); memory_limit_mb=db.Column(db.Integer,default=128); placement_level=db.Column(db.String(30),default='Basic'); category=db.Column(db.String(40),default='General Placement'); language=db.relationship('CodingLanguage',backref='problems')
class CodingTestCase(db.Model):
    id=db.Column(db.Integer,primary_key=True); problem_id=db.Column(db.Integer,db.ForeignKey('coding_problem.id')); input=db.Column(db.Text); expected_output=db.Column(db.Text); hidden=db.Column(db.Boolean,default=False); problem=db.relationship('CodingProblem',backref='test_cases')
class DSAProblem(db.Model):
    id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(180)); category=db.Column(db.String(80)); difficulty=db.Column(db.String(20)); statement=db.Column(db.Text); examples=db.Column(db.Text,default=''); explanation=db.Column(db.Text,default=''); approach=db.Column(db.Text,default=''); complexity=db.Column(db.String(180),default=''); tags=db.Column(db.String(300),default='')
class InterviewQuestion(db.Model):
    id=db.Column(db.Integer,primary_key=True); category=db.Column(db.String(80)); topic=db.Column(db.String(120),default='General'); question=db.Column(db.Text); interviewer_checking=db.Column(db.Text,default=''); how_to_answer=db.Column(db.Text,default=''); sample_answer=db.Column(db.Text,default=''); follow_up=db.Column(db.Text,default=''); company=db.Column(db.String(120),default='')
class Achievement(db.Model):
    id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),unique=True); description=db.Column(db.Text); xp=db.Column(db.Integer,default=0)
class UserAchievement(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id')); achievement_id=db.Column(db.Integer,db.ForeignKey('achievement.id')); earned_at=db.Column(db.DateTime,default=datetime.utcnow); achievement=db.relationship('Achievement')
class Resume(db.Model):
    id=db.Column(db.Integer,primary_key=True); user_id=db.Column(db.Integer,db.ForeignKey('user.id')); title=db.Column(db.String(160),default='My Resume'); data=db.Column(db.JSON,default=dict); ats_score=db.Column(db.Integer,default=0); storage_key=db.Column(db.String(500),default=''); updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow); user=db.relationship('User',backref='resumes')


class CodingSubmission(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,index=True)
    problem_id=db.Column(db.Integer,db.ForeignKey('coding_problem.id'),nullable=False,index=True)
    language=db.Column(db.String(40),nullable=False)
    code=db.Column(db.Text,default='')
    status=db.Column(db.String(40),nullable=False)
    runtime_ms=db.Column(db.Integer,default=0)
    memory_mb=db.Column(db.Float,default=0)
    passed=db.Column(db.Integer,default=0)
    total=db.Column(db.Integer,default=0)
    created_at=db.Column(db.DateTime,default=datetime.utcnow,index=True)
    user=db.relationship('User')
    problem=db.relationship('CodingProblem')

class CodingProgress(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,index=True)
    problem_id=db.Column(db.Integer,db.ForeignKey('coding_problem.id'),nullable=False,index=True)
    status=db.Column(db.String(20),default='attempted')
    attempts=db.Column(db.Integer,default=0)
    last_runtime_ms=db.Column(db.Integer,default=0)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    user=db.relationship('User')
    problem=db.relationship('CodingProblem')
