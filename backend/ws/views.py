from django.shortcuts import render


def websocket_interface(request):
    return render(request, "ws_forms/ws_interface.html")
