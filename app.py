#!/usr/bin/env python3
from flask import Flask, render_template, render_template_string, request, redirect, jsonify
from src.mysql_connector import MysqlConnector
from src.forms import InsertForm, UpdateForm
import os

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
db = MysqlConnector(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('query'):
            sql_command = request.form['query']
            resp_code, df = db.get(sql_command)
            if not resp_code:
                return render_template_string(f'FAILED -> {df}')
            return df.to_html()
        if request.form.get('command'):
            sql_command = request.form['command']
            resp_code, resp = db.post(sql_command)
            if resp_code == 1:
                result = f'SUCCESS -> affected {resp.rowcount} rows'
            else:
                result = f'FAILED -> {resp}'
            return render_template_string(result)
        if request.form.get('insert'):
            sql_command = request.form['insert']
            # redirect
        if request.form.get('update'):
            sql_command = request.form['update']
            # redirect
    database = db.descibe_database()
    tablenames, tables = zip(*database)
    return render_template('index.html', tablenames=tablenames, )

@app.route('/schema', methods=['GET', 'POST'])
def schema():
    database = db.descibe_database()
    tablenames, tables = zip(*database)
    for table in tables:
        table['type'] = table['type'].apply(lambda t: str(t).split()[0])
    # Need na for white space problem
    tablenames =  ['na'] + list(tablenames)
    tables = [table.to_html() for table in tables]
    return render_template('schema.html', tables=tables, tablenames=tablenames)

@app.route('/insert/<tablename>')
def insert(tablename):
    table = db.get_table(tablename)
    return render_template_string(tablename)
    table['_type'] = table['type'].apply(lambda t: str(t).split()[0])
    fields = [{'gene_name':'', 'gene_type':''}]
    # form = InsertForm(fields=table[['name', '_type']].to_dict('records'))
    form = InsertForm(fields=fields)
    # print(table.to_dict('records'))
    for field in form.fields:
        print(vars(field))
    #     print(field.object_data['name'])
    #     print(str(field.object_data['_type']))
    # print(vars(form.fields[0].label))
    return render_template('insert_form.html', form=form)

@app.route('/update')
def update():
    return render_template('update_form.html')

if __name__ == '__main__':
    app.run(debug=True)
