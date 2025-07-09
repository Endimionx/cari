import requests

def load_data(lokasi, hari, putaran):
    url = f"https://wysiwygscan.com/api?pasaran={lokasi.lower()}&hari={hari}&putaran={putaran}&format=json&urut=asc"
    headers = {"Authorization": "Bearer 6705327a2c9a9135f2c8fbad19f09b46"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        angka_list = [
            item["result"] for item in data.get("data", [])
            if len(item["result"]) == 4 and item["result"].isdigit()
        ]
        return angka_list
    except Exception as e:
        print("Gagal mengambil data:", e)
        return []

def cari_putaran_terbaik(selected_lokasi, selected_hari, metode, max_auto_putaran, model_type,
                         top6_markov, top6_markov_order2, top6_markov_hybrid, top6_model):
    best_putaran = 100
    best_acc = -1

    for p in range(50, max_auto_putaran + 1, 50):
        angka = load_data(selected_lokasi, selected_hari, p)
        if len(angka) < 11:
            continue
        df = [{"angka": a} for a in angka]

        pred = (
            top6_markov(df) if metode == "Markov" else
            top6_markov_order2(df) if metode == "Markov Order-2" else
            top6_markov_hybrid(df) if metode == "Markov Gabungan" else
            top6_model(df, selected_lokasi, model_type)
        )

        if not pred:
            continue

        uji_df = df[-10:]
        benar, total = 0, 0
        for i in range(len(uji_df)):
            actual = f"{int(uji_df[i]['angka']):04d}"
            for j in range(4):
                if int(actual[j]) in pred[j]:
                    benar += 1
                total += 1
        acc = benar / total * 100 if total else 0
        if acc > best_acc:
            best_acc = acc
            best_putaran = p

    return best_putaran, best_acc
