from __future__ import annotations

import datetime
import typing

import database
import database.objects
import utils


class ScoredTrack(typing.TypedDict):
    tra_id: str
    score_played_amount: float
    score_played_amount_since_last_week: float
    score_on_day_continuity: float
    score_total: float


def score_based_on_played_amount(use_username: str, *, weight: float = 1,
                                 since: typing.Union[str, datetime.datetime] = "0000-00-00T00:00:00") -> dict:
    if type(since) is datetime.datetime:
        since = since.strftime("%Y-%m-%dT%H:%M:%S")
    with database.Database() as db:
        results = db.select(
            "SELECT `tra_id`, COUNT(*) AS `amount` FROM `history` WHERE `use_username`=:use_username AND `his_played_at` >= :his_played_at GROUP BY `tra_id` ORDER BY  `amount` DESC",
            use_username=use_username,
            his_played_at=since)
    scored = dict()
    for result in results:
        scored[result["tra_id"]] = result["amount"] * weight
    return scored


def score_based_on_played_amount_since_last_week(use_username: str, *, weight: float = 1) -> dict:
    since = datetime.datetime.utcnow() - datetime.timedelta(weeks=1)
    return score_based_on_played_amount(use_username=use_username, weight=weight, since=since)


def score_based_on_day_continuity(use_username: str, timezone_offset: int, *, weight: float = 1) -> dict:
    with database.Database() as db:
        results = db.select(
            "SELECT `tra_id`, `his_played_at`  FROM `history` WHERE `use_username`=:use_username ORDER BY `his_played_at` DESC",
            use_username=use_username)

    days_offset = dict()
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(minutes=timezone_offset, days=1)).date()
    for result in results:
        result["days_offset"] = (yesterday - (utils.parse_datetime(result["his_played_at"]) - datetime.timedelta(
            minutes=timezone_offset)).date()).days
        current_day_offset = result["days_offset"]
        if current_day_offset < 0:
            continue
        current_days_offset = days_offset.get(current_day_offset, [])
        if result["tra_id"] not in current_days_offset:
            current_days_offset.append(result["tra_id"])
        days_offset[current_day_offset] = current_days_offset

    still_scoring = set(days_offset.get(0, []).copy())
    current_day_offset = 0
    scores = days_offset.get(0, []).copy()
    while still_scoring:
        current_days_offset = days_offset.get(current_day_offset + 1, [])
        for track_id in still_scoring.copy():
            if track_id not in current_days_offset:
                still_scoring.remove(track_id)
        scores.extend(still_scoring)
        current_day_offset += 1

    final_scoring = dict()
    for track_id in scores:
        final_scoring[track_id] = final_scoring.get(track_id, 0) + weight
    return final_scoring


def score_based_on_multiple_day_reproductions(use_username: str, timezone_offset: int, *, weight: float = 1) -> dict:
    with database.Database() as db:
        results = db.select(
            "SELECT `tra_id`, `his_played_at`  FROM `history` WHERE `use_username`=:use_username ORDER BY `his_played_at` DESC",
            use_username=use_username)

    each_day_results = dict()
    today = (datetime.datetime.utcnow() - datetime.timedelta(minutes=timezone_offset)).date()
    for result in results:
        current_day_offset = (today - (utils.parse_datetime(result["his_played_at"]) - datetime.timedelta(
            minutes=timezone_offset)).date()).days
        result["days_offset"] = current_day_offset
        current_day_offset_results = each_day_results.get(current_day_offset, {})
        current_day_offset_results[result["tra_id"]] = current_day_offset_results.get(result["tra_id"], 0) + 1
        each_day_results[current_day_offset] = current_day_offset_results

    scored = {}
    for day_offset, day_offset_results in each_day_results.items():
        for tra_id, reproductions in day_offset_results.items():
            scored[tra_id] = scored.get(tra_id, 0) + (reproductions - 1) * weight

    return scored


def wrap_all_scores(use_username: str, timezone_offset: int, limit: int = None) -> typing.List[ScoredTrack]:
    scored_on_played_amount = score_based_on_played_amount(use_username=use_username)
    scored_on_played_amount_since_last_week = score_based_on_played_amount_since_last_week(use_username=use_username)
    scored_on_day_continuity = score_based_on_day_continuity(use_username=use_username, timezone_offset=timezone_offset)
    scored_on_multiple_reproductions = score_based_on_multiple_day_reproductions(use_username=use_username,
                                                                                 timezone_offset=timezone_offset)
    all_track_ids = set(
        list(scored_on_played_amount.keys()) + list(scored_on_played_amount_since_last_week.keys()) + list(
            scored_on_day_continuity.keys()) + list(
            scored_on_multiple_reproductions.keys()))
    scores = []
    for tra_id in all_track_ids:
        current_score_on_played_amount = scored_on_played_amount.get(tra_id, 0)
        current_score_on_played_amount_since_last_week = scored_on_played_amount_since_last_week.get(tra_id, 0)
        current_score_on_day_continuity = scored_on_day_continuity.get(tra_id, 0)
        current_score_on_multiple_reproductions = scored_on_multiple_reproductions.get(tra_id, 0)
        current_total_score = current_score_on_played_amount + current_score_on_played_amount_since_last_week + current_score_on_day_continuity + current_score_on_multiple_reproductions

        scores.append({
            "track": database.objects.Track.get(tra_id=tra_id),
            "score_played_amount": current_score_on_played_amount,
            "score_played_amount_since_last_week": current_score_on_played_amount_since_last_week,
            "score_on_day_continuity": current_score_on_day_continuity,
            "score_on_multiple_reproductions": current_score_on_multiple_reproductions,
            "score_total": current_total_score
        })
    return sorted(scores, key=lambda x: x["score_total"], reverse=True)[:limit]


if __name__ == "__main__":
    print(wrap_all_scores("alex", 180))
