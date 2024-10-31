from flask import Flask, Response

import PortFolioRepository

app = Flask(__name__)



@app.route('/today/vector', methods = ['POST'])
def save_today_vector():

    portfolio = PortFolioRepository.get_portfolio()
    print(portfolio)

    return Response(status = 200)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)