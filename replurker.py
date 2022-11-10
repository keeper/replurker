import argparse
import json
import datetime
from typing import Any, Dict, List

from loguru import logger
from plurk_oauth import PlurkAPI


def parse_args(args: List[str] = None) -> Any:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth_key")
    parser.add_argument("-k", "--keyword")
    parser.add_argument("-a", "--allow_anonymous", action="store_true", default=False)

    if args:
        return parser.parse_args(args)
    return parser.parse_args()


def is_replurkable(p: Dict, allow_anonymous: bool) -> bool:
    return (
        p["replurkable"]
        and not p["replurked"]
        and args.keyword in p["content_raw"]
        and (allow_anonymous or not p["anonymous"])
    )


if __name__ == "__main__":
    args = parse_args()
    logger.debug(args)
    key_file = args.auth_key
    allow_anonymous = args.allow_anonymous
    plurk = PlurkAPI.fromfile(key_file)

    today = datetime.datetime.today()
    plurks = plurk.callAPI(
        "/APP/PlurkSearch/search",
        {"query": args.keyword},
    )
    logger.info(f"Found {len(plurks['plurks'])} plurks")
    logger.trace(json.dumps(plurks, indent=2))
    replurk_ids = []
    manual_replurk_ids = []
    for p in plurks["plurks"]:
        logger.trace(json.dumps(p, indent=2))
        if is_replurkable(p, allow_anonymous):
            replurk_ids.append(p["plurk_id"])
        else:
            manual_replurk_ids.append(p["plurk_id"])

    replurk = plurk.callAPI("/APP/Timeline/replurk", {"ids": json.dumps(replurk_ids)})

    replurk_results = replurk["results"]
    logger.trace(json.dumps(replurk_results, indent=2, ensure_ascii=False))
    logger.info(f"Replurk {len(replurk_results)}")
    replurk_ids = [r_id for r_id in replurk_results]
    failed_id = [r_id for r_id in replurk_ids if not replurk_results[r_id]["success"]]
    if failed_id:
        logger.warning(f"failed ids: {', '.join(map(str, failed_id))}")
    logger.trace(f"manual replurk ids: {', '.join(map(str, manual_replurk_ids))}")
    # print(json.dumps(failed_replurk, indent=2, ensure_ascii=False))
