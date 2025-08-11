from flask import request, jsonify

def v_user_browse_history(request):
    pass

def v_user_search_history(request):
    pass

def v_get_search_suggestions_entries(request):
    json_obj = {}
    json_obj["items"] = []
    return jsonify(json_obj)

def v_json_user_search_history(request):
    json_obj = {}
    json_obj["histories"] = []


    #for history in histories[:50]:
    #    json_obj["histories"].append(history_to_json(history))

    return jsonify(json_obj)
