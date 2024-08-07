// upload.service.js
angular.module('myApp').service('UploadService', function($http) {
    this.uploadFile = function(file, language) {
        var formData = new FormData();
        formData.append('file', file);
        formData.append('language', language);
        return $http.post('http://localhost:5000/upload', formData, {
            headers: { 'Content-Type': undefined }
        });
    };

    this.summarize = function(text, language) {
        return $http.post('http://localhost:5000/summarize', {
            text: text,
            language: language
        });
    };

    this.askQuestion = function(text, question, language) {
        return $http.post('http://localhost:5000/answer', {
            text: text,
            question: question,
            language: language
        });
    };
});
