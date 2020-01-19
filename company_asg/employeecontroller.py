from company_asg.models import *
from company_asg.addresscontroller import *
from company_asg.companycontroller import *

def get_removed_employee():
    emp = [emp.id for emp in get_all_employee()]
    if len(emp) == 0:
        return '1'
    else:
        allEmp = [item+1 for item in range(emp[-1]+1)]
        removed = set(allEmp) - set(emp)
        if removed:
            removed = list(removed)
            removed.sort()
            return removed[0]


def generator():
    employee = [emp.id for emp in get_all_employee()]
    if employee:
        eid = employee[-1]
    else:
        eid=0
    while True:
        eid+=1
        yield eid

gen = generator()

def dummy_employee():
    return Employee(id=0, name='', age=0, salary=0, cmp_id=0)



@app.route('/mvc/employee/', methods=['GET', 'POST'])
def save_update_employee():
    #global emplist
    msg = ''
    if request.method=='POST':
        emid = int(request.form['eid'])
        if emid==0:
            eid = get_removed_employee()
            if eid:
                emp = Employee(id=eid, name=request.form['ename'], age=int(request.form['eage']), salary=float(request.form['esal']), cmp_id=request.form['cmp'])
            else:
                emp = Employee(id=next(gen), name=request.form['ename'], age=int(request.form['eage']),
                               salary=float(request.form['esal']), cmp_id=request.form['cmp'])
            db.session.add(emp)
            db.session.commit()
            adrslist = request.form.getlist('adrs')
            adrInstance = []
            for item in adrslist:
                ad1 = Address.query.filter_by(id=int(item)).first()
                adrInstance.append(ad1)
            emp.adrsref.extend(adrInstance)
            db.session.commit()
            msg = 'Employee Information Successfully Added..!'

        else:

            dbemp = Employee.query.filter_by(id=emid).first()
            dbemp.name = request.form['ename']
            dbemp.age = int(request.form['eage'])
            dbemp.salary = float(request.form['esal'])
            dbemp.cmp_id = request.form['cmp']
            adrslist = request.form.getlist('adrs')

            adrInstance = []
            for item in adrslist:
                ad1 = Address.query.filter_by(id=int(item)).first()
                adrInstance.append(ad1)
            dbemp.adrsref.clear()
            dbemp.adrsref.extend(adrInstance)
            db.session.commit()
            msg = 'Employee Information Successfully Updated..!'

    return render_template('employee.html', action=msg, ad=dummy_address(),emp=dummy_employee(), adrs=get_all_address(), emps=get_all_employee(), cmps=get_all_company())

@app.route('/mvc/employee/edit/<int:eid>')
def edit_employee(eid):
    emp = Employee.query.filter_by(id=eid).first()
    return render_template('employee.html', emp=emp, ad=dummy_address(), adrs=get_all_address(), emps=get_all_employee(), cmps=get_all_company())

@app.route('/mvc/employee/delete/<int:eid>')
def delete_employee(eid):
    emp = Employee.query.filter_by(id=eid).first()
    db.session.delete(emp)
    db.session.commit()
    msg = 'Employee {} is delete successfully'.format(emp.name)
    return render_template('employee.html', emp=dummy_employee(), ad=dummy_address(), adrs=get_all_address(), cmps=get_all_company(), emps=get_all_employee(), action=msg)


def get_all_employee():
    return Employee.query.all()

emplist=get_all_employee()
emplist=list(emplist)