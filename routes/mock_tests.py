from datetime import datetime, timezone
from flask import Blueprint,render_template,request,redirect,url_for,jsonify,abort
from flask_login import login_required,current_user
from extensions import db
from models.content import Test,TestQuestion,TestAttempt,AttemptAnswer
mock_bp=Blueprint('mock',__name__,url_prefix='/mock-tests')
@mock_bp.route('')
def index():
    category=request.args.get('category','')
    q=Test.query.filter_by(published=True)
    if category:q=q.filter_by(category=category)
    return render_template('mock_tests/index.html',tests=q.order_by(Test.id.desc()).all(),category=category)
@mock_bp.route('/<int:test_id>')
def detail(test_id): return render_template('mock_tests/detail.html',test=Test.query.get_or_404(test_id))
@mock_bp.route('/<int:test_id>/start',methods=['POST'])
@login_required
def start(test_id):
    test=Test.query.get_or_404(test_id)
    if not test.questions:return redirect(url_for('mock.detail',test_id=test.id))
    a=TestAttempt(user_id=current_user.id,test_id=test.id);db.session.add(a);db.session.commit();return redirect(url_for('mock.exam',attempt_id=a.id))
@mock_bp.route('/exam/<int:attempt_id>')
@login_required
def exam(attempt_id):
    a=TestAttempt.query.get_or_404(attempt_id)
    if a.user_id!=current_user.id:abort(403)
    if a.submitted_at:return redirect(url_for('mock.result',attempt_id=a.id))
    elapsed=max(0,int((datetime.utcnow()-a.started_at).total_seconds()));remaining=max(0,a.test.duration_minutes*60-elapsed)
    return render_template('mock_tests/exam.html',attempt=a,test=a.test,items=sorted(a.test.questions,key=lambda x:x.position),remaining_seconds=remaining)
@mock_bp.route('/exam/<int:attempt_id>/save',methods=['POST'])
@login_required
def save(attempt_id):
    a=TestAttempt.query.get_or_404(attempt_id); 
    if a.user_id!=current_user.id or a.submitted_at: return jsonify({'ok':False}),403
    data=request.get_json() or {};qid=int(data.get('question_id'));allowed={x.question_id for x in a.test.questions}
    if qid not in allowed:return jsonify({'ok':False,'error':'Question does not belong to this test.'}),400
    row=AttemptAnswer.query.filter_by(attempt_id=a.id,question_id=qid).first() or AttemptAnswer(attempt_id=a.id,question_id=qid)
    row.answer=data.get('answer','');row.marked_review=bool(data.get('marked_review'));db.session.add(row);db.session.commit();return jsonify({'ok':True})
@mock_bp.route('/exam/<int:attempt_id>/submit',methods=['POST'])
@login_required
def submit(attempt_id):
    a=TestAttempt.query.get_or_404(attempt_id)
    if a.user_id!=current_user.id:abort(403)
    if a.submitted_at:return redirect(url_for('mock.result',attempt_id=a.id))
    answers={x.question_id:x.question for x in a.test.questions};rows=AttemptAnswer.query.filter_by(attempt_id=a.id).all();correct=wrong=0
    for r in rows:
        q=answers.get(r.question_id)
        if not q or not r.answer:continue
        if r.answer==q.correct_answer:correct+=1
        else:wrong+=1
    total=len(a.test.questions);a.correct=correct;a.wrong=wrong;a.skipped=max(0,total-correct-wrong);a.score=(correct/total*100 if total else 0);a.time_taken=min(a.test.duration_minutes*60,max(0,int((datetime.utcnow()-a.started_at).total_seconds())));a.submitted_at=datetime.utcnow();db.session.commit();current_user.xp += correct*5;db.session.commit();return redirect(url_for('mock.result',attempt_id=a.id))
@mock_bp.route('/result/<int:attempt_id>')
@login_required
def result(attempt_id):
    a=TestAttempt.query.get_or_404(attempt_id)
    if a.user_id!=current_user.id:abort(403)
    answers={x.question_id:x for x in a.answers};items=[]
    for tq in sorted(a.test.questions,key=lambda x:x.position):items.append({'number':tq.position,'question':tq.question,'answer':answers.get(tq.question_id),'correct':tq.question.correct_answer})
    return render_template('mock_tests/result.html',attempt=a,items=items)
