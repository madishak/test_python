import requests


def fns_post_request(ifns, oktmmf):
    data = requests.post('https://service.nalog.ru/addrno-proc.json',
                         data={'c': 'next', 'step': 1, 'npKind': 'fl', 'ifns': ifns, 'oktmmf': oktmmf}).json()
    results = []

    for key, value in data.items():
        if key == 'payeeDetails':
            results.append({'Получатель платежа': value['payeeName']})
            results.append({'ИНН получателя': value['payeeInn']})
            results.append({'КПП получателя': value['payeeKpp']})
            results.append({'Банк получателя': value['bankName']})
            results.append({'БИК': value['bankBic']})
            results.append({'Счет №': value['payeeAcc']})

    return results


print(fns_post_request(7840, 40913000))
