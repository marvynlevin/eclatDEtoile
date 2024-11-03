#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__, template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    mycursor.execute("DROP TABLE IF EXISTS ligne_panier;")
    mycursor.execute("DROP TABLE IF EXISTS ligne_commande;")
    mycursor.execute("DROP TABLE IF EXISTS commentaire;")
    mycursor.execute("DROP TABLE IF EXISTS note;")
    mycursor.execute("DROP TABLE IF EXISTS commande;")
    mycursor.execute("DROP TABLE IF EXISTS etat;")
    mycursor.execute("DROP TABLE IF EXISTS utilisateur;")
    mycursor.execute("DROP TABLE IF EXISTS peinture;")
    mycursor.execute("DROP TABLE IF EXISTS categorie;")
    mycursor.execute("DROP TABLE IF EXISTS couleur;")


    sql = '''CREATE TABLE IF NOT EXISTS categorie (
    id_categorie INT AUTO_INCREMENT NOT NULL,
    nom_categorie VARCHAR(64) NOT NULL,

    PRIMARY KEY (id_categorie)
);
'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS couleur (
    id_couleur INT AUTO_INCREMENT NOT NULL,
    nom_couleur VARCHAR(128) NOT NULL,

    PRIMARY KEY (id_couleur)
);'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS peinture (
    id_peinture INT AUTO_INCREMENT,
    nom_peinture VARCHAR(50),
    volume_pot DECIMAL(5, 2),
    numero_melange INT,
    prix_peinture DECIMAL(15, 2),
    couleur_id INT,
    categorie_id INT,
    fournisseur VARCHAR(50),
    marque VARCHAR(50),
    image VARCHAR(128),
    description VARCHAR(2048),
    stock INT,

    PRIMARY KEY (id_peinture),
    FOREIGN KEY (couleur_id) REFERENCES couleur (id_couleur),
    FOREIGN KEY (categorie_id) REFERENCES categorie (id_categorie)
);'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(320),
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    est_actif CHAR(1),

    PRIMARY KEY (id_utilisateur)
);'''

    #la taille maximal d'un mail est de 320 caractères, voir ci-dessous

    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS etat (
    id_etat INT AUTO_INCREMENT,
    libelle VARCHAR(50),
    PRIMARY KEY (id_etat)
);
'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS commande (
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    utilisateur_id INT,
    etat_id INT,
    PRIMARY KEY (id_commande),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
);'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS ligne_commande (
        commande_id INT,
        peinture_id INT,
        prix DECIMAL(15, 2),
        quantite INT,
        PRIMARY KEY (commande_id, peinture_id),
        FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
        FOREIGN KEY (peinture_id) REFERENCES peinture(id_peinture)
    );'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS ligne_panier (
        utilisateur_id INT,
        peinture_id INT,
        quantite INT,
        date_ajout DATE,
        PRIMARY KEY (utilisateur_id, peinture_id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (peinture_id) REFERENCES peinture(id_peinture)
    );'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS commentaire (
    date_publication DATETIME,
    peinture_id      INT,
    utilisateur_id   INT,
    commentaire      VARCHAR(255),
    valider          INT,
    PRIMARY KEY (date_publication, peinture_id, utilisateur_id),
    FOREIGN KEY (peinture_id) REFERENCES peinture (id_peinture),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS note (
        peinture_id INT,
        utilisateur_id INT,
        note DECIMAL(2,1),
        PRIMARY KEY (peinture_id, utilisateur_id),
        FOREIGN KEY (peinture_id) REFERENCES peinture (id_peinture),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
    );'''
    mycursor.execute(sql)




    sql = '''INSERT INTO etat (libelle) VALUES ('en attente'), ('expédié'), ('validé'), ('confirmé');'''
    mycursor.execute(sql)

    sql = """INSERT INTO categorie (nom_categorie) VALUES
    ('Peintures d''Intérieur'),
    ('Peintures d''Extérieur'),
    ('Peintures Spécialisées'),
    ('Apprêt'),
    ('Peintures Artistiques'),
    ('Peintures Écologiques');"""
    mycursor.execute(sql)

    sql = '''INSERT INTO couleur (nom_couleur) VALUES
    ('Chartreuse'),
    ('Bleu'),
    ('Viva magenta'),
    ('Jaune');'''
    mycursor.execute(sql)

    sql = '''INSERT INTO peinture (nom_peinture, volume_pot, numero_melange, prix_peinture, couleur_id, categorie_id, fournisseur, marque, image, description, stock) VALUES
    ('Bouclier Bleu Extérieur', 1.0, 102, 15.50, 2, 1, 'Eclat d''étoile', 'Eclat d''étoile', 'bouclier_bleu_exterieur.png', 'Le Bouclier Bleu Extérieur est votre allié ultime contre les éléments. Sa teinte bleue profonde et riche ajoute une touche de sérénité à vos extérieurs, tandis que sa formule résistante aux intempéries offre une protection durable contre la pluie, le vent et le soleil. Que ce soit pour les portes, les fenêtres ou les clôtures, cette peinture assure une finition impeccable et une couleur éclatante qui dure.', 8),
    ('Vert Écologique', 3.0, 103, 30.75, 3, 2, 'Team Chartreuse', 'Team Chartreuse', 'vert_ecologique.png', 'Le Vert Écologique est un choix conscient pour les amoureux de la nature. Sa teinte verte rafraîchissante apporte une bouffée d''air frais à votre environnement, tandis que sa formule respectueuse de l''environnement garantit une empreinte écologique réduite. Que ce soit pour les murs intérieurs ou extérieurs, cette peinture offre une couverture exceptionnelle et une finition durable, pour des résultats durables et magnifiques.', 11),
    ('Apprêt Jaune Universel', 2.0, 104, 20.00, 4, 2, 'Eclat d''étoile', 'Eclat d''étoile', 'appret_jaune_universel.png', 'L''Apprêt Jaune Universel est votre premier pas vers un résultat parfait. Sa teinte jaune lumineuse offre une base idéale pour une variété de couleurs, assurant une adhérence optimale et une finition uniforme. Que ce soit pour les murs intérieurs ou extérieurs, cette peinture préparatoire vous permet de créer une surface lisse et prête à accueillir votre couleur préférée.', 58),
    ('Harmonie Intérieure Rouge', 1.5, 105, 18.99, 1, 3, 'Bricodeco', 'Team Chartreuse', 'harmonie_interieure_rouge.png', 'L''Harmonie Intérieure Rouge crée une atmosphère chaleureuse et accueillante dans votre maison. Sa teinte rouge vibrante évoque la passion et l''énergie, tandis que sa formule de haute qualité offre une couverture exceptionnelle et une finition durable. Que ce soit pour un salon, une salle à manger ou une chambre à coucher, cette peinture ajoute une touche de glamour à votre décor intérieur.', 26),
    ('ProShield Bleu Extérieur', 2.5, 106, 25.50, 2, 3, 'Bricodeco', 'Team Chartreuse', 'proshield_bleu_exterieur.png', 'Le ProShield Bleu Extérieur est votre gardien contre les éléments. Sa teinte bleue profonde et riche ajoute une touche de calme à vos extérieurs, tandis que sa formule résistante aux intempéries offre une protection maximale contre la pluie, le vent et les rayons UV. Que ce soit pour les portes, les fenêtres ou les clôtures, cette peinture assure une finition impeccable et une couleur durable qui dure des années.', 3),
    ('Peinture Écologique GreenTech', 1.0, 107, 15.75, 3, 4, 'Eclat d''étoile', 'Eclat d''étoile', 'peinture_ecologique_greentech.png', 'La Peinture Écologique GreenTech est votre choix pour un intérieur sain et respectueux de l''environnement. Sa formule à base d''ingrédients naturels offre une alternative durable aux peintures traditionnelles, tout en offrant une couleur riche et une finition impeccable. Que ce soit pour les murs de votre salon, de votre chambre ou de votre bureau, cette peinture écologique crée un environnement sain et sûr pour votre famille.', 89),
    ('Premium Jaune Extérieur', 3.0, 108, 32.00, 4, 4, 'Team Chartreuse', 'Team Chartreuse', 'premium_jaune_exterieur.png', 'Le Premium Jaune Extérieur est le rayon de soleil dont vos extérieurs ont besoin. Sa teinte jaune lumineuse apporte de la joie et de la luminosité à n''importe quel espace, tandis que sa formule résistante aux intempéries offre une protection durable contre les éléments. Que ce soit pour les murs, les portes ou les volets, cette peinture assure une finition impeccable et une couleur éclatante qui dure.', 7),
    ('Harmonie Intérieure Rouge', 2.0, 109, 21.99, 1, 5, 'Adam Peinture', 'Team Chartreuse', 'harmonie_interieure_rouge.png', 'L''Harmonie Intérieure Rouge apporte une touche de passion à votre décor intérieur. Sa teinte rouge profonde et riche crée une ambiance chaleureuse et accueillante dans n''importe quelle pièce, tandis que sa formule de haute qualité offre une couverture exceptionnelle et une finition durable. Que ce soit pour un salon, une salle à manger ou une chambre à coucher, cette peinture ajoute une touche de glamour à votre espace de vie.', 4),
    ('Ciel Étoilé Bleu', 1.5, 110, 17.50, 2, 5, 'Adam Peinture', 'Team Chartreuse', 'ciel_etoile_bleu.png', 'Le Ciel Étoilé Bleu capture la beauté et la tranquillité du ciel nocturne. Sa teinte bleue douce et paisible crée une atmosphère relaxante dans n''importe quelle pièce. Que ce soit pour une chambre, un salon ou un bureau, cette peinture ajoute une touche de sérénité à votre espace. Avec sa formule de haute qualité, elle offre une couverture exceptionnelle et une finition durable. Laissez-vous emporter par la magie des étoiles avec cette peinture magnifique.', 56),
    ('Éclat Vert Artistique', 2.5, 111, 28.75, 3, 6, 'Adam Peinture', 'Team Chartreuse', 'eclat_vert_artistique.png', 'L''Éclat Vert Artistique apporte une touche de nature et de fraîcheur à votre espace. Sa teinte verte vibrante évoque la vie et la croissance, créant une ambiance dynamique et inspirante. Que ce soit pour un salon, une salle à manger ou un bureau, cette peinture ajoute une touche artistique à votre décoration intérieure. Avec sa formule de haute qualité, elle offre une couverture exceptionnelle et une finition durable, pour des résultats époustouflants à chaque fois.', 23),
    ('Apprêt Gris Universel', 2.0, 112, 22.00, 4, 6, 'Team Chartreuse', 'Team Chartreuse', 'appret_gris_universel.png', 'L''Apprêt Gris Universel est le choix idéal pour préparer vos surfaces avant de peindre. Sa teinte grise neutre offre une base parfaite pour une variété de couleurs, assurant une adhérence optimale et une finition uniforme. Que ce soit pour les murs intérieurs ou extérieurs, cette peinture préparatoire vous permet de créer une surface lisse et prête à accueillir votre couleur préférée.', 32),
    ('Lueur Écologique Vert Intérieur', 2.5, 115, 24.75, 3, 5, 'Adam Peinture', 'Team Chartreuse', 'lueur_ecologique_vert_interieur.png', 'La Lueur Écologique Vert Intérieur illumine votre intérieur avec sa couleur verte apaisante et sa formule respectueuse de l''environnement. Conçue pour offrir une couverture exceptionnelle et une finition durable, cette peinture crée une ambiance calme et relaxante dans n''importe quelle pièce. Que ce soit pour les murs de votre salon, de votre chambre ou de votre bureau, cette peinture écologique est le choix parfait pour un intérieur sain et beau.', 7),
    ('Ecru', 1.5, 117, 15.55, 4, 6, 'Adam Peinture', 'Team Chartreuse', 'ecru.png', 'L''Ecru apporte une touche de douceur et d''élégance à votre décor. Sa teinte crème neutre offre une toile de fond polyvalente pour une variété de styles et de palettes de couleurs. Que ce soit pour les murs, les meubles ou les accessoires, cette peinture ajoute une note subtile de sophistication à n''importe quelle pièce. Avec sa formule de haute qualité, elle offre une couverture exceptionnelle et une finition durable, pour des résultats impeccables.', 89),
    ('Chartreuse', 3.5, 127, 32.99, 1, 3, 'Team Chartreuse', 'Team Chartreuse', 'chartreuse.png', 'La Chartreuse est bien plus qu''une simple couleur - c''est une déclaration audacieuse. Sa teinte vert citron éclatante apporte une énergie vibrante à n''importe quel espace, créant une ambiance dynamique et stimulante. Que ce soit pour les murs, les meubles ou les accents, cette peinture ajoute une touche d''audace et de personnalité à votre décoration. Avec sa formule de haute qualité, elle offre une couverture exceptionnelle et une finition durable, pour des résultats éblouissants à chaque fois.', 10);'''
    mycursor.execute(sql)

    sql = '''INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
    (1,'admin','admin@admin.fr',
    'pbkdf2:sha256:600000$olNVM35LlMvBbE12$8e04be309fd45d72c684f5caa3804afbb77bfb3f6bec5fdd5a9a86165cd7092a',
    'ROLE_admin','admin'),
    (2,'client','client@client.fr',
    'pbkdf2:sha256:600000$dYjw0xxqdHAIA1GO$eaef95ecf21a51f50769bb3b45cbc59edebf575bbefe91a52c16b8525a6ed3c2',
    'ROLE_client','client'),
    (3,'client2','client2@client2.fr',
    'pbkdf2:sha256:600000$LLJIBGNbPjJ63uJM$b774cf95df80c722d09f957b1831d82689153544916b460410e2d0de73337db0',
    'ROLE_client','client2');
