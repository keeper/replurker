import argparse
import json
from typing import Any, Dict, List

from loguru import logger
from plurk_oauth import PlurkAPI


def parse_args(args: List[str] = None) -> Any:
    parser = argparse.ArgumentParser()
    parser.add_argument("auth_key")
    parser.add_argument("keyword")
    parser.add_argument("-a", "--allow_anonymous", action="store_true", default=False)

    if args:
        return parser.parse_args(args)
    return parser.parse_args()


def is_replurkable(p: Dict, keyword: str, allow_anonymous: bool) -> bool:
    return (
        p["replurkable"]
        and not p["replurked"]
        and keyword in p["content_raw"]
        and (allow_anonymous or not p["anonymous"])
    )


def get_plurk_ids(plurk: PlurkAPI, keyword: str, allow_anonymous: bool) -> List[Dict]:
    plurks = plurk.callAPI(
        "/APP/PlurkSearch/search",
        {"query": keyword},
    )
    logger.info(f"Found {len(plurks['plurks'])} plurks")
    logger.trace(json.dumps(plurks, indent=2))
    replurk_ids = []
    for p in plurks["plurks"]:
        logger.trace(json.dumps(p, indent=2))
        if is_replurkable(p, keyword, allow_anonymous):
            replurk_ids.append(p["plurk_id"])

    return replurk_ids


def replurk(plurk: PlurkAPI, ids: List[int]) -> List[Dict]:
    replurk = plurk.callAPI("/APP/Timeline/replurk", {"ids": json.dumps(ids)})

    return replurk["results"]


def main():
    args = parse_args()
    logger.debug(args)
    key_file = args.auth_key
    allow_anonymous = args.allow_anonymous
    plurk = PlurkAPI.fromfile(key_file)

    replurk_ids = get_plurk_ids(plurk, args.keyword, allow_anonymous)
    replurk_results = replurk(plurk, replurk_ids)

    logger.trace(json.dumps(replurk_results, indent=2, ensure_ascii=False))
    logger.info(f"Replurk {len(replurk_results)}")
    replurked_ids = list(replurk_results.keys())
    try:
        failed_id = [
            r_id for r_id in replurked_ids if not replurk_results[r_id]["success"]
        ]
        if failed_id:
            logger.warning(f"failed ids: {', '.join(map(str, failed_id))}")
    except KeyError as e:
        logger.error(f"Replurked id mismatch, can't get replurk status. Missed id: {e}")


if __name__ == "__main__":
    main()
