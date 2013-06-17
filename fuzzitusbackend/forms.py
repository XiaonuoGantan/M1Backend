from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from django.template import Context, Template

from fuzzitusbackend.settings import SERVER_ROOT_URL
from fuzzitusbackend import models as m


class GameForm(ModelForm):
    class Meta:
        model = m.Game
        fields = ['name', 'password']


FormMapper = {
    'user_creation_form': UserCreationForm,
    'authentication_form': AuthenticationForm,
    'game_form': GameForm,
}

FormAction = {
    'user_creation_form': SERVER_ROOT_URL + 'signup',
    'authentication_form': SERVER_ROOT_URL + 'login',
    'game_form': SERVER_ROOT_URL + '/api/v1/game/',
}

def render_form_with_bootstrap(form):
    assert(form is not None)
    form_template = Template(
        """
        {% load bootstrap %}
        {{ form|bootstrap }}
        <div class="control-group">
            <div class="controls">
                <button class="btn btn-primary" type="submit">Submit</button>
            </div>
        </div>
        """)
    ctx = Context({'form': form})
    return form_template.render(ctx)
