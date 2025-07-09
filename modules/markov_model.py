from collections import defaultdict, Counter

def build_transition_matrix(data, digit_index=0, order=1):
    transitions = defaultdict(Counter)
    for i in range(order, len(data)):
        prev_digits = tuple(int(data[j][digit_index]) for j in range(i - order, i))
        next_digit = int(data[i][digit_index])
        transitions[prev_digits][next_digit] += 1
    return transitions

def predict_next(transitions, prev_digits, top_k=6):
    counts = transitions.get(tuple(prev_digits), Counter())
    if not counts:
        return list(range(6))  # fallback
    return [digit for digit, _ in counts.most_common(top_k)]

def top6_markov(data):
    result = []
    for digit_index in range(4):
        transitions = build_transition_matrix(data, digit_index=digit_index, order=1)
        prev_digits = [int(data[-1][digit_index])]
        pred = predict_next(transitions, prev_digits)
        result.append(pred)
    return result

def top6_markov_order2(data):
    result = []
    for digit_index in range(4):
        transitions = build_transition_matrix(data, digit_index=digit_index, order=2)
        prev_digits = [int(data[-2][digit_index]), int(data[-1][digit_index])]
        pred = predict_next(transitions, prev_digits)
        result.append(pred)
    return result

def top6_markov_hybrid(data):
    simple = top6_markov(data)
    order2 = top6_markov_order2(data)
    hybrid = []
    for i in range(4):
        combined = simple[i] + order2[i]
        counter = Counter(combined)
        hybrid.append([digit for digit, _ in counter.most_common(6)])
    return hybrid
