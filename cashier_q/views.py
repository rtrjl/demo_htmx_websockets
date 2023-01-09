import time
from multiprocessing import Process, Queue
import threading

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_POST
from django.utils import translation

global_timer = None


def demo_cashier(request):
    return render(request, template_name="cashier_screen.html")


def demo_cashier_buttons(request):
    current_lang = translation.get_language()
    context = {"languages": settings.LANGUAGES, "n_list": range(1, 5), "lang_code": current_lang}
    if request.POST:
        current_lang = request.POST.get('language', None)
        translation.activate(current_lang)
        context["lang_code"] = current_lang
        response = render(request, template_name="cashier_buttons_content.html", context=context)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, current_lang, samesite="Lax")
        demo_cashier_reset(language=current_lang)
        return response

    return render(request, template_name="cashier_buttons_main.html", context=context)


def demo_cashier_reset(language=settings.LANGUAGE_CODE):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("cashier_q_channel_group",
                                            {"type": "cashier.message", "num_cashier": "0", "language": language})


@require_POST
def demo_cashier_action(request):
    global global_timer
    num_cashier = request.POST.get("cashier", "0")
    language = request.POST.get("language", settings.LANGUAGE_CODE)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("cashier_q_channel_group",
                                            {"type": "cashier.message", "num_cashier": num_cashier,
                                             "language": language})

    if global_timer is not None and global_timer.is_alive():
        global_timer.cancel()

    timer = threading.Timer(3.0, demo_cashier_reset, kwargs={"language": language})
    timer.start()
    global_timer = timer

    return HttpResponse(status=204)
