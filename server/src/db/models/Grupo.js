const { DataTypes } = require('sequelize');
const sequelize = require('../connection');

const Grupo = sequelize.define('Grupo', {
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  nombre: { type: DataTypes.STRING(10), allowNull: false },
  grado: { type: DataTypes.INTEGER, allowNull: false },
  turno: { type: DataTypes.ENUM('matutino', 'vespertino', 'nocturno'), allowNull: false },
}, { tableName: 'grupos', timestamps: false });

module.exports = Grupo;
