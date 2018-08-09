import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy


#find the project path
project_dir = os.path.dirname(os.path.abspath(__file__))
#setup database as sqlite file in the project path
database_file = "sqlite:///{}".format(os.path.join(project_dir, "employeedatabase.db"))

#create the flask app
app = Flask(__name__)
#tell the webapp where the database is
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initialize connection to the database, store as db
db = SQLAlchemy(app)


class Employee(db.Model):#create class for employee
    #add attribute called employee_name, a string of up to 80 charachters, must be unique
    employee_name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):#format string for print command
        return "<Name: {}>".format(self.employee_name)


@app.route("/", methods=["GET", "POST"]) #accept get and post requests
def home():#
    if request.form:#if something is posted to the form
        #initialize a new Employee object, add their name to it
        employee = Employee(employee_name=request.form.get("employee_name"))
        db.session.add(employee)#add the newly created employee object to the db
        db.session.commit()#commit the change to the db
    if Employee:
        employees = Employee.query.all()
    else:
        employees = ('None')
    #render the page home.html and pass list of employees to it
    return render_template("home.html", employees=employees)
  
@app.route("/update", methods=["POST"])
def update():#function to update names of employees
    newname = request.form.get("newname") #variable to hold new name gotten from form
    oldname = request.form.get("oldname") #variable to hold old name gotten from form
    #create variable to search through employees in db based on old name
    employee = Employee.query.filter_by(employee_name=oldname).first()
    employee.employee_name = newname #change old name to new name in db
    db.session.commit() #commit changes to db
    return redirect("/") #reload the page

@app.route("/delete", methods=["POST"])
def delete():#function to delete an employee from the db
    employee_name = request.form.get("employee_name") #variable to hold name imported from form
    #create variable to search for the entry using the variable just created
    employee = Employee.query.filter_by(employee_name=employee_name).first()
    db.session.delete(employee) #remove employee object from db
    db.session.commit() #commit changes to db
    return redirect("/") #reload the page



if __name__ == "__main__":#run app, but only if called as the main
    app.run(debug=False)