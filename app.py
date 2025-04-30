from flask import Flask, render_template, redirect, url_for, request
import random
import pandas as pd

app = Flask(__name__)

dataframe = pd.read_csv("pokemon (1).csv")
dataframe.columns = dataframe.columns.str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

valori_punti = {
    "Comune": 1,
    "Non Comune": 2,
    "Rara": 3,
    "Ultra Rara": 10,
}

collezione = []

giocatore = {
    "punti": 100
}

def pesca_carta():
    probabilita = random.randint(1, 100)
    if probabilita <= 1:
        rarita = "Ultra Rara"
    elif probabilita <= 10:
        rarita = "Rara"
    elif probabilita <= 30:
        rarita = "Non Comune"
    else:
        rarita = "Comune"
    
    carta = random.choice(dataframe["nome"].tolist()) 
    return carta, rarita

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if giocatore["punti"] < 10:
            return render_template("index.html", punti=giocatore["punti"], collezione=collezione, pacchetto=None, errore="Punti insufficienti!")
        
        giocatore["punti"] -= 10
        pacchetto = []

        for i in range(5):
            carta, rarita = pesca_carta()
            if carta:
                collezione.append({"nome": carta, "rarita": rarita})
                giocatore["punti"] += valori_punti[rarita]
                pacchetto.append({"nome": carta, "rarita": rarita})

        return render_template("index.html", punti=giocatore["punti"], collezione=collezione, pacchetto=pacchetto, errore=None)

    return render_template("index.html", punti=giocatore["punti"], collezione=collezione, pacchetto=None, errore=None)

@app.route("/collezione")
def mostra_collezione():
    return render_template("collezione.html", collezione=collezione)  

if __name__ == "__main__":
    app.run(debug=True, port=5000)
