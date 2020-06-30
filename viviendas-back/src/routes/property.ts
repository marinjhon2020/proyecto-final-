import { Router } from 'express';
import { addProperty, getProperties, editProperty, deleteProperty, getSortedProperties, getPropertyById, getPropertiesAdmin, getSortedPropertiesAdmin } from '../controllers/property';
import { verifyToken, verifyRole } from '../middlewares/authentication';

// asignamos nuestros endpoints para el schema Property
export const property_router: Router = Router();
property_router.post('/property', verifyToken, verifyRole , addProperty);
property_router.get('/propertiesadmin', verifyToken, verifyRole ,getPropertiesAdmin);
property_router.get('/properties', getProperties);
property_router.put('/property/:id', verifyToken, verifyRole, editProperty);
property_router.delete('/property/:id', verifyToken, verifyRole, deleteProperty);
property_router.get('/properties/price', getSortedProperties);
property_router.get('/properties/priceadmin', verifyToken ,verifyRole ,getSortedPropertiesAdmin );
property_router.get('/property/:id', getPropertyById);