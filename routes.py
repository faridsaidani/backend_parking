from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import Utilisateur, Facture, Entree_Sortie, Vehicule
from datetime import datetime, timezone
# import str


@app.route('/vehicules', methods=['GET'])
def get_vehicules():
    vehicules = Vehicule.objects()
    return jsonify(vehicules), 200

@app.route('/vehicules', methods=['POST'])
def add_vehicule():
    data = request.get_json()
    vehicule = Vehicule(numero_immatriculation=data['numero_immatriculation'], marque=data['marque'], modele=data['modele'], couleur=data['couleur'], annee=data['annee'], photos=data['photos'], propietaire=data['propietaire'])
    vehicule.save()
    return jsonify(vehicule), 201

@app.route('/vehicules/<numero_immatriculation>', methods=['GET'])
def get_vehicule(numero_immatriculation):
    vehicule = Vehicule.objects(numero_immatriculation=numero_immatriculation).first()
    return jsonify(vehicule), 200

@app.route('/vehicules/<numero_immatriculation>', methods=['PUT'])
def update_vehicule(numero_immatriculation):
    data = request.get_json()
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
    vehicule.delete()
    return jsonify({'message': 'Deleted successfully'}), 200

@app.route('/factures', methods=['GET'])
def get_factures():
    factures = Facture.query.all()
    print(factures)
    factures = [facture.to_dict() for facture in factures]
    return jsonify(factures), 200

@app.route('/factures', methods=['POST'])
def add_facture():
    data = request.get_json()
    new_facture = Facture(id_utilisateur=data['id_utilisateur'], entree_sortie=data['entree_sortie'], montant_a_regler=data['montant_a_regler'], regle=data['regle'])
    db.session.add(new_facture)
    db.session.commit()
    return jsonify(new_facture.to_dict()), 201

@app.route('/factures/<id>', methods=['GET'])
def get_facture(id):
    facture = Facture.query.get(id)
    return jsonify(facture), 200

@app.route('/factures/<id>', methods=['PUT'])
def update_facture(id):
    data = request.get_json()
    facture = Facture.query.get(id)
    facture.id_utilisateur = data.get('id_utilisateur', facture.id_utilisateur)
    facture.entree_sortie = data.get('entree_sortie', facture.entree_sortie)
    facture.montant_a_regler = data.get('montant_a_regler', facture.montant_a_regler)
    facture.regle = data.get('regle', facture.regle)
    db.session.commit()
    return jsonify(facture.to_dict()), 200

@app.route('/factures/<id>', methods=['DELETE'])
def delete_facture(id):
    facture = Facture.query.get(id)
    db.session.delete(facture)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

@app.route('/factures/user/<id_utilisateur>', methods=['GET'])
def get_factures_by_user(id_utilisateur):
    factures = Facture.query.filter_by(id_utilisateur=id_utilisateur).all()
    return jsonify(factures), 200

@app.route('/entrees_sorties', methods=['GET'])
def get_entrees_sorties():
    entrees_sorties = Entree_Sortie.query.all()
    entrees_sorties_dict = [entree_sortie.to_dict() for entree_sortie in entrees_sorties]
    print(entrees_sorties_dict)
    return jsonify(entrees_sorties_dict), 200

@app.route('/entrees_sorties', methods=['POST'])
def add_entree_sortie():
    data = request.get_json()
    heure_entree = datetime.strptime(str(datetime.strptime(data['heure_entree'], '%Y-%m-%dT%H:%M:%SZ')), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    heure_sortie = datetime.strptime(str(datetime.strptime(data['heure_sortie'], '%Y-%m-%dT%H:%M:%SZ')), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    new_entree_sortie = Entree_Sortie(numero_immatriculation=data['numero_immatriculation'], heure_entree=heure_entree, heure_sortie=heure_sortie, photo_entree=data['photo_entree'], photo_sortie=data['photo_sortie'])
    db.session.add(new_entree_sortie)
    db.session.commit()
    return jsonify(new_entree_sortie.to_dict()), 201

@app.route('/entrees_sorties/<id>', methods=['GET'])
def get_entree_sortie(id):
    entree_sortie = Entree_Sortie.query.get(id)
    return jsonify(entree_sortie), 200

# TODO: Fix this (heure_sortie is not defined) 
@app.route('/entrees_sorties/<id>', methods=['PUT'])
def update_entree_sortie(id):
    data = request.get_json()
    entree_sortie = Entree_Sortie.query.get(id)
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
    db.session.delete(entree_sortie)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

@app.route('/entrees_sorties/vehicule/<numero_immatriculation>', methods=['GET'])
def get_entrees_sorties_by_vehicle(numero_immatriculation):
    entrees_sorties = Entree_Sortie.query.filter_by(numero_immatriculation=numero_immatriculation).all()
    return jsonify(entrees_sorties), 200

@app.route('/entrees_sorties/vehicule/<numero_immatriculation>', methods=['DELETE'])
def delete_entrees_sorties_by_vehicle(numero_immatriculation):
    entrees_sorties = Entree_Sortie.query.filter_by(numero_immatriculation=numero_immatriculation).all()
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
    new_user = Utilisateur(nom_complet=data['nom_complet'], email=data['email'], mot_de_passe=hashed_password, numero_de_telephone=data['numero_de_telephone'], information_bancaires=data['information_bancaires'])
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
        return jsonify({'message': 'Logged in successfully'}), 200
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
