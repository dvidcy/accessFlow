const { DataTypes } = require('sequelize');
const sequelize = require('../connection');

const Asistencia = sequelize.define('Asistencia', {
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  alumno_id: { type: DataTypes.INTEGER, allowNull: false },
  fecha_entrada: { type: DataTypes.DATE, allowNull: false, defaultValue: DataTypes.NOW },
  fecha_salida: { type: DataTypes.DATE, allowNull: true },
}, { tableName: 'asistencias', timestamps: false });

module.exports = Asistencia;
