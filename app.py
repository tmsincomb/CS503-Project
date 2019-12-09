#!/usr/bin/env python3
"""
Usage:
  app.py [-d FILE]
  app.py (-h | --help)

Options:
  -h, --help
  -d, --db_url=FILE
"""
from flask import Flask, render_template, render_template_string, request, redirect, jsonify, Response, url_for
from src.mysql_connector import MysqlConnector
from src.forms import dynamic_form
import os
import json
from wtforms import TextField, Form, Label
from werkzeug.datastructures import MultiDict
from docopt import docopt
args=docopt(__doc__)

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
db_url = open(args['--db_url']).read() if args.get('--db_url') else None
db = MysqlConnector(app, db_url)

header = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Schema</title>
    <link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
<a href="/">&#8592; BACK HOME</a><br></br>
</body>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('query'):
            sql_command = request.form['query']
            resp_code, df = db.get(sql_command)
            if resp_code == 0:
                result = f'FAILED -> {df}'
                return render_template('message.html', result=result)
            return render_template_string(header + df.to_html())
        if request.form.get('command'):
            sql_command = request.form['command']
            resp_code, resp = db.post(sql_command)
            if resp_code == 1:
                result = f'SUCCESS -> affected {resp.rowcount} rows'
            else:
                result = f'FAILED -> {resp}'
            return render_template('message.html', result=result)
        if request.form.get('insert'):
            tablename = request.form['insert']
            return redirect(url_for('insert', tablename=tablename))
        if request.form.get('update'):
            entity_meta = request.form['update']
            return redirect(url_for('update', entity_meta=entity_meta))
        if request.form.get('delete'):
            entity_meta = request.form['delete']
            return delete_entity(entity_meta)
    database = db.descibe_database()
    tablenames, tables = zip(*database)
    rows=[]
    for tablename in tablenames:
        sql_command = f'SELECT * FROM {tablename}' # WHERE LIKE %{value}%'
        status, table = db.get(sql_command)
        for i, row in table.iterrows():
            values = list(row.to_dict().values())
            rows.append(tablename+':'+str(i)+','+str(values))
    return render_template('index.html', tablenames=tablenames, rows=rows)

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

@app.route('/insert/<string:tablename>', methods=['GET', 'POST'])
def insert(tablename):
    table = db.get_table(tablename)
    table['type'] = table['type'].apply(lambda t: str(t).split()[0])
    headers = list(table['name'])
    types = [t.lower () for t in list(table['type'])]
    sform = dynamic_form(table)
    form = sform()
    if form.validate_on_submit():
        values = []
        for i, field in enumerate(headers):
            if 'integer' in types[i] or 'float' in types[i] or 'double' in types[i]:
                values.append(form[field].data)
            else:
                values.append("'" + str(form[field].data) + "'")
        sql_command = f"INSERT INTO {tablename} ({', '.join(headers)}) VALUES ({', '.join(values)});"
        resp_code, resp = db.post(sql_command)
        if resp_code == 1:
            result = f'SUCCESS -> affected {resp.rowcount} rows'
        else:
            result = f'FAILED -> {resp}'
        return render_template('message.html', result=result)
    return render_template('insert_form.html', form=form, headers=headers, types=types, table_len=len(headers))

@app.route('/update/<string:entity_meta>', methods=['GET', 'POST'])
def update(entity_meta):
    tablename, index = entity_meta.split(':')
    table_schema = db.get_table(tablename)
    table_schema['type'] = table_schema['type'].apply(lambda t: str(t).split()[0])
    headers = list(table_schema['name'])
    types = [t.lower () for t in list(table_schema['type'])]
    status, table = db.get(f'SELECT * FROM {tablename};')
    row = table.iloc[int(index)]
    row = row.to_dict()
    sform = dynamic_form(table_schema)
    form = sform(**row)
    if form.validate_on_submit():
        new_conditions = []
        old_conditions = []
        for i, field in enumerate(headers):
            if 'integer' in types[i] or 'float' in types[i] or 'double' in types[i]:
                new_conditions.append(field+' = '+str(form[field].data))
                old_conditions.append(field+' = '+str(row[field]))
            else:
                new_conditions.append(field+' = '+"'"+str(form[field].data)+"'")
                old_conditions.append(field+' = '+"'"+str(row[field])+"'")
        sql_command = f"UPDATE {tablename} SET {', '.join(new_conditions)} WHERE {' and '.join(old_conditions)};"
        resp_code, resp = db.post(sql_command)
        if resp_code == 1:
            result = f'SUCCESS -> affected {resp.rowcount} rows'
        else:
            result = f'FAILED -> {resp}'
        return render_template('message.html', result=result)
    return render_template('update_form.html', form=form, headers=headers, types=types, table_len=len(headers))

@app.route('/update/<string:entity_meta>', methods=['GET', 'POST'])
def delete_entity(entity_meta):
    tablename, index = entity_meta.split(':')
    table_schema = db.get_table(tablename)
    table_schema['type'] = table_schema['type'].apply(lambda t: str(t).split()[0])
    headers = list(table_schema['name'])
    types = [t.lower () for t in list(table_schema['type'])]
    status, table = db.get(f'SELECT * FROM {tablename};')
    row = table.iloc[int(index)]
    row = row.to_dict()

    conditions = []
    for i, field in enumerate(headers):
        if 'integer' in types[i] or 'float' in types[i] or 'double' in types[i]:
            conditions.append(field+' = '+str(row[field]))
        else:
            conditions.append(field+' = '+"'"+str(row[field])+"'")
    sql_command = f"DELETE FROM {tablename} WHERE {' and '.join(conditions)};"
    resp_code, resp = db.post(sql_command)
    if resp_code == 1:
        result = f'SUCCESS -> affected {resp.rowcount} rows'
    else:
        result = f'FAILED -> {resp}'
    return render_template('message.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
