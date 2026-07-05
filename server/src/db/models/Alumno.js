const { DataTypes } = require('sequelize');
const sequelize = require('../connection');

const Alumno = sequelize.define('Alumno', {
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  nombre: { type: DataTypes.STRING(100), allowNull: false },
  rfid_uid: { type: DataTypes.STRING(50), allowNull: true, unique: true },
  grupo_id: { type: DataTypes.INTEGER, allowNull: false },
}, { tableName: 'alumnos', timestamps: false });

module.exports = Alumno;
