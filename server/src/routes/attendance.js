const router = require('express').Router();
const { buscarAlumno, registrarAsistencia, getAsistenciasHoy } = require('../services/attendance');
const { notificarEntrada, notificarSalida } = require('../services/email');
const { Alumno } = require('../db/models');

router.get('/today', async (req, res) => {
  try {
    res.json(await getAsistenciasHoy());
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

router.post('/', async (req, res) => {
  const { value } = req.body;
  if (!value) return res.status(400).json({ error: 'Valor requerido' });

  const alumno = await buscarAlumno(String(value).trim());
  if (!alumno) return res.status(404).json({ error: 'Alumno no encontrado' });

  const { tipo, registro } = await registrarAsistencia(alumno.id);
  if (tipo === 'completo') {
    return res.json({ tipo, mensaje: 'Entrada y salida ya registradas hoy', alumno: alumno.nombre });
  }

  const hora = tipo === 'entrada'
    ? registro.fecha_entrada.toTimeString().slice(0, 8)
    : registro.fecha_salida.toTimeString().slice(0, 8);

  // Notificar tutores en background
  const alumnoConTutores = await Alumno.findByPk(alumno.id, { include: ['Tutores'] });
  for (const tutor of alumnoConTutores.Tutores) {
    if (tipo === 'entrada') notificarEntrada(tutor.email, alumno.nombre, hora);
    else notificarSalida(tutor.email, alumno.nombre, hora);
  }

  res.json({ tipo, alumno: alumno.nombre, hora });
});

module.exports = router;