'''
    mycursor.execute(sql)

    sql = '''INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id)
VALUES  (1, '2024-03-30', 2, 1),
        (2, '2024-03-30', 2, 1),
        (3, '2024-03-30', 2, 1),
        (4, '2024-03-30', 3, 1),
        (5, '2024-03-30', 3, 1),
        (6, '2024-03-30', 2, 1);'''
    mycursor.execute(sql)

    sql = '''
    INSERT INTO ligne_commande (commande_id, peinture_id, prix, quantite)
VALUES  (5, 1, 15.50, 1),
        (5, 2, 30.75, 1),
        (5, 3, 20.00, 1),
        (5, 4, 18.99, 1),
        (5, 5, 25.50, 2),
        (5, 6, 15.75, 1),
        (5, 7, 32.00, 1),
        (5, 8, 21.99, 1),
        (5, 9, 17.50, 1),
        (5, 10, 28.75, 1),
        (5, 11, 22.00, 1),
        (5, 12, 24.75, 1),
        (5, 13, 15.55, 1),
        (5, 14, 32.99, 1),
        (6, 1, 15.50, 1),
        (6, 2, 30.75, 1),
        (6, 3, 20.00, 1),
        (6, 4, 18.99, 1),
        (6, 5, 25.50, 1),
        (6, 6, 15.75, 1),
        (6, 7, 32.00, 2),
        (6, 8, 21.99, 2),
        (6, 9, 17.50, 2),
        (6, 13, 15.55, 1),
        (6, 14, 32.99, 1);'''
    mycursor.execute(sql)

    sql = '''INSERT INTO note (peinture_id, utilisateur_id, note)
    VALUES  (1, 2, 4.0),
            (1, 3, 1.0),
            (2, 2, 4.0),
            (3, 2, 2.0),
            (4, 3, 4.6),
            (5, 3, 4.0),
            (6, 2, 3.5),
            (9, 3, 4.0),
            (13, 3, 2.8),
            (14, 2, 5.0),
            (14, 3, 4.0);'''
    mycursor.execute(sql)

    sql = '''INSERT INTO commentaire (date_publication, peinture_id, utilisateur_id, commentaire, valider)
