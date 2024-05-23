from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

# Importar modelos después de definir db para evitar la importación circular
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Transaction {self.amount} - {self.category}>'

@app.route('/')
def index():
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')

        new_transaction = Transaction(amount=amount, category=category, description=description, date=date)
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_transaction.html')

@app.route('/report')
def report():
    transactions = Transaction.query.all()
    return render_template('report.html', transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)
