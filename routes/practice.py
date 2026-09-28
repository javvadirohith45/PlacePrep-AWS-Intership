from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort
from flask_login import login_required, current_user
from extensions import db
from models.content import Topic, Category, Question, QuestionOption, Bookmark, UserProgress, Test

practice_bp=Blueprint('practice',__name__,url_prefix='/practice')

@practice_bp.route('')
def index():
    aptitude=Category.query.filter_by(kind='aptitude').first()
    reasoning=Category.query.filter_by(kind='reasoning').first()
    return render_template('aptitude/index.html',aptitude=aptitude,reasoning=reasoning,topics=Topic.query.order_by(Topic.name).all())

@practice_bp.route('/topic/<slug>')
def topic(slug):
    t=Topic.query.filter_by(slug=slug).first_or_404()
    qs=Question.query.filter_by(topic_id=t.id,active=True).order_by(Question.id).all()
    test=Test.query.filter_by(topic_id=t.id,title=f'{t.name} Mock Test',published=True).first()
    return render_template('aptitude/topic.html',topic=t,questions=qs[:5],question_count=len(qs),test=test)

@practice_bp.route('/quiz/<int:topic_id>')
@login_required
def quiz(topic_id):
    t=Topic.query.get_or_404(topic_id)
    test=Test.query.filter_by(topic_id=t.id,title=f'{t.name} Mock Test',published=True).first()
    if not test: abort(404)
    return redirect(url_for('mock.detail',test_id=test.id))

@practice_bp.route('/api/answer',methods=['POST'])
@login_required
def answer():
    data=request.get_json() or {}; q=Question.query.get_or_404(data.get('question_id'))
    if not q.topic_id:return jsonify({'error':'Question has no topic mapping.'}),400
    chosen=data.get('answer'); correct=chosen==q.correct_answer
    p=UserProgress.query.filter_by(user_id=current_user.id,topic_id=q.topic_id).first() or UserProgress(user_id=current_user.id,topic_id=q.topic_id)
    p.solved+=1; p.correct+=1 if correct else 0; p.wrong+=0 if correct else 1; p.seconds+=int(data.get('seconds',0) or 0)
    db.session.add(p); db.session.commit()
    return jsonify({'correct':correct,'correct_answer':q.correct_answer,'explanation':q.explanation})

@practice_bp.route('/bookmark/<int:question_id>',methods=['POST'])
@login_required
def bookmark(question_id):
    q=Question.query.get_or_404(question_id)
    b=Bookmark.query.filter_by(user_id=current_user.id,question_id=q.id).first()
    if b: db.session.delete(b); saved=False
    else: db.session.add(Bookmark(user_id=current_user.id,question_id=q.id)); saved=True
    db.session.commit(); return jsonify({'saved':saved})

@practice_bp.route('/bookmarks')
@login_required
def bookmarks(): return render_template('dashboard/bookmarks.html',bookmarks=Bookmark.query.filter_by(user_id=current_user.id).all())

@practice_bp.route('/mistakes')
@login_required
def mistakes():
    from models.content import AttemptAnswer
    rows=[]
    for a in AttemptAnswer.query.join(AttemptAnswer.attempt).filter(AttemptAnswer.answer!='').all():
        if a.attempt.user_id==current_user.id and a.answer != a.question.correct_answer: rows.append(a)
    return render_template('dashboard/mistakes.html',mistakes=rows)
