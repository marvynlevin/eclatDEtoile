#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()

    labels=[]
    labels2=[]
    values=[]
    values2=[]
    values3=[]

    sql_nb_type_peinture = '''
    SELECT 
    COUNT(DISTINCT id_categorie) AS types_articles_nb 
    FROM categorie;
    '''
    mycursor.execute(sql_nb_type_peinture)
    types_articles_nb = mycursor.fetchone()


    sql_nb_notes = '''
    SELECT COUNT(note) AS nbr_notes
    FROM note;'''
    mycursor.execute(sql_nb_notes)
    nbr_notes = mycursor.fetchone()

    sql_moy_notes = '''
    SELECT AVG(note) AS moy_notes
    FROM note;'''
    mycursor.execute(sql_moy_notes)
    moy_notes = mycursor.fetchone()

    sql_nb_commentaires = '''
    SELECT COUNT(commentaire) AS nbr_commentaires
    FROM commentaire;'''
    mycursor.execute(sql_nb_commentaires)
    nbr_commentaires = mycursor.fetchone()

    lignes = '''
        SELECT
        t.nom_categorie AS libelle,
        t.id_categorie AS id_type_article,
        COUNT(DISTINCT(n.note)) AS nbr_notes,
        AVG(DISTINCT(n.note)) AS moy_notes
    FROM
        note n
    INNER JOIN peinture p ON p.id_peinture = n.peinture_id
    INNER JOIN categorie t ON t.id_categorie = p.categorie_id
    GROUP BY
        t.id_categorie
    ORDER BY t.nom_categorie ASC;'''
    mycursor.execute(lignes)
    lignes = mycursor.fetchall()

    lignes2= '''
    SELECT
        t.nom_categorie AS libelle,
        t.id_categorie AS id_type_article,
        COUNT(DISTINCT(c.commentaire)) AS nbr_commentaires
    FROM
        commentaire c
    INNER JOIN peinture p ON p.id_peinture = c.peinture_id
    INNER JOIN categorie t ON t.id_categorie = p.categorie_id
    GROUP BY
        t.id_categorie
    ORDER BY t.nom_categorie ASC;'''
    mycursor.execute(lignes2)
    lignes2 = mycursor.fetchall()

    if nbr_notes is None:
        nbr_notes = 0

    if nbr_commentaires is None:
        nbr_commentaires = 0

    for ligne in lignes:
        labels.append(ligne['libelle'])
        values.append(ligne['nbr_notes'])
        values2.append(ligne['moy_notes'])

    for ligne in lignes2:
        labels2.append(ligne['libelle'])
        values3.append(ligne['nbr_commentaires'])

    values2_float = [float(value) for value in values2]
    values2 = []
    for value in values2_float:
        values2.append(value)


    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , labels=labels
                           , labels2=labels2
                           , values=values
                           , values2=values2
                           , values3=values3
                           , types_articles_nb=types_articles_nb
                           , nbr_notes=nbr_notes
                           , moy_notes=moy_notes
                           , nbr_commentaires=nbr_commentaires
                           , lignes=lignes
                           , lignes2=lignes2)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


