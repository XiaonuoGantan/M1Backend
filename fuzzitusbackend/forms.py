from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.template import Context, Template

from fuzzitusbackend.settings import SERVER_ROOT_URL

FormMapper = {
    'user_creation_form': UserCreationForm,
    'authentication_form': AuthenticationForm,
}

FormAction = {
    'user_creation_form': SERVER_ROOT_URL + 'signup',
    'authentication_form': SERVER_ROOT_URL + 'login',
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
