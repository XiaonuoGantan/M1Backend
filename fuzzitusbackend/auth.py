from tastypie.authorization import Authorization


class GameOwnerAuthorization(Authorization):
    def create_detail(self, object_list, bundle):
        return bundle.request.user.is_staff

