d = {
    'Бытовая техника': {
        'url': 'http://byt.com',
        'children': {
            'Утюги': {
                'url': 'http://utug.com',
                'children': {
                    'Паровые утюги': {
                        'url': 'http://par.com',
                    },
                    'ДВС утюги': {
                        'url': 'http://dvs.com',
                    }
                }
            },
        }
    },
    'Автоуход': {
        'url': 'http://auto.com',
        'children': {
            'Стёкла': {
                'url': 'http://stekla.com',
            },
            'Фары': {
                'url': 'http://fary.com'
            }
        }
    }
}

def iter_chains(base_dict: dict, curr_chain: list=[]) -> tuple:
    for key in base_dict:
        new_chain = curr_chain.copy()
        new_chain.append(key)
        yield " > ".join(new_chain), base_dict[key]["url"]
        if base_dict[key].get("children") is not None:
            yield from iter_chains(base_dict[key]["children"], new_chain)


bread_crumbs = {chain: url for chain, url in iter_chains(d)}

import json 
print(json.dumps(bread_crumbs, indent=4, ensure_ascii=False))