from flask import Blueprint,render_template
from flask_login import login_required,current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from models.content import TestAttempt,UserProgress,Question,Bookmark,Topic
from extensions import db
dashboard_bp=Blueprint('dashboard',__name__,url_prefix='/dashboard')
@dashboard_bp.route('')
@login_required
def index():
    attempts=TestAttempt.query.filter_by(user_id=current_user.id).order_by(TestAttempt.started_at.desc()).all(); solved=db.session.query(func.sum(UserProgress.solved)).filter_by(user_id=current_user.id).scalar() or 0; correct=db.session.query(func.sum(UserProgress.correct)).filter_by(user_id=current_user.id).scalar() or 0; total=max(solved,1); accuracy=round(correct/total*100,1); chart_attempts=list(reversed(attempts[:10]));scores=[round(a.score or 0,1) for a in chart_attempts]
    topic_stats=[]
    for p in UserProgress.query.filter_by(user_id=current_user.id).all(): topic_stats.append({'topic':p.topic.name,'accuracy':round(p.correct/max(p.solved,1)*100,1),'solved':p.solved})
    activity={}; today=datetime.utcnow().date()
    for a in attempts: activity[a.started_at.date().isoformat()]=activity.get(a.started_at.date().isoformat(),0)+1
    heatmap=[]
    for offset in range(119,-1,-1):
        day=today-timedelta(days=offset);heatmap.append({'date':day.isoformat(),'count':activity.get(day.isoformat(),0)})
    return render_template('dashboard/index.html',attempts=attempts,solved=solved,accuracy=accuracy,scores=scores,chart_attempts=chart_attempts,topic_stats=topic_stats,bookmarks=Bookmark.query.filter_by(user_id=current_user.id).count(),heatmap=heatmap)
