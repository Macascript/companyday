const urlbase = "http://127.0.0.1:5000/"
        $(document).ready(function() {
        $('.logo-carousel').slick({
          slidesToShow: 6,
          slidesToScroll: 1,
          autoplay: true,
          autoplaySpeed: 1000,
          arrows: true,
          dots: false,
          pauseOnHover: false,
          responsive: [{
            breakpoint: 768,
            settings: {
              slidesToShow: 4
            }
          }, {
            breakpoint: 520,
            settings: {
              slidesToShow: 2
            }
          }]
        });
      });

        /*var exampleModal = document.getElementById('exampleModal')
        exampleModal.addEventListener('show.bs.modal', function (event) {
        // Button that triggered the modal
        var button = event.relatedTarget
        // Extract info from data-bs-* attributes
        var recipient = button.getAttribute('data-bs-whatever')
        // If necessary, you could initiate an AJAX request here
        // and then do the updating in a callback.
        //
        // Update the modal's content.
        var modalTitle = exampleModal.querySelector('.modal-title')
        var modalBodyInput = exampleModal.querySelector('.modal-body input')

        modalTitle.textContent = 'DATOS A RELLENAR'
        modalBodyInput.value = ""
        })*/
      
        const app=new Vue({
            el: '#app',
            delimiters:["[[","]]"],
            data: {
              pProyectos:"",
              sMeetings: "",
              ccharla:"",
              fEmpresas:"",
              // loginState:"",
              tasks:[
                {
                  modalidad:"online",
                  fecha:"2018-07-22",
                  tiempo:"10",
                  descripcion:""
                }
              ],
              logindata: {
                email: "",
                password: "",
                remember: ""
              },
              listaPaises: [],
              paises: {},
              provincias: {},
              poblaciones: {},
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
                this.$http.get(urlbase + "session/status").then(
                    function(response){
                        console.log("Bienvenido "+JSON.stringify(response.data));
                        this.empresas = response.data.empresas;
                    }
                )
            },
            
            methods:{
              comprobar:function(){console.log(this.pProyectos)},
              // checkLoginState: function(){
            // Hace falta envio de 'state' por api flask para comprobar errores

              // },
              addSpeedM: function(){
              //e.preventDefault();
              this.tasks.push({
                modalidad:"online",
                fecha:"2018-07-22",
                tiempo:"10",
                descripcion:""
              });
              },
              deleteSpeedM: function(task){
                this.tasks.splice(this.tasks.indexOf(task),1)
              },
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
              },
              login: function(){
                const path = 'http://127.0.0.1/login'
                axios.post(path, {
                  email: this.data.logindata.email,
                  password: this.data.logindata.password,
                  remember: this.data.logindata.remember
                })
                  .then(response => {
                    console.log(response)
                  })
                  .catch(err => {
                    console.log(err)
                  });
              }
            }
        });

       /* const appDos= new Vue({
          el:"#appDos",
          data:{

            tasks:[
              {
                modalidad:"online",
                fecha:"2018-07-22",
                tiempo:"10",
                descripcion:""
              }
            ]

          },
          methods:{
            addSpeedM: function(){
              //e.preventDefault();
              this.tasks.push({
                modalidad:"online",
                fecha:"2018-07-22",
                tiempo:"10",
                descripcion:""
              });
            },
            deleteSpeedM: function(task){
              this.tasks.splice(this.tasks.indexOf(task),1)
            }
          }



      });*/