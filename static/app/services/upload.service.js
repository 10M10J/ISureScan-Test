const config = {
    apiUrl: 'https://isurescan-756660766241.us-central1.run.app/'
    //apiUrl: 'http://127.0.0.1/'

};

// upload.service.js
angular.module('myApp').service('UploadService', function($http) {
    this.uploadFile = function(file, language) {
        var formData = new FormData();
        formData.append('file', file);
        formData.append('language', language);
        return $http.post(config.apiUrl + 'upload', formData, {
            headers: { 'Content-Type': undefined }
        });
    };

    this.summarize = function(text, language) {
        return $http.post(config.apiUrl + 'summarize', {
            text: text,
            language: language
        });
    };

    this.askQuestion = function(text, question, language) {
        return $http.post(config.apiUrl + 'answer', {
            text: text,
            question: question,
            language: language
        });
    };
});
