import { Router } from 'express'
import { authRouter } from './auth.routes'
import { userRouter } from './user.routes'
import { authenticate } from '@/middlewares/auth.middleware'
import { GetMeController } from '@/controllers/get-me.controller'

const router = Router()

const getMeController = new GetMeController()

router.use('/auth', authRouter)

router.use(authenticate)
router.use('/users', userRouter)
router.get('/me', getMeController.handle)

export { router }
