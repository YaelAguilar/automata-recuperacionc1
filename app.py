from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
initial_state = 'q0'
accept_states = {'q2', 'q5'}
alfabeto = {'a', 'b', 'c'}
transition_table = {
    'q0': {'a': 'q1', 'b': 'q0', 'c': 'q0'},
    'q1': {'a': 'q1', 'b': 'q2', 'c': 'q1'},
    'q2': {'a': 'q2', 'b': 'q0', 'c': 'q3'},
    'q3': {'a': 'q1', 'b': 'q0', 'c': 'q0'},
    'q4': {'a': 'q4', 'b': 'q5', 'c': 'q4'},
    'q5': {'a': 'q5', 'b': 'q0', 'c': 'q3'}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        cadena = data['cadena']
        nodes, edges, message = build_automata_data(cadena)
        return jsonify({'nodes': nodes, 'edges': edges, 'message': message})
    return render_template('index.html')


def build_automata_data(cadena):
    actual_state = initial_state
    for simbolo in cadena:
        if simbolo not in alfabeto or actual_state not in transition_table or simbolo not in transition_table[actual_state]:
            return [], [], "Cadena inválida: contiene caracteres no permitidos o transiciones no definidas"
        actual_state = transition_table[actual_state][simbolo]
    
    accepted = "Aceptado" if actual_state in accept_states else "Rechazado"
    nodes = [{'id': state, 'label': state, 'color': 'red' if state == actual_state else 'blue'} for state in states]
    edges = [{'from': src, 'to': dest, 'label': char} for src, trans in transition_table.items() for char, dest in trans.items()]
    return nodes, edges, accepted


if __name__ == '__main__':
    app.run(debug=True)
