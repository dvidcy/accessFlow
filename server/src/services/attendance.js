const { Op } = require('sequelize');
const { Alumno, Asistencia } = require('../db/models');

async function buscarAlumno(value) {
  let alumno = await Alumno.findOne({ where: { rfid_uid: value } });
  if (!alumno && /^\d+$/.test(value)) {
    alumno = await Alumno.findByPk(parseInt(value));
  }
  return alumno;
}

async function registrarAsistencia(alumno_id) {
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);

  const registro = await Asistencia.findOne({
    where: { alumno_id, fecha_entrada: { [Op.gte]: hoy } },
  });

  if (!registro) {
    const nuevo = await Asistencia.create({ alumno_id, fecha_entrada: new Date() });
    return { tipo: 'entrada', registro: nuevo };
  }
  if (!registro.fecha_salida) {
    registro.fecha_salida = new Date();
    await registro.save();
    return { tipo: 'salida', registro };
  }
  return { tipo: 'completo', registro };
}

async function getAsistenciasHoy() {
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);

  const registros = await Asistencia.findAll({
    where: { fecha_entrada: { [Op.gte]: hoy } },
    include: [{ model: Alumno, include: ['Grupo'] }],
    order: [['fecha_entrada', 'DESC']],
  });

  return registros.map(r => ({
    alumno: r.Alumno?.nombre ?? '—',
    grupo: r.Alumno?.Grupo ? `${r.Alumno.Grupo.grado}° ${r.Alumno.Grupo.nombre}` : '—',
    fecha_entrada: r.fecha_entrada.toTimeString().slice(0, 8),
    fecha_salida: r.fecha_salida ? r.fecha_salida.toTimeString().slice(0, 8) : '—',
  }));
}

module.exports = { buscarAlumno, registrarAsistencia, getAsistenciasHoy };
