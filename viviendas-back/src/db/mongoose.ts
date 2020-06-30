import { userSchema } from './../collections/users';
import { propertySchema } from '../collections/property';
import { model } from "mongoose"


// la conexion del modelo a nuestra BD
export const User = model('User', userSchema );
export const Property = model('Property', propertySchema );