import re

class ValidateModelMixin(object):
    
    def clean(self):
        
        def repl_func(m):
            """process regular expression match groups for word upper-casing problem"""
            return m.group(1) + m.group(2).upper()
        
        for field in self._meta.fields:

            value = getattr(self, field.name)

            if field.name == 'name' or field.name == 'city' or field.name == 'state_or_country':
                # ducktyping attempt to strip whitespace
                try:

                    value = re.sub("(^|\s)(\S)", repl_func, value)

                    setattr(self, field.name, value)
                    
                    setattr(self, field.name, value.strip())

                except Exception:
                    pass

    def save(self, *args, **kwargs):
        self.full_clean()
        
        super(ValidateModelMixin, self).save(*args, **kwargs)


