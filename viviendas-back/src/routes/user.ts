import { Router } from 'express';
import { logged, checkin } from '../controllers/users';

// asignamos nuestros endpoints para el schema User
export const user_router : Router = Router();
user_router.post('/login', logged);
user_router.post('/user', checkin);