VALUES  ('2024-03-30 17:14:17', 1, 1, 'Avisadmin1', 1),
        ('2024-03-30 17:14:17', 1, 2, 'avis1', 1),
        ('2024-03-30 17:14:29', 2, 2, 'Avis2', 0),
        ('2024-03-30 17:14:33', 2, 2, 'Avis3', 0),
        ('2024-03-30 17:14:45', 3, 2, 'Avis4', 0),
        ('2024-03-30 17:14:49', 3, 2, 'Avis5', 0),
        ('2024-03-30 17:14:51', 3, 2, 'Avis6', 0),
        ('2024-03-30 17:14:54', 3, 2, 'Avis7', 0),
        ('2024-03-30 17:15:11', 6, 2, 'Avis8', 0),
        ('2024-03-30 17:15:15', 6, 2, 'Avis9', 0),
        ('2024-03-30 17:15:41', 14, 2, 'Avis10', 0),
        ('2024-03-30 17:15:44', 14, 2, 'Avis11', 0),
        ('2024-03-30 17:15:48', 14, 2, 'Avis12', 0),
        ('2024-03-30 17:15:51', 14, 2, 'Avis13', 0),
        ('2024-03-30 17:15:56', 14, 2, 'Avis14', 0),
        ('2024-03-30 17:16:58', 1, 3, 'Avis15', 1),
        ('2024-03-30 17:17:07', 1, 1, 'Avisadmin2', 1),
        ('2024-03-30 17:17:07', 1, 3, 'Avis17', 1),
        ('2024-03-30 17:17:20', 5, 3, 'Avis19', 0),
        ('2024-03-30 17:17:24', 5, 3, 'Avis20', 0),
        ('2024-03-30 17:17:29', 5, 3, 'Avis21', 0),
        ('2024-03-30 17:17:39', 4, 3, 'Avis22', 0),
        ('2024-03-30 17:17:55', 9, 3, 'Avis23', 0),
        ('2024-03-30 17:18:07', 14, 3, 'Avis26', 0),
        ('2024-03-30 17:18:13', 14, 3, 'Avis27', 0),
        ('2024-03-30 17:18:23', 13, 3, 'Avis30', 0),
        ('2024-03-30 17:18:27', 13, 3, 'Avis31', 0);'''
    mycursor.execute(sql)


    get_db().commit()
    return redirect('/')
