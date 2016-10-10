# from wye.base.constants import WorkshopStatus


# # def validate_action_param(action_map):
# #     print("validate_action_param")
# #     def wrapper(func):
# #         def inner(self, user, **kwargs):
# #             response = {'status': False, 'msg': ''}
# #             pk = kwargs.get('pk')
# #             action = kwargs.get('action')

# #             # validate parameters
# #             if not (pk and action):
# #                 response['msg'] = 'Invalid request.'
# #                 return response
# #             # validate action
# #             if action not in action_map:
# #                 response['msg'] = 'Action not allowed.'
# #                 return response
# #             return func(self, user, **kwargs)
# #         return inner
# #     return wrapper


# def validate_assignme_action(func):
#     def inner(self, user, **kwargs):
#         # if workshop completed don't accept
#         # presenter.
#         if self.status == WorkshopStatus.HOLD:
#             return {
#                 'status': False,
#                 'msg': 'Not accepting presenter as \
#                 workshop is on hold.'
#             }
#         elif self.status == WorkshopStatus.COMPLETED:
#             return {
#                 'status': False,
#                 'msg': 'Sorry, but it would seem that this \
#                 workshop is already completed and hence \
#                 won\'t be able to accept a presenter.'}
#         return func(self, user, **kwargs)
#     return inner
