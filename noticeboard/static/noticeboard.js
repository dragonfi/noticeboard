(function(){
    "use strict";
    angular.module("noticeboard", [])
    .controller("Noticeboard", NoticeboardCtrl)
    .directive("noticeboard", function(){
        return {
            restict: "E",
            templateUrl: "noticeboard.html",
            controller: "Noticeboard as ctrl"
        };
    });

    NoticeboardCtrl.$inject = ["$scope", "$http"];
    function NoticeboardCtrl($scope, $http){
        $http.get("/api/v1/notes").success(function(data){
            $scope.notes = data["notes"];
        });
    }
})();
