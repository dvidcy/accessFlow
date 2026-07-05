const { DataTypes } = require('sequelize');
const sequelize = require('../connection');

const Admin = sequelize.define('Admin', {
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  nombre: { type: DataTypes.STRING(100), allowNull: false },
  email: { type: DataTypes.STRING(150), allowNull: false, unique: true },
  password_hash: { type: DataTypes.STRING(255), allowNull: false },
}, { tableName: 'admins', timestamps: false });

module.exports = Admin;
