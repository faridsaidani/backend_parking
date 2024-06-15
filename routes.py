from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, mongo
from models import Utilisateur, Facture, Entree_Sortie, Vehicule
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bib import *


@app.route('/vehicules/<id>', methods=['GET'])
def get_vehicules(id):
    vehicules = Vehicule.objects()
    vehicules = [vehicule.to_dict() for vehicule in vehicules if vehicule['propietaire'] == int(id)]
    if not vehicules:
        return jsonify({'message': 'No vehicules found'}), 404
    return jsonify(vehicules), 200



@app.route('/vehicules', methods=['POST'])
def add_vehicule():
    data = request.get_json()
    existing_vehicule = Vehicule.objects(numero_immatriculation=data['numero_immatriculation']).first()
    if existing_vehicule:
        return jsonify({'message': 'A vehicle with this registration number already exists'}), 400
    vehicule = Vehicule(numero_immatriculation=data['numero_immatriculation'], marque=data['marque'], modele=data['modele'], couleur=data['couleur'], annee=data['annee'], photos=data['photos'], propietaire=data['propietaire'])
    vehicule.save()
    return jsonify(vehicule), 201

@app.route('/vehicules/<numero_immatriculation>', methods=['GET'])
def get_vehicule(numero_immatriculation):
    vehicule = Vehicule.objects(numero_immatriculation=numero_immatriculation).first()
    if not vehicule:
        return jsonify({'message': 'Vehicule not found'}), 404
    if session['user_id'] != vehicule.propietaire:
        return jsonify({'message': 'You are not authorized to view this vehicule'}), 403
    return jsonify(vehicule), 200


@app.route('/vehicules', methods=['GET'])
def get_allVehicules():
    vehicule = Vehicule.objects()
    if not vehicule:
        return jsonify({'message': 'Vehicule not found'}), 404
    return jsonify(vehicule), 200

@app.route('/vehicules/<numero_immatriculation>', methods=['PUT'])
def update_vehicule(numero_immatriculation):
    data = request.get_json()
    if not session['logged_in']:
        return jsonify({'message': 'You are not logged in'}), 401
    if (session['user_id'] != Vehicule.objects(numero_immatriculation=numero_immatriculation).first().propietaire) or (session['user_id'] != 1):
        return jsonify({'message': 'You are not authorized to update this vehicule'}), 403
    vehicule = Vehicule.objects(numero_immatriculation=numero_immatriculation).first()
    vehicule.marque = data.get('marque', vehicule.marque)
    vehicule.modele = data.get('modele', vehicule.modele)
    vehicule.couleur = data.get('couleur', vehicule.couleur)
    vehicule.annee = data.get('annee', vehicule.annee)
    vehicule.photos = data.get('photos', vehicule.photos)
    vehicule.save()
    return jsonify(vehicule), 200

@app.route('/vehicules/<numero_immatriculation>', methods=['DELETE'])
def delete_vehicule(numero_immatriculation):
    vehicule = Vehicule.objects(numero_immatriculation=numero_immatriculation).first()
    if not vehicule:
        return jsonify({'message': 'Vehicule not found'}), 404
    if session['user_id'] != vehicule.propietaire:
        return jsonify({'message': 'You are not authorized to delete this vehicule'}), 403
    vehicule.delete()
    return jsonify({'message': 'Deleted successfully'}), 200

@app.route('/factures', methods=['POST'])
def create_facture():
    data = request.get_json()
    facture = Facture(**data).save()
    return jsonify(facture.to_dict()), 201

@app.route('/factures', methods=['GET'])
def get_factures():
    factures = Facture.objects()
    return jsonify([facture.to_dict() for facture in factures]), 200

@app.route('/factures/<id>', methods=['GET'])
def get_facture(id):
    facture = Facture.objects.get_or_404(id=id)
    return jsonify(facture.to_dict()), 200

@app.route('/factures/<id>', methods=['PUT'])
def update_facture(id):
    data = request.get_json()
    Facture.objects(id=id).update(**data)
    return '', 204

@app.route('/factures/<id>', methods=['DELETE'])
def delete_facture(id):
    Facture.objects(id=id).delete()
    return '', 204
@app.route('/entrees_sorties', methods=['GET'])
def get_entrees_sorties():
    entrees_sorties = Entree_Sortie.query.all()
    entrees_sorties_dict = [entree_sortie.to_dict() for entree_sortie in entrees_sorties]
    print(entrees_sorties_dict)
    return jsonify(entrees_sorties_dict), 200

@app.route('/entrees_sorties', methods=['POST'])
def add_entree_sortie():
    data = request.get_json()
    new_entree_sortie = Entree_Sortie(numero_immatriculation=data['numero_immatriculation'], heure_entree=data["heure_entree"], heure_sortie=data["heure_sortie"], photo_entree=data['photo_entree'], photo_sortie=data['photo_sortie'])
    db.session.add(new_entree_sortie)
    db.session.commit()
    return jsonify(new_entree_sortie.to_dict()), 201

