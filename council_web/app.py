import os
import json
import threading
import anthropic
from flask import Flask, render_template, request, Response, stream_with_context

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
MODEL = "claude-opus-4-7"

ADVISORS = [
    {
        "id": "contrarian",
        "name": "CONTRARIAN",
        "title": "Fatal Flaw Hunter",
        "icon": "💥",
        "color": "#E53935",
        "border": "#E53935",
        "bg": "#FFF5F5",
        "system": (
            "Du bist der Contrarian-Berater eines 5-köpfigen Expertenrats. "
            "Deine Aufgabe: Identifiziere schonungslos die kritischsten Schwachstellen, "
            "fatalen Fehler und blinden Flecken in jeder Idee. "
            "Sei direkt, präzise, aber respektvoll. Keine falschen Freundlichkeiten — "
            "echte Gefahren brauchen klare Worte. Antworte auf Deutsch, max. 200 Wörter. "
            "Beginne direkt mit der stärksten Kritik."
        ),
    },
    {
        "id": "firstprinciples",
        "name": "FIRST PRINCIPLES",
        "title": "Problem-Zerleger",
        "icon": "🧩",
        "color": "#43A047",
        "border": "#43A047",
        "bg": "#F1F8E9",
        "system": (
            "Du bist der First-Principles-Berater eines 5-köpfigen Expertenrats. "
            "Zerlege jede Idee auf ihre fundamentalen Grundannahmen. "
            "Frage: Was ist wirklich wahr? Was wird nur angenommen? Was sind die Kernelemente? "
            "Denke wie Elon Musk oder Aristoteles — von Grund auf neu denken, "
            "keine Analogien, keine Konventionen. Antworte auf Deutsch, max. 200 Wörter. "
            "Beginne mit der wichtigsten Grundannahme."
        ),
    },
    {
        "id": "expansionist",
        "name": "EXPANSIONIST",
        "title": "Upside-Scout",
        "icon": "🚀",
        "color": "#1E88E5",
        "border": "#1E88E5",
        "bg": "#E3F2FD",
        "system": (
            "Du bist der Expansionist-Berater eines 5-köpfigen Expertenrats. "
            "Deine Aufgabe: Erkunde das maximale Potenzial, ungenutzten Upside und "
            "verborgene Chancen jeder Idee. Denke groß — 10x, nicht 10%. "
            "Zeige Wege auf, die noch niemand gesehen hat. "
            "Sei optimistisch aber realistisch. Antworte auf Deutsch, max. 200 Wörter. "
            "Beginne mit der größten ungenutzten Chance."
        ),
    },
    {
        "id": "outsider",
        "name": "OUTSIDER",
        "title": "Fresh Eye",
        "icon": "👁️",
        "color": "#8E24AA",
        "border": "#8E24AA",
        "bg": "#F3E5F5",
        "system": (
            "Du bist der Outsider-Berater eines 5-köpfigen Expertenrats. "
            "Du bringst den Blick eines völligen Außenseiters — jemand aus einer "
            "völlig anderen Branche, Kultur oder Denkschule. "
            "Benenne, was alle im Raum übersehen, weil sie zu nah dran sind. "
            "Vergleiche mit analogen Situationen aus anderen Bereichen. "
            "Antworte auf Deutsch, max. 200 Wörter. "
            "Beginne mit deiner überraschendsten Beobachtung."
        ),
    },
    {
        "id": "executor",
        "name": "EXECUTOR",
        "title": "Action-Giver",
        "icon": "⚡",
        "color": "#F9A825",
        "border": "#F9A825",
        "bg": "#FFFDE7",
        "system": (
            "Du bist der Executor-Berater eines 5-köpfigen Expertenrats. "
            "Theorie ist dir egal — du willst Ergebnisse. "
            "Gib konkrete, sofort umsetzbare nächste Schritte. "
            "Was genau, bis wann, wer, wie gemessen? "
            "Keine vagen Ratschläge — nur präzise Aktionen mit klaren Erfolgskriterien. "
            "Antworte auf Deutsch, max. 200 Wörter. "
            "Beginne mit dem allerersten konkreten Schritt."
        ),
    },
]


@app.route("/")
def index():
    return render_template("index.html", advisors=ADVISORS)


@app.route("/council", methods=["POST"])
def council():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return Response("data: {\"error\": \"Keine Frage angegeben\"}\n\n", mimetype="text/event-stream")

    def generate():
        results = {}
        lock = threading.Lock()
        threads = []

        def call_advisor(advisor):
            chunks = []
            try:
                with client.messages.stream(
                    model=MODEL,
                    max_tokens=600,
                    system=[
                        {
                            "type": "text",
                            "text": advisor["system"],
                            "cache_control": {"type": "ephemeral"},
                        }
                    ],
                    messages=[{"role": "user", "content": question}],
                ) as stream:
                    for text in stream.text_stream:
                        chunks.append(text)
            except Exception as e:
                chunks.append(f"[Fehler: {e}]")
            with lock:
                results[advisor["id"]] = "".join(chunks)

        for adv in ADVISORS:
            t = threading.Thread(target=call_advisor, args=(adv,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        payload = json.dumps({"results": results})
        yield f"data: {payload}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, port=5050)
