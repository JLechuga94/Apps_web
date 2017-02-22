from flask import Flask,request,render_template,jsonify
import requests
import logging
app=Flask(__name__)

@app.route("/home")
def bienvenida():
    return render_template("home_locations.html",descripcion="Que onda!")

@app.route("/<radio>/<tipo>/<zona>")
def places_radio(radio,tipo,zona):
    params=info_places(radio,tipo,zona)
    return render_template("locations.html",**params)

@app.route("/api/<radio>/<tipo>/<zona>")
def api_places_radio(radio,tipo,zona):
    params=info_places(radio,tipo,zona)
    return jsonify(params)


def info_places(radio,tipo,zona):
    lola={"Polanco":"19.434008,-99.197064",
    "Condesa":"19.414966,-99.177107",
    "Coyoacán":"19.349282, -99.163769",
    "Lomas":"19.424180, -99.211688",
    "Roma":"19.415601, -99.165373",
    "Centro":"19.432842, -99.133834",
    "San Ángel":"19.345622, -99.190686",
    "Santa Fe":"19.386837, -99.251676",
    "Nápoles":"19.393414, -99.174996"
    }
    params={"location":lola[zona],"radius":radio,"type":tipo,
    "key":"AIzaSyAznRxeRR8KWFmNKbNmV5W0pqpCHb39yZ0"
    }
    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?",params=params)

    if response.status_code==200:
        nombre=[]
        ubicacion=[]
        rate=[]
        response_dict=response.json()
        results=response_dict["results"]

        for i in range(len(results)):
            nombre.append(results[i]["name"])
            ubicacion.append(results[i]["vicinity"])
            #rate.append(results[i]["rating"])
        #print(response.text)

    else:
        nombre,ubicacion,rate=[],[],[]
        print("Error!!!")

    params={"nombres":nombre,"ubicaciones":ubicacion,"ratings":rate}
    return params

#Warth de Python
if __name__=="__main__":
    app.run(debug=True)
