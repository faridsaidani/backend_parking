from app import db, mongo

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_complet = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    numero_de_telephone = db.Column(db.String(40), nullable=False)
    information_bancaires = db.Column(db.String(255), nullable=True)
    solde = db.Column(db.Integer, nullable=True)
    def to_dict(self):
        return {
            'id': self.id,
            'nom_complet': self.nom_complet,
            'email': self.email,
            'numero_de_telephone': self.numero_de_telephone,
            'information_bancaires': self.information_bancaires,
            'solde' : self.solde
        }

class Facture(mongo.Document):
    id_utilisateur = mongo.IntField(required=True)
    numero_immatriculation = mongo.StringField(required=True)
    heure_entree = mongo.DateTimeField(required=True)
    heure_sortie = mongo.DateTimeField(required=True)
    tarif = mongo.FloatField(required=True)
    total_cost = mongo.FloatField(required=True)
    regle = mongo.BooleanField(default=False)
    def to_dict(self):
        return {
            'id': str(self.id),
            'id_utilisateur': self.id_utilisateur,
            'heure_entree': self.heure_entree,
            'heure_sortie': self.heure_sortie,
            'tarif': self.tarif,
            'total_cost': self.total_cost,
            'numero_immatriculation': self.numero_immatriculation,
            'regle': self.regle,
        }

class Entree_Sortie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_immatriculation = db.Column(db.String(20), nullable=False)
    heure_entree = db.Column(db.DateTime, nullable=False)
    heure_sortie = db.Column(db.DateTime, nullable=False)
    photo_entree = db.Column(db.String(255))
    photo_sortie = db.Column(db.String(255))
    def to_dict(self):
        return {
            'id': self.id,
            'numero_immatriculation': self.numero_immatriculation,
            'heure_entree': self.heure_entree.isoformat(),
            'heure_sortie': self.heure_sortie.isoformat(),
            'photo_entree': self.photo_entree,
            'photo_sortie': self.photo_sortie,
        }


class Vehicule(mongo.Document):
    numero_immatriculation = mongo.StringField(required=True, unique=True)
    marque = mongo.StringField(required=True)
    modele = mongo.StringField(required=True)
    couleur = mongo.StringField(required=True)
    annee = mongo.IntField(required=True)
    photos = mongo.ListField(mongo.StringField(), required=True)
    propietaire = mongo.IntField(required=True)
    def to_dict(self):
        return {
            'numero_immatriculation': self.numero_immatriculation,
            'marque': self.marque,
            'modele': self.modele,
            'couleur': self.couleur,
            'annee': self.annee,
            'photos': self.photos,
            'propietaire': self.propietaire,
        }

