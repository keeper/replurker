import json
import datetime
import sys

from plurk_oauth import PlurkAPI


if __name__ == "__main__":
    KEYS = sys.argv[1]
    allow_anonymous = True
    if len(sys.argv) >= 2:
        allow_anonymous = bool(sys.argv[3])
    plurk = PlurkAPI.fromfile(KEYS)

    today = datetime.datetime.today()
    plurks = plurk.callAPI(
        "/APP/PlurkSearch/search",
        {
            "query": sys.argv[2],
        },
    )
    print(plurks)
    replurk_ids = []
    manual_replurk_ids = []
    for p in plurks["plurks"]:
        print(p)
        if p["replurkable"] and not p["replurked"] and sys.argv[2] in p["content_raw"]:
            if not allow_anonymous and p["anonymous"]:
                continue
            replurk_ids.append(p["plurk_id"])
        else:
            manual_replurk_ids.append(p["plurk_id"])

    replurk = plurk.callAPI("/APP/Timeline/replurk", {"ids": json.dumps(replurk_ids)})

    replurk_results = replurk["results"]
    with open("./replurk.log", "a") as log_fh:
        log_fh.write(json.dumps(replurk_results, indent=2, ensure_ascii=False))
    replurk_ids = [r_id for r_id in replurk_results]
    failed_id = [r_id for r_id in replurk_ids if not replurk_results[r_id]["success"]]
    print(failed_id)
    print(manual_replurk_ids)
    # print(json.dumps(failed_replurk, indent=2, ensure_ascii=False))
