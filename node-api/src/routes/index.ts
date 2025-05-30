import { Router } from 'express'
import { authRouter } from './auth.routes'
import { userRouter } from './user.routes'
import { authenticate } from '@/middlewares/auth.middleware'

const router = Router()

router.use('/auth', authRouter)

router.use(authenticate)
router.use('/users', userRouter)

export { router }
