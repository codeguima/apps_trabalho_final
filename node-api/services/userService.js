// ./services/userService.js

const bcrypt = require('bcrypt');


class UserService {
    constructor(userModel, authenticateToken) {
        this.User = userModel;
        this.authenticateToken = authenticateToken;
    }

    //--------------------------------------------------------------------------------------------------//

    async create(name, lastname, email, password) {
        try {
            const senhaHash = await bcrypt.hash(password, 10);
            const result = await this.User.create({
                name: name,
                lastname: lastname,
                email: email,
                password: senhaHash,
                status: true
            });
            const { password: _, ...userWithoutPassword } = result.dataValues;
            return userWithoutPassword;
        } catch (error) {
            throw error;
        }
    }

    //--------------------------------------------------------------------------------------------------//

    async verifyUser(email, password) {
        try {
            const result = await this.User.findOne({ where: { email } });
            if (!result) return null;
            const match = await bcrypt.compare(password, result.password);
            return match ? result : null;
        } catch (error) {
            throw error;
        }
    }

    //--------------------------------------------------------------------------------------------------//

    async login(email, password) {
        try {
            const result = await this.verifyUser(email, password);
            if (result) {
                const token = this.authenticateToken.generateToken(result.id);
                return { user: result.id, token };
            } else {
                return null;
            }
        } catch (error) {
            throw error;
        }
    }
    
    //--------------------------------------------------------------------------------------------------//

    async update(id, updates) {
        try {
            // Verificar se o ID fornecido é válido
            if (!id) {
                throw new Error("ID inválido para atualização");
            }
    
            // Atualizar os registros na tabela
            const [updatedRowsCount, updatedRows] = await this.User.update(updates, {
                where: { id },
            });
            // Verificar se algum registro foi atualizado
            if (updatedRowsCount === 0) {
                throw new Error("Nenhum registro encontrado para atualização");
            } else {
                // Retornar algo específico para indicar que a atualização foi bem-sucedida
                return { message: "Atualização bem-sucedida", updatedRowsCount, updatedRows };
            }
        } catch (error) {
            // Lançar novamente o erro para ser tratado na camada de controle
            throw error;
        }
           
    }

    //--------------------------------------------------------------------------------------------------//

    async findAll(page = 1, pageSize = 10) {
        try {
            const offset =(page -1) *pageSize;
            const result = await this.User.findAndCountAll({ 

                attributes: { exclude: ['password'] },
                limit: pageSize,
                offset: offset 
            
            });
            return result;
        } catch (error) {
            throw error;
        }
    }

    //--------------------------------------------------------------------------------------------------//

    async findbyId(id) {

        try {
            const result = await this.User.findOne({ where: { id }, attributes: { exclude: ['password'] }});
            return result ? result : null;
        } catch (error) {
            console.error('Erro ao procurar registro por ID:', error);
            throw error;
        }
    }

    //--------------------------------------------------------------------------------------------------//
    async delete(id) {
        try {
          const result = await this.User.destroy({
            where: { id: id }
          });
      
          if (result === 0) {
            throw new Error('Registro não encontrado');
          }
      
          return { message: 'Registro deletado com sucesso' };
        } catch (error) {
          throw error;
        }
    }
    
}

module.exports = UserService;
