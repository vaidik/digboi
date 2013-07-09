app.controller('Jobs', function($scope, $http){
    $scope.server = 'Default Name';

    $scope.job_name = null;
    $scope.jobs = [];
    $scope.tests = [];
    $scope.errors = [];
    $scope.selected_test = null;

    $scope.init = function() {
        this.get_job();
    }

    $scope.get_job = function() {
        $http.get('/api/jobs').success(function(data) {
            $scope.jobs = data['jobs'];
            var jobs_filter = document.getElementById('job_name');
            jobs_filter.removeAttribute('disabled');
            jobs_filter.setAttribute('placeholder', 'Select Job');
        });
    }

    $scope.get_job_tests = function(job_name) {
        var tests_nav = document.getElementById('testsNav');
        tests_nav.className += ' loading';
        $scope.errors = [];

        $http.get('/api/job/' + job_name + '/tests').success(function(data) {
            tests_nav.className = tests_nav.className.replace('loading', '');
            $scope.tests = data.tests;
            $scope.job_name = job_name;
        });
    }

    $scope.get_test_details = function(test) {
        var test_details = document.getElementsByClassName('content')[0];
        test_details.className += ' loading';

        $scope.selected_test = test;
        $http.get('/api/job/' + $scope.job_name + '/test/' + test).success(function(data) {
            $scope.errors = data.errors;
            test_details.className = test_details.className.replace('loading', '');
        });
    }
});