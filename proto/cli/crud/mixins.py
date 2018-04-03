class NamedModelMixin(object):

    def find(self, val):
        if not val:
            val = self.readln('Please, specify name or ID: ')

        try:
            int(val)
            return self.model_class.objects.filter(id=val)
        except ValueError as e:
            return self.model_class.objects.filter(name=val)
