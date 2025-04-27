from flask import Flask, render_template, request, redirect, url_for, session
import random
import csv

app = Flask(__name__)
app.secret_key = 'supersecretkey'  


def carica_pokemon():
    pokedex = {
        "Comune": [],
        "Non Comune": [],
        "Rara": [],
        "Ultra Rara": []
    }
    try:
        with open("pokemon (1).csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)   
            for row in reader:
                nome = row["Nome"]
                rarita = row["Rarità"]
                if rarita in pokedex:
                    pokedex[rarita].append(nome)
    except FileNotFoundError:
        print("Errore: Il file 'pokemon (1).csv' non è stato trovato.")
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")
    return pokedex


pokedex = carica_pokemon()


valori_punti = {
    "Comune": 1,
    "Non Comune": 3,
    "Rara": 7,
    "Ultra Rara": 15
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

    if pokedex[rarita]:
        return random.choice(pokedex[rarita]), rarita
    else:
        return None, None



@app.route("/")
def menu_principale():
    if 'punti' not in session:
        session['punti'] = 100
        session['collezione'] = []
    return render_template("index.html")

@app.route("/apri_pacchetto")
def apri_pacchetto():
    if session['punti'] < 10:
        return redirect(url_for('menu_principale'))

    session['punti'] -= 10
    nuovo_pacchetto = []

    for _ in range(5):
        carta, rarita = pesca_carta()
        if carta:
            session['collezione'].append([carta, rarita])
            session['punti'] += valori_punti[rarita]
            nuovo_pacchetto.append((carta, rarita))

    session.modified = True
    return render_template("apri_pacchetto.html", pacchetto=nuovo_pacchetto)

@app.route("/collezione")
def mostra_collezione():
    return render_template("collezione.html", collezione=session.get('collezione', []))

@app.route("/punti")
def mostra_punti():
    return render_template("punti.html", punti=session.get('punti', 0))

if __name__ == "__main__":
    app.run(debug=True)
