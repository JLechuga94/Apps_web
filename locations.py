from flask import Flask,request,render_template,jsonify
import requests
import logging
app=Flask(__name__)

@app.route("/home")
def bienvenida():
    return render_template("home_locations.html")

@app.route("/<radio>/<tipo>/<zona>")
def places_radio(radio,tipo,zona):
    params=info_places(radio,tipo,zona)
    return render_template("locations.html",type=tipo,zone=zona,**params)

@app.route("/<tipo>")
def lugares_grid(tipo):
    return render_template("lugares_int.html",type=tipo)


@app.route("/api/<radio>/<tipo>/<zona>")
def api_places_radio(radio,tipo,zona):
    params=info_places(radio,tipo,zona)
    return jsonify(params)

@app.route("/api/imagen/<radio>/<tipo>/<zona>")
def photos_places(radio,tipo,zona):
    params=info_places(radio,tipo,zona)
    params_photos=params["photos"]
    return jsonify(params_photos)

def info_places(radio,tipo,zona):
    lola={"Polanco":"19.434008,-99.197064",
    "Condesa":"19.414966,-99.177107",
    "Coyoacán":"19.349282, -99.163769",
    "Roma":"19.415601, -99.165373",
    "Centro":"19.432842, -99.133834",
    "San Ángel":"19.345622, -99.190686",
    "Santa Fe":"19.386837, -99.251676",
    "Nápoles":"19.393414, -99.174996",
    "Reforma":"19.427170, -99.167751"
    }
    params={"location":lola[zona],"radius":radio,"type":tipo,
    "key":"AIzaSyAznRxeRR8KWFmNKbNmV5W0pqpCHb39yZ0",
    }
    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?",params=params)

    if response.status_code==200:
        nombre=[]
        ubicacion=[]
        rate=[]
        photo=[]
        mapa=[]
        response_dict=response.json()
        results=response_dict["results"]

        for result in results:
            nombre.append(result["name"])
            ubicacion.append(result["vicinity"])

            if "photos" in result:
                photo.append("https://maps.googleapis.com/maps/api/place/photo?maxwidth=600&maxheight=500&photoreference="+result["photos"][0]["photo_reference"]+"&key=AIzaSyAznRxeRR8KWFmNKbNmV5W0pqpCHb39yZ0")
                mapa.append(result["photos"][0]["html_attributions"][0][9:74])

            else:
                photo.append("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Blank_map_of_Mexico.svg/800px-Blank_map_of_Mexico.svg.png")
                mapa.append("https://www.google.com.mx/maps/")

            if "rating" in result:
                rate.append(result["rating"])
            else:
                rate.append(0)

        #print(response.text)

    else:
        nombre,ubicacion,rate,photo=[],[],[]
        print("Error!!!")

    params={"nombres":nombre,"ubicaciones":ubicacion,"ratings":rate,"photos":photo,"mapas":mapa}
    return params

#Warth de Python
if __name__=="__main__":
    app.run(debug=True)
