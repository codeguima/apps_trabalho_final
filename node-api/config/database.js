// config/database.js

const db = require('../models');

async function applyMigrations(retries = 10, delay = 5000) {
  for (let i = 0; i < retries; i++) {
    try {
      await db.sequelize.authenticate();
      console.log('✅ Conectado ao banco de dados!');
      await db.sequelize.sync();
      console.log('✅ Sincronização com o banco de dados realizada.');
      return;
    } catch (error) {
      console.error(`⏳ Tentativa ${i + 1} falhou:`, error.message);
      await new Promise((res) => setTimeout(res, delay));
    }
  }

  console.error('❌ Não foi possível conectar ao banco de dados após múltiplas tentativas.');
  process.exit(1);
}

module.exports = {
  applyMigrations,
};
