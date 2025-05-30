import { Router } from 'express'
import { UserController } from '../controllers/user.controller'

const userRouter = Router()
const userController = new UserController()

userRouter.post('/', userController.create)
userRouter.get('/', userController.findAll)
userRouter.get('/:id', userController.findOne)
userRouter.put('/:id', userController.update)
userRouter.delete('/:id', userController.delete)

export { userRouter }
