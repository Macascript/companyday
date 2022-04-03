var urlbase = "http://127.0.0.1:5000/"

const app = new Vue({
    el: "#app",
    delimiters: ["[[","]]"],
    data: {
        listaPaises: [],
        paises: {},
        provincias: {},
        poblaciones: {},
        empresas: [],
        pais: "",
        provincia: "",
        poblacion: "",
        eventoCambio: false,
        paisSeleccionado: false,
        provinciaSeleccionada: false,
        poblacionSeleccionada: false
    },
    mounted: function(){
        this.$http.get(urlbase + "user/getpaises").then(
            function(response){
                console.log("respuesta del servidor: "+JSON.stringify(response.data));
                this.listaPaises = response.data.paises;
                for (i in response.data.paises){
                    this.paises[response.data.paises[i].nombre] = i;
                    
                    for (j in response.data.paises[i].provincias){
                        this.provincias[response.data.paises[i].provincias[j].nombre] = [i,j];
                        for (k in response.data.paises[i].provincias[j].poblaciones){
                            this.poblaciones[response.data.paises[i].provincias[j].poblaciones[k].nombre] = [i,j,k];
                        }
                    }
                }
            }
        )
        this.$http.get(urlbase + "user/getempresas").then(
            function(response){
                console.log("respuesta del servidor: "+JSON.stringify(response.data));
                this.empresas = response.data.empresas;
            }
        )
    },
    methods: {
        debug: function(){
            console.log("el pais esta: " + this.paisSeleccionado);
            console.log("la provincia esta: " + this.provinciaSeleccionada);
            console.log("la poblacion esta: " + this.poblacionSeleccionada);
            console.log(this.paises);
            console.log(this.provincias);
            console.log(this.poblaciones);
        },
        trigger: function(e){
            this.eventoCambio = e.key ? false : true;
        },
        cambioPais: function(){
            this.paisSeleccionado = this.eventoCambio;

            if (!this.eventoCambio) return;
            
            console.log(this.pais);
            // $("input[name='provincia']").val("");
            // $("input[name='poblacion']").val("");
            this.provincia = "";
            this.poblacion = "";
            this.provinciaSeleccionada = false;
            this.poblacionSeleccionada = false;
            
        },
        cambioProvincia: function(){
            this.provinciaSeleccionada = this.eventoCambio;
            
            if (!this.eventoCambio) return;

            // $("input[name='poblacion']").val("");

            let indices = this.provincias[this.provincia];
            console.log(indices);
            // $("input[name='pais']").val(this.listaPaises[indices[0]].nombre);
            this.pais = this.listaPaises[indices[0]].nombre;
            this.poblacion = "";
            this.poblacionSeleccionada = false
            this.paisSeleccionado = true;
        },
        cambioPoblacion: function(){
            this.poblacionSeleccionada = this.eventoCambio;

            if (!this.eventoCambio) return;

            let indices = this.poblaciones[this.poblacion];
            console.log(indices);
            // $("input[name='pais']").val(this.listaPaises[indices[0]].nombre);
            // $("input[name='provincia']").val(this.listaPaises[indices[0]].provincias[indices[1]]);
            this.pais = this.listaPaises[indices[0]].nombre;
            this.provincia = this.listaPaises[indices[0]].provincias[indices[1]].nombre;
            this.paisSeleccionado = true;
            this.provinciaSeleccionada = true;
        }
    }
});