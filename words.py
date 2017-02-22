from flask import Flask,request,render_template,jsonify
import requests
import logging
app=Flask(__name__)

@app.route("/home")
def home():
    desc="Este es el home de tu aplicación web."
    return render_template("home_words.html",title="Home app",descripcion=desc)

@app.route("/word/<word>")
def def_palabra(word):
    params=get_params_for_word(word)
    return render_template("words.html",title="Word app",**params)

@app.route("/api/word/<word>")
def api_words(word):
    params=get_params_for_word(word)
    return jsonify(params)


def get_params_for_word(word):

    headers={
    "app_id":"a53eb00a",
    "app_key":"d08f00869989748024ce748801324ad2"
    }

    response = requests.get("https://od-api.oxforddictionaries.com:443/api/v1/entries/es/"+
    word.lower(), headers=headers)

    if response.status_code==200:
        response_dict=response.json()
        results=response_dict["results"][0]
        lexical_entries=results["lexicalEntries"]
        definitions=[]

        for le in lexical_entries:
            entries=le["entries"]

            for entry in entries:
                senses=entry["senses"]

                for sense in senses:
                    defs=sense["definitions"]

                    for definition in defs:
                        definitions.append(definition)

        print("Response---------------------------\n")
        print(results.keys())
        #print(response.text)

    else:
        definitions=[]
        print("Error!!!")

    params={"nombre":word,"ubicacion":definitions,}
    return params

#Warth de Python
if __name__=="__main__":
    app.run(debug=True)
