// upload.component.js
angular.module('myApp').controller('UploadController', ['$scope', 'UploadService', function($scope, UploadService) {
    $scope.language = 'en'; // default language
    $scope.uploadedText = '';
    $scope.summary = '';
    $scope.question = '';
    $scope.answer = '';

    $scope.setLanguage = function(lang) {
        $scope.language = lang;
    };

    $scope.uploadFile = function() {
        var fileInput = document.getElementById('fileInput');  // Ensure 'fileInput' matches the input ID
        if (!fileInput) {
            console.log("Debug: fileInput element not found.");
            return;
        }
        var file = fileInput.files[0];
        console.log("Debug: File selected for upload:", file);
        if (file) {
            UploadService.uploadFile(file, $scope.language).then(function(response) {
                console.log("Debug: Upload response:", response);
                $scope.uploadedText = response.data.text;
                // Call summarize API if needed
                $scope.summarize();
            }, function(error) {
                console.error('Error uploading file:', error);
            });
        }else {
            console.log("Debug: No file selected.");
        }
    };

    $scope.summarize = function() {
        console.log("Debug: Text to summarize:", $scope.uploadedText);
        UploadService.summarize($scope.uploadedText, $scope.language).then(function(response) {
            console.log("Debug: Summarize response:", response);
            $scope.summary = response.data.summary;
        }, function(error) {
            console.error('Error summarizing text:', error);
        });
    };

    $scope.askQuestion = function() {
        console.log("Debug: Text to ask question:", $scope.uploadedText);
        console.log("Debug: Question:", $scope.question);
        UploadService.askQuestion($scope.uploadedText, $scope.question, $scope.language).then(function(response) {
            console.log("Debug: Ask question response:", response);
            $scope.answer = response.data.answer;
        }, function(error) {
            console.error('Error getting answer:', error);
        });
    };
}]);

// Directive to bind file input to scope variable
angular.module('myApp').directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);
