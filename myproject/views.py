from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import  login_required , current_user
from .models import Note
from . import db


views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('note is too short!',category='error')
        else:
            new_note = Note(data=note,user_id=current_user.id)  
            db.session.add(new_note)
            db.session.commit()
            flash('note added!',category='success')
    return render_template("home.html",user=current_user)

@views.route('/<int:id>',methods=['GET','POST']) 
@login_required
def delete(id):
    datatodelete = Note.query.get(id)
    db.session.delete(datatodelete)
    db.session.commit()
    flash('note deleted',category='success')
    return redirect(url_for('views.home'))
       


