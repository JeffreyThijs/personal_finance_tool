class BaseFormHandler:
    def __init__(self, forms=None, default_forms=None):
        self._default_forms = default_forms
        self._forms = forms if forms is not None else self._default_forms

    @property
    def default_forms(self):
        return self.default_forms

    @default_forms.setter
    def default_forms(self, value):
        raise Exception("Cant change the default forms")

    @property
    def forms(self):
        return self._forms

    @forms.setter
    def forms(self, value):
        self._forms = self.default_forms if not isinstance(value, dict) else value

    def handle_forms(self) -> bool:
        raise NotImplementedError