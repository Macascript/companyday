const urlbase = "http://127.0.0.1:5000/"

console.log(document.cookie);

const app = new Vue({
    el: "#app",
    delimiters: ["[[","]]"],
    data: {
        empresa: {}
    },
    mounted: function(){
        this.$http.get(urlbase + "user/getempresa").then(function(response){
            empresa = response.data.empresa;
        })
    },
    methods: {
        
    }
})