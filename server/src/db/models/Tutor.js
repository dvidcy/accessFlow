const { DataTypes } = require('sequelize');
const sequelize = require('../connection');

const Tutor = sequelize.define('Tutor', {
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  nombre: { type: DataTypes.STRING(100), allowNull: false },
  email: { type: DataTypes.STRING(150), allowNull: false },
  telefono: { type: DataTypes.STRING(20), allowNull: true },
}, { tableName: 'tutores', timestamps: false });

module.exports = Tutor;
