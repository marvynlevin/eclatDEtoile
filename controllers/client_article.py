#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():             # remplace client_index
    mycursor = get_db().cursor()
    id_client = session.get('id_user', '')

    sql = '''
    SELECT
    p.id_peinture AS id_article,
    p.nom_peinture AS nom,
    p.volume_pot,
    COALESCE(n.nb_notes, 0) AS nb_notes,
    CASE
        WHEN n.nb_notes > 0 THEN n.moyenne_notes
        ELSE NULL
    END AS moy_notes,
    COALESCE(com.nb_avis, 0) AS nb_avis,
    p.numero_melange,
    p.prix_peinture AS prix,
    p.couleur_id,
    p.categorie_id,
    p.fournisseur,
    p.marque,
    p.image,
    c.nom_couleur,
    cat.nom_categorie,
    p.stock
FROM peinture p
JOIN couleur c ON p.couleur_id = c.id_couleur
JOIN categorie cat ON p.categorie_id = cat.id_categorie
LEFT JOIN (
    SELECT peinture_id, COUNT(*) AS nb_notes, AVG(note) AS moyenne_notes
    FROM note
    GROUP BY peinture_id
) n ON p.id_peinture = n.peinture_id
LEFT JOIN (
    SELECT peinture_id, COUNT(*) AS nb_avis
    FROM commentaire
    GROUP BY peinture_id
) com ON p.id_peinture = com.peinture_id
GROUP BY p.id_peinture;
'''

    list_param = []
    condition = []
#
    #if session.get('filter_word', None):
    #    condition.append("nom_peinture LIKE %s")
    #    list_param.append(f"%{session['filter_word']}%")
    #if session.get('filter_prix_min', None) and session.get('filter_prix_max', None):
    #    condition.append("prix_peinture BETWEEN %s AND %s")
    #    list_param.extend([float(session['filter_prix_min']), float(session['filter_prix_max'])])
    #if session.get('filter_couleur', None):
    #    condition.append("couleur_id IN ({})".format(','.join(['%s'] * len(session['filter_couleur']))))
    #    list_param.extend([int(x) for x in session['filter_couleur']])
    #if session.get('filter_categorie', None):
    #    condition.append("categorie_id IN ({})".format(','.join(['%s'] * len(session['filter_categorie']))))
    #    list_param.extend([int(x) for x in session['filter_categorie']])
#
    condition_and = ""
    #if len(condition) > 0:
    #    condition_and = " WHERE " + " AND ".join(condition)
    ## utilisation du filtre
    #sql3 = ''' prise en compte des commentaires et des notes dans le SQL    '''  # TODO
    mycursor.execute(sql+condition_and, tuple(list_param))
    articles = mycursor.fetchall()
    print(articles)

    # pour le filtre
    sql2 = '''
    SELECT 
        id_couleur,
        nom_couleur AS libelle
    FROM couleur;
    '''
    mycursor.execute(sql2)
    types_couleur = mycursor.fetchall()
    sql2 = '''
    SELECT 
        id_categorie,
        nom_categorie AS libelle
    FROM categorie;
    '''
    mycursor.execute(sql2)
    categorie = mycursor.fetchall()

    # Fetch des articles du panier
    sql = '''SELECT
    l.*,
    p.prix_peinture AS prix,
    p.stock AS stock,
    p.nom_peinture AS nom
FROM
    ligne_panier l
LEFT JOIN peinture p on l.peinture_id = p.id_peinture
WHERE
    l.utilisateur_id = %s;'''

    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:

        sql = '''SELECT
    SUM(p.prix_peinture * l.quantite) as total
FROM
    ligne_panier l
LEFT JOIN peinture p on l.peinture_id = p.id_peinture
WHERE
    l.utilisateur_id = %s;'''

        mycursor.execute(sql, id_client)
        res = mycursor.fetchall()
        if res and len(res) > 0:
            prix_total = res[0]['total']
    else:
        prix_total = None  # FIXME wtf?
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           # , prix_total=prix_total
                           , filtre_couleur=types_couleur
                           , filtre_categorie=categorie
                           )
