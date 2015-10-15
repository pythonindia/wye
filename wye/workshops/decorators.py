def validate_action_param(action_map):
    def wrapper(func):
        def inner(self, user, **kwargs):
            response = {'status': False, 'msg': ''}
            pk = kwargs.get('pk')
            action = kwargs.get('action')

            # validate parameters
            if not (pk and action):
                response['msg'] = 'Invalid request.'
                return response
            # validate action
            if action not in action_map:
                response['msg'] = 'Action not allowed.'
                return response
            return func(self, user, **kwargs)
        return inner
    return wrapper
