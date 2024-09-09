from flask import Flask, request

from parser import Parser

app = Flask(__name__)


@app.route('/info/<flight_id>', methods=["GET"])
def get_info(flight_id):
    p = Parser()
    info = p.data.get(flight_id, {})
    info["status"] = 200 if info else 404
    if info["status"] == 200:
        for key in ["arrival_time", "departure_time"]:
            info[key] = f"{info[key].strftime('%H:%M')}"
        info["success"] = 'success' if info["success"] else 'fail'
        info["flightID"] = flight_id
        info.pop('fligt_time')

    return info


@app.route('/update', methods=["POST"])
def update_file():
    p = Parser()
    try:
        p.add_field(request.data.decode("utf-8"))
        return {"status": 200}
    except Exception as e:
        return {"status": 500, "error": f"{e}"}


if __name__ == "__main__":
    app.run(debug=True)