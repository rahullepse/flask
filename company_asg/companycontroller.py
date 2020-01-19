
from company_asg.models import *
from company_asg.addresscontroller import *

def get_cmpid():
    cmpId=[cmp.id for cmp in get_all_company()]
    if len(cmpId)==0:
        return '1'
    else:
        allcmpId = [item+1 for item in range(cmpId[-1]+1)]
        removed = set(allcmpId)-set(cmpId)
        if removed:
            removed = list(removed)
            removed.sort()
            return removed[0]

def generator():
    cmplist = [cmp.id for cmp in get_all_company()]
    if cmplist:
        cid = cmplist[-1]
    else:
        cid=0
    while True:
        cid+=1
        yield cid

gencmp = generator()

def dummy_cmp():
    return Company(id=0, name='', adr_id=0)

def get_all_company():
    return Company.query.all()

@app.route('/mvc/company/', methods=['GET', 'POST'])
def save_update_cmp():
    msg = ''
    if request.method=='POST':
        cpid = int(request.form['cid'])

        obj = Company.query.filter(Company.adr_id==request.form['adrselect']).first()

        if cpid==0:
            if obj==None:
                cid = get_cmpid()
                if cid:
                    cmps = Company(id=cid, name=request.form['cnm'], adr_id=request.form['adrselect'])
                else:
                    cmps = Company(id=next(gencmp), name=request.form['cnm'], adr_id=request.form['adrselect'])
                db.session.add(cmps)
                db.session.commit()
                msg = 'Company {} info saved successufully..!'.format(cmps.name)
            else:
                msg = 'Address already given to another company..Please Select another address..!'

        else:
            dbcmp = Company.query.filter_by(id=cpid).first()
            dbcmp.name = request.form['cnm']
            if obj==None:
                dbcmp.adr_id = request.form['adrselect']
                msg = 'Company {} info updated successfully'.format(dbcmp.name)
            else:
                msg = 'Address already given to another company..Please Select another address..!'
    return render_template('company.html', cmp=dummy_cmp(), cmps=get_all_company(), adrs=get_all_address(), action=msg)

@app.route('/mvc/company/edit/<int:cid>')
def edit_cmp(cid):
    cmp=Company.query.filter_by(id=cid).first()
    return render_template('company.html', cmp=cmp,adrs=get_all_address(),cmps=get_all_company())

@app.route('/mvc/company/delete/<int:cid>')
def delete_cmp(cid):
    cmp=Company.query.filter_by(id=cid).first()
    db.session.delete(cmp)
    db.session.commit()
    msg = 'Company {} info successfully deleted'.format(cmp.id)
    return render_template('company.html', cmp=dummy_cmp(), cmps=get_all_company(), action=msg, adrs=get_all_address())

#app.run(debug=True)