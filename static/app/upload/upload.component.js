// upload.component.js
var language = 'en';
angular.module('myApp').controller('UploadController', ['$scope', 'UploadService', function($scope, UploadService) {
    $scope.language = 'en'; // default language
    $scope.uploadedText = '';
    $scope.summary = '';
    $scope.question = '';
    $scope.answer = '';
    $scope.conversation = [];  // to hold the conversation history

    // Function to set the language
    $scope.setLanguage = function(lang) {
        language = lang;
    };

    $scope.uploadFile = function() {
    //    console.log("Debug: Language before upload:", language);  // Ensure correct language is passed
        var fileInput = document.getElementById('fileInput');  // Ensure 'fileInput' matches the input ID
        if (!fileInput) {
    //        console.log("Debug: fileInput element not found.");
            return;
        }
        var file = fileInput.files[0];
    //    console.log("Debug: File selected for upload:", file);
    //    console.log("Debug: Language to be used for upload:", language);
        if (file) {
            UploadService.uploadFile(file, language).then(function(response) {
    //            console.log("Debug: Upload response:", response);
                $scope.uploadedText = response.data.text;
                // Call summarize API if needed
                $scope.summarize();
            }, function(error) {
    //            console.error('Error uploading file:', error);
                //$scope.uploadedText = error
                alert("Oops! Looks like uploaded file is Corrupted or Password Protected.")
            });
        }else {
    //        console.log("Debug: No file selected.");
                alert("Please upload your policy document.")
        }
    };

    $scope.summarize = function() {
    //    console.log("Debug: Text to summarize:", $scope.uploadedText);
        UploadService.summarize($scope.uploadedText, language).then(function(response) {
    //        console.log("Debug: Summarize response:", response);
            $scope.summary = response.data.summary;
        }, function(error) {
    //        console.error('Error summarizing text:', error);
        });
    };

    $scope.askQuestion = function() {
    //    console.log("Debug: Text to ask question:", $scope.uploadedText);
    //    console.log("Debug: Question:", $scope.question);
        if (!$scope.question.trim()) return;  // Ensure question is not empty

        // Add the user's question to the conversation
        $scope.conversation.push({
            sender: 'User',
            text: $scope.question
        });
        // Make the request to get the chatbot's answer
        UploadService.askQuestion($scope.uploadedText, $scope.question, language).then(function(response) {
    //        console.log("Debug: Ask question response:", response);
            // Add the chatbot's answer to the conversation
            $scope.conversation.push({
                sender: 'ChatBot',
                text: response.data.answer
            });
            // Clear the input question field
            $scope.question = '';
            //$scope.answer = response.data.answer;
        }, function(error) {
    //        console.error('Error getting answer:', error);
        });
    };

    $scope.refreshPage = function() {
        window.location.reload();  // This will refresh the page
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
