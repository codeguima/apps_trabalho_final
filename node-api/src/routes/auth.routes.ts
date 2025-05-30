import { Router } from 'express'
import { AuthController } from '../controllers/auth.controller'

const authController = new AuthController()

const authRouter = Router()

authRouter.post('/sessions', authController.login)

export { authRouter }
