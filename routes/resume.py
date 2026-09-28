import io,re
from flask import Blueprint,render_template,request,redirect,url_for,send_file,flash,jsonify,current_app
from flask_login import login_required,current_user
from extensions import db
from models.content import Resume
from services.aws_storage import enabled as aws_storage_enabled, upload_bytes, presigned_get_url

resume_bp=Blueprint('resume',__name__,url_prefix='/resume')

def score_resume(data):
    score=0; missing=[]
    personal=data.get('personal',{})
    checks=[('name','Name'),('email','Email'),('phone','Phone'),('linkedin','LinkedIn'),('github','GitHub')]
    for key,label in checks:
        if personal.get(key):score+=8
        else:missing.append(label)
    sections=[('summary','Summary',10),('education','Education',15),('skills','Skills',15),('projects','Projects',15),('experience','Experience',10),('certifications','Certifications',5),('achievements','Achievements',4)]
    for key,label,pts in sections:
        value=data.get(key)
        if value and (isinstance(value,str) and value.strip() or isinstance(value,list) and any(value)):score+=pts
        else:missing.append(label)
    text=str(data).lower(); keywords=['python','sql','excel','power bi','java','c++','javascript','data','analysis','project','internship']
    matched=sum(1 for k in keywords if k in text); score+=min(10,matched)
    score=min(100,score)
    tips=[]
    if missing:tips.append('Add missing sections: '+', '.join(missing[:6])+'.')
    if matched<4:tips.append('Add role-relevant technical keywords that genuinely match your experience.')
    tips.append('Use standard section headings, readable typography and achievement-focused bullet points.')
    return score,tips

@resume_bp.route('',methods=['GET','POST'])
@login_required
def builder():
    resume=Resume.query.filter_by(user_id=current_user.id).order_by(Resume.updated_at.desc()).first()
    if request.method=='POST':
        data=request.form.to_dict(flat=False)
        # Keep the form extensible while storing a normalized JSON structure.
        normalized={
            'personal':{k:(v[0] if v else '') for k,v in data.items() if k in ['name','email','phone','location','linkedin','github','portfolio']},
            'summary':data.get('summary',[''])[0],
            'education':data.get('education',[''])[0],
            'skills':data.get('skills',[''])[0],
            'projects':data.get('projects',[''])[0],
            'experience':data.get('experience',[''])[0],
            'certifications':data.get('certifications',[''])[0],
            'achievements':data.get('achievements',[''])[0],
            'coding_profiles':data.get('coding_profiles',[''])[0],
            'extra':data.get('extra',[''])[0],
        }
        score,tips=score_resume(normalized)
        if not resume:resume=Resume(user_id=current_user.id)
        resume.data=normalized;resume.ats_score=score;resume.storage_key='';db.session.add(resume);db.session.commit();flash('Resume saved.','success');return redirect(url_for('resume.builder'))
    return render_template('resume/builder.html',resume=resume,data=(resume.data if resume else {}),score=(resume.ats_score if resume else 0))

@resume_bp.route('/ats',methods=['POST'])
@login_required
def ats():
    data=request.get_json() or {};score,tips=score_resume(data);return jsonify({'score':score,'tips':tips,'disclaimer':'This is an ATS-style checklist score, not a guarantee of any employer screening result.'})

@resume_bp.route('/download')
@login_required
def download():
    resume=Resume.query.filter_by(user_id=current_user.id).order_by(Resume.updated_at.desc()).first_or_404(); data=resume.data or {}

    # In AWS production, prefer the private S3 copy when one exists. The
    # presigned URL expires automatically and the bucket can remain private.
    if aws_storage_enabled() and resume.storage_key:
        url=presigned_get_url(resume.storage_key)
        if url:
            return redirect(url)

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
        from reportlab.lib.units import mm
    except ImportError:
        flash('PDF generation requires reportlab. Run: pip install reportlab','error');return redirect(url_for('resume.builder'))
    buf=io.BytesIO();doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=16*mm,bottomMargin=16*mm)
    styles=getSampleStyleSheet(); title=ParagraphStyle('Title2',parent=styles['Title'],alignment=TA_CENTER,fontSize=18,spaceAfter=5);h=ParagraphStyle('H2',parent=styles['Heading2'],fontSize=11,spaceBefore=8,spaceAfter=3);body=styles['BodyText'];story=[]
    p=data.get('personal',{});story.append(Paragraph(p.get('name') or current_user.name,title));contact=' · '.join([x for x in [p.get('email'),p.get('phone'),p.get('location'),p.get('linkedin'),p.get('github'),p.get('portfolio')] if x]);story.append(Paragraph(contact,body));
    for key,label in [('summary','SUMMARY'),('education','EDUCATION'),('skills','SKILLS'),('projects','PROJECTS'),('experience','EXPERIENCE'),('certifications','CERTIFICATIONS'),('achievements','ACHIEVEMENTS'),('coding_profiles','CODING PROFILES'),('extra','EXTRA-CURRICULAR')]:
        value=data.get(key,'')
        if value:story += [Paragraph(label,h),Paragraph(str(value).replace('\n','<br/>'),body)]
    doc.build(story);buf.seek(0)
    pdf_bytes=buf.getvalue()

    # Real S3 integration: when a bucket is configured, store the generated
    # resume privately in S3 and remember its key. Local development continues
    # to download the same PDF directly from Flask.
    if aws_storage_enabled():
        key=f"{current_app.config.get('AWS_S3_PREFIX','placeprep')}/resumes/user-{current_user.id}/resume-{resume.id}.pdf"
        try:
            upload_bytes(pdf_bytes,key,'application/pdf')
            resume.storage_key=key
            db.session.commit()
            url=presigned_get_url(key)
            if url:
                return redirect(url)
        except RuntimeError as exc:
            current_app.logger.exception('Resume S3 storage failed: %s', exc)
            flash(str(exc),'error')

    return send_file(io.BytesIO(pdf_bytes),as_attachment=True,download_name='PlacePrep_Resume.pdf',mimetype='application/pdf')
