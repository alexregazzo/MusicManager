# import database.objects
#
#
# histories = database.objects.History.getAll()
#
# total_time = 0
# for history in histories:
#     track = history.track
#     total_time += track.tra_duration_ms
#
# print(total_time)
# print("342679694")
#
# # SELECT SUM(tra_duration_ms) FROM history NATURAL JOIN track;
# # SELECT track.*, COUNT(*) AS amount FROM history NATURAL JOIN track GROUP BY tra_id ORDER BY amount DESC;
