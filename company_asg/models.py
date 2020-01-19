
from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/company_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

emp_adrs = db.Table('Emp_Adr',
                    db.Column('e_id',db.Integer,db.ForeignKey('employee.e_id'),primary_key=True),
                    db.Column('a_id',db.Integer,db.ForeignKey('address.a_id'),primary_key=True)
                    )

class Address(db.Model):
    id = db.Column('a_id', db.Integer, primary_key=True)
    city = db.Column('a_city', db.String(100))
    state = db.Column('a_state', db.String(100))
    pincode = db.Column('a_pin', db.Integer)
    cmp = db.relationship('Company',uselist=False,lazy=True,backref='adrref')
    emp = db.relationship('Employee',secondary=emp_adrs,lazy='subquery',backref=db.backref('adrsref',lazy=True))

class Employee(db.Model):
    id = db.Column('e_id', db.Integer, primary_key=True)
    name = db.Column('e_nm', db.String(100))
    age = db.Column('e_age', db.Integer)
    salary = db.Column('e_sal', db.Float)
    cmp_id = db.Column('c_id',db.ForeignKey('company.c_id'),unique=False)

class Company(db.Model):
    id = db.Column('c_id', db.Integer, primary_key=True)
    name = db.Column('c_nm', db.String(100))
    emp = db.relationship('Employee',uselist=True,lazy=False,backref='cmpref')
    adr_id = db.Column('a_id', db.ForeignKey('address.a_id'), unique=False)

if __name__ == '__main__':
    db.create_all()
    print('Created..')

