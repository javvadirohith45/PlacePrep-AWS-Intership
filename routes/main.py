from flask import Blueprint, render_template, request, jsonify
from extensions import db
from models.content import Category,Topic,Question,Company,Test,CodingProblem,InterviewQuestion
main_bp=Blueprint('main',__name__)
@main_bp.route('/')
def home():
    return render_template('index.html',categories=Category.query.all(),companies=Company.query.limit(8).all(),tests=Test.query.filter_by(published=True).limit(6).all())
@main_bp.route('/search')
def search():
    q=request.args.get('q','').strip()
    results=[]
    if q:
        for t in Topic.query.filter(Topic.name.ilike(f'%{q}%')).limit(8): results.append({'type':'Topic','title':t.name,'url':'/practice/topic/'+t.slug})
        for c in Company.query.filter(Company.name.ilike(f'%{q}%')).limit(8): results.append({'type':'Company','title':c.name,'url':f'/companies/{c.id}'})
        for test in Test.query.filter(Test.title.ilike(f'%{q}%')).limit(8): results.append({'type':'Test','title':test.title,'url':f'/mock-tests/{test.id}'})
        for qp in CodingProblem.query.filter(CodingProblem.title.ilike(f'%{q}%')).limit(8): results.append({'type':'Coding','title':qp.title,'url':f'/coding/{qp.id}'})
        for iq in InterviewQuestion.query.filter(InterviewQuestion.question.ilike(f'%{q}%')).limit(8): results.append({'type':'Interview','title':iq.question[:80],'url':'/interviews'})
    return render_template('search.html',q=q,results=results)
@main_bp.route('/api/search')
def api_search(): return jsonify([])
