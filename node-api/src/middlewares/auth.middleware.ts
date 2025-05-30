import { UserService } from '@/services/user.service'
import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'

export function authenticate(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization

  if (!authHeader) return res.status(401).json({ error: 'Token não fornecido' })

  const token = authHeader.split(' ')[1]

  try {
    const { userId } = jwt.verify(token, process.env.JWT_SECRET as string) as {
      userId: number
    }

    const userService = new UserService()

    const user = userService.findById(userId)

    if (!user) {
      return res.status(401).json({ error: 'Token inválido' })
    }

    req.user = { id: userId }

    next()
  } catch (error) {
    return res.status(401).json({ error: 'Token inválido' })
  }
}
