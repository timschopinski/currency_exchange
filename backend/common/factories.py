class UniqueSequenceFactoryMixin:
    @classmethod
    def _setup_next_sequence(cls):
        try:
            return cls._meta.model.objects.only('id').latest('id').id + 1
        except cls._meta.model.DoesNotExist:
            return 1
