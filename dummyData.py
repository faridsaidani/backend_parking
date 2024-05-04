from app import db, app
from faker import Faker
from models import Utilisateur, Facture, Entree_Sortie, Vehicule
from werkzeug.security import generate_password_hash
import pandas as pd

# create an empty DataFrame with columns named email and password
df = pd.DataFrame(columns=['name', 'email', 'password', 'phone_number', 'credit_card_number'])

fake = Faker()

with app.app_context():
    # Generate 15 Utilisateurs
    db.session.add(Utilisateur(nom_complet='Admin', email='farid@gmail.com', mot_de_passe=generate_password_hash('admin', method='sha256'), numero_de_telephone='1234567890', information_bancaires='1234567890'))
    for _ in range(14):
        name = fake.name()
        email = fake.email()
        passw = fake.password()
        num = fake.phone_number()[:15]
        infos = fake.credit_card_number()
        pd.concat([df, pd.DataFrame([name, email, passw, num,infos])], ignore_index=True)
        hashed_pass = generate_password_hash(passw, method='sha256')
        utilisateur = Utilisateur(
            nom_complet=name,
            email=email,
            mot_de_passe=hashed_pass,
            numero_de_telephone=num,
            information_bancaires=infos
        )
        db.session.add(utilisateur)
    db.session.commit()
    
    # Generate 10 Facture
    for _ in range(20):
        id_utilisateur = fake.random_int(min=1, max=15)  # Assuming user IDs are integers
        utilisateur = Utilisateur.query.get(id_utilisateur)
        if utilisateur is not None:
            facture = Facture(
                id_utilisateur=id_utilisateur,
                entree_sortie=fake.random_int(min=1, max=10),  # Assuming entree_sortie IDs are integers
                montant_a_regler=fake.random_number(digits=2, fix_len=True),
                regle=fake.boolean(chance_of_getting_true=50)
            )
            db.session.add(facture)
        else:
            print(f"No utilisateur found with ID {id_utilisateur}")
    db.session.commit()

    # Generate 10 Entree_Sortie
    for _ in range(30):
        entree_sortie = Entree_Sortie(
            numero_immatriculation=fake.license_plate(),
            heure_entree=fake.date_time_this_year(),
            heure_sortie=fake.date_time_this_year(),
            photo_entree=fake.image_url(),
            photo_sortie=fake.image_url()
        )
        db.session.add(entree_sortie)

    # Generate 10 Vehicule documents
    for _ in range(20):
        vehicule = Vehicule(
            numero_immatriculation=fake.unique.license_plate(),
            marque=fake.company(),
            modele=fake.random_element(elements=('Model1', 'Model2', 'Model3')),
            couleur=fake.color_name(),
            annee=fake.year(),
            photos=[fake.image_url() for _ in range(3)],  # Generate 3 image URLs
            propietaire=fake.random_int(min=1, max=15)  # Assuming owner IDs are integers
        )
        vehicule.save()

        db.session.commit()

df.to_csv('dummyUsers.csv', index=False)