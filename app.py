from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

pokedex = {
    "Comune": ["Bulbasaur", "Charmander", "Squirtle", "Eevee", "Snorlax"],
    "Non Comune": ["Gengar", "Dragonite", "Cyndaquil", "Umbreon", "Piplup"],
    "Rara": ["Pikachu", "Togepi", "Ampharos", "Latios", "Garchomp"],
    "Ultra Rara": ["Mewtwo"]
}

valori_punti = {
    "Comune": 1,
    "Non Comune": 2,
    "Rara": 3,
    "Ultra Rara": 10,
}

giocatore = {
    "punti": 100,
    "collezione": []
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

    if len(pokedex[rarita]) > 0:
        carta = random.choice(pokedex[rarita])
        return carta, rarita
    return None, None

@app.route("/")
def menu_principale():
    return render_template("menu.html", punti=giocatore["punti"])

@app.route("/apri_pacchetto", methods=["POST"])
def apri_pacchetto():
    if giocatore["punti"] < 10:
        return redirect(url_for("menu_principale"))

    giocatore["punti"] -= 10
    pacchetto = []

    for i in range(5):
        carta, rarita = pesca_carta()
        if carta:
            giocatore["collezione"].append({"nome": carta, "rarita": rarita})
            giocatore["punti"] += valori_punti[rarita]
            pacchetto.append({"nome": carta, "rarita": rarita})

    return render_template("pacchetto.html", pacchetto=pacchetto, punti=giocatore["punti"])

@app.route("/collezione")
def mostra_collezione():
    return render_template("collezione.html", collezione=giocatore["collezione"])

if __name__ == "__main__":
    app.run(debug=True)
