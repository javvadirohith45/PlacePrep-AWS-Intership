from flask import Blueprint,render_template,request
from models.content import DSAProblem

dsa_bp=Blueprint('dsa',__name__,url_prefix='/dsa')
@dsa_bp.route('')
def index():
    cat=request.args.get('category','').strip(); q=DSAProblem.query
    if cat:q=q.filter_by(category=cat)
    problems=q.order_by(DSAProblem.id).all()
    cats=[x[0] for x in DSAProblem.query.with_entities(DSAProblem.category).distinct().order_by(DSAProblem.category).all()]
    return render_template('dsa/index.html',problems=problems,categories=cats,selected=cat)
@dsa_bp.route('/<int:problem_id>')
def problem(problem_id):return render_template('dsa/problem.html',problem=DSAProblem.query.get_or_404(problem_id))