@app.route('/entrees_sorties/<id>', methods=['GET'])
def get_entree_sortie_by_id(id):
    entree_sortie = Entree_Sortie.query.get(id)
    return jsonify(entree_sortie), 200

# TODO: Fix this (heure_sortie is not defined) 
@app.route('/entrees_sorties/<id>', methods=['PUT'])
def update_entree_sortie(id):
    data = request.get_json()
    entree_sortie = Entree_Sortie.query.get(id)
    if not entree_sortie:
        return jsonify({'message': 'Entree_Sortie not found'}), 404
    entree_sortie.numero_immatriculation = data.get('numero_immatriculation', entree_sortie.numero_immatriculation)
    entree_sortie.heure_entree = data.get('heure_entree', entree_sortie.heure_entree)
    entree_sortie.heure_sortie = data.get('heure_sortie', entree_sortie.heure_sortie)
    entree_sortie.photo_entree = data.get('photo_entree', entree_sortie.photo_entree)
    entree_sortie.photo_sortie = data.get('photo_sortie', entree_sortie.photo_sortie)
    db.session.commit()
    return jsonify(entree_sortie.to_dict()), 200

@app.route('/entrees_sorties/<id>', methods=['DELETE'])
def delete_entree_sortie(id):
    entree_sortie = Entree_Sortie.query.get(id)
    if not entree_sortie:
        return jsonify({'message': 'Entree_Sortie not found'}), 404
    db.session.delete(entree_sortie)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

@app.route('/entrees_sorties/vehicule/<numero_immatriculation>', methods=['GET'])
def get_entrees_sorties_by_vehicle(numero_immatriculation):
    entrees_sorties = Entree_Sortie.query.filter_by(numero_immatriculation=numero_immatriculation).all()
    if not entrees_sorties:
        return jsonify({'message': 'No entrees_sorties found'}), 404
    if session['user_id'] != 1:
        entrees_sorties = [entree_sortie.to_dict() for entree_sortie in entrees_sorties if entree_sortie.id_utilisateur == session['user_id']]
    entrees_sorties = [entree_sortie.to_dict() for entree_sortie in entrees_sorties]
    return jsonify(entrees_sorties), 200

@app.route('/entrees_sorties/vehicule/<numero_immatriculation>', methods=['DELETE'])
def delete_entrees_sorties_by_vehicle(numero_immatriculation):
    entrees_sorties = Entree_Sortie.query.filter_by(numero_immatriculation=numero_immatriculation).all()
    if session['user_id'] != 1:
        return jsonify({'message': 'You are not authorized to delete these entrees_sorties'}), 403
    if not entrees_sorties:
        return jsonify({'message': 'No entrees_sorties found'}), 404
    for entree_sortie in entrees_sorties:
        db.session.delete(entree_sortie)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200


@app.route('/')
def home():
    return "Hello, World!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['mot_de_passe'], method='sha256')
    # check if the provided email already exists
    user = Utilisateur.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'message': 'Email already exists'}), 400
    new_user = Utilisateur(nom_complet=data['nom_complet'], email=data['email'], mot_de_passe=hashed_password, numero_de_telephone=data['numero_de_telephone'], information_bancaires=data['information_bancaires'], solde=0)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Utilisateur.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.mot_de_passe, data['mot_de_passe']):
        session['logged_in'] = True
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully', "uid" : user.id, "username" : user.nom_complet}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/update', methods=['PUT'])
def update():
    if 'logged_in' in session and session['logged_in']:
        data = request.get_json()
        user = Utilisateur.query.get(session['user_id'])
        user.nom_complet = data.get('nom_complet', user.nom_complet)
        user.email = data.get('email', user.email)
        user.numero_de_telephone = data.get('numero_de_telephone', user.numero_de_telephone)
        user.information_bancaires = data.get('information_bancaires', user.information_bancaires)
        db.session.commit()
        return jsonify({'message': 'Updated successfully'}), 200
    else:
        return jsonify({'message': 'You are not logged in'}), 401

@app.route('/delete', methods=['DELETE'])
def delete():
    if 'logged_in' in session and session['logged_in']:
        user = Utilisateur.query.get(session['user_id'])
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'}), 200
    else:
        return jsonify({'message': 'You are not logged in'}), 401

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    # if 'logged_in' in session and session['logged_in']:
    #     if session['user_id'] == 1 or session['user_id'] == id:
    user = Utilisateur.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict()), 200
    # return {"message": "You are not authorized to view this page"}, 403

@app.route('/user/<id>/ajouterSolde/<somme>', methods=['POST'])
def ajouter_solde(id, somme):
    user = Utilisateur.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    if user.solde is None:
        user.solde = 0

    user.solde += int(somme)
    db.session.commit()

    return jsonify({'message': 'Solde ajouté avec succès'}), 200

