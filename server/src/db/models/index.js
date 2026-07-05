const sequelize = require('../connection');
const Admin = require('./Admin');
const Grupo = require('./Grupo');
const Alumno = require('./Alumno');
const Tutor = require('./Tutor');
const Asistencia = require('./Asistencia');
const Mensaje = require('./Mensaje');
const { DataTypes } = require('sequelize');

// Junction: alumno_tutor
const AlumnoTutor = sequelize.define('AlumnoTutor', {
  parentesco: { type: DataTypes.STRING(30), allowNull: true },
}, { tableName: 'alumno_tutor', timestamps: false });

// Junction: mensaje_destinatario
const MensajeDestinatario = sequelize.define('MensajeDestinatario', {}, {
  tableName: 'mensaje_destinatario',
  timestamps: false,
});

// Grupo <-> Alumno
Grupo.hasMany(Alumno, { foreignKey: 'grupo_id', onDelete: 'RESTRICT' });
Alumno.belongsTo(Grupo, { foreignKey: 'grupo_id' });

// Alumno <-> Tutor (many-to-many)
Alumno.belongsToMany(Tutor, { through: AlumnoTutor, foreignKey: 'alumno_id', otherKey: 'tutor_id' });
Tutor.belongsToMany(Alumno, { through: AlumnoTutor, foreignKey: 'tutor_id', otherKey: 'alumno_id' });

// Alumno -> Asistencia
Alumno.hasMany(Asistencia, { foreignKey: 'alumno_id', onDelete: 'CASCADE' });
Asistencia.belongsTo(Alumno, { foreignKey: 'alumno_id' });

// Admin -> Mensaje
Admin.hasMany(Mensaje, { foreignKey: 'admin_id' });
Mensaje.belongsTo(Admin, { foreignKey: 'admin_id' });

// Mensaje <-> Tutor (many-to-many)
Mensaje.belongsToMany(Tutor, { through: MensajeDestinatario, foreignKey: 'mensaje_id', otherKey: 'tutor_id' });
Tutor.belongsToMany(Mensaje, { through: MensajeDestinatario, foreignKey: 'tutor_id', otherKey: 'mensaje_id' });

module.exports = { sequelize, Admin, Grupo, Alumno, Tutor, Asistencia, Mensaje, AlumnoTutor, MensajeDestinatario };
