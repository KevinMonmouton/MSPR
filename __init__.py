from flask import Flask, render_template_string, flash,render_template, jsonify, request,redirect, url_for,json
from flask_mysqldb import MySQL
from . authentificationForm import AuthentificationForm
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

app.config['MYSQL_HOST'] = 'mysql-msprtop.alwaysdata.net'
app.config['MYSQL_USER'] = 'msprtop_admin'
app.config['MYSQL_PASSWORD'] = 'ePSI2023!'
app.config['MYSQL_DB'] = 'msprtop_crm'
 
mysql = MySQL(app) 

@app.route('/')
def accueil():  
 return render_template('accueil.html')

@app.route("/authentification", methods=['GET', 'POST'])
def authentification():
    form = AuthentificationForm()
    if form.validate_on_submit():
      cursor = mysql.connection.cursor()  
      query = ("SELECT * FROM utilisateurs WHERE email = %s AND mot_de_passe = %s")
      cursor.execute(query, (form.email.data, form.password.data))
      row = cursor.fetchone()
      mysql.connection.commit()
      cursor.close()
      if row is not None:
        flash('Vous vous êtes authentifié avec succès {}!'.format(form.email.data), 'success')
        return render_template('accueil.html')
      else:
        return render_template('authentification.html', form=form)                
    return render_template('authentification.html', form=form)

@app.route('/clients')
def clients():  
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT nom, siret, email, telephone, adresse, ville, code_postal, pays, id FROM clients ')
    data = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template('clients.html', data=data)

@app.route('/modifier_client/<int:id>', methods=['GET', 'POST'])
def modifier_client(id):    
    return render_template('modifier_client.html')

@app.route('/supprimer_client/<int:id>', methods=['POST'])
def supprimer_client(id):    
    return render_template('supprimer_client.html')
  
@app.route('/ajouter_client', methods=['GET', 'POST'])
def ajouter_client(id):    
    return render_template('ajouter_client.html')
  
  
@app.route('/produits')
def produits():  
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, code_ean, description, prix, quantite, date_creation FROM produits ')
    data = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template('produits.html', data=data)

@app.route('/modifier_produit/<int:id>', methods=['GET', 'POST'])
def modifier_produit(id):    
    return render_template('modifier_produit.html')

@app.route('/supprimer_produit/<int:id>', methods=['POST'])
def supprimer_produit(id):    
    return render_template('supprimer_produit.html')
  
@app.route('/ajouter_produit', methods=['GET', 'POST'])
def ajouter_produit(id):    
    return render_template('ajouter_produit.html')

if __name__ == "__main__":
  app.run(debug=True)
