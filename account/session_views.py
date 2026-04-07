from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.views import View


class ClearSessionsView(LoginRequiredMixin, View):
    """Clear user session data (recently viewed posts, page visits, etc)."""
    login_url = 'account:login'

    def post(self, request):
        # Clear session data but keep important ones like CSRF token
        session_keys_to_clear = ['recently_viewed', 'page_visits']

        for key in session_keys_to_clear:
            if key in request.session:
                del request.session[key]

        request.session.modified = True
        messages.success(request, 'Session data cleared successfully!')
        return redirect('account:profile')

