import express, {Request,Response} from "express"
import mongoose from "mongoose";
import { user_router } from '../routes/user';
import { property_router } from '../routes/property';

//defnicion de clase 
 export  class Server { 
    public app: express.Application;
    public static _instance:Server;
    public port=3001;

    // contructor para llamar  a todas las funciones
    constructor() {
       this.app=express();
       this.settings__cors();
       this.settings__json();
       this.settings__routers();
       this.connect__mongodb();
  

    }

     //configurando el json (permitir datos) 
    settings__json() {
        this.app.use(express.json());
        this.app.use(express.urlencoded({ extended:true }))
    }

    // config routers , express usa esta ruta
    settings__routers() {
        this.app.get("/", (req: Request, res: Response) => {
            res.json({
                ok: true, 
                message:"the server is active"
            })
        });

        this.app.use('', user_router);
        this.app.use('', property_router);
    
    } 
    // agregar datos (autorizacion al frontend)
    settings__cors(){
        this.app.use((req, res, next) => {
          res.header('Access-Control-Allow-Origin', '*');
          res.header('Access-Control-Allow-Headers', 'Authorization, X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Allow-Request-Method');
          res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
          res.header('Allow', 'GET, POST, OPTIONS, PUT, DELETE');
          next();
        });
    };


    //conection mongodb (resive su host como parametro, retorna una promesa)
    connect__mongodb() {
        mongoose.connect("mongodb://localhost:27017", {
            useCreateIndex: true, 
            useNewUrlParser: true,
            useUnifiedTopology: true,
            dbName:"viviendas"
        }).then(() => {
            
            console.log("conection mongodb")
        })
        .catch((error) => {

            console.log("error",error)
        })    
    }
   
    // corriendo el servidor (resive dos parametros el puerto y la funcion anonima)
    run__start() {
        this.app.listen(this.port, () => {
            console.log("server running successfully in port", this.port)
        })
        
    }
   
}