from company_asg.models import *

def get_removed_id():
    addressId = [adr.id for adr in get_all_address()]
    if len(addressId)==0:
        return '1'
    else:
        allAddressId = [item+1 for item in range(addressId[-1]+1)]
        removed = set(allAddressId)-set(addressId)
        if removed:
            removed=list(removed)
            removed.sort()
            return removed[0]

def generator():
    addressid = [adr.id for adr in get_all_address()]
    if addressid:
        adid = addressid[-1]
    else:
        adid=0
    while True:
        adid+=1
        yield adid
gen = generator()

def get_all_address():
    return Address.query.all()



def dummy_address():
    return Address(id=0,city='',state='',pincode=0)

@app.route('/mvc/address/',methods=['GET','POST'])
def save_update_address():
    msg=''
    if request.method=='GET':
        pass
    else:
        adid = int(request.form['aid'])
        if adid==0:
            aid = get_removed_id()
            address = Address(id=aid, city=request.form['acity'], state=request.form['astate'],
                                  pincode=request.form['apin'])

            #address = Address(id=next(gen),city=request.form['acity'],state=request.form['astate'],pincode=request.form['apin'])
            db.session.add(address)
            msg = 'Address added successfully..!'
        else:
            dbad = Address.query.filter_by(id=adid).first()
            dbad.city = request.form['acity']
            dbad.state = request.form['astate']
            dbad.pincode = request.form['apin']
            msg = 'Address updated successfully..!'
    db.session.commit()
    return render_template('address.html', ad=dummy_address(), adrs=get_all_address(), action=msg)

@app.route('/mvc/address/edit/<int:aid>')
def edit_address(aid):
    adrs=Address.query.filter_by(id=aid).first()
    return render_template('address.html',adrs=get_all_address(), ad=adrs)

@app.route('/mvc/address/delete/<int:aid>')
def delete_address(aid):
    dbad = Address.query.filter_by(id=aid).first()
    db.session.delete(dbad)
    db.session.commit()
    msg = 'Deleted Successfully...!'
    return render_template('address.html', ad=dummy_address(), adrs=get_all_address(), action=msg)
