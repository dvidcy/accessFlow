const { DataTypes } = require('sequelize');
const sequelize = require('../connection');

const Mensaje = sequelize.define('Mensaje', {
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  admin_id: { type: DataTypes.INTEGER, allowNull: false },
  asunto: { type: DataTypes.STRING(200), allowNull: false },
  cuerpo: { type: DataTypes.TEXT, allowNull: false },
  tipo: { type: DataTypes.ENUM('individual', 'grupal'), allowNull: false },
  enviado_en: { type: DataTypes.DATE, defaultValue: DataTypes.NOW },
}, { tableName: 'mensajes', timestamps: false });

module.exports = Mensaje;
