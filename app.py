from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Open')

@app.route('/')
def index():
    tickets = Ticket.query.all()
    return render_template('index.html', tickets=tickets)

@app.route('/submit', methods=['GET', 'POST'])
def submit_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        new_ticket = Ticket(title=title, description=description, priority=priority)

        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('submit_ticket.html')

@app.route('/update/<int:id>')
def update_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    ticket.status = 'Resolved'
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
