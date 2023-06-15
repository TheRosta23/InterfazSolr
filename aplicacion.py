import os
from flask import Flask, render_template, request, send_from_directory, send_file
import requests


app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.form['search']:

        url ="http://localhost:8983/solr/periodicos/select?hl.fl=*&hl.requireFieldMatch=true&hl.snippet=1&hl=true&indent=true&q.op=OR&q=texto%3A"+request.form['search']+"&rows=10&start=0&useParams=&wt=json"
        solar = requests.get(url)
        dataSolar = solar.json()
        totalPeri = dataSolar['response']['numFound']
        




        if dataSolar['response']['numFound'] < 10:

            numPeri = dataSolar['response']['numFound']
            listaDocumentos = []

            for i in range(0, numPeri):
                listaDocumentos.append(dataSolar['response']['docs'][i]['enlace'])



            return render_template('busquedaMenosDiez.html', data = dataSolar, numPeri = numPeri, listaDocumentos = listaDocumentos)
        



        elif dataSolar['response']['numFound'] >= 10:
            url ="http://localhost:8983/solr/periodicos/select?hl.fl=*&hl.requireFieldMatch=true&hl.snippet=1&hl=true&indent=true&q.op=OR&q=texto%3A"+request.form['search']+"&rows="+str(totalPeri)+"&start=0&useParams=&wt=json"
            solar = requests.get(url)
            dataSolar = solar.json()
            numPeri = dataSolar['response']['numFound']

            listaDocumentos = []

            for i in range(0, numPeri):
                listaDocumentos.append(dataSolar['response']['docs'][i]['enlace'])

            


            return render_template('paginaDosCol.html', data = dataSolar, numPeri = numPeri, listaDocumentos = listaDocumentos)




if __name__ == '__main__':
    app.run(debug=True, port=4000)


