import json
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from . import services


@csrf_exempt
def todos_list(request: HttpRequest):
    """Handle GET (list todos) and POST (create todo)."""

    if request.method == "GET":
        todos = services.list_todos()
        return JsonResponse(todos, safe=False)

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            data = {}

        created = services.create_todo(data)
        return JsonResponse(created, status=201)

    # if method not allowed
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def todo_detail(request: HttpRequest, todo_id: str):
    """Handle PATCH (update todo) and DELETE (delete todo)."""

    if request.method == "PATCH":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            data = {}

        updated = services.patch_todo(todo_id, data)

        if updated:
            return JsonResponse(updated)

        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "DELETE":
        deleted = services.delete_todo(todo_id)

        if deleted:
            return JsonResponse({"deleted": True})

        return JsonResponse({"error": "Not found"}, status=404)

    return JsonResponse({"error": "Method not allowed"}, status=405)
