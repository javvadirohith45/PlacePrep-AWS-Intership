from flask import Blueprint,render_template,request
from models.content import InterviewQuestion
interviews_bp=Blueprint('interviews',__name__,url_prefix='/interviews')
@interviews_bp.route('')
def index():
    return render_template('interviews/index.html',questions=InterviewQuestion.query.order_by(InterviewQuestion.category,InterviewQuestion.id).all())
@interviews_bp.route('/hr')
def hr():return render_template('interviews/list.html',title='HR Interview',subtitle='Behavioral questions with structured answer guidance.',questions=InterviewQuestion.query.filter_by(category='HR').all(),kind='HR')
@interviews_bp.route('/technical')
def technical():
    topic=request.args.get('topic','');q=InterviewQuestion.query.filter_by(category='Technical');
    if topic:q=q.filter_by(topic=topic)
    questions=q.order_by(InterviewQuestion.topic,InterviewQuestion.id).all();topics=[x[0] for x in InterviewQuestion.query.filter_by(category='Technical').with_entities(InterviewQuestion.topic).distinct().order_by(InterviewQuestion.topic).all()]
    return render_template('interviews/technical.html',questions=questions,topics=topics,selected=topic)
