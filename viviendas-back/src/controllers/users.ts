import { Request, Response } from 'express';
import { User } from '../db/mongoose';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

// logeamos un usuario
export const logged = (req: Request, res: Response) => {
    let { body } = req;

    User.findOne({ email: body.email }, (err, userDB: any) => {

        if(err) {
            res.status(500).json({
                success: false,
                error: {
                    title: 'database error',
                    message: err
                }
            })
        }

        if(!userDB) {
            return res.status(404).json({
                success: false,
                error: {
                    title: 'not found',
                    message: 'wrong username or password'
                }
            })
        }

        if( !bcrypt.compareSync( body.password, userDB.password )) {
            return res.status(404).json({
                success: false,
                error: {
                    title: 'not found',
                    message: 'wrong username or password'
                }
            })
        }

        let token = jwt.sign({
            user: userDB
                                // s, m, horas, dias
        }, 'code', { expiresIn: 60* 60* 24 * 30 } )

        res.status(200).json({
            success: true,
            token
        })

    })
}


// registramos un usuario
export const checkin = (req: Request, res: Response) => {
    let { body } = req;

    let objUser = new User({
        name: body.name,
        lastname: body.lastname,
        email: body.email,
        password: bcrypt.hashSync(body.password, 10),
        role: body.role
    })

    objUser.save((err, userDB) => {
        if(err) {
            return res.status(500).json({
                success: false,
                error: {
                    title: 'database error',
                    message: err
                }
            })
        }

        res.status(200).json({
            success: true,
            data: userDB
        })
    })
}