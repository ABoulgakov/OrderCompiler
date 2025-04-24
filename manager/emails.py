import json

def prep_orders_json():
    with open("data/inbox_emails.json", "r", encoding="utf-8") as f:
        mailbox = json.load(f)

    orders_dict = dict()

    for mail in mailbox:
        if mail["from"] not in orders_dict.keys():
            orders_dict[mail["from"]] = [{"time": mail["time"],
                                "subject": mail["subject"],
                                "body": mail["body"]
                                    }]
        else:
            orders_dict[mail["from"]].append({"time": mail["time"],
                                        "subject": mail["subject"],
                                        "body": mail["body"]
                                    })
    return orders_dict



if __name__=="__main__":
    orders_dict = prep_orders_json()
    string = prep_single_client_string(orders_dict, list(orders_dict.keys())[1] )  
    print(string)