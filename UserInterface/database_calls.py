

import plyvel
import json



def instagram_batch_insert(posts):

    db = plyvel.DB("./database", create_if_missing=True)
    with db.write_batch() as wb:
        for post in posts: 
            if isinstance(post["image_id"], str):
                key = b'instagram_' + post["image_id"].encode()  
                value = json.dumps(post).encode()



            wb.put(key, value)

    db.close()
    return 

def insert(key, value):
    if isinstance(key, str):
        key = key.encode()
    

    if isinstance(value, str):
        value = value.encode()
    else:
        value = json.dumps(value).encode()
    


    db = plyvel.DB("./database", create_if_missing=True)
    db.put(key, value)
    db.close()
    return 


def get(key):
    if isinstance(key, str):
        key = key.encode()

    db = plyvel.DB("./database", create_if_missing=True)
    value = db.get(key)
    if not value:
        return None

    db.close()

    try:
        
        return json.loads(value)  

    except json.JSONDecodeError:
        return str(value)

    return 