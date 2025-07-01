import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, jsonify
import openai
import logging

# 📌 Configura logging para ver lo que hace tu app
logging.basicConfig(level=logging.DEBUG)

# Configura acceso con scopes de Sheets y Drive
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",  # necesario para escritura :contentReference[oaicite:1]{index=1}
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("My Expenses Sheet").sheet1

app = Flask(__name__)
openai.api_key = "TU_LLAVE_OPENAI"


@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json or {}
    fila = [data.get("fecha", ""), data.get("categoria", ""), data.get("monto", "")]
    logging.debug(f"Intentando añadir fila: {fila}")

    # append_row con table_range para apuntar a A1 y evitar desplazamientos :contentReference[oaicite:2]{index=2}
    sheet.append_row(fila, table_range="A1", value_input_option="USER_ENTERED")
    logging.debug("Fila añadida exitosamente")

    return jsonify({"status": "ok", "fila": fila})


@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    records = sheet.get_all_records()
    return jsonify(records)


if __name__ == "__main__":
    app.run(debug=True)
