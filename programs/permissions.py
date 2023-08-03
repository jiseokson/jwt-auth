from rest_framework import permissions


class IsConsumerOrReadOnly(permissions.BasePermission):
    # 인증된 유저에 대해 목록 조회, consumer만 등록 허용
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_consumer
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 읽기 권한 요청이 들어오면 허용(SAFE_METHOD: GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # PUT, PATCH, DELETE 경우에
        if request.user.is_consumer:
            # 요청자(request.user)가 객체(Program)의 user와 동일한지 확인
            return obj.author == request.user