@app.route('/user/<id>/payInvoice/<id_invoice>/<sum>', methods=['POST'])
def pay_invoice(id, id_invoice, sum):
    # Fetch the user from the database
    user = Utilisateur.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Fetch the invoice from the database
    invoice = Facture.objects(id=id_invoice).first()
    if not invoice:
        return jsonify({'message': 'Invoice not found'}), 404
    # if sum is float then convert it to int
    if '.' in sum:
        sum = sum.split('.')[0]
        
    sum = int(sum)
    # Check if the user has enough balance to pay the invoice
    if user.solde < sum:
        return jsonify({'message': 'Insufficient balance'}), 400

    # Deduct the sum from the user's balance
    user.solde -= sum

    # Mark the invoice as paid
    invoice.regle = True

    # Save the changes to the database
    db.session.commit()
    invoice.save()

    return jsonify({'message': 'Invoice paid successfully'}), 200


@app.route('/users', methods=['GET'])
def get_users():
    # if 'logged_in' in session and session['logged_in']:
        # if session[é'user_id'] == 1:    
    users = Utilisateur.query.all()
    users = [user.to_dict() for user in users]
    return jsonify(users), 200
    return {"message": "You are not authorized to view this page"}, 403

# create admin routes that let me access to all cars, all invoices, all entries and exits and all users
# create a route that let me see all the cars of a user
@app.route('/users/<id>/cars', methods=['GET'])
def get_user_cars(id):
    if 'logged_in' in session and session['logged_in']:
        if session['user_id'] == 1:
            cars = Vehicule.objects(propietaire=id)
            cars = [car.to_dict() for car in cars]
            return jsonify(cars), 200
    return {"message": "You are not authorized to view this page"}, 403

# create a route that let me see all the entries and exits of a user
@app.route('/users/<id>/entrees_sorties', methods=['GET'])
def get_user_entrees_sorties(id):
    if 'logged_in' in session and session['logged_in']:
        if session['user_id'] == 1:
            entrees_sorties = Entree_Sortie.query.filter_by(id_utilisateur=id).all()
            entrees_sorties = [entree_sortie.to_dict() for entree_sortie in entrees_sorties]
            return jsonify(entrees_sorties), 200
    return {"message": "You are not authorized to view this page"}, 403

# create a route that let me see all the invoices of a user
@app.route('/users/<id>/invoices', methods=['GET'])
def get_user_invoices(id):
    # if 'logged_in' in session and session['logged_in']:
    #     if session['user_id'] == 1:
    invoices = Facture.objects(id_utilisateur=int(id))
    invoices = [invoice.to_dict() for invoice in invoices]
    return jsonify(invoices), 200
    # return {"message": "You are not authorized to view this page"}, 403

# create a route that will let me flush the database
@app.route('/flush', methods=['DELETE'])
def flush():
    if 'logged_in' in session and session['logged_in']:
        if session['user_id'] == 1:
            db.drop_all()
            db.create_all()
            return {"message": "Database flushed successfully"}, 200
    return {"message": "You are not authorized to view this page"}, 403

# create a route that will show me all the cars
@app.route('/cars', methods=['GET'])
def get_cars():
    if 'logged_in' in session and session['logged_in']:
        if session['user_id'] == 1:
            cars = Vehicule.objects()
            cars = [car.to_dict() for car in cars]
            return jsonify(cars), 200
    return {"message": "You are not authorized to view this page"}, 403


# create a route the will synchronize 
@app.route('/syncES', methods=['POST'])
def sync():
    # if 'logged_in' in session and session['logged_in']:
    #     if session['user_id'] == 1:
    #         # get all the cars from the mongo database
    try:
        get_entree_sortie()
        return {"message": "Synchronized successfully"}, 200
    except Exception as e:
        print(e)
        return {"message": "An error occured"}, 500
    
@app.route('/syncFactures', methods=['POST'])
def syncFactures():
    try :
        sync_factures()
        return {"message": "Factures synced successfully"}, 200
    except Exception as e:
        print(e)
        return {"message": "An error occured"}, 500



@app.route('/syncVehicule', methods=['POST'])
def syncVehicule():
    uri = "mongodb+srv://kfsaidani:saidani2003@cluster0.adfmw12.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    try:
        migrate_data('vehicule', uri)
        return {"message": "Vehicules synced successfully"}, 200
    except Exception as e:
        print(e)
        return {"message": "An error occured"}, 500
        

@app.route('/synchronize', methods=['POST'])
def synchronize():
    try:
        # Sync ES
        get_entree_sortie()

        # Sync Factures
        sync_factures()

        # Sync Vehicule
        uri = "mongodb+srv://kfsaidani:saidani2003@cluster0.adfmw12.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        migrate_data('vehicule', uri)

        return {"message": "Synchronized successfully"}, 200
    except Exception as e:
        print(e)
        return {"message": "An error occured"}, 500