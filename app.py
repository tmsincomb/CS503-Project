from flask import Flask, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# TODO: link this to a .mypass file
# app.config['MYSQLALCHEMY_DATABASE_URI'] = 'mysql://root:water@localhost/CS503'
db = SQLAlchemy(app)


# @app.route('/modifier')
# def users():
#     conn = db.cursor()
#     command = '''INSERT user, host FROM mysql.user'''
#     conn.execute(command)
#     rv = conn.fetchall()
#     return command, str(rv)


@app.route('/')
def users():
    return render_template_string('here')


if __name__ == '__main__':
    app.run(debug=True)